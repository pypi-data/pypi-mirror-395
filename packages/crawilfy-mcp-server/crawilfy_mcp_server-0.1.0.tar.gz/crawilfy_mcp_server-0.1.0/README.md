# Crawilfy MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Advanced web crawling platform with deep analysis capabilities, automatic API discovery, and crawler generation. Built as an MCP (Model Context Protocol) server for seamless integration with AI assistants and development tools.

## Features

### 🔧 Core Engine
- Browser Pool Manager with context isolation
- Session & Credential Manager with rotation
- Advanced Cache Layer

### 🌐 Deep Network Engine
- Network Interceptor for HTTP/HTTPS/WebSocket
- API Discovery Engine (REST, GraphQL, Hidden APIs)
- Request Analyzer with auth and pagination analysis

### 📜 JavaScript Analysis
- Static Code Analyzer
- Dynamic Runtime Analysis
- JS Deobfuscator

### 🎬 Session Recording & Replay
- Full Session Recorder
- State Machine Generator
- Automatic Crawler Generation

### 🛡️ Security & Anti-Bot
- Bot Detection Analyzer
- Stealth Mode
- Auth Flow Analyzer

### 🔌 MCP Server
MCP Protocol support with advanced tools for analysis and crawling.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

### CLI

```bash
# Deep analysis
python -m src.cli.main deep-analyze https://example.com --full

# Discover APIs
python -m src.cli.main discover-apis https://example.com --include-hidden

# Record session
python -m src.cli.main record https://example.com --output session.json

# Generate crawler
python -m src.cli.main generate --from-recording session.json --output crawler.yaml
```

### MCP Server

```bash
python -m src.mcp.server
```

The MCP server provides the following tools:
- `deep_analyze`: Deep analysis of a website
- `discover_apis`: Discover all APIs
- `introspect_graphql`: Extract GraphQL schema
- `analyze_websocket`: Analyze WebSocket connections
- `record_session`: Record interactive session
- `generate_crawler`: Generate crawler from recording
- `analyze_auth`: Analyze authentication flow
- `detect_protection`: Detect anti-bot systems
- `deobfuscate_js`: Deobfuscate JavaScript code
- `extract_from_js`: Extract API/URL/keys from JavaScript

### Python API Example

```python
import asyncio
from src.core.browser.pool import BrowserPool
from src.core.browser.stealth import create_stealth_context
from src.intelligence.network.interceptor import DeepNetworkInterceptor
from src.intelligence.network.api_discovery import APIDiscoveryEngine

async def analyze_site(url):
    pool = BrowserPool()
    await pool.initialize()
    
    try:
        context = await create_stealth_context(pool)
        page = await context.new_page()
        
        interceptor = DeepNetworkInterceptor()
        await interceptor.start_intercepting(page)
        
        await page.goto(url)
        
        requests = await interceptor.capture_all_requests()
        responses = await interceptor.capture_all_responses()
        
        discovery = APIDiscoveryEngine()
        endpoints = discovery.detect_rest_endpoints(requests, responses)
        
        print(f"Found {len(endpoints)} API endpoints")
        
        await page.close()
        await context.close()
    finally:
        await pool.close()

asyncio.run(analyze_site("https://example.com"))
```

## Project Structure

```
src/
├── core/           # Core engine
│   ├── browser/    # Browser management
│   ├── session/    # Session management
│   └── cache/      # Cache layer
├── intelligence/   # Analysis engines
│   ├── network/    # Network analysis
│   ├── js/         # JavaScript analysis
│   ├── security/   # Security analysis
│   ├── recorder/   # Session recording
│   └── generator/  # Crawler generation
├── mcp/            # MCP Server
├── cli/            # Command line interface
└── crawlers/       # Generated crawlers
```

## Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Install Playwright browsers
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_browser_pool.py
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type checking
mypy src
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.
