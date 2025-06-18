import asyncio
import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add the parent directory to the path so we can import server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import GeminiMCPServer, Request


@pytest.fixture
def mock_requests():
    """Mock the requests library."""
    with patch("server.requests") as mock:
        yield mock


@pytest.fixture
async def server_instance():
    """Create a test server instance."""
    with patch.dict("os.environ", {"GEMINI_API_KEY": "test-api-key"}):
        instance = GeminiMCPServer()
        yield instance


class TestGeminiMCPServer:
    """Test suite for GeminiMCPServer."""

    @pytest.mark.asyncio
    async def test_server_initialization_with_api_key(self):
        """Test server initializes correctly with API key."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            instance = GeminiMCPServer()
            assert instance.api_configured is True
            assert instance.api_key == "test-key"

    @pytest.mark.asyncio
    async def test_server_initialization_no_api_key(self):
        """Test server initializes without API key."""
        with patch.dict("os.environ", {}, clear=True):
            instance = GeminiMCPServer()
            assert instance.api_configured is False

    @pytest.mark.asyncio
    async def test_handle_initialize(self, server_instance):
        """Test initialize request handling."""
        request = Request(id=1, method="initialize", params={})
        response = await server_instance.handle_request(request)

        assert response.id == 1
        assert response.result is not None
        assert response.result["protocolVersion"] == "2024-11-05"
        assert "capabilities" in response.result
        assert "serverInfo" in response.result

    @pytest.mark.asyncio
    async def test_handle_tools_list(self, server_instance):
        """Test tools/list request handling."""
        request = Request(id=2, method="tools/list", params={})
        response = await server_instance.handle_request(request)

        assert response.id == 2
        assert response.result is not None
        assert "tools" in response.result
        tools = response.result["tools"]
        assert len(tools) == 4

        tool_names = [tool["name"] for tool in tools]
        assert "ask_gemini" in tool_names
        assert "gemini_code_review" in tool_names
        assert "gemini_brainstorm" in tool_names
        assert "gemini_analyze_large" in tool_names

    @pytest.mark.asyncio
    async def test_handle_unknown_method(self, server_instance):
        """Test handling of unknown method."""
        request = Request(id=3, method="unknown/method", params={})
        response = await server_instance.handle_request(request)

        assert response.id == 3
        assert response.error is not None
        assert response.error["code"] == -32601
        assert "Method not found" in response.error["message"]

    @pytest.mark.asyncio
    async def test_tools_call_no_api_key(self):
        """Test tools/call without API key configured."""
        with patch.dict("os.environ", {}, clear=True):
            instance = GeminiMCPServer()
            request = Request(
                id=4,
                method="tools/call",
                params={"name": "ask_gemini", "arguments": {"question": "test"}},
            )
            response = await instance.handle_request(request)

            assert response.error is not None
            assert "Gemini API not configured" in response.error["message"]

    @pytest.mark.asyncio
    async def test_tools_call_missing_name(self, server_instance):
        """Test tools/call with missing tool name."""
        request = Request(id=5, method="tools/call", params={})
        response = await server_instance.handle_request(request)

        assert response.error is not None
        assert response.error["code"] == -32602
        assert "missing tool name" in response.error["message"]

    @pytest.mark.asyncio
    async def test_tools_call_unknown_tool(self, server_instance):
        """Test tools/call with unknown tool."""
        request = Request(
            id=6, method="tools/call", params={"name": "unknown_tool", "arguments": {}}
        )
        response = await server_instance.handle_request(request)

        assert response.error is not None
        assert response.error["code"] == -32602
        assert "Unknown tool" in response.error["message"]

    @pytest.mark.asyncio
    async def test_ask_gemini_success(self, server_instance, mock_requests):
        """Test successful ask_gemini call."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Test response"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        request = Request(
            id=7,
            method="tools/call",
            params={"name": "ask_gemini", "arguments": {"question": "Test question"}},
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert response.result["content"][0]["text"] == "Test response"

    @pytest.mark.asyncio
    async def test_ask_gemini_empty_question(self, server_instance):
        """Test ask_gemini with empty question."""
        request = Request(
            id=8,
            method="tools/call",
            params={"name": "ask_gemini", "arguments": {"question": ""}},
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert "Please provide a question" in response.result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_code_review_success(self, server_instance, mock_requests):
        """Test successful code review."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Code review feedback"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        request = Request(
            id=9,
            method="tools/call",
            params={
                "name": "gemini_code_review",
                "arguments": {
                    "code": "def hello(): print('world')",
                    "context": "test.py",
                    "focus_areas": "Check for bugs",
                },
            },
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert response.result["content"][0]["text"] == "Code review feedback"

    @pytest.mark.asyncio
    async def test_code_review_empty_code(self, server_instance):
        """Test code review with empty code."""
        request = Request(
            id=10,
            method="tools/call",
            params={"name": "gemini_code_review", "arguments": {"code": ""}},
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert "Please provide code to review" in response.result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_brainstorm_success(self, server_instance, mock_requests):
        """Test successful brainstorming."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Brainstorm ideas"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        request = Request(
            id=11,
            method="tools/call",
            params={
                "name": "gemini_brainstorm",
                "arguments": {"topic": "Test topic", "constraints": "Test constraints"},
            },
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert response.result["content"][0]["text"] == "Brainstorm ideas"

    @pytest.mark.asyncio
    async def test_analyze_large_success(self, server_instance, mock_requests):
        """Test successful large content analysis."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Analysis results"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        request = Request(
            id=12,
            method="tools/call",
            params={
                "name": "gemini_analyze_large",
                "arguments": {
                    "content": "x" * 10000,
                    "analysis_type": "performance",
                    "questions": "specific questions",
                },
            },
        )
        response = await server_instance.handle_request(request)

        assert response.result is not None
        assert response.result["content"][0]["text"] == "Analysis results"

    @pytest.mark.asyncio
    async def test_analyze_large_truncation(self, server_instance, mock_requests):
        """Test that large content is truncated properly."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Truncated analysis"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        # Create content larger than the limit
        large_content = "x" * 35000
        request = Request(
            id=13,
            method="tools/call",
            params={
                "name": "gemini_analyze_large",
                "arguments": {
                    "content": large_content,
                    "analysis_type": "general",
                    "questions": "",
                },
            },
        )
        await server_instance.handle_request(request)

        # Check that the content was truncated
        call_args = mock_requests.post.call_args
        payload = call_args[1]["json"]
        sent_content = payload["contents"][0]["parts"][0]["text"]
        assert "[Content truncated due to size...]" in sent_content

    @pytest.mark.asyncio
    async def test_api_error_handling(self, server_instance, mock_requests):
        """Test API error handling."""
        mock_requests.post.side_effect = Exception("API Error")

        request = Request(
            id=14,
            method="tools/call",
            params={"name": "ask_gemini", "arguments": {"question": "Test"}},
        )
        response = await server_instance.handle_request(request)

        assert response.error is not None
        assert "Error calling Gemini" in response.error["message"]

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, server_instance, mock_requests):
        """Test server handles concurrent requests properly."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Concurrent response"}]}}]
        }
        mock_response.raise_for_status = Mock()
        mock_requests.post.return_value = mock_response

        # Create multiple requests
        requests = [
            Request(
                id=i,
                method="tools/call",
                params={
                    "name": "ask_gemini",
                    "arguments": {"question": f"Question {i}"},
                },
            )
            for i in range(5)
        ]

        # Handle them concurrently
        tasks = [server_instance.handle_request(req) for req in requests]
        responses = await asyncio.gather(*tasks)

        assert len(responses) == 5
        for i, response in enumerate(responses):
            assert response.id == i
            assert response.result["content"][0]["text"] == "Concurrent response"
