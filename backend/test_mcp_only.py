"""Test MCP with no fallback to see exact error"""
import sys
sys.path.insert(0, '.')

from mcp_financial_client import MCPFinancialClientSync

print("=" * 70)
print("TESTING MCP ONLY (NO FALLBACK)")
print("=" * 70)

client = MCPFinancialClientSync(
    server_command=r"C:\Users\daksh\.local\bin\uvx.exe",
    server_args=["mcp-server-fetch", "--ignore-robots-txt"]
)

print("\n1. Testing Stock Quote for AAPL...")
print("-" * 70)
try:
    quote = client.get_stock_quote("AAPL")
    if quote:
        print("✅ SUCCESS! MCP returned data:")
        print(f"   Symbol: {quote.get('symbol')}")
        print(f"   Price: ${quote.get('price')}")
        print(f"   Source: {quote.get('source')}")
    else:
        print("❌ FAILED: MCP returned None")
except Exception as e:
    print(f"❌ FAILED with error:")
    print(f"   {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n" + "=" * 70)
print("\n2. Testing Historical Data for AAPL (30 days)...")
print("-" * 70)
try:
    historical = client.get_historical_data("AAPL", days=30)
    if historical:
        print("✅ SUCCESS! MCP returned data:")
        print(f"   Data points: {len(historical.get('close', []))}")
        print(f"   Source: {historical.get('source')}")
    else:
        print("❌ FAILED: MCP returned None")
except Exception as e:
    print(f"❌ FAILED with error:")
    print(f"   {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n" + "=" * 70)
