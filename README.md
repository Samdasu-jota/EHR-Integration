# Epic FHIR Authentication Setup

This guide helps you set up JWT-based authentication for Epic FHIR backend systems.

## Overview

Epic requires **JWK Set URL** (not direct key upload) for backend system authentication. You need to:
1. Generate RSA key pair
2. Convert public key to JWK Set format
3. Host the JWK Set at a publicly accessible URL
4. Register the URL in Epic app settings

## Step-by-Step Setup

### 1. Generate RSA Key Pair

```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

Or use the helper script:
```bash
chmod +x generate_keys.sh
./generate_keys.sh
```

### 2. Create JWK Set

Convert your public key to JWK Set format:

```bash
python3 create_jwks.py
```

This creates `jwks.json` file containing your public key in JWK format.

### 3. Host JWK Set at a URL

Epic needs to access your JWK Set via HTTPS (for production) or HTTP (for testing).

#### Option A: GitHub Pages (Recommended - Free & Easy)

1. **Create a GitHub repository** (or use this one)
   ```bash
   mkdir docs
   cp jwks.json docs/
   ```

2. **Push to GitHub:**
   ```bash
   git add docs/jwks.json
   git commit -m "Add JWK Set"
   git push
   ```

3. **Enable GitHub Pages:**
   - Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/pages`
   - Source: **"Deploy from a branch"**
   - Branch: **"main"**, Folder: **"/docs"**
   - Save

4. **Your JWK Set URL:**
   - `https://YOUR_USERNAME.github.io/YOUR_REPO/jwks.json`

See `github_pages_setup.md` for detailed instructions.

#### Option B: For Testing (Quick Setup with ngrok)

1. Start the simple server:
   ```bash
   python3 simple_jwks_server.py
   ```

2. Expose it with ngrok:
   ```bash
   ngrok http 8000
   ```

3. Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io/jwks.json`)

#### Option C: Other Hosting

- AWS S3 + CloudFront
- Your own web server
- Any static hosting service

**Important:** Use HTTPS for production!

### 4. Register JWK Set URL in Epic

1. Go to: https://fhir.epic.com/Developer/Edit?appId=47790
2. Find **"Non-Production JWK Set URL"** or **"Production JWK Set URL"**
3. Enter your JWK Set URL (e.g., `https://your-domain.com/jwks.json`)
4. Save the settings

### 5. Test Authentication

```bash
python3 simple_auth.py
```

## File Structure

- `simple_auth.py` - Main authentication script
- `create_jwks.py` - Converts public key to JWK Set
- `simple_jwks_server.py` - Simple HTTP server for testing
- `generate_keys.sh` - Helper to generate key pair
- `private_key.pem` - Your private key (KEEP SECURE!)
- `public_key.pem` - Your public key
- `jwks.json` - JWK Set file to host

## Security Notes

- ⚠️ **Never share or commit your private key!**
- ✅ Keep `private_key.pem` secure and local
- ✅ The public key in JWK Set can be public
- ✅ Use HTTPS for production JWK Set URLs
- ✅ Add `*.pem` and `jwks.json` to `.gitignore` if using version control

## Troubleshooting

**"JWK Set URL not accessible"**
- Make sure the URL is publicly accessible (not behind firewall)
- Test the URL in a browser - should show JSON
- For production, use HTTPS

**"Invalid JWT" or "Authentication failed"**
- Verify private key matches the public key in JWK Set
- Check that JWK Set URL is correctly registered in Epic
- Ensure JWT is signed with RS256 algorithm
- Verify JWT hasn't expired

**"Key not found"**
- Make sure the `kid` (key ID) in your JWK matches what Epic expects
- Check that JWK Set format is correct (should have "keys" array)

## Next Steps

Once authentication works, you can:
- Use the access token to make FHIR API calls
- Create Patient resources
- Read/update other FHIR resources based on your app permissions

