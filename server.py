#!/usr/bin/env python3
"""
Gemini MCP Server v1 - using direct HTTP requests
"""

import asyncio
import json
import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging to file instead of stderr
log_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(log_dir, "gemini-mcp.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, mode="a"),
    ],
)
logger = logging.getLogger(__name__)

# Thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=2)


@dataclass
class Request:
    id: Optional[str]
    method: str
    params: Optional[Dict[str, Any]] = None


@dataclass
class Response:
    id: Optional[str]
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class GeminiMCPServer:
    def __init__(self):
        # Configure Gemini
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            self.api_configured = False
        else:
            self.api_configured = True
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
            logger.info("Gemini API configured successfully")

        self.running = True

    async def handle_request(self, request: Request) -> Response:
        """Handle incoming JSON-RPC request"""
        try:
            logger.debug(f"Handling request: method={request.method}, id={request.id}")

            if request.method == "initialize":
                return self._handle_initialize(request)
            elif request.method == "tools/list":
                return self._handle_tools_list(request)
            elif request.method == "tools/call":
                return await self._handle_tools_call(request)
            else:
                return Response(
                    id=request.id,
                    error={
                        "code": -32601,
                        "message": f"Method not found: {request.method}",
                    },
                )
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            return Response(id=request.id, error={"code": -32603, "message": str(e)})

    def _handle_initialize(self, request: Request) -> Response:
        """Handle initialize request"""
        return Response(
            id=request.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "gemini-collab", "version": "1.0.0"},
            },
        )

    def _handle_tools_list(self, request: Request) -> Response:
        """Handle tools/list request"""
        tools = [
            {
                "name": "ask_gemini",
                "description": "Ask Gemini a question",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "Question to ask"}
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "gemini_code_review",
                "description": "Get code review from Gemini (supports large codebases)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Code to review (can be very large)",
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context",
                            "default": "",
                        },
                        "focus_areas": {
                            "type": "string",
                            "description": "Specific areas to focus on",
                            "default": "",
                        },
                    },
                    "required": ["code"],
                },
            },
            {
                "name": "gemini_brainstorm",
                "description": "Brainstorm ideas with Gemini",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to brainstorm",
                        },
                        "constraints": {
                            "type": "string",
                            "description": "Any constraints",
                            "default": "",
                        },
                    },
                    "required": ["topic"],
                },
            },
            {
                "name": "gemini_analyze_large",
                "description": "Analyze large documents or codebases with Gemini (optimized for 1M+ token contexts)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Large content to analyze (documents, logs, codebases)",
                        },
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of analysis needed",
                            "default": "general",
                        },
                        "questions": {
                            "type": "string",
                            "description": "Specific questions to answer",
                            "default": "",
                        },
                    },
                    "required": ["content"],
                },
            },
        ]

        return Response(id=request.id, result={"tools": tools})

    async def _handle_tools_call(self, request: Request) -> Response:
        """Handle tools/call request"""
        if not request.params or "name" not in request.params:
            return Response(
                id=request.id,
                error={"code": -32602, "message": "Invalid params: missing tool name"},
            )

        tool_name = request.params["name"]
        arguments = request.params.get("arguments", {})

        logger.info(f"Calling tool: {tool_name}")

        if not self.api_configured:
            return Response(
                id=request.id,
                error={
                    "code": -32603,
                    "message": "Gemini API not configured. Please set GEMINI_API_KEY environment variable.",
                },
            )

        try:
            # Run blocking API calls in thread pool
            if tool_name == "ask_gemini":
                result = await self._ask_gemini_async(arguments.get("question", ""))
            elif tool_name == "gemini_code_review":
                result = await self._code_review_async(
                    arguments.get("code", ""),
                    arguments.get("context", ""),
                    arguments.get("focus_areas", ""),
                )
            elif tool_name == "gemini_brainstorm":
                result = await self._brainstorm_async(
                    arguments.get("topic", ""), arguments.get("constraints", "")
                )
            elif tool_name == "gemini_analyze_large":
                result = await self._analyze_large_async(
                    arguments.get("content", ""),
                    arguments.get("analysis_type", "general"),
                    arguments.get("questions", ""),
                )
            else:
                return Response(
                    id=request.id,
                    error={"code": -32602, "message": f"Unknown tool: {tool_name}"},
                )

            return Response(
                id=request.id, result={"content": [{"type": "text", "text": result}]}
            )
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}", exc_info=True)
            return Response(
                id=request.id,
                error={"code": -32603, "message": f"Error calling Gemini: {str(e)}"},
            )

    def _call_gemini_api(self, prompt: str, model: str = "gemini-1.5-flash") -> str:
        """Make direct HTTP request to Gemini API"""
        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"

        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "No response generated"

        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return "Error: Request timed out after 30 seconds"
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return f"Error: {e}"
        except Exception as e:
            logger.error(f"API error: {e}")
            return f"Error: {str(e)}"

    async def _ask_gemini_async(self, question: str) -> str:
        """Ask Gemini a question (async wrapper)"""
        if not question:
            return "Please provide a question."

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, self._call_gemini_api, question)

    async def _code_review_async(
        self, code: str, context: str, focus_areas: str
    ) -> str:
        """Code review (async wrapper)"""
        if not code:
            return "Please provide code to review."

        prompt = f"""Please review the following code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Suggestions for improvement

{"Context: " + context if context else ""}
{"Focus areas: " + focus_areas if focus_areas else ""}

Code:
```
{code}
```
"""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, self._call_gemini_api, prompt)

    async def _brainstorm_async(self, topic: str, constraints: str) -> str:
        """Brainstorm (async wrapper)"""
        if not topic:
            return "Please provide a topic to brainstorm."

        prompt = f"""Let's brainstorm ideas about: {topic}

{"Constraints/Requirements: " + constraints if constraints else ""}

Please provide:
1. Creative ideas and approaches
2. Potential challenges to consider
3. Resources or tools that might help
4. Next steps to explore these ideas
"""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, self._call_gemini_api, prompt)

    async def _analyze_large_async(
        self, content: str, analysis_type: str, questions: str
    ) -> str:
        """Analyze large content (async wrapper)"""
        if not content:
            return "Please provide content to analyze."

        # Truncate if too large (Gemini has token limits)
        max_content_length = 30000  # Conservative limit
        if len(content) > max_content_length:
            content = (
                content[:max_content_length] + "\n\n[Content truncated due to size...]"
            )

        prompt = f"""Please analyze the following content.

Analysis type: {analysis_type}
{"Specific questions to answer: " + questions if questions else ""}

Content:
```
{content}
```

Provide a comprehensive analysis covering:
1. Key insights and patterns
2. Important findings
3. Potential issues or concerns
4. Recommendations
"""

        loop = asyncio.get_event_loop()
        # Try pro model for large content
        model = "gemini-1.5-pro" if len(content) > 10000 else "gemini-1.5-flash"
        return await loop.run_in_executor(
            executor, self._call_gemini_api, prompt, model
        )


