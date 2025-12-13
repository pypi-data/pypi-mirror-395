#!/usr/bin/env python3
"""Test script to properly test MCP protocol sequence"""

import subprocess
import json
import sys
import time

def test_mcp_server():
    cmd = [
        "/Users/wontseemecomin/Dev/AI Agents/memory-hub/.venv/bin/memory-hub-mcp",
        "--qdrant-url", "http://192.168.0.90:6333",
        "--lm-studio-url", "http://192.168.0.90:1234/v1",
        "--log-level", "INFO"
    ]
    
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Step 1: Initialize
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        logger.info("Sending initialize...")
        proc.stdin.write(json.dumps(init_msg) + "\n")
        proc.stdin.flush()
        
        # Read response
        response = proc.stdout.readline()
        logger.info(f"Initialize response: {response.strip()}")
        
        # Step 2: Send initialized notification
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        logger.info("Sending initialized notification...")
        proc.stdin.write(json.dumps(initialized_msg) + "\n")
        proc.stdin.flush()
        
        # Wait a bit for initialization to complete
        time.sleep(1)
        
        # Step 3: List tools
        list_tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        logger.info("Sending tools/list...")
        proc.stdin.write(json.dumps(list_tools_msg) + "\n")
        proc.stdin.flush()
        
        # Read response
        response = proc.stdout.readline()
        logger.info(f"Tools list response: {response.strip()}")
        
    except Exception as e:
        logger.info(f"Error: {e}")
    finally:
        proc.terminate()
        stderr = proc.stderr.read()
        if stderr:
            logger.info(f"Stderr: {stderr}")

if __name__ == "__main__":
    test_mcp_server()