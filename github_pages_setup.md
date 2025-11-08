# Hosting JWK Set on GitHub Pages

GitHub Pages is a free and easy way to host your JWK Set for Epic FHIR authentication.

## Quick Setup

### Option 1: Simple Repository (Recommended)

1. **Create a new GitHub repository** (can be private or public)
   - Name it something like `epic-fhir-jwks` or `my-jwks`

2. **Upload your jwks.json file**
   ```bash
   # In your project directory
   git init
   git add jwks.json
   git commit -m "Add JWK Set for Epic FHIR"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source", select **"Deploy from a branch"**
   - Choose **"main"** branch and **"/ (root)"** folder
   - Click **Save**

4. **Get your JWK Set URL**
   - Your JWK Set will be available at:
   - `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/jwks.json`
   - Example: `https://taehuynglee.github.io/epic-fhir-jwks/jwks.json`

5. **Register in Epic**
   - Go to Epic app settings
   - Enter: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/jwks.json`
   - Save

### Option 2: Use This Repository

If you want to keep everything in this EHR2 repository:

1. **Create a `docs` folder** (GitHub Pages can serve from `/docs` folder)
   ```bash
   mkdir docs
   cp jwks.json docs/
   ```

2. **Enable GitHub Pages from `/docs` folder**
   - Go to repository Settings → Pages
   - Source: **"Deploy from a branch"**
   - Branch: **"main"**, Folder: **"/docs"**
   - Save

3. **Your JWK Set URL will be:**
   - `https://YOUR_USERNAME.github.io/EHR2/jwks.json`

## Important Notes

- ✅ GitHub Pages provides HTTPS (required for production)
- ✅ Free and reliable
- ✅ Easy to update (just push new jwks.json)
- ⚠️ Make sure `jwks.json` is committed (not in .gitignore for this file)
- ⚠️ If using private repo, GitHub Pages still works but URL is public

## Updating Your JWK Set

If you need to update your keys:

1. Generate new keys
2. Run `python3 create_jwks.py` to create new `jwks.json`
3. Copy to your GitHub repo
4. Commit and push:
   ```bash
   git add jwks.json
   git commit -m "Update JWK Set"
   git push
   ```
5. GitHub Pages updates automatically (may take a few minutes)

## Testing

After setting up, test that your JWK Set is accessible:

```bash
curl https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/jwks.json
```

You should see the JSON response with your public key.

