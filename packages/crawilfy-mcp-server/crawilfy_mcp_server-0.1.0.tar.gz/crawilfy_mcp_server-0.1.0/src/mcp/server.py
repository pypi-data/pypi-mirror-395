"""MCP Server implementation for Crawilfy."""

import asyncio
import logging
import json
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.types import Tool, TextContent

from ..core.browser.pool import BrowserPool
from ..core.browser.stealth import create_stealth_context
from ..intelligence.network.interceptor import DeepNetworkInterceptor
from ..intelligence.network.api_discovery import APIDiscoveryEngine
from ..intelligence.network.analyzer import RequestAnalyzer
from ..intelligence.js.analyzer import JSAnalyzer
from ..intelligence.js.deobfuscator import JSDeobfuscator
from ..intelligence.recorder.session import SessionRecorder, SessionRecording, Event, EventType, StateSnapshot
from ..intelligence.security.bot_detection import BotDetectionAnalyzer
from ..intelligence.generator.crawler_gen import CrawlerGenerator

logger = logging.getLogger(__name__)

# Initialize global instances
browser_pool = BrowserPool()
network_interceptor = DeepNetworkInterceptor()
api_discovery = APIDiscoveryEngine()
request_analyzer = RequestAnalyzer()
js_analyzer = JSAnalyzer()
js_deobfuscator = JSDeobfuscator()
bot_detector = BotDetectionAnalyzer()

# Initialize browser pool
async def init_browser_pool():
    """Initialize browser pool."""
    await browser_pool.initialize()

