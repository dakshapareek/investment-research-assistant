#!/usr/bin/env python3
"""Test subscription system"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_subscription_flow():
    print("="*60)
    print("TESTING SUBSCRIPTION SYSTEM")
    print("="*60)
    
    # Test data
    test_email = "test@example.com"
    test_tickers = ["AAPL", "MSFT", "NVDA"]
    test_threshold = 2.0
    
    # 1. Subscribe
    print("\n1. Testing Subscribe...")
    response = requests.post(f"{BASE_URL}/subscribe", json={
        "email": test_email,
        "tickers": test_tickers,
        "threshold": test_threshold
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✓ Subscription created successfully")
            print(f"   Email: {data['subscription']['email']}")
            print(f"   Tickers: {', '.join(data['subscription']['tickers'])}")
            print(f"   Threshold: {data['subscription']['threshold']}%")
            subscription_id = data['subscription']['id']
        else:
            print(f"   ✗ Subscribe failed: {data.get('error')}")
            return
    else:
        print(f"   ✗ HTTP Error: {response.status_code}")
        return
    
    # 2. Get Subscription
    print("\n2. Testing Get Subscription...")
    response = requests.get(f"{BASE_URL}/subscription/{test_email}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✓ Subscription retrieved successfully")
            print(f"   Active: {data['subscription']['active']}")
        else:
            print(f"   ✗ Subscription not found")
    else:
        print(f"   ✗ HTTP Error: {response.status_code}")
    
    # 3. Test Alerts (Manual Trigger)
    print("\n3. Testing Manual Alert Trigger...")
    print("   (This will check stocks and send emails if thresholds are met)")
    response = requests.post(f"{BASE_URL}/test-alerts")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Alerts triggered successfully")
        print(f"   Sent: {data.get('sent', 0)}")
        print(f"   Failed: {data.get('failed', 0)}")
    else:
        print(f"   ✗ HTTP Error: {response.status_code}")
    
    # 4. Unsubscribe
    print("\n4. Testing Unsubscribe...")
    response = requests.post(f"{BASE_URL}/unsubscribe", json={
        "id": subscription_id
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✓ Unsubscribed successfully")
            print(f"   Email: {data.get('email')}")
        else:
            print(f"   ✗ Unsubscribe failed: {data.get('error')}")
    else:
        print(f"   ✗ HTTP Error: {response.status_code}")
    
    # 5. Verify Unsubscribe
    print("\n5. Verifying Unsubscribe...")
    response = requests.get(f"{BASE_URL}/subscription/{test_email}")
    
    if response.status_code == 200:
        data = response.json()
        if not data.get('success'):
            print(f"   ✓ Subscription no longer active")
        else:
            print(f"   ⚠️  Subscription still active (unexpected)")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    try:
        test_subscription_flow()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to server")
        print("   Make sure the backend is running: python backend/app.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
