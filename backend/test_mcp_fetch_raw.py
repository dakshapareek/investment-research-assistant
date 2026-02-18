"""Test raw MCP fetch response"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_fetch():
    server_params = StdioServerParameters(
        command=r"C:\Users\daksh\.local\bin\uvx.exe",
        args=["mcp-server-fetch"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Fetch Yahoo Finance data
            url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
            print(f"Fetching: {url}")
            
            result = await session.call_tool(
                "fetch",
                arguments={"url": url}
            )
            
            if result.content:
                print("\nResponse type:", type(result.content))
                print("Number of content items:", len(result.content))
                
                for i, content_item in enumerate(result.content):
                    print(f"\nContent item {i}:")
                    print(f"  Type: {content_item.type}")
                    print(f"  Text length: {len(content_item.text)}")
                    print(f"  First 500 chars:\n{content_item.text[:500]}")

asyncio.run(test_fetch())
