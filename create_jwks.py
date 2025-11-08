"""
Convert RSA public key to JWK Set format for Epic FHIR
This creates a JWK Set JSON that you need to host at a URL
"""

import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

def pem_to_jwk(public_key_pem):
    """
    Convert PEM public key to JWK format
    """
    # Load the public key
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    
    # Get the public numbers
    public_numbers = public_key.public_numbers()
    
    # Convert to JWK format
    # RSA public key has 'n' (modulus) and 'e' (exponent)
    n = public_numbers.n
    e = public_numbers.e
    
    # Convert to base64url encoding (RFC 7518)
    def int_to_base64url(value):
        """Convert integer to base64url encoded string"""
        # Convert to bytes (big-endian)
        value_bytes = value.to_bytes((value.bit_length() + 7) // 8, 'big')
        # Base64 encode
        base64_value = base64.urlsafe_b64encode(value_bytes).decode('utf-8')
        # Remove padding
        return base64_value.rstrip('=')
    
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "n": int_to_base64url(n),
        "e": int_to_base64url(e),
        "kid": "epic-fhir-key-1"  # Key ID - you can change this
    }
    
    return jwk

def create_jwks_set(public_key_path="public_key.pem", output_path="jwks.json"):
    """
    Create a JWK Set from a public key file
    """
    try:
        # Read the public key
        with open(public_key_path, 'r') as f:
            public_key_pem = f.read()
        
        # Convert to JWK
        jwk = pem_to_jwk(public_key_pem)
        
        # Create JWK Set (array of keys)
        jwks = {
            "keys": [jwk]
        }
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(jwks, f, indent=2)
        
        print(f"✓ JWK Set created: {output_path}")
        print(f"\nJWK Set content:")
        print(json.dumps(jwks, indent=2))
        print(f"\nNext steps:")
        print(f"1. Host this file at a publicly accessible URL (HTTPS for production)")
        print(f"2. Enter the URL in Epic app settings:")
        print(f"   - Non-Production JWK Set URL: http://your-domain.com/jwks.json")
        print(f"   - Production JWK Set URL: https://your-domain.com/jwks.json")
        print(f"\nExample hosting options:")
        print(f"  - GitHub Pages (free)")
        print(f"  - AWS S3 + CloudFront")
        print(f"  - Your own web server")
        print(f"  - For testing: Use ngrok or similar to expose local server")
        
        return jwks
        
    except FileNotFoundError:
        print(f"✗ ERROR: Public key file not found: {public_key_path}")
        print(f"\nFirst generate your keys:")
        print(f"  openssl genrsa -out private_key.pem 2048")
        print(f"  openssl rsa -in private_key.pem -pubout -out public_key.pem")
        return None
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return None

if __name__ == "__main__":
    print("Creating JWK Set from public key...")
    print("=" * 50)
    create_jwks_set()

