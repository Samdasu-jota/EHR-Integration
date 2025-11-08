"""
Simple Epic FHIR Authentication using JWT
For backend systems - uses JWT instead of client secret
Follows Epic's OAuth 2.0 Tutorial: https://fhir.epic.com/Documentation?docId=oauth2tutorial
"""

import requests
import jwt
import time
from datetime import datetime, timedelta

# ============================================
# STEP 1: Configure your credentials
# ============================================
CLIENT_ID = "8d984921-09fb-4818-b0f2-7959b44064d4"  # Your non-production client ID

# Epic FHIR OAuth 2.0 Token Endpoint
# For Epic's sandbox/testing environment
AUTH_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

# ============================================
# STEP 2: Set up your private key and JWK Set URL
# ============================================
# Epic requires a JWK Set URL (not direct key upload)
# 1. Generate keys: openssl genrsa -out private_key.pem 2048
# 2. Extract public key: openssl rsa -in private_key.pem -pubout -out public_key.pem
# 3. Create JWK Set: python3 create_jwks.py
# 4. Host jwks.json at a publicly accessible URL
# 5. Register the JWK Set URL in Epic app settings (Non-Production/Production JWK Set URL)

# Path to your private key file
PRIVATE_KEY_PATH = "private_key.pem"  # ⚠️ Update this path to your private key file

# Or paste your private key directly here (keep it secure!)
PRIVATE_KEY = None  # Set this if you want to paste the key directly

print("Epic FHIR OAuth 2.0 Authentication (JWT)")
print("=" * 50)
print(f"Client ID: {CLIENT_ID}")
print(f"Auth URL: {AUTH_URL}")
print("-" * 50)

# Load private key
try:
    if PRIVATE_KEY:
        private_key = PRIVATE_KEY
    else:
        with open(PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()
    print(f"✓ Private key loaded")
except FileNotFoundError:
    print(f"\n⚠️  ERROR: Private key file not found: {PRIVATE_KEY_PATH}")
    print("\nTo set up JWT authentication:")
    print("1. Generate a private key:")
    print("   openssl genrsa -out private_key.pem 2048")
    print("2. Extract public key:")
    print("   openssl rsa -in private_key.pem -pubout -out public_key.pem")
    print("3. Create JWK Set:")
    print("   python3 create_jwks.py")
    print("4. Host jwks.json at a publicly accessible URL")
    print("   (For testing: python3 simple_jwks_server.py + ngrok)")
    print("5. Register the JWK Set URL in Epic app settings")
    print("   (Non-Production JWK Set URL or Production JWK Set URL)")
    print("6. Update PRIVATE_KEY_PATH in this file if needed")
    exit(1)
except Exception as e:
    print(f"\n⚠️  ERROR loading private key: {e}")
    exit(1)

# Create JWT for authentication
# JWT should contain: iss (client_id), sub (client_id), aud (token endpoint), exp, jti
print("\nCreating JWT...")

now = datetime.utcnow()
jwt_payload = {
    'iss': CLIENT_ID,  # Issuer = your client ID
    'sub': CLIENT_ID,  # Subject = your client ID
    'aud': AUTH_URL,   # Audience = token endpoint URL
    'exp': int((now + timedelta(minutes=5)).timestamp()),  # Expires in 5 minutes
    'jti': f"{int(time.time())}-{CLIENT_ID[:8]}",  # Unique token ID
    'iat': int(now.timestamp())  # Issued at
}

# Sign the JWT with your private key
try:
    client_assertion = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='RS256'
    )
    print("✓ JWT created and signed")
except Exception as e:
    print(f"✗ ERROR creating JWT: {e}")
    exit(1)

# Prepare OAuth 2.0 request with JWT assertion
# Epic uses JWT bearer assertion for backend systems
print("\nSending authentication request with JWT...")

data = {
    'grant_type': 'client_credentials',
    'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
    'client_assertion': client_assertion,
    'client_id': CLIENT_ID
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Send POST request to Epic's token endpoint
response = requests.post(AUTH_URL, data=data, headers=headers)

# Check authentication result
if response.status_code == 200:
    result = response.json()
    access_token = result.get('access_token')
    
    if access_token:
        print("✓ SUCCESS! Authentication successful")
        print("\n" + "=" * 50)
        print("ACCESS TOKEN RECEIVED")
        print("=" * 50)
        print(f"Token (first 50 chars): {access_token[:50]}...")
        print(f"Token expires in: {result.get('expires_in', 'N/A')} seconds")
        print(f"Token type: {result.get('token_type', 'N/A')}")
        print("\n✓ You can now use this token to make FHIR API calls!")
        print("  Include it in the Authorization header:")
        print(f"  Authorization: Bearer {access_token[:20]}...")
    else:
        print("✗ ERROR: No access token in response")
        print(f"Response: {result}")
        
else:
    print("✗ AUTHENTICATION FAILED")
    print(f"\nStatus Code: {response.status_code}")
    print("\nError Details:")
    try:
        error_data = response.json()
        print(f"  Error: {error_data.get('error', 'Unknown error')}")
        print(f"  Description: {error_data.get('error_description', 'No description')}")
    except:
        print(f"  {response.text}")
    
    print("\nTroubleshooting:")
    print("  • Verify your Client ID is correct")
    print("  • Verify your private key is correct and matches the public key registered in Epic")
    print("  • Check that your JWK Set URL is registered in Epic app settings")
    print("  • Ensure you're using the correct auth URL for your Epic instance")
    print("  • Verify the JWT is properly formatted and signed with RS256 algorithm")

