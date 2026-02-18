"""Test JSON parsing from MCP response"""
import sys
sys.path.insert(0, '.')

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_parse():
    async with stdio_client(
        StdioServerParameters(
            command=r"C:\Users\daksh\.local\bin\uvx.exe",
            args=["mcp-server-fetch", "--ignore-robots-txt"],
            env=None
        )
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL"
            result = await session.call_tool(
                "fetch",
                arguments={"url": url}
            )
            
            if result.content:
                content = result.content[0].text
                print("=" * 70)
                print("RAW MCP RESPONSE:")
                print("=" * 70)
                print(content[:2000])  # First 2000 chars
                print("=" * 70)
                print(f"\nTotal length: {len(content)} characters")
                
                # Save to file for inspection
                with open('mcp_response.txt', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("\n✓ Full response saved to mcp_response.txt")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(test_parse())
loop.close()
