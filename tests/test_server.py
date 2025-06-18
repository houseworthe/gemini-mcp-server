import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from server import GeminiMCPServer


@pytest.fixture
def mock_model():
    """Create a mock Gemini model."""
    with patch('google.generativeai.GenerativeModel') as mock:
        model_instance = Mock()
        model_instance.generate_content_async = AsyncMock()
        mock.return_value = model_instance
        yield model_instance


@pytest.fixture
async def server(mock_model):
    """Create a test server instance."""
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-api-key'}):
        server = GeminiMCPServer()
        server.model = mock_model
        yield server


class TestGeminiMCPServer:
    """Test suite for GeminiMCPServer."""
    
    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test server initializes correctly with API key."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            with patch('google.generativeai.configure') as mock_configure:
                server = GeminiMCPServer()
                mock_configure.assert_called_once_with(api_key='test-key')
    
    @pytest.mark.asyncio
    async def test_server_initialization_no_api_key(self):
        """Test server raises error without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
                server = GeminiMCPServer()
    
    @pytest.mark.asyncio
    async def test_ask_gemini_success(self, server, mock_model):
        """Test successful ask_gemini call."""
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_model.generate_content_async.return_value = mock_response
        
        result = await server.ask_gemini("Test question")
        
        assert result == "Test response"
        mock_model.generate_content_async.assert_called_once_with(
            "Test question",
            generation_config=server.generation_config
        )
    
    @pytest.mark.asyncio
    async def test_ask_gemini_error_handling(self, server, mock_model):
        """Test ask_gemini error handling."""
        mock_model.generate_content_async.side_effect = Exception("API Error")
        
        with pytest.raises(RuntimeError, match="Gemini API error: API Error"):
            await server.ask_gemini("Test question")
    
    @pytest.mark.asyncio
    async def test_code_review_success(self, server, mock_model):
        """Test successful code review."""
        mock_response = Mock()
        mock_response.text = "Code review feedback"
        mock_model.generate_content_async.return_value = mock_response
        
        code = "def hello(): print('world')"
        result = await server.code_review(code, "test.py", "Check for bugs")
        
        assert result == "Code review feedback"
        call_args = mock_model.generate_content_async.call_args[0][0]
        assert "def hello(): print('world')" in call_args
        assert "test.py" in call_args
        assert "Check for bugs" in call_args
    
    @pytest.mark.asyncio
    async def test_brainstorm_success(self, server, mock_model):
        """Test successful brainstorming."""
        mock_response = Mock()
        mock_response.text = "Brainstorm ideas"
        mock_model.generate_content_async.return_value = mock_response
        
        result = await server.brainstorm("Test topic", "Test constraints")
        
        assert result == "Brainstorm ideas"
        call_args = mock_model.generate_content_async.call_args[0][0]
        assert "Test topic" in call_args
        assert "Test constraints" in call_args
    
    @pytest.mark.asyncio
    async def test_analyze_large_content(self, server, mock_model):
        """Test large content analysis."""
        mock_response = Mock()
        mock_response.text = "Analysis results"
        mock_model.generate_content_async.return_value = mock_response
        
        large_content = "x" * 10000  # Simulate large content
        result = await server.analyze_large(large_content, "performance", "specific questions")
        
        assert result == "Analysis results"
        call_args = mock_model.generate_content_async.call_args[0][0]
        assert large_content in call_args
        assert "performance" in call_args
        assert "specific questions" in call_args
    
    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test list_tools returns all expected tools."""
        tools = await server.list_tools()
        
        tool_names = [tool["name"] for tool in tools]
        assert "ask_gemini" in tool_names
        assert "gemini_code_review" in tool_names
        assert "gemini_brainstorm" in tool_names
        assert "gemini_analyze_large" in tool_names
        assert len(tools) == 4
    
    @pytest.mark.asyncio
    async def test_call_tool_ask_gemini(self, server, mock_model):
        """Test calling ask_gemini through call_tool."""
        mock_response = Mock()
        mock_response.text = "Tool response"
        mock_model.generate_content_async.return_value = mock_response
        
        result = await server.call_tool("ask_gemini", {"question": "Test"})
        
        assert result["content"][0]["type"] == "text"
        assert result["content"][0]["text"] == "Tool response"
    
    @pytest.mark.asyncio
    async def test_call_tool_invalid_tool(self, server):
        """Test calling invalid tool raises error."""
        with pytest.raises(ValueError, match="Unknown tool: invalid_tool"):
            await server.call_tool("invalid_tool", {})
    
    @pytest.mark.asyncio
    async def test_call_tool_missing_arguments(self, server):
        """Test calling tool with missing arguments."""
        with pytest.raises(TypeError):
            await server.call_tool("ask_gemini", {})
    
    @pytest.mark.asyncio
    async def test_generation_config(self, server):
        """Test generation config is properly set."""
        assert server.generation_config["temperature"] == 0.7
        assert server.generation_config["top_p"] == 0.9
        assert server.generation_config["top_k"] == 40
        assert server.generation_config["max_output_tokens"] == 8192
    
    @pytest.mark.asyncio
    async def test_code_review_with_empty_context(self, server, mock_model):
        """Test code review with empty context."""
        mock_response = Mock()
        mock_response.text = "Review"
        mock_model.generate_content_async.return_value = mock_response
        
        result = await server.code_review("code", "", "")
        assert result == "Review"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, server, mock_model):
        """Test server handles concurrent requests properly."""
        mock_response = Mock()
        mock_response.text = "Concurrent response"
        mock_model.generate_content_async.return_value = mock_response
        
        # Make multiple concurrent requests
        tasks = [
            server.ask_gemini(f"Question {i}")
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert all(r == "Concurrent response" for r in results)
        assert mock_model.generate_content_async.call_count == 5