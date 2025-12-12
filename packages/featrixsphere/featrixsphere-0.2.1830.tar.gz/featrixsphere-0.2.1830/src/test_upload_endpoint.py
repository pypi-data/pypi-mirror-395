#!/usr/bin/env python3
"""
Test script to verify the upload endpoint works on sphere-api.featrix.com
This will help diagnose the 404 error from the Vercel frontend.
"""

import requests
import io
import sys

def test_upload_endpoint():
    """Test the /upload endpoint with a sample CSV file."""
    
    # Test both endpoints that should work
    base_urls = [
        "https://sphere-api.featrix.com",
        "http://sphere-compute.featrix.com:8000"  # Direct backend
    ]
    
    # Create a simple test CSV
    test_csv_content = """name,age,city
John,25,New York
Jane,30,San Francisco
Bob,35,Chicago"""
    
    for base_url in base_urls:
        print(f"\n🧪 Testing upload endpoint: {base_url}")
        
        # Test /upload endpoint (what frontend expects)
        upload_url = f"{base_url}/upload"
        print(f"📤 POST {upload_url}")
        
        try:
            # Create file-like object
            csv_file = io.StringIO(test_csv_content)
            files = {
                'file': ('test_data.csv', csv_file.getvalue().encode(), 'text/csv')
            }
            
            response = requests.post(upload_url, files=files, timeout=30)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                print(f"   ✅ Success! Session ID: {session_id}")
                return session_id
            
            elif response.status_code == 404:
                print(f"   ❌ 404 Not Found - /upload endpoint doesn't exist")
                print(f"   Response: {response.text[:200]}")
                
                # Try the alternative endpoint
                alt_url = f"{base_url}/upload_with_new_session/"
                print(f"\n   🔄 Trying alternative: {alt_url}")
                
                csv_file = io.StringIO(test_csv_content)
                files = {
                    'file': ('test_data.csv', csv_file.getvalue().encode(), 'text/csv')
                }
                
                alt_response = requests.post(alt_url, files=files, timeout=30)
                print(f"   Status: {alt_response.status_code}")
                
                if alt_response.status_code == 200:
                    data = alt_response.json()
                    session_id = data.get('session_id')
                    print(f"   ✅ Alternative works! Session ID: {session_id}")
                    print(f"   🚨 ISSUE: Frontend expects /upload but only /upload_with_new_session/ works")
                    return session_id
                else:
                    print(f"   ❌ Alternative also failed: {alt_response.text[:200]}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    return None

def test_health_endpoints():
    """Test health endpoints to verify server status."""
    
    health_urls = [
        "https://sphere-api.featrix.com/health",
        "http://sphere-compute.featrix.com:8000/health"
    ]
    
    print("🏥 Testing health endpoints...")
    
    for url in health_urls:
        try:
            response = requests.get(url, timeout=10)
            print(f"   {url}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                service = data.get('service', 'unknown')
                version = data.get('version', 'unknown')
                print(f"      Service: {service}, Version: {version}")
        except Exception as e:
            print(f"   {url}: ❌ {e}")

def main():
    print("🚀 Sphere API Upload Endpoint Test")
    print("=" * 50)
    
    # Test health first
    test_health_endpoints()
    
    # Test upload
    session_id = test_upload_endpoint()
    
    if session_id:
        print(f"\n✅ Upload test successful!")
        print(f"   Session ID: {session_id}")
        print(f"   You can check status at: https://sphere-api.featrix.com/session/{session_id}")
    else:
        print(f"\n❌ Upload test failed!")
        print(f"   The /upload endpoint is not working properly.")
        print(f"   This explains why the Vercel frontend is getting 404 errors.")
        print(f"\n🔧 ACTION NEEDED:")
        print(f"   1. Deploy the latest code with the /upload endpoint fix")
        print(f"   2. Verify the deployment worked")
        print(f"   3. Test again")

if __name__ == "__main__":
    main() 