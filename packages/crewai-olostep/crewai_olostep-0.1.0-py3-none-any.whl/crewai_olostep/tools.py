"""
CrewAI tools for Olostep web scraping and research capabilities.

These tools wrap the Olostep API to provide powerful web access
for CrewAI agents. Each tool is decorated with @tool from crewai.tools.
"""

import os
import json
import requests
from typing import Optional

from crewai.tools import tool


def _get_api_key() -> str:
    """Get Olostep API key from environment."""
    api_key = os.environ.get("OLOSTEP_API_KEY")
    if not api_key:
        raise ValueError(
            "OLOSTEP_API_KEY environment variable is not set. "
            "Get your API key from https://olostep.com/dashboard"
        )
    return api_key


def _api_request(endpoint: str, payload: dict, timeout: int = 120) -> dict:
    """Make a request to the Olostep API."""
    api_key = _get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"https://api.olostep.com/v1/{endpoint}",
        headers=headers,
        json=payload,
        timeout=timeout
    )
    
    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")
    
    return response.json()


def _api_get(endpoint: str, timeout: int = 60) -> dict:
    """Make a GET request to the Olostep API."""
    api_key = _get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(
        f"https://api.olostep.com/v1/{endpoint}",
        headers=headers,
        timeout=timeout
    )
    
    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")
    
    return response.json()


@tool("Olostep Web Scraper")
def olostep_scrape_tool(url: str, format: str = "markdown") -> str:
    """
    Scrape content from a single web page using Olostep.
    
    This tool extracts content from any URL in your preferred format.
    Supports JavaScript rendering and handles dynamic content automatically.
    
    Args:
        url: The URL to scrape (must include http:// or https://).
             Example: "https://example.com/page"
        format: Output format - 'markdown' (default), 'html', or 'text'.
    
    Returns:
        The scraped content in the requested format, or an error message.
    
    Examples:
        - Scrape a blog post: url="https://blog.example.com/post", format="markdown"
        - Get HTML source: url="https://example.com", format="html"
    """
    try:
        # Map format names
        format_map = {
            "markdown": "markdown",
            "html": "html", 
            "text": "text"
        }
        api_format = format_map.get(format.lower(), "markdown")
        
        payload = {
            "url_to_scrape": url,
            "formats": [api_format]
        }
        
        result = _api_request("scrapes", payload)  # Note: 'scrapes' with 's'
        
        # Content is nested in 'result' key
        result_data = result.get("result", result)
        
        # Extract content based on format
        if api_format == "markdown":
            content = result_data.get("markdown_content", "")
        elif api_format == "html":
            content = result_data.get("html_content", "")
        elif api_format == "text":
            content = result_data.get("text_content", "")
        else:
            content = result_data.get("markdown_content", str(result))
        
        if not content:
            content = f"Scrape completed but no {format} content returned. Raw result: {json.dumps(result, indent=2)[:500]}"
        
        return f"Successfully scraped {url}:\n\n{content}"
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


@tool("Olostep Batch Scraper")
def olostep_batch_tool(urls: str, format: str = "markdown") -> str:
    """
    Scrape multiple URLs in parallel using Olostep batch processing.
    
    Efficiently process up to 10,000 URLs at once. Batch jobs typically
    complete in 5-8 minutes regardless of the number of URLs.
    
    Args:
        urls: Comma-separated list of URLs to scrape.
              Example: "https://site1.com,https://site2.com,https://site3.com"
        format: Output format - 'markdown' (default), 'html', or 'text'.
    
    Returns:
        A summary of the batch job including batch_id and status,
        followed by available results.
    
    Examples:
        - Scrape 3 pages: urls="https://a.com,https://b.com,https://c.com"
    """
    try:
        url_list = [u.strip() for u in urls.split(",") if u.strip()]
        
        if not url_list:
            return "Error: No valid URLs provided. Please provide comma-separated URLs."
        
        # Start the batch - uses 'items' array with url objects
        batch_items = [
            {"url": u, "custom_id": f"url_{i}"}
            for i, u in enumerate(url_list)
        ]
        payload = {
            "items": batch_items
        }
        
        result = _api_request("batches", payload)
        batch_id = result.get("id") or result.get("batch_id")
        
        if not batch_id:
            return f"Batch created but no ID returned. Response: {json.dumps(result, indent=2)}"
        
        return f"Batch job started successfully!\n\nBatch ID: {batch_id}\nURLs submitted: {len(url_list)}\nStatus: Processing\n\nThe batch will complete in a few minutes. Use the batch ID to check results."
    except Exception as e:
        return f"Error processing batch: {str(e)}"


