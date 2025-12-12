# CrewAI Olostep Integration

[![PyPI version](https://badge.fury.io/py/crewai-olostep.svg)](https://pypi.org/project/crewai-olostep/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Give your CrewAI agents the power to scrape, search, and research the web.**

This package provides ready-to-use CrewAI tools that integrate with the [Olostep API](https://olostep.com) for powerful web data access capabilities.

## Features

- 🌐 **Web Scraping** - Extract content from any URL in markdown, HTML, or text format
- 📦 **Batch Processing** - Scrape up to 10,000 URLs in parallel
- 🕷️ **Website Crawling** - Automatically discover and scrape entire websites
- 🗺️ **Sitemap Extraction** - Get all URLs from a website for site structure analysis
- 🔍 **AI-Powered Search** - Get answers to questions with web sources and structured output

## Installation

```bash
pip install crewai-olostep
```

## Quick Start

```bash
export OLOSTEP_API_KEY="your_api_key_here"
```

```python
from crewai import Agent, Task, Crew
from crewai_olostep import olostep_scrape_tool, olostep_answer_tool

# Create an agent with Olostep tools
researcher = Agent(
    role="Web Researcher",
    goal="Find accurate information from the web",
    backstory="Expert researcher with web scraping skills.",
    tools=[olostep_scrape_tool, olostep_answer_tool],
    verbose=True
)

# Create a task
task = Task(
    description="Research the pricing of Stripe's payment processing",
    expected_output="A summary of Stripe's pricing tiers and fees",
    agent=researcher
)

# Run the crew
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print(result)
```

## Available Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `olostep_scrape_tool` | Scrape single pages | `url`, `format` |
| `olostep_batch_tool` | Process 10K+ URLs in parallel | `urls` (comma-separated), `format` |
| `olostep_crawl_tool` | Crawl entire websites | `start_url`, `max_pages`, `include_pattern`, `exclude_pattern` |
| `olostep_sitemap_tool` | Extract all URLs from a site | `url`, `search_query`, `max_urls` |
| `olostep_answer_tool` | AI-powered web search | `question`, `output_schema` |

### Get All Tools

```python
from crewai_olostep import get_all_tools

all_tools = get_all_tools()  # Returns all 5 tools
```

## Example: Multi-Agent Research Crew

```python
from crewai import Agent, Task, Crew, Process
from crewai_olostep import (
    olostep_scrape_tool,
    olostep_sitemap_tool,
    olostep_answer_tool,
)

# Specialized agents
explorer = Agent(
    role="Site Explorer",
    goal="Discover website structures",
    tools=[olostep_sitemap_tool],
)

scraper = Agent(
    role="Content Extractor", 
    goal="Extract web content",
    tools=[olostep_scrape_tool],
)

analyst = Agent(
    role="Research Analyst",
    goal="Analyze and synthesize",
    tools=[olostep_answer_tool],
)

# Chained tasks
task1 = Task(description="Find all product pages on https://example.com", agent=explorer)
task2 = Task(description="Scrape the top 3 pages", agent=scraper, context=[task1])
task3 = Task(description="Summarize findings", agent=analyst, context=[task2])

crew = Crew(
    agents=[explorer, scraper, analyst],
    tasks=[task1, task2, task3],
    process=Process.sequential,
)

result = crew.kickoff()
```

## Documentation

Full documentation at [docs.olostep.com/integrations/crewai](https://docs.olostep.com/integrations/crewai)

## Support

- **PyPI**: [pypi.org/project/crewai-olostep](https://pypi.org/project/crewai-olostep/)
- **Docs**: [docs.olostep.com](https://docs.olostep.com)
- **Email**: info@olostep.com

## License

MIT License
