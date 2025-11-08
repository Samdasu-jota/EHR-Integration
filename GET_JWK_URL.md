# How to Get Your JWK Set URL

Follow these steps to create and host your JWK Set, then get the URL for Epic.

## Step 1: Generate RSA Keys

```bash
# Generate private key
openssl genrsa -out private_key.pem 2048

# Extract public key
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

## Step 2: Create JWK Set File

```bash
python3 create_jwks.py
```

This creates `jwks.json` file in your current directory.

## Step 3: Host on GitHub Pages (Easiest Method)

### Option A: New Repository (Recommended)

1. **Create a new GitHub repository:**
   - Go to https://github.com/new
   - Name it (e.g., `epic-fhir-jwks`)
   - Create repository

2. **Upload jwks.json:**
   ```bash
   # Create docs folder
   mkdir docs
   cp jwks.json docs/
   
   # Initialize git and push
   git init
   git add docs/jwks.json
   git commit -m "Add JWK Set"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/epic-fhir-jwks.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to: `https://github.com/YOUR_USERNAME/epic-fhir-jwks/settings/pages`
   - Under "Source": Select **"Deploy from a branch"**
   - Branch: **"main"**
   - Folder: **"/docs"**
   - Click **Save**

4. **Your JWK Set URL is:**
   ```
   https://YOUR_USERNAME.github.io/epic-fhir-jwks/jwks.json
   ```
   Replace `YOUR_USERNAME` with your GitHub username.

### Option B: Use This Repository

If you want to keep everything in this EHR2 repo:

```bash
# Create docs folder
mkdir docs
cp jwks.json docs/

# Commit and push
git add docs/jwks.json
git commit -m "Add JWK Set for Epic FHIR"
git push
```

Then enable GitHub Pages from `/docs` folder in repository settings.

Your URL will be: `https://YOUR_USERNAME.github.io/EHR2/jwks.json`

## Step 4: Verify Your JWK Set URL

Test that your URL works:

```bash
curl https://YOUR_USERNAME.github.io/YOUR_REPO/jwks.json
```

You should see JSON output with your public key.

## Step 5: Register URL in Epic

1. Go to: https://fhir.epic.com/Developer/Edit?appId=47790
2. Find **"Non-Production JWK Set URL"** field
3. Paste your URL: `https://YOUR_USERNAME.github.io/YOUR_REPO/jwks.json`
4. Click **Save**

## That's It!

Now you can test authentication:
```bash
python3 simple_auth.py
```

---

## Quick Reference

**Your JWK Set URL format:**
- GitHub Pages: `https://USERNAME.github.io/REPO_NAME/jwks.json`
- Example: `https://taehuynglee.github.io/epic-fhir-jwks/jwks.json`

**Important:**
- ✅ Use HTTPS (GitHub Pages provides this automatically)
- ✅ URL must be publicly accessible
- ✅ File must be valid JSON
- ⚠️ Keep `private_key.pem` secret - never commit it!

