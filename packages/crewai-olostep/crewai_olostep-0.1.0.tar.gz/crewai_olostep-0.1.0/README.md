# CrewAI Olostep Integration

**Give your CrewAI agents the power to scrape, search, and research the web.**

This package provides ready-to-use CrewAI tools that integrate with the [Olostep API](https://olostep.com).

## Installation

```bash
pip install crewai-olostep
```

Or install from source:
```bash
cd olostep-tools/integrations/crewai/crewai-olostep
pip install -e .
```

## Quick Start

```bash
export OLOSTEP_API_KEY="your_api_key_here"
```

```python
from crewai import Agent, Task, Crew
from crewai_olostep import olostep_scrape_tool, olostep_answer_tool

researcher = Agent(
    role="Web Researcher",
    goal="Find accurate information from the web",
    tools=[olostep_scrape_tool, olostep_answer_tool],
)

task = Task(
    description="Research Stripe's pricing",
    expected_output="Summary of Stripe's pricing tiers",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `olostep_scrape_tool` | Scrape single pages (markdown/HTML/text) |
| `olostep_batch_tool` | Process up to 10K URLs in parallel |
| `olostep_crawl_tool` | Crawl entire websites by following links |
| `olostep_sitemap_tool` | Extract all URLs from a website |
| `olostep_answer_tool` | AI-powered web search with structured output |

## Documentation

See full documentation at [docs.olostep.com/integrations/crewai](https://docs.olostep.com/integrations/crewai)

