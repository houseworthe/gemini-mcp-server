#!/usr/bin/env python3
"""
Test script for the fixed Gemini MCP server
"""

import json
import subprocess
import time
import os
from threading import Thread
import queue
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_request(proc, request):
    """Send a JSON-RPC request to the server"""
    request_str = json.dumps(request) + '\n'
    proc.stdin.write(request_str.encode())
    proc.stdin.flush()
    print(f"Sent: {request_str.strip()}")

def read_response(proc, response_queue):
    """Read responses from the server"""
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        response_queue.put(line.decode().strip())

def test_server():
    """Test the MCP server"""
    print("Starting Fixed Gemini MCP Server test...")
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\nWARNING: GEMINI_API_KEY not set!")
        print("The server will start but API calls will fail.")
        print("To set it: export GEMINI_API_KEY='your-key-here'")
        print()
    
    # Start the server
    proc = subprocess.Popen(
        ['python3', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )
    
    # Set up response reading thread
    response_queue = queue.Queue()
    reader_thread = Thread(target=read_response, args=(proc, response_queue))
    reader_thread.daemon = True
    reader_thread.start()
    
    time.sleep(1)  # Give server time to start
    
    try:
        # Test 1: Initialize
        print("\n1. Testing initialize...")
        send_request(proc, {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {}
        })
        
        # Wait for response
        time.sleep(0.5)
        while not response_queue.empty():
            response = response_queue.get()
            print(f"Response: {response}")
            data = json.loads(response)
            if data.get("result", {}).get("serverInfo", {}).get("name") == "gemini-collab":
                print("✓ Initialize successful")
        
        # Test 2: List tools
        print("\n2. Testing tools/list...")
        send_request(proc, {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list",
            "params": {}
        })
        
        time.sleep(0.5)
        while not response_queue.empty():
            response = response_queue.get()
            print(f"Response: {response}")
            data = json.loads(response)
            tools = data.get("result", {}).get("tools", [])
            if len(tools) > 0:
                print(f"✓ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
        
        # Test 3: Call a tool (if API key is set)
        if os.getenv("GEMINI_API_KEY"):
            print("\n3. Testing tool call (ask_gemini)...")
            send_request(proc, {
                "jsonrpc": "2.0",
                "id": "3",
                "method": "tools/call",
                "params": {
                    "name": "ask_gemini",
                    "arguments": {
                        "question": "What is 2+2?"
                    }
                }
            })
            
            print("Waiting for Gemini response (this may take a few seconds)...")
            time.sleep(5)  # Give more time for API response
            
            while not response_queue.empty():
                response = response_queue.get()
                print(f"Response: {response}")
                data = json.loads(response)
                if "result" in data:
                    print("✓ Tool call successful")
                elif "error" in data:
                    print(f"✗ Tool call failed: {data['error']}")
        else:
            print("\n3. Skipping tool call test (no API key)")
        
        print("\n✓ All tests completed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
    finally:
        # Clean up
        proc.terminate()
        proc.wait()
        
        # Check for any stderr output
        stderr = proc.stderr.read().decode()
        if stderr:
            print(f"\nServer stderr output:\n{stderr}")

if __name__ == "__main__":
    test_server()