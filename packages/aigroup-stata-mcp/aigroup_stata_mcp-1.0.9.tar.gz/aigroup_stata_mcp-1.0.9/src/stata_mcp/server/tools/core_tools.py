#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from ...core.stata import StataController


def register_core_tools(server: FastMCP) -> None:
    """Register core Stata tools with the MCP server."""
    
    @server.tool()
    def mk_dir(ctx: Context[ServerSession, Dict], path: str) -> bool:
        """
        Safely create a directory using pathvalidate for security validation.
        
        Args:
            path: The path you want to create
            
        Returns:
            bool: True if the path exists now, False if not successful
            
        Raises:
            ValueError: if path is invalid or contains unsafe components
            PermissionError: if insufficient permissions to create directory
        """
        from pathvalidate import ValidationError, sanitize_filepath

        # Input validation
        if not path or not isinstance(path, str):
            raise ValueError("Path must be a non-empty string")

        try:
            # Use pathvalidate to sanitize and validate path
            safe_path = sanitize_filepath(path, platform="auto")

            # Get absolute path for further validation
            absolute_path = os.path.abspath(safe_path)

            # Create directory with reasonable permissions
            os.makedirs(absolute_path, exist_ok=True, mode=0o755)

            # Verify successful creation
            return os.path.exists(absolute_path) and os.path.isdir(absolute_path)

        except ValidationError as e:
            raise ValueError(f"Invalid path detected: {e}") from e
        except PermissionError as e:
            raise PermissionError(f"Insufficient permissions to create directory: {path}") from e
        except OSError as e:
            raise OSError(f"Failed to create directory {path}: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error when creating directory {path}: {str(e)}") from e