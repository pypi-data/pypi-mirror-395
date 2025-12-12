#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from ...core.data_info import CsvDataInfo, DtaDataInfo
from ...core.stata import StataDo


class DataInfoResult(BaseModel):
   
   
    """Result model for data information operation."""
    
    data_path: str = Field(description="The path to the data file")
    file_extension: str = Field(description="The file extension of the data file")
    summary: Dict[str, Dict] = Field(description="Summary statistics of the data")
    info_file_path: Optional[str] = Field(description="Path to the saved info file, if applicable")


class StataDoResult(BaseModel):
   
   
    """Result model for Stata dofile execution."""
    
    dofile_path: str = Field(description="Path to the executed dofile")
    log_file_path: str = Field(description="Path to the generated log file")
    log_content: Optional[str] = Field(description="Content of the log file, if requested")
    execution_time: str = Field(description="Timestamp of execution")


class SscInstallResult(BaseModel):
   
   
    """Result model for SSC package installation."""
    
    package: str = Field(description="The package that was installed")
    success: bool = Field(description="Whether installation was successful")
    log_content: str = Field(description="Installation log content")


def register_stata_tools(server: FastMCP) -> None:
    """Register Stata-specific tools with the MCP server."""
    
    @server.tool()
    def get_data_info(
        ctx: Context[ServerSession, Dict],
        data_path: str,
        vars_list: Optional[List[str]] = None,
        encoding: str = "utf-8",
        file_extension: Optional[str] = None,
        is_save: bool = True,
        save_path: Optional[str] = None,
        info_file_encoding: str = "utf-8"
    ) -> DataInfoResult:
        """
        Get descriptive statistics for the data file.
        
        Args:
            data_path: the data file's absolute path.
            vars_list: the vars you want to get info (default is None, means all vars).
            encoding: data file encoding method (dta file is not supported this arg).
            file_extension: the data file's extension, default is None, then would find it automatically.
            is_save: whether save the result to a txt file.
            save_path: the data-info saved file path.
            info_file_encoding: the data-info saved file encoding.
            
        Returns:
            DataInfoResult: Structured result containing data information.
        """
        # Validate data_path
        if not data_path:
            raise ValueError("data_path cannot be empty")
        
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        tmp_base_path = stata_context.output_base_path / "stata-mcp-tmp"
        
        EXTENSION_METHOD_MAPPING: Dict[str, Callable] = {
            "dta": DtaDataInfo,
            "csv": CsvDataInfo
        }
        
        if file_extension is None:
            file_extension = Path(data_path).suffix
        file_extension = file_extension.split(".")[-1].lower()
        
        if file_extension not in EXTENSION_METHOD_MAPPING:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        cls = EXTENSION_METHOD_MAPPING.get(file_extension)
        
        try:
            data_info = cls(
                data_path=data_path,
                vars_list=vars_list,
                encoding=encoding,
                is_save=is_save,
                save_path=save_path,
                info_file_encoding=info_file_encoding
            ).info
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Data file not found: {str(e)}") from e
        except ValueError as e:
            raise ValueError(f"Invalid data file: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to process data file: {str(e)}") from e

        info_file_path = None
        if is_save:
            if save_path is None:
                data_name = Path(data_path).name.split(".")[0]
                info_file_path = tmp_base_path / f"{data_name}.txt"
            else:
                info_file_path = Path(save_path)

            info_file_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(info_file_path, "w", encoding=info_file_encoding) as f:
                    f.write(str(data_info))
            except Exception as e:
                raise RuntimeError(f"Failed to save info file: {str(e)}") from e

        return DataInfoResult(
            data_path=data_path,
            file_extension=file_extension,
            summary=data_info,
            info_file_path=str(info_file_path) if info_file_path else None
        )

    @server.tool()
    def stata_do(
        ctx: Context[ServerSession, Dict],
        dofile_path: str,
        log_file_name: Optional[str] = None,
        is_read_log: bool = True
    ) -> StataDoResult:
        """
        Execute a Stata do-file and return the log file path with optional log content.
        
        Args:
            dofile_path: Absolute or relative path to the Stata do-file (.do) to execute.
            log_file_name: Set log file name without a time-string. If None, using nowtime as filename.
            is_read_log: Whether to read and return the log file content.
            
        Returns:
            StataDoResult: Structured result containing execution details.
        """
        # Validate dofile_path
        if not dofile_path:
            raise ValueError("dofile_path cannot be empty")
        
        # Convert to Path object for better handling
        dofile_path_obj = Path(dofile_path)
        
        # Check if file exists
        if not dofile_path_obj.exists():
            raise FileNotFoundError(f"Stata do-file not found: {dofile_path}")
        
        # Check file extension
        if dofile_path_obj.suffix.lower() != '.do':
            raise ValueError(f"File must have .do extension, got: {dofile_path_obj.suffix}")
        
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        stata_cli = stata_context.stata_finder.STATA_CLI
        log_base_path = stata_context.output_base_path / "stata-mcp-log"
        dofile_base_path = stata_context.output_base_path / "stata-mcp-dofile"
        
        # Initialize Stata executor with system configuration
        stata_executor = StataDo(
            stata_cli=stata_cli,
            log_file_path=str(log_base_path),
            dofile_base_path=str(dofile_base_path),
            sys_os=platform.system()
        )

        # Execute the do-file and get log file path
        try:
            log_file_path = stata_executor.execute_dofile(dofile_path, log_file_name)
        except Exception as e:
            raise RuntimeError(f"Failed to execute Stata do-file: {str(e)}") from e

        # Return log content based on user preference
        log_content = None
        if is_read_log:
            try:
                log_content = stata_executor.read_log(log_file_path)
            except Exception as e:
                raise RuntimeError(f"Failed to read log file: {str(e)}") from e

        return StataDoResult(
            dofile_path=dofile_path,
            log_file_path=log_file_path,
            log_content=log_content,
            execution_time=datetime.now().isoformat()
        )

    @server.tool()
    def ssc_install(
        ctx: Context[ServerSession, Dict],
        command: str,
        is_replace: bool = True
    ) -> SscInstallResult:
        """
        Install a package from SSC.
        
        Args:
            command: The name of the package to be installed from SSC.
            is_replace: Whether to force replacement of an existing installation.
            
        Returns:
            SscInstallResult: Structured result containing installation details.
        """
        # Validate command
        if not command:
            raise ValueError("Command cannot be empty")
        
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        stata_cli = stata_context.stata_finder.STATA_CLI
        log_base_path = stata_context.output_base_path / "stata-mcp-log"
        dofile_base_path = stata_context.output_base_path / "stata-mcp-dofile"
        
        replace_clause = ", replace" if is_replace else ""
        
        # Create dofile content
        content = f"ssc install {command}{replace_clause}"
        file_path = dofile_base_path / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.do"
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f"Failed to create temporary do-file: {str(e)}") from e
        
        # Execute the dofile using StataDo directly
        stata_executor = StataDo(
            stata_cli=stata_cli,
            log_file_path=str(log_base_path),
            dofile_base_path=str(dofile_base_path),
            sys_os=platform.system()
        )
        
        try:
            log_file_path = stata_executor.execute_dofile(str(file_path))
            log_content = stata_executor.read_log(log_file_path)
        except Exception as e:
            raise RuntimeError(f"Failed to execute SSC installation: {str(e)}") from e
        
        # Check for success
        success = "not found" not in log_content.lower() if log_content else False
        
        return SscInstallResult(
            package=command,
            success=success,
            log_content=log_content or ""
        )


