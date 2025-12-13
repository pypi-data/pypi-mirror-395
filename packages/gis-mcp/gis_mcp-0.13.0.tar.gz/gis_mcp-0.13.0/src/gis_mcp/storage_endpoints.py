"""
Storage HTTP endpoints for GIS MCP Server.

This module provides HTTP endpoints for file upload, download, and listing
operations when the server runs in HTTP/SSE transport mode.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.datastructures import UploadFile

from .mcp import gis_mcp
from .storage_config import get_storage_path, resolve_path

logger = logging.getLogger("gis-mcp")


@gis_mcp.custom_route("/storage/upload", methods=["POST"])
async def upload_file(request: Request) -> JSONResponse:
    """
    Upload a file to remote storage.
    
    Expected request:
    - Content-Type: multipart/form-data
    - Fields: 'file' (file data), 'path' (optional remote path)
    
    Returns JSON with:
    - remote_path: Path where file was saved
    - size: File size in bytes
    - message: Success message
    """
    try:
        # Parse multipart form data
        form = await request.form()
        
        # Get file from form
        if "file" not in form:
            return JSONResponse(
                {"error": "Missing 'file' field in form data"},
                status_code=400
            )
        
        file_item = form["file"]
        if not isinstance(file_item, UploadFile):
            return JSONResponse(
                {"error": "Invalid file field"},
                status_code=400
            )
        
        # Get optional remote path
        remote_path = form.get("path")
        if remote_path is None:
            remote_path = file_item.filename or "uploaded_file"
        
        # Clean up path (remove leading slash)
        remote_path = str(remote_path).lstrip('/')
        
        # Resolve path relative to storage directory
        target_path = resolve_path(remote_path, relative_to_storage=True)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_content = await file_item.read()
        target_path.write_bytes(file_content)
        
        file_size = len(file_content)
        
        logger.info(f"File uploaded: {remote_path} -> {target_path} ({file_size} bytes)")
        
        # Return response matching client expectations
        return JSONResponse({
            "remote_path": remote_path,
            "size": file_size,
            "message": f"File uploaded successfully to {remote_path}"
        })
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": str(e), "message": f"Failed to upload file: {str(e)}"},
            status_code=500
        )


@gis_mcp.custom_route("/storage/download", methods=["GET"])
async def download_file(request: Request) -> FileResponse:
    """
    Download a file from remote storage.
    
    Query parameters:
    - path: Path to the file to download (required)
    
    Returns the file content with appropriate Content-Type.
    """
    try:
        # Get path from query parameters
        path_param = request.query_params.get("path")
        if not path_param:
            return JSONResponse(
                {"error": "Missing 'path' query parameter"},
                status_code=400
            )
        
        # Clean up path
        remote_path = str(path_param).lstrip('/')
        
        # Resolve path relative to storage directory
        file_path = resolve_path(remote_path, relative_to_storage=True)
        
        # Check if file exists
        if not file_path.exists():
            return JSONResponse(
                {"error": f"File not found: {remote_path}"},
                status_code=404
            )
        
        if not file_path.is_file():
            return JSONResponse(
                {"error": f"Path is not a file: {remote_path}"},
                status_code=400
            )
        
        logger.info(f"File download requested: {remote_path} -> {file_path}")
        
        # Return file as response
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": str(e), "message": f"Failed to download file: {str(e)}"},
            status_code=500
        )


@gis_mcp.custom_route("/storage/list", methods=["GET"])
async def list_files(request: Request) -> JSONResponse:
    """
    List files in remote storage.
    
    Query parameters:
    - path: Optional directory path to list (defaults to storage root)
    
    Returns JSON with:
    - files: List of file/directory information
    - path: The path that was listed
    """
    try:
        # Get optional path from query parameters
        path_param = request.query_params.get("path")
        
        if path_param:
            remote_path = str(path_param).lstrip('/')
            target_path = resolve_path(remote_path, relative_to_storage=True)
        else:
            remote_path = ""
            target_path = get_storage_path()
        
        # Check if path exists
        if not target_path.exists():
            return JSONResponse(
                {"error": f"Path not found: {remote_path or 'root'}"},
                status_code=404
            )
        
        # If it's a file, return just that file
        if target_path.is_file():
            stat = target_path.stat()
            return JSONResponse({
                "files": [{
                    "name": target_path.name,
                    "path": remote_path,
                    "size": stat.st_size,
                    "type": "file",
                    "modified": stat.st_mtime
                }],
                "path": remote_path or "/"
            })
        
        # If it's a directory, list contents
        files_list = []
        try:
            for item in target_path.iterdir():
                stat = item.stat()
                relative_path = item.relative_to(get_storage_path())
                files_list.append({
                    "name": item.name,
                    "path": str(relative_path).replace("\\", "/"),  # Normalize path separators
                    "size": stat.st_size if item.is_file() else None,
                    "type": "file" if item.is_file() else "directory",
                    "modified": stat.st_mtime
                })
        except PermissionError:
            return JSONResponse(
                {"error": f"Permission denied: {remote_path or 'root'}"},
                status_code=403
            )
        
        # Sort: directories first, then files, both alphabetically
        files_list.sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))
        
        logger.info(f"Listed {len(files_list)} items in {remote_path or 'root'}")
        
        return JSONResponse({
            "files": files_list,
            "path": remote_path or "/"
        })
        
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": str(e), "message": f"Failed to list files: {str(e)}"},
            status_code=500
        )
