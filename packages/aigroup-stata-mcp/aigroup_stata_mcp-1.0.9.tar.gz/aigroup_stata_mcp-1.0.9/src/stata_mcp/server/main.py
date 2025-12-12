#!/usr/bin/python3
# -*- coding: utf-8 -*-


import locale
import os
import platform
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP, Icon
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from ..core.data_info import CsvDataInfo, DtaDataInfo
from ..core.stata import StataController, StataDo, StataFinder
from ..utils.Prompt import pmp
from ..config import ConfigManager, StataServerConfig

from .tools.core_tools import register_core_tools
from .tools.file_tools import register_file_tools
from .tools.stata_tools import register_stata_tools
from .prompts.core_prompts import register_core_prompts


class StataServerContext(BaseModel):
   
   
    """Application context with typed dependencies."""
    
    config: StataServerConfig
    stata_finder: Any = Field(description="StataFinder instance")
    working_directory: Path
    output_base_path: Path

    class Config:
        arbitrary_types_allowed = True


@asynccontextmanager
async def server_lifespan(server: FastMCP, config: StataServerConfig) -> AsyncIterator[StataServerContext]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize system configuration
    system_os = platform.system()
    if system_os not in ["Darwin", "Linux", "Windows"]:
        raise RuntimeError(f"Unsupported operating system: {system_os}")
    
    # Find Stata CLI
    stata_finder = StataFinder()
    stata_cli = config.stata_cli or stata_finder.STATA_CLI
    
    # Determine working directory
    if config.working_directory:
        working_directory = Path(config.working_directory)
    else:
        client = os.getenv("STATA-MCP-CLIENT")
        if client == "cc":  # Claude Code
            working_directory = Path.cwd()
        else:
            cwd = os.getenv("STATA_MCP_CWD", os.getenv("STATA-MCP-CWD", None))
            if cwd:
                working_directory = Path(cwd)
            else:
                if system_os in ["Darwin", "Linux"]:
                    working_directory = Path.home() / "Documents"
                else:
                    working_directory = Path(os.getenv("USERPROFILE", "~")) / "Documents"
    
    # Create output directories
    output_base_path = working_directory / "stata-mcp-folder"
    output_base_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    log_base_path = output_base_path / "stata-mcp-log"
    dofile_base_path = output_base_path / "stata-mcp-dofile"
    result_doc_path = output_base_path / "stata-mcp-result"
    tmp_base_path = output_base_path / "stata-mcp-tmp"
    
    for path in [log_base_path, dofile_base_path, result_doc_path, tmp_base_path]:
        path.mkdir(exist_ok=True)
    
    # Set language for prompts
    lang_mapping = {"zh-CN": "cn", "en_US": "en"}
    lang, _ = locale.getdefaultlocale()
    pmp.set_lang(lang_mapping.get(lang, "en"))
    
    yield StataServerContext(
        config=config,
        stata_finder=stata_finder,
        working_directory=working_directory,
        output_base_path=output_base_path
    )


def create_stata_server(config: Optional["StataServerConfig"] = None) -> FastMCP:
    """Create and configure the Stata MCP server."""
    # If no config provided, try to load from file or use default
    if config is None:
        config_manager = ConfigManager()
        try:
            config = config_manager.load_config()
        except Exception:
            # Fall back to default config if loading fails
            config = config_manager.create_default_config()
    
    # Create server with lifespan
    @asynccontextmanager
    async def lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
        async with server_lifespan(server, config) as context:
            yield {"stata_context": context}
    
    # Initialize server with latest MCP features
    server = FastMCP(
        name=config.name,
        instructions=config.instructions,
        website_url=config.website_url,
        icons=[
            Icon(
                src="https://avatars.githubusercontent.com/u/201514154?v=4",
                mimeType="image/png",
                sizes=["460*460"]
            )
        ],
        lifespan=lifespan
    )
    
    # Register all components
    register_core_tools(server)
    register_file_tools(server)
    register_stata_tools(server)
    register_core_prompts(server)
    
    return server


# Export the default server instance
stata_server = create_stata_server()


def run_server(transport: str = "stdio", config_path: Optional[str] = None) -> None:
    """
    Run the Stata MCP server with the specified transport.
    
    Args:
        transport: The transport method to use (stdio, sse, http, streamable-http)
        config_path: Path to configuration file. If None, uses default config.
    """
    # Load configuration from file if specified
    if config_path is not None:
        config_manager = ConfigManager(config_path)
        try:
            config = config_manager.load_config()
            global stata_server
            stata_server = create_stata_server(config)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {config_path}: {str(e)}") from e
    
    stata_server.run(transport=transport)


if __name__ == "__main__":
    run_server()