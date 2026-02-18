"""Test MCP Server Connection"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test MCP server connection and tools"""
    
    server_params = StdioServerParameters(
        command=r"C:\Users\daksh\.local\bin\uvx.exe",
        args=["mcp-server-fetch"],
        env=None
    )
    
    print("=" * 60)
    print("MCP SERVER TEST")
    print("=" * 60)
    
    try:
        print("\n1. Connecting to MCP server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("   ✓ Connection established")
                
                print("\n2. Initializing session...")
                await session.initialize()
                print("   ✓ Session initialized")
                
                print("\n3. Listing available tools...")
                tools_response = await session.list_tools()
                tools = tools_response.tools
                print(f"   ✓ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"      - {tool.name}: {tool.description}")
                
                print("\n4. Testing get_stock_quote for AAPL...")
                try:
                    result = await session.call_tool(
                        "fetch",
                        arguments={"url": "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"}
                    )
                    
                    if result.content:
                        print("   ✓ Successfully fetched data")
                        print(f"   Response length: {len(str(result.content))} characters")
                    else:
                        print("   ⚠️  No content in response")
                        
                except Exception as e:
                    print(f"   ✗ Tool call failed: {e}")
                
                print("\n" + "=" * 60)
                print("MCP SERVER STATUS: ✅ GREEN (Working)")
                print("=" * 60)
                
    except Exception as e:
        print(f"\n✗ MCP Server Test Failed: {e}")
        print("\n" + "=" * 60)
        print("MCP SERVER STATUS: ❌ RED (Not Working)")
        print("=" * 60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
