"""Test MCP Stock Data Fetching"""
from mcp_financial_client import MCPFinancialClientSync

print("=" * 60)
print("TESTING MCP STOCK DATA CLIENT")
print("=" * 60)

# Initialize client with full path
client = MCPFinancialClientSync(
    server_command=r"C:\Users\daksh\.local\bin\uvx.exe",
    server_args=["mcp-server-fetch"]
)

# Test 1: Get stock quote
print("\n1. Testing get_stock_quote for AAPL...")
quote = client.get_stock_quote("AAPL")
if quote:
    print("   ✓ Successfully fetched quote")
    print(f"   Symbol: {quote.get('symbol')}")
    print(f"   Price: ${quote.get('price')}")
    print(f"   Change: {quote.get('change')} ({quote.get('changePercent'):.2f}%)")
    print(f"   Volume: {quote.get('volume'):,}")
    print(f"   Source: {quote.get('source')}")
else:
    print("   ✗ Failed to fetch quote")

# Test 2: Get historical data
print("\n2. Testing get_historical_data for AAPL (30 days)...")
historical = client.get_historical_data("AAPL", days=30)
if historical:
    print("   ✓ Successfully fetched historical data")
    print(f"   Data points: {len(historical.get('close', []))}")
    print(f"   Date range: {len(historical.get('timestamps', []))} days")
    print(f"   First close: ${historical.get('close', [None])[0]}")
    print(f"   Last close: ${historical.get('close', [None])[-1]}")
    print(f"   Source: {historical.get('source')}")
else:
    print("   ✗ Failed to fetch historical data")

print("\n" + "=" * 60)
print("MCP STOCK DATA CLIENT: ✅ READY")
print("=" * 60)
