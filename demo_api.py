#!/usr/bin/env python3
"""
REST API Demo Script
Demonstrates how to interact with the MySQL Practice REST API.
"""

import json

import requests

API_BASE_URL = "http://localhost:5002"


def test_api_endpoint(endpoint: str, description: str) -> None:
    """Test an API endpoint and display results."""
    print(f"\n🔍 {description}")
    print("=" * 50)

    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {endpoint}")
            print(
                json.dumps(data, indent=2)[:500] + "..."
                if len(str(data)) > 500
                else json.dumps(data, indent=2)
            )
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed. Make sure API is running at {API_BASE_URL}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run API demo tests."""
    print("🌐 MySQL Practice REST API Demo")
    print("=" * 50)
    print(f"Testing API at: {API_BASE_URL}")

    # Test various endpoints
    test_api_endpoint("/api/stats", "Database Statistics")
    test_api_endpoint("/api/customers?limit=3", "First 3 Customers")
    test_api_endpoint("/api/products?limit=5", "First 5 Products")
    test_api_endpoint("/api/analytics/top-products?limit=3", "Top 3 Products by Sales")
    test_api_endpoint("/api/analytics/sales-by-month", "Monthly Sales Analytics")
    test_api_endpoint("/api/search/customers?q=John", "Search for 'John' in Customers")

    print(f"\n🎉 Demo complete!")
    print(f"💻 Visit {API_BASE_URL} in your browser for the interactive interface")
    print(f"📊 Try these direct links:")
    print(f"   • {API_BASE_URL}/api/stats")
    print(f"   • {API_BASE_URL}/api/customers?limit=5")
    print(f"   • {API_BASE_URL}/api/analytics/top-products")


if __name__ == "__main__":
    main()
