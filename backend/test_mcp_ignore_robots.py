"""Test MCP fetch with --ignore-robots-txt"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_fetch():
    server_params = StdioServerParameters(
        command=r"C:\Users\daksh\.local\bin\uvx.exe",
        args=["mcp-server-fetch", "--ignore-robots-txt"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Fetch Yahoo Finance data
            url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
            print(f"Fetching: {url}")
            print("With --ignore-robots-txt flag\n")
            
            result = await session.call_tool(
                "fetch",
                arguments={"url": url}
            )
            
            if result.content:
                content_text = result.content[0].text
                print(f"Response length: {len(content_text)} characters")
                print(f"\nFirst 1000 chars:\n{content_text[:1000]}")
                
                # Try to parse as JSON
                try:
                    data = json.loads(content_text)
                    print("\n✓ Successfully parsed as JSON")
                    print(f"Keys: {list(data.keys())}")
                    
                    if 'chart' in data:
                        print("\n✓ Found 'chart' key")
                        if 'result' in data['chart']:
                            result_data = data['chart']['result'][0]
                            meta = result_data.get('meta', {})
                            print(f"\nStock Data:")
                            print(f"  Symbol: {meta.get('symbol')}")
                            print(f"  Price: ${meta.get('regularMarketPrice')}")
                            print(f"  Previous Close: ${meta.get('previousClose')}")
                            print(f"  Volume: {meta.get('regularMarketVolume'):,}")
                except json.JSONDecodeError as e:
                    print(f"\n✗ Failed to parse as JSON: {e}")

asyncio.run(test_fetch())
