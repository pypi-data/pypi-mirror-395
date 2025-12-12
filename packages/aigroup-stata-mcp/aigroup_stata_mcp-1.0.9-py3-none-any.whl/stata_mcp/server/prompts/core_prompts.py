#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from datetime import datetime
from typing import Dict, Optional

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

from ...utils.Prompt import pmp


class PromptResult(BaseModel):
   
   
    """Result model for prompt operations."""
    
    prompt_id: str = Field(description="The identifier of the prompt")
    content: str = Field(description="The generated prompt content")
    language: str = Field(description="The language of the prompt")
    timestamp: str = Field(description="The timestamp when the prompt was generated")


def register_core_prompts(server: FastMCP) -> None:
    """Register core prompts with the MCP server."""
    
    @server.prompt()
    def stata_assistant_role(ctx: Context[ServerSession, Dict], lang: Optional[str] = None) -> PromptResult:
        """
        Return the Stata assistant role prompt content.
        
        This function retrieves a predefined prompt that defines the role and capabilities
        of a Stata analysis assistant. The prompt helps set expectations and context for
        the assistant's behavior when handling Stata-related tasks.
        
        Args:
            lang: Language code for localization of the prompt content.
                If None, returns the default language version. Defaults to None.
                Examples: "en" for English, "cn" for Chinese.
                
        Returns:
            PromptResult: Structured result containing prompt content and metadata.
        """
        content = pmp.get_prompt(prompt_id="stata_assistant_role", lang=lang)
        actual_lang = lang or "default"
        
        return PromptResult(
            prompt_id="stata_assistant_role",
            content=content,
            language=actual_lang,
            timestamp=datetime.now().isoformat()
        )

    @server.prompt()
    def stata_analysis_strategy(ctx: Context[ServerSession, Dict], lang: Optional[str] = None) -> PromptResult:
        """
        Return the Stata analysis strategy prompt content.
        
        This function retrieves a predefined prompt that outlines the recommended
        strategy for conducting data analysis using Stata. The prompt includes
        guidelines for data preparation, code generation, results management,
        reporting, and troubleshooting.
        
        Args:
            lang: Language code for localization of the prompt content.
                If None, returns the default language version. Defaults to None.
                Examples: "en" for English, "cn" for Chinese.
                
        Returns:
            PromptResult: Structured result containing prompt content and metadata.
        """
        content = pmp.get_prompt(prompt_id="stata_analysis_strategy", lang=lang)
        actual_lang = lang or "default"
        
        return PromptResult(
            prompt_id="stata_analysis_strategy",
            content=content,
            language=actual_lang,
            timestamp=datetime.now().isoformat()
        )

    @server.prompt()
    def results_doc_path(ctx: Context[ServerSession, Dict]) -> PromptResult:
        """
        Generate and return a result document storage path based on the current timestamp.
        
        This function performs the following operations:
        1. Gets the current system time and formats it as a '%Y%m%d%H%M%S' timestamp string
        2. Concatenates this timestamp string with the preset result_doc_path base path to form a complete path
        3. Creates the directory corresponding to that path (no error if directory already exists)
        4. Returns the complete path string of the newly created directory
        
        Returns:
            PromptResult: Structured result containing the generated path and metadata.
        """
        stata_context = ctx.request_context.lifespan_context["stata_context"]
        result_doc_path = stata_context.output_base_path / "stata-mcp-result"
        
        path = result_doc_path / datetime.now().strftime("%Y%m%d%H%M%S")
        path.mkdir(exist_ok=True)
        
        content = f"""
        The result document path has been created at:
        {path}
        
        You can use this path for Stata commands that generate output files, such as:
        - outreg2: outreg2 using "{path}/results", replace
        - esttab: esttab using "{path}/regression_results.rtf", replace
        - graph export: graph export "{path}/figure.png", replace
        
        Make sure to include the appropriate file extensions in your Stata commands.
        """
        
        return PromptResult(
            prompt_id="results_doc_path",
            content=content,
            language="en",
            timestamp=datetime.now().isoformat()
        )