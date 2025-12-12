"""Tests for MCP server."""

import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch

from src.mcp.server import (
    server,
    list_tools,
    call_tool,
    handle_deep_analyze,
    handle_discover_apis,
    handle_deobfuscate_js,
    handle_extract_from_js,
)


@pytest.mark.asyncio
async def test_list_tools():
    """Test listing available tools."""
    tools = await list_tools()
    
    assert len(tools) > 0
    assert any(tool.name == "deep_analyze" for tool in tools)
    assert any(tool.name == "discover_apis" for tool in tools)
    assert any(tool.name == "deobfuscate_js" for tool in tools)


@pytest.mark.asyncio
async def test_tool_schemas():
    """Test tool input schemas are valid."""
    tools = await list_tools()
    
    for tool in tools:
        assert tool.inputSchema is not None
        assert "type" in tool.inputSchema
        assert tool.inputSchema["type"] == "object"
        assert "properties" in tool.inputSchema


@pytest.mark.asyncio
async def test_call_tool_deep_analyze():
    """Test calling deep_analyze tool."""
    arguments = {
        "url": "https://example.com",
        "depth": "full",
    }
    
    with patch("src.mcp.server.handle_deep_analyze") as mock_handle:
        mock_handle.return_value = {"status": "success"}
        
        result = await call_tool("deep_analyze", arguments)
        
        assert len(result) > 0
        assert result[0].type == "text"
        mock_handle.assert_called_once_with(arguments)


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Test calling unknown tool."""
    arguments = {}
    
    result = await call_tool("unknown_tool", arguments)
    
    assert len(result) > 0
    data = json.loads(result[0].text)
    assert "error" in data


@pytest.mark.asyncio
async def test_call_tool_exception():
    """Test tool call with exception."""
    arguments = {"url": "https://example.com"}
    
    with patch("src.mcp.server.handle_deep_analyze") as mock_handle:
        mock_handle.side_effect = Exception("Test error")
        
        result = await call_tool("deep_analyze", arguments)
        
        assert len(result) > 0
        data = json.loads(result[0].text)
        assert "error" in data


@pytest.mark.asyncio
async def test_handle_deobfuscate_js():
    """Test deobfuscate_js handler."""
    arguments = {
        "code": "var _0x1234=['test'];",
    }
    
    result = await handle_deobfuscate_js(arguments)
    
    assert "deobfuscated" in result
    assert "obfuscation_type" in result
    assert "original_length" in result


@pytest.mark.asyncio
async def test_handle_extract_from_js():
    """Test extract_from_js handler."""
    arguments = {
        "code": "fetch('https://api.example.com');",
    }
    
    result = await handle_extract_from_js(arguments)
    
    assert "api_calls" in result
    assert "hardcoded_urls" in result
    assert "constants" in result


@pytest.mark.asyncio
async def test_handle_discover_apis():
    """Test discover_apis handler."""
    arguments = {
        "url": "https://example.com",
        "include_hidden": True,
    }
    
    with patch("src.mcp.server.browser_pool") as mock_pool:
        mock_context = AsyncMock()
        mock_page = AsyncMock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        mock_pool.acquire = AsyncMock(return_value=mock_context)
        
        with patch("src.mcp.server.network_interceptor") as mock_interceptor:
            mock_interceptor.start_intercepting = AsyncMock()
            mock_interceptor.capture_all_requests = AsyncMock(return_value=[])
            mock_interceptor.capture_all_responses = AsyncMock(return_value=[])
            
            with patch("src.mcp.server.api_discovery") as mock_discovery:
                mock_discovery.detect_rest_endpoints.return_value = []
                mock_discovery.detect_graphql.return_value = None
                mock_discovery.find_undocumented_endpoints.return_value = []
                
                result = await handle_discover_apis(arguments)
                
                assert "rest_endpoints" in result
                assert "graphql" in result
                assert "internal_apis" in result


@pytest.mark.asyncio
async def test_tool_descriptions():
    """Test all tools have descriptions."""
    tools = await list_tools()
    
    for tool in tools:
        assert tool.description is not None
        assert len(tool.description) > 0


@pytest.mark.asyncio
async def test_tool_required_fields():
    """Test tool required fields are properly defined."""
    tools = await list_tools()
    
    for tool in tools:
        if "required" in tool.inputSchema:
            required = tool.inputSchema["required"]
            assert isinstance(required, list)
            assert all(field in tool.inputSchema["properties"] for field in required)

