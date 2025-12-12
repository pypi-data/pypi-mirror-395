#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP, Image
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field


class ReadFileResult(BaseModel):
    
    """Result model for file reading operation."""
    
    file_path: str = Field(description="The path to the file that was read")
    content: str = Field(description="The content of the file")
    encoding: str = Field(description="The encoding used to read the file")


class WriteDofileResult(BaseModel):
    
    """Result model for dofile writing operation."""
    
    file_path: str = Field(description="The path to the created dofile")
    content_length: int = Field(description="The length of the content written")
    timestamp: str = Field(description="The timestamp when the file was created")


class AppendDofileResult(BaseModel):
    
    """Result model for dofile appending operation."""
    
    new_file_path: str = Field(description="The path to the new dofile")
    original_exists: bool = Field(description="Whether the original file existed")
    total_content_length: int = Field(description="Total length of content after appending")


def register_file_tools(server: FastMCP) -> None:
    """Register file-related tools with the MCP server."""
    
    @server.tool()
    def read_file(ctx: Context[ServerSession, Dict], file_path: str, encoding: str = "utf-8") -> ReadFileResult:
        """
        Reads a file and returns its content as a string.
        
        Args:
            file_path: The full path to the file to be read.
            encoding: The encoding used to decode the file. Defaults to "utf-8".
            
        Returns:
            ReadFileResult: Structured result containing file content and metadata.
        """
        # Validate file_path
        if not file_path:
            raise ValueError("file_path cannot be empty")
        
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        
        try:
            with open(file_path, "r", encoding=encoding) as file:
                log_content = file.read()
            
            return ReadFileResult(
                file_path=file_path,
                content=log_content,
                encoding=encoding
            )
        except PermissionError as e:
            raise PermissionError(f"Permission denied when reading {file_path}: {str(e)}") from e
        except UnicodeDecodeError as e:
            raise ValueError(f"Failed to decode file {file_path} with encoding {encoding}: {str(e)}") from e
        except OSError as e:
            raise OSError(f"Failed to read file {file_path}: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error when reading file: {str(e)}") from e

    @server.tool()
    def write_dofile(ctx: Context[ServerSession, Dict], content: str, encoding: str = "utf-8") -> WriteDofileResult:
        """
        Write stata code to a dofile and return the do-file path.
        
        Args:
            content: The stata code content which will be written to the designated do-file.
            encoding: The encoding method for the dofile, default -> 'utf-8'
            
        Returns:
            WriteDofileResult: Structured result containing file path and metadata.
        """
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        dofile_base_path = stata_context.output_base_path / "stata-mcp-dofile"
        
        # Ensure the directory exists
        dofile_base_path.mkdir(parents=True, exist_ok=True)
        
        file_path = dofile_base_path / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.do"
        
        try:
            with open(file_path, "w", encoding=encoding) as f:
                f.write(content)
        except PermissionError as e:
            raise PermissionError(f"Permission denied when writing to {file_path}: {str(e)}") from e
        except OSError as e:
            raise OSError(f"Failed to write to {file_path}: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error when writing do-file: {str(e)}") from e
        
        return WriteDofileResult(
            file_path=str(file_path),
            content_length=len(content),
            timestamp=datetime.now().isoformat()
        )

    @server.tool()
    def append_dofile(ctx: Context[ServerSession, Dict], original_dofile_path: str, content: str, encoding: str = "utf-8") -> AppendDofileResult:
        """
        Append stata code to an existing dofile or create a new one.
        
        Args:
            original_dofile_path: Path to the original dofile to append to.
                If empty or invalid, a new file will be created.
            content: The stata code content which will be appended to the designated do-file.
            encoding: The encoding method for the dofile, default -> 'utf-8'
            
        Returns:
            AppendDofileResult: Structured result containing new file path and metadata.
        """
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        dofile_base_path = stata_context.output_base_path / "stata-mcp-dofile"
        
        # Ensure the directory exists
        dofile_base_path.mkdir(parents=True, exist_ok=True)
        
        # Create a new file path for the output
        new_file_path = dofile_base_path / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.do"
        
        # Check if original file exists and is valid
        original_exists = False
        original_content = ""
        if original_dofile_path:
            original_path = Path(original_dofile_path)
            # Check if file exists and has .do extension
            if original_path.exists():
                if original_path.suffix.lower() == '.do':
                    try:
                        with open(original_dofile_path, "r", encoding=encoding) as f:
                            original_content = f.read()
                        original_exists = True
                    except Exception as e:
                        # If there's any error reading the file, we'll create a new one
                        original_exists = False
                else:
                    # File exists but is not a .do file, we'll create a new one
                    original_exists = False

        # Write to the new file (either copying original content + new content, or just new content)
        try:
            with open(new_file_path, "w", encoding=encoding) as f:
                if original_exists:
                    f.write(original_content)
                    # Add a newline if the original file doesn't end with one
                    if original_content and not original_content.endswith("\n"):
                        f.write("\n")
                f.write(content)
        except PermissionError as e:
            raise PermissionError(f"Permission denied when writing to {new_file_path}: {str(e)}") from e
        except OSError as e:
            raise OSError(f"Failed to write to {new_file_path}: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error when writing do-file: {str(e)}") from e
        
        total_length = len(original_content) + len(content) if original_exists else len(content)
        
        return AppendDofileResult(
            new_file_path=str(new_file_path),
            original_exists=original_exists,
            total_content_length=total_length
        )

    @server.tool()
    def load_figure(ctx: Context[ServerSession, Dict], figure_path: str) -> Image:
        """
        Load figure from device.
        
        Args:
            figure_path: the figure file path, only support png and jpg format
            
        Returns:
            Image: the figure thumbnail
        """
        # Validate figure_path
        if not figure_path:
            raise ValueError("figure_path cannot be empty")
        
        figure_path_obj = Path(figure_path)
        
        if not figure_path_obj.exists():
            raise FileNotFoundError(f"{figure_path} not found")
        
        # Check file extension
        supported_extensions = {'.png', '.jpg', '.jpeg'}
        if figure_path_obj.suffix.lower() not in supported_extensions:
            raise ValueError(f"Unsupported image format: {figure_path_obj.suffix}. "
                           f"Supported formats are: {', '.join(supported_extensions)}")
        
        try:
            return Image(figure_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load figure {figure_path}: {str(e)}") from e