@tool("Olostep Website Crawler")
def olostep_crawl_tool(
    start_url: str,
    max_pages: int = 50,
    include_pattern: str = "",
    exclude_pattern: str = ""
) -> str:
    """
    Crawl an entire website by following links starting from a URL.
    
    Automatically discovers and scrapes pages within a website.
    Useful for extracting documentation, blog archives, or entire sites.
    
    Args:
        start_url: The starting URL for the crawl.
                   Example: "https://docs.example.com"
        max_pages: Maximum number of pages to crawl (default: 50, max: 1000).
        include_pattern: Glob pattern for URLs to include (e.g., "/docs/**").
                        Leave empty to include all URLs.
        exclude_pattern: Glob pattern for URLs to exclude (e.g., "/admin/**").
    
    Returns:
        A summary of the crawl job with crawl_id and status.
    
    Examples:
        - Crawl docs: start_url="https://docs.example.com", max_pages=100
        - Crawl blog only: start_url="https://example.com", include_pattern="/blog/**"
    """
    try:
        payload = {
            "start_url": start_url,
            "max_pages": min(max_pages, 1000),
        }
        
        if include_pattern:
            payload["include_urls"] = [include_pattern]
        if exclude_pattern:
            payload["exclude_urls"] = [exclude_pattern]
        
        result = _api_request("crawls", payload)
        crawl_id = result.get("id") or result.get("crawl_id")
        
        if not crawl_id:
            return f"Crawl started but no ID returned. Response: {json.dumps(result, indent=2)}"
        
        return f"Crawl job started successfully!\n\nCrawl ID: {crawl_id}\nStarting URL: {start_url}\nMax pages: {max_pages}\nStatus: Processing\n\nThe crawl will discover and process pages. Use the crawl ID to check results."
    except Exception as e:
        return f"Error crawling {start_url}: {str(e)}"


@tool("Olostep Sitemap Extractor")
def olostep_sitemap_tool(
    url: str,
    search_query: str = "",
    max_urls: int = 100
) -> str:
    """
    Extract all URLs from a website to understand its structure.
    
    Quickly discovers all accessible pages on a website without
    scraping their content. Useful for site audits and planning.
    
    Args:
        url: The website URL to extract URLs from.
             Example: "https://example.com"
        search_query: Optional query to filter URLs by relevance.
                     Example: "pricing" to find pricing-related pages.
        max_urls: Maximum number of URLs to return (default: 100).
    
    Returns:
        A list of discovered URLs on the website.
    
    Examples:
        - Get all URLs: url="https://example.com"
        - Find blog posts: url="https://example.com", search_query="blog"
    """
    try:
        payload = {
            "url": url,
            "top_n": max_urls
        }
        
        if search_query:
            payload["search_query"] = search_query
        
        result = _api_request("maps", payload)
        
        urls = result.get("urls", [])
        
        if not urls:
            return f"No URLs found for {url}. Response: {json.dumps(result, indent=2)[:500]}"
        
        urls_text = "\n".join(f"• {u}" for u in urls[:max_urls])
        query_info = f" matching '{search_query}'" if search_query else ""
        return f"Found {len(urls)} URLs{query_info} on {url}:\n\n{urls_text}"
    except Exception as e:
        return f"Error extracting sitemap from {url}: {str(e)}"


@tool("Olostep AI Web Search")
def olostep_answer_tool(question: str, output_schema: str = "") -> str:
    """
    Search the web and get AI-powered answers with sources.
    
    Performs intelligent web research to answer questions.
    Can return structured data using a JSON schema.
    
    Args:
        question: The question or research task to answer.
                  Example: "What is the latest pricing for Stripe?"
        output_schema: Optional JSON schema for structured output.
                      Example: '{"company": "", "ceo": "", "founded": ""}'
    
    Returns:
        An AI-generated answer based on web sources, with citations.
    
    Examples:
        - Simple question: question="Who founded OpenAI?"
        - Structured data: question="Find info about Tesla", 
          output_schema='{"ceo": "", "headquarters": "", "stock_price": ""}'
    """
    try:
        payload = {"task": question}
        
        if output_schema:
            try:
                schema = json.loads(output_schema)
                payload["json_schema"] = schema
            except json.JSONDecodeError:
                return f"Error: Invalid JSON schema provided: {output_schema}"
        
        result = _api_request("answers", payload, timeout=180)
        
        # Format the response
        answer = result.get("answer", {})
        sources = result.get("sources", [])
        
        if isinstance(answer, dict):
            result_text = f"Answer:\n{json.dumps(answer, indent=2)}"
        else:
            result_text = f"Answer: {answer}"
        
        if sources:
            sources_text = "\n".join(f"  • {s.get('url', s) if isinstance(s, dict) else s}" for s in sources[:5])
            result_text += f"\n\nSources:\n{sources_text}"
        
        return result_text
    except Exception as e:
        return f"Error answering question: {str(e)}"


def get_all_tools() -> list:
    """
    Get all available Olostep tools for CrewAI.
    
    Returns:
        A list of all Olostep tools ready to use with CrewAI agents.
    
    Usage:
        from crewai_olostep import get_all_tools
        from crewai import Agent
        
        agent = Agent(
            role="Research Assistant",
            tools=get_all_tools()
        )
    """
    return [
        olostep_scrape_tool,
        olostep_batch_tool,
        olostep_crawl_tool,
        olostep_sitemap_tool,
        olostep_answer_tool,
    ]

