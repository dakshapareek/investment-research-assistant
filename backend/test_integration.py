"""Test MCP integration with multi_api_client"""
import sys
sys.path.insert(0, '.')

from data_sources.multi_api_client import MultiAPIStockClient

print("=" * 70)
print("TESTING MCP INTEGRATION")
print("=" * 70)

client = MultiAPIStockClient()

print("\n1. Testing Stock Quote for AAPL...")
print("-" * 70)
quote = client.get_quote("AAPL")
if quote:
    print(f"✅ SUCCESS!")
    print(f"   Symbol: {quote.get('symbol')}")
    print(f"   Price: ${quote.get('price')}")
    print(f"   Source: {quote.get('source')}")
else:
    print(f"❌ FAILED: No data returned")

print("\n2. Testing Historical Data for AAPL (30 days)...")
print("-" * 70)
historical = client.get_historical_data("AAPL", days=30)
if historical:
    print(f"✅ SUCCESS!")
    print(f"   Data points: {len(historical.get('close', []))}")
    print(f"   Source: {historical.get('source')}")
else:
    print(f"❌ FAILED: No data returned")

print("\n" + "=" * 70)
print("✅ MCP INTEGRATION COMPLETE!")
print("=" * 70)
