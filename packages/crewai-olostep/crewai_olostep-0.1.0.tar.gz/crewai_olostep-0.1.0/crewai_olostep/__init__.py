"""
CrewAI tools for web scraping and research using Olostep API.

This package provides ready-to-use CrewAI tools for:
- Scraping individual web pages
- Batch scraping multiple URLs
- Crawling entire websites
- Extracting site maps
- AI-powered web search and answers

Usage:
    from crewai_olostep import (
        olostep_scrape_tool,
        olostep_batch_tool,
        olostep_crawl_tool,
        olostep_sitemap_tool,
        olostep_answer_tool,
        get_all_tools,
    )
    
    # Use individual tools
    from crewai import Agent
    agent = Agent(tools=[olostep_scrape_tool, olostep_answer_tool])
    
    # Or get all tools at once
    tools = get_all_tools()
"""

from .tools import (
    olostep_scrape_tool,
    olostep_batch_tool,
    olostep_crawl_tool,
    olostep_sitemap_tool,
    olostep_answer_tool,
    get_all_tools,
)

__version__ = "0.1.0"
__all__ = [
    "olostep_scrape_tool",
    "olostep_batch_tool",
    "olostep_crawl_tool",
    "olostep_sitemap_tool",
    "olostep_answer_tool",
    "get_all_tools",
]