async def read_stdin():
    """Read from stdin asynchronously"""
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


async def write_stdout(data: str):
    """Write to stdout asynchronously"""
    sys.stdout.write(data)
    sys.stdout.flush()


async def main():
    """Main server loop"""
    logger.info("Starting Gemini MCP Server v1")

    server = GeminiMCPServer()

    # Set up signal handling
    def signal_handler(sig, _frame):
        logger.info(f"Received signal {sig}, shutting down")
        server.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Read from stdin
        reader = await read_stdin()
        buffer = ""

        while server.running:
            try:
                # Read data with timeout to allow checking running flag
                data = await asyncio.wait_for(reader.read(1024), timeout=0.1)
                if not data:
                    logger.info("EOF received, shutting down")
                    break

                buffer += data.decode("utf-8")

                # Process complete lines
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        # Parse JSON-RPC request
                        request_data = json.loads(line)
                        logger.debug(f"Received: {line}")

                        # Create request object
                        request = Request(
                            id=request_data.get("id"),
                            method=request_data.get("method"),
                            params=request_data.get("params"),
                        )

                        # Handle request
                        response = await server.handle_request(request)

                        # Build response
                        response_data = {"jsonrpc": "2.0"}

                        if response.id is not None:
                            response_data["id"] = response.id

                        if response.error:
                            response_data["error"] = response.error
                        else:
                            response_data["result"] = response.result

                        # Send response
                        output = json.dumps(response_data) + "\n"
                        await write_stdout(output)
                        logger.debug(f"Sent: {output.strip()}")

                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e} for line: {line}")
                    except Exception as e:
                        logger.error(f"Error processing request: {e}", exc_info=True)
                        # Try to send error response
                        try:
                            req_data = json.loads(line)
                            if "id" in req_data:
                                error_response = {
                                    "jsonrpc": "2.0",
                                    "id": req_data["id"],
                                    "error": {"code": -32603, "message": str(e)},
                                }
                                await write_stdout(json.dumps(error_response) + "\n")
                        except Exception:
                            pass

            except asyncio.TimeoutError:
                # Timeout is normal, continue loop
                continue
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        executor.shutdown(wait=True)
        logger.info("Server stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
