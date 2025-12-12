#!/usr/bin/env python3
"""Test if MCP server can list tools correctly"""
import subprocess
import json
import sys

print("Testing MCP server tool discovery...")
print("=" * 60)

# Test 1: Can we start the server?
print("\n1. Testing if server starts...")
result = subprocess.run(
    ["uvx", "--from", "/home/lysander-z-f-q/PycharmProjects/sj_ai_patent", "patent-mcp-server"],
    input=json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }).encode(),
    capture_output=True,
    timeout=10
)

print(f"Return code: {result.returncode}")
print(f"stdout: {result.stdout.decode()}")
print(f"stderr: {result.stderr.decode()}")

print("=" * 60)
