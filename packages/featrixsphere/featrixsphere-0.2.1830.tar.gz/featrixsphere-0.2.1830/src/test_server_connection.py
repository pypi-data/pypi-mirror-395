#!/usr/bin/env python3
"""
Server Connection Test

Simple script to test connectivity to the Featrix Sphere API server
and verify which endpoints are available.
"""

import requests
from test_api_client import FeatrixSphereClient


def test_server_connectivity():
    """Test basic server connectivity and API endpoints."""
    
    base_url = "https://sphere-api.featrix.com"
    print(f"Testing connectivity to: {base_url}")
    print("=" * 50)
    
    # Test basic connectivity
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✓ Server is reachable")
        print(f"  Status: {response.status_code}")
        print(f"  Server: {response.headers.get('server', 'Unknown')}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('location')
            print(f"  Redirects to: {redirect_url}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Server connection failed: {e}")
        return False
    
    # Test common API endpoints
    endpoints_to_test = [
        "/health",
        "/api/health", 
        "/compute/session",
        "/session",
        "/api/session",
        "/docs",
        "/api/docs",
        "/openapi.json"
    ]
    
    print("\nTesting API endpoints:")
    print("-" * 30)
    
    available_endpoints = []
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{base_url}{endpoint}"
            if endpoint == "/compute/session":
                # Test POST for session creation
                response = requests.post(url, json={}, timeout=5)
            else:
                # Test GET for other endpoints
                response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✓ {endpoint} - Available (200)")
                available_endpoints.append(endpoint)
            elif response.status_code == 405:  # Method not allowed (might be POST only)
                print(f"? {endpoint} - Method not allowed (405) - might be POST only")
                available_endpoints.append(endpoint)
            elif response.status_code == 500:  # Server error (might be working but erroring)
                print(f"? {endpoint} - Server error (500) - endpoint exists but erroring")
                available_endpoints.append(endpoint)
            else:
                print(f"✗ {endpoint} - {response.status_code}")
                
        except requests.exceptions.RequestException:
            print(f"✗ {endpoint} - Connection failed")
    
    print(f"\nAvailable endpoints: {len(available_endpoints)}")
    
    # Test the API client
    print("\nTesting API client:")
    print("-" * 20)
    
    try:
        client = FeatrixSphereClient()
        print(f"✓ Client created successfully")
        print(f"  Base URL: {client.base_url}")
        
        # Try to create a session
        try:
            session = client.create_session("sphere")
            print(f"✓ Session creation successful: {session.session_id}")
            return True
        except requests.exceptions.HTTPError as e:
            print(f"✗ Session creation failed: {e.response.status_code}")
            if e.response.status_code == 404:
                print("  → API endpoints may not be deployed yet")
            elif e.response.status_code == 500:
                print("  → Server error - API may be partially deployed")
            return False
        except Exception as e:
            print(f"✗ Session creation failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Client creation failed: {e}")
        return False


def main():
    """Main test function."""
    
    print("Featrix Sphere API Server Connection Test")
    print("=" * 50)
    
    success = test_server_connectivity()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ API server is fully operational!")
        print("You can now use the API client for testing.")
    else:
        print("✗ API server needs deployment or configuration.")
        print("\nNext steps:")
        print("1. Deploy the API application to sphere-api.featrix.com")
        print("2. Ensure API endpoints are properly routed")
        print("3. Run this test again to verify functionality")
    
    return success


if __name__ == "__main__":
    exit(0 if main() else 1) 