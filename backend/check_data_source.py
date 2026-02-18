"""Quick script to check where data is coming from"""
import requests
import json

print("=" * 70)
print("DATA SOURCE CHECKER")
print("=" * 70)

# Check configuration
print("\n1. Checking Configuration...")
try:
    from config import USE_MCP_FOR_FINANCIAL_DATA
    print(f"   MCP Enabled in Config: {USE_MCP_FOR_FINANCIAL_DATA}")
except Exception as e:
    print(f"   Error reading config: {e}")

# Make API request
print("\n2. Fetching Stock Data for AAPL...")
try:
    response = requests.get("http://127.0.0.1:5000/api/analyze/AAPL", timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n3. Data Sources Used:")
        print("   " + "-" * 66)
        
        # Stock Quote Source
        if 'quote' in data and 'source' in data['quote']:
            source = data['quote']['source']
            price = data['quote'].get('price', 'N/A')
            print(f"   📊 Stock Quote:      {source}")
            print(f"      Price: ${price}")
            if 'MCP' in source:
                print("      ✅ Using MCP Server!")
            else:
                print("      ℹ️  Using Direct API")
        
        # Historical Data Source
        if 'chart_data' in data and 'source' in data['chart_data']:
            source = data['chart_data']['source']
            points = len(data['chart_data'].get('close', []))
            print(f"\n   📈 Historical Data:  {source}")
            print(f"      Data Points: {points}")
            if 'MCP' in source:
                print("      ✅ Using MCP Server!")
            else:
                print("      ℹ️  Using Direct API")
        
        # News Source
        if 'news_summary' in data and 'source' in data['news_summary']:
            source = data['news_summary']['source']
            headlines = len(data['news_summary'].get('headlines', []))
            print(f"\n   📰 News:             {source}")
            print(f"      Headlines: {headlines}")
        
        # Social Media Source
        if 'social_pulse' in data and 'source' in data['social_pulse']:
            source = data['social_pulse']['source']
            mentions = data['social_pulse'].get('mentions', 'unknown')
            print(f"\n   💬 Social Media:     {source}")
            print(f"      Mentions: {mentions}")
        
        print("   " + "-" * 66)
        
        # Summary
        print("\n4. Summary:")
        has_mcp = any('MCP' in str(data.get(key, {}).get('source', '')) 
                      for key in ['quote', 'chart_data'])
        
        if has_mcp:
            print("   ✅ Data is coming from MCP Server")
        else:
            print("   ℹ️  Data is coming from Direct APIs (Yahoo Finance, Alpha Vantage, etc.)")
        
    else:
        print(f"   ✗ API request failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("   ✗ Server is not running!")
    print("   Start the server with: cd backend && python app.py")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
