"""Test the API to verify MCP is working"""
import requests
import json

print("=" * 70)
print("TESTING API WITH MCP")
print("=" * 70)

# Test stock quote
print("\n1. Testing /api/analyze/AAPL...")
print("-" * 70)
try:
    response = requests.get('http://127.0.0.1:5000/api/analyze/AAPL', timeout=60)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Price: ${data.get('price')}")
        print(f"   Source: {data.get('source')}")
        if 'historical_data' in data:
            print(f"   Historical data points: {len(data['historical_data'].get('close', []))}")
            print(f"   Historical source: {data['historical_data'].get('source')}")
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 70)