# MCP Server
server = Server("crawilfy-mcp-server")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="deep_analyze",
            description="Deep analysis of a website (network + JS + security)",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to analyze"
                    },
                    "depth": {
                        "type": "string",
                        "enum": ["basic", "full"],
                        "description": "Analysis depth",
                        "default": "full"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="discover_apis",
            description="Discover all APIs including hidden and internal ones",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Website URL"
                    },
                    "include_hidden": {
                        "type": "boolean",
                        "description": "Include hidden APIs",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="introspect_graphql",
            description="Extract complete GraphQL schema",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "GraphQL endpoint URL"
                    }
                },
                "required": ["endpoint"]
            }
        ),
        Tool(
            name="analyze_websocket",
            description="Intercept and decode WebSocket messages",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Page URL with WebSocket connection"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="record_session",
            description="Start recording an interactive session",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Starting URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="generate_crawler",
            description="Generate crawler from recording",
            inputSchema={
                "type": "object",
                "properties": {
                    "recording_id": {
                        "type": "string",
                        "description": "Recording ID"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["yaml", "python", "playwright"],
                        "default": "yaml"
                    }
                },
                "required": ["recording_id"]
            }
        ),
        Tool(
            name="analyze_auth",
            description="Analyze authentication flow",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Login page URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="detect_protection",
            description="Detect anti-bot systems",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Website URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="deobfuscate_js",
            description="Deobfuscate JavaScript code",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Obfuscated JavaScript code"
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="extract_from_js",
            description="Extract API/URL/keys from JavaScript code",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "JavaScript code"
                    }
                },
                "required": ["code"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "deep_analyze":
            result = await handle_deep_analyze(arguments)
        elif name == "discover_apis":
            result = await handle_discover_apis(arguments)
        elif name == "introspect_graphql":
            result = await handle_introspect_graphql(arguments)
        elif name == "analyze_websocket":
            result = await handle_analyze_websocket(arguments)
        elif name == "record_session":
            result = await handle_record_session(arguments)
        elif name == "generate_crawler":
            result = await handle_generate_crawler(arguments)
        elif name == "analyze_auth":
            result = await handle_analyze_auth(arguments)
        elif name == "detect_protection":
            result = await handle_detect_protection(arguments)
        elif name == "deobfuscate_js":
            result = await handle_deobfuscate_js(arguments)
        elif name == "extract_from_js":
            result = await handle_extract_from_js(arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def handle_deep_analyze(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle deep_analyze tool."""
    url = arguments["url"]
    depth = arguments.get("depth", "full")
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    # Start network interception
    await network_interceptor.start_intercepting(page)
    
    # Navigate to URL
    await page.goto(url, wait_until="networkidle")
    
    # Get page content
    content = await page.content()
    
    # Analyze network
    requests = await network_interceptor.capture_all_requests()
    responses = await network_interceptor.capture_all_responses()
    
    # Discover APIs
    api_discovery.detect_rest_endpoints(requests, responses)
    graphql_endpoint = api_discovery.detect_graphql(requests, responses)
    
    # Analyze security
    protection_type = bot_detector.detect_protection_type(content, {})
    fingerprinting = bot_detector.analyze_fingerprinting(content)
    
    # Analyze JavaScript
    js_code = await page.evaluate("() => document.documentElement.outerHTML")
    api_calls = js_analyzer.extract_api_calls(js_code)
    
    result = {
        "url": url,
        "apis": {
            "rest": len(api_discovery.discovered_apis),
            "graphql": 1 if graphql_endpoint else 0,
            "websocket": len(network_interceptor.websockets),
        },
        "protection": protection_type.value if protection_type else "none",
        "fingerprinting": {
            "canvas": fingerprinting.canvas_fingerprint,
            "webgl": fingerprinting.webgl_fingerprint,
            "audio": fingerprinting.audio_fingerprint,
        },
        "network_requests": len(requests),
        "api_calls_found": len(api_calls),
    }
    
    await page.close()
    await context.close()
    
    return result


async def handle_discover_apis(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle discover_apis tool."""
    url = arguments["url"]
    include_hidden = arguments.get("include_hidden", True)
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    await network_interceptor.start_intercepting(page)
    await page.goto(url, wait_until="networkidle")
    
    requests = await network_interceptor.capture_all_requests()
    responses = await network_interceptor.capture_all_responses()
    
    # Discover APIs
    rest_endpoints = api_discovery.detect_rest_endpoints(requests, responses)
    graphql_endpoint = api_discovery.detect_graphql(requests, responses)
    
    internal_apis = []
    if include_hidden:
        internal_apis = api_discovery.find_undocumented_endpoints(requests)
    
    result = {
        "rest_endpoints": [
            {
                "url": ep.url,
                "method": ep.method,
                "path": ep.path,
            }
            for ep in rest_endpoints
        ],
        "graphql": {
            "url": graphql_endpoint.url if graphql_endpoint else None,
        },
        "internal_apis": [
            {
                "url": api.url,
                "method": api.method,
                "confidence": api.confidence,
            }
            for api in internal_apis
        ],
    }
    
    await page.close()
    await context.close()
    
    return result


async def handle_introspect_graphql(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle introspect_graphql tool."""
    endpoint = arguments["endpoint"]
    
    schema = await api_discovery.run_introspection(endpoint)
    
    if schema:
        operations = api_discovery.extract_queries_mutations(schema)
        return {
            "endpoint": endpoint,
            "schema": schema,
            "operations": [
                {
                    "name": op.name,
                    "type": op.type,
                }
                for op in operations
            ],
        }
    else:
        return {
            "endpoint": endpoint,
            "error": "Introspection failed or not enabled",
        }


async def handle_analyze_websocket(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle analyze_websocket tool."""
    url = arguments["url"]
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    await network_interceptor.start_intercepting(page)
    await page.goto(url, wait_until="networkidle")
    
    # Wait for WebSocket connections
    await asyncio.sleep(2)
    
    ws_session = await network_interceptor.intercept_websocket()
    
    if ws_session:
        messages = await network_interceptor.decode_ws_messages(ws_session.url)
        return {
            "url": ws_session.url,
            "messages": [
                {
                    "direction": msg.direction,
                    "message": msg.message[:100] + "..." if len(msg.message) > 100 else msg.message,
                    "type": msg.message_type,
                }
                for msg in messages[:10]  # Limit to first 10
            ],
        }
    else:
        return {
            "error": "No WebSocket connections found",
        }


async def handle_record_session(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle record_session tool."""
    url = arguments["url"]
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    recorder = SessionRecorder()
    recording = await recorder.start_recording(page)
    
    await page.goto(url)
    
    return {
        "recording_id": recording.id,
        "status": "recording",
        "message": "Session recording started. Use stop_recording to finish.",
    }


async def handle_generate_crawler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle generate_crawler tool."""
    recording_id = arguments["recording_id"]
    output_format = arguments.get("output_format", "yaml")
    
    # Load recording (in a real implementation, this would load from storage)
    # For now, we'll need to get the recording from active sessions or storage
    # This is a simplified version - in production, you'd have a recording storage system
    
    # Try to find recording in active recorders or load from file
    # For MCP, we might need to store recordings temporarily or have a storage system
    # For now, return an error if recording not found in active sessions
    
    # Check if we have an active recording with this ID
    # In a full implementation, you'd have a recording storage/manager
    # For now, we'll create a minimal implementation that expects the recording
    # to be passed or stored somewhere accessible
    
    generator = CrawlerGenerator()
    
    # Since we don't have a recording storage system yet, we'll need to
    # either: 1) Store recordings in memory, 2) Load from file path, or 3) Use recording_id as file path
    # For now, let's assume recording_id could be a file path or we need to implement storage
    
    try:
        # Try to load from file if recording_id looks like a path
        import os
        if os.path.exists(recording_id):
            recording = _load_recording_from_file(recording_id)
        else:
            # In a full implementation, you'd query a recording storage
            return {
                "error": f"Recording {recording_id} not found. Please provide a file path or ensure recording is stored.",
                "recording_id": recording_id,
            }
        
        # Generate crawler from recording
        crawler_def = generator.from_recording(recording)
        crawler_def = generator.optimize_crawler(crawler_def)
        
        # Convert to requested format
        if output_format == "yaml":
            output = generator.to_yaml(crawler_def)
        elif output_format == "python":
            output = generator.to_python_code(crawler_def)
        elif output_format == "playwright":
            output = generator.to_playwright_script(crawler_def)
        else:
            output = generator.to_yaml(crawler_def)
        
        return {
            "recording_id": recording_id,
            "output_format": output_format,
            "status": "generated",
            "crawler": {
                "name": crawler_def.name,
                "description": crawler_def.description,
                "steps_count": len(crawler_def.steps),
            },
            "output": output,
        }
    except Exception as e:
        logger.error(f"Error generating crawler: {e}", exc_info=True)
        return {
            "error": str(e),
            "recording_id": recording_id,
        }


def _load_recording_from_file(file_path: str) -> SessionRecording:
    """Load recording from JSON file."""
    import json
    from datetime import datetime
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Reconstruct events from saved data
    # Note: This is a simplified version - full implementation would
    # properly deserialize all event types
    events = []
    if "events" in data:
        for event_data in data.get("events", []):
            try:
                event_type = EventType(event_data.get("type", "click"))
                events.append(Event(
                    type=event_type,
                    timestamp=datetime.fromisoformat(event_data.get("timestamp", datetime.now().isoformat())),
                    data=event_data.get("data", {}),
                    selector=event_data.get("selector"),
                ))
            except Exception as e:
                logger.warning(f"Error loading event: {e}")
    
    # Reconstruct state snapshots
    state_snapshots = []
    if "state_snapshots" in data:
        for snap_data in data.get("state_snapshots", []):
            try:
                state_snapshots.append(StateSnapshot(
                    url=snap_data.get("url", ""),
                    html=snap_data.get("html", ""),
                    timestamp=datetime.fromisoformat(snap_data.get("timestamp", datetime.now().isoformat())),
                    cookies=snap_data.get("cookies", {}),
                    local_storage=snap_data.get("local_storage", {}),
                ))
            except Exception as e:
                logger.warning(f"Error loading snapshot: {e}")
    
    recording = SessionRecording(
        id=data.get("id", "unknown"),
        events=events,
        state_snapshots=state_snapshots,
        duration=data.get("duration", 0.0),
    )
    
    return recording


async def handle_analyze_auth(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle analyze_auth tool."""
    url = arguments["url"]
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    await network_interceptor.start_intercepting(page)
    await page.goto(url, wait_until="networkidle")
    
    requests = await network_interceptor.capture_all_requests()
    
    auth_requests = []
    for req in requests:
        analyzed = request_analyzer.analyze(req)
        if analyzed.auth_type.value != "none":
            auth_requests.append({
                "url": analyzed.url,
                "auth_type": analyzed.auth_type.value,
            })
    
    await page.close()
    await context.close()
    
    return {
        "url": url,
        "auth_flows": auth_requests,
    }


async def handle_detect_protection(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle detect_protection tool."""
    url = arguments["url"]
    
    context = await create_stealth_context(browser_pool)
    page = await context.new_page()
    
    await page.goto(url, wait_until="networkidle")
    content = await page.content()
    
    response = await page.goto(url)
    headers = response.headers if response else {}
    
    protection_type = bot_detector.detect_protection_type(content, headers)
    fingerprinting = bot_detector.analyze_fingerprinting(content)
    captcha_type = bot_detector.detect_captcha_type(content)
    
    await page.close()
    await context.close()
    
    return {
        "url": url,
        "protection_type": protection_type.value,
        "captcha_type": captcha_type.value,
        "fingerprinting": {
            "canvas": fingerprinting.canvas_fingerprint,
            "webgl": fingerprinting.webgl_fingerprint,
            "audio": fingerprinting.audio_fingerprint,
        },
    }


async def handle_deobfuscate_js(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle deobfuscate_js tool."""
    code = arguments["code"]
    
    # Detect obfuscation type
    obfuscation_type = js_deobfuscator.detect_obfuscation_type(code)
    
    # Deobfuscate based on type
    deobfuscated = code
    if obfuscation_type.value == "string_encoding":
        deobfuscated = js_deobfuscator.deobfuscate_strings(code)
    elif obfuscation_type.value == "control_flow_flattening":
        deobfuscated = js_deobfuscator.simplify_control_flow(code)
    else:
        # Try all deobfuscation methods
        deobfuscated = js_deobfuscator.deobfuscate_strings(code)
        deobfuscated = js_deobfuscator.simplify_control_flow(deobfuscated)
    
    # Extract original names if possible
    name_map = js_deobfuscator.extract_original_names(code)
    
    return {
        "original_length": len(code),
        "deobfuscated_length": len(deobfuscated),
        "obfuscation_type": obfuscation_type.value,
        "deobfuscated": deobfuscated,
        "extracted_names": name_map,
        "improvement": f"{((len(code) - len(deobfuscated)) / len(code) * 100):.1f}% size change" if code else "0%",
    }


async def handle_extract_from_js(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle extract_from_js tool."""
    code = arguments["code"]
    
    api_calls = js_analyzer.extract_api_calls(code)
    urls = js_analyzer.find_hardcoded_urls(code)
    constants = js_analyzer.extract_constants(code)
    auth_logic = js_analyzer.find_auth_logic(code)
    
    return {
        "api_calls": [
            {
                "url": call.url,
                "method": call.method,
                "type": call.type,
            }
            for call in api_calls
        ],
        "hardcoded_urls": urls,
        "constants": constants,
        "auth_logic": {
            "flow_type": auth_logic.flow_type if auth_logic else None,
            "token_storage": auth_logic.token_storage if auth_logic else None,
        },
    }


async def main():
    """Main entry point for MCP server."""
    await init_browser_pool()
    
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

