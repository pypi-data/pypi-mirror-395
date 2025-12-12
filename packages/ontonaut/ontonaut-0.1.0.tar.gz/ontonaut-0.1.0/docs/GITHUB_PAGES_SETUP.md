# GitHub Pages Setup Guide

This guide explains how to set up GitHub Pages for Ontonaut documentation.

## 🚀 Quick Setup

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll to **Pages** (in the sidebar)
4. Under **Source**, select:
   - Source: **GitHub Actions**
5. Click **Save**

That's it! The workflow will automatically deploy on every push to `main`.

## 📋 What Gets Deployed

The GitHub Actions workflow automatically:

1. **Exports Marimo Notebooks**
   - `01-getting-started.py` → `01-getting-started.html`
   - `02-chatbot-guide.py` → `02-chatbot-guide.html`
   - `03-openai-integration.py` → `03-openai-integration.html`

2. **Copies Documentation**
   - `docs/index.html` → Home page
   - `book/markdown/*.md` → Markdown guides

3. **Deploys to GitHub Pages**
   - Available at: `https://yourusername.github.io/ontonaut/`

## 🔧 Workflow Details

The workflow is defined in `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Manual trigger
```

### Workflow Steps

1. **Checkout** - Gets the repository code
2. **Setup Python** - Installs Python 3.11
3. **Install dependencies** - Installs marimo and ontonaut
4. **Export notebooks** - Converts `.py` to `.html`
5. **Copy files** - Copies index.html and guides
6. **Upload artifact** - Prepares for deployment
7. **Deploy** - Publishes to GitHub Pages

## 📁 File Structure

```
_site/                          # Deployed to GitHub Pages
├── index.html                  # Home page (fancy landing)
├── 01-getting-started.html     # Getting Started notebook
├── 02-chatbot-guide.html       # ChatBot Guide notebook
├── 03-openai-integration.html  # OpenAI Integration notebook
└── guides/                     # Markdown documentation
    ├── quick-start.md
    ├── code-editor.md
    ├── chatbot.md
    ├── executors.md
    ├── handlers.md
    └── custom-executors.md
```

## 🎨 Landing Page Features

The `docs/index.html` includes:

- ✨ **Fancy gradient design**
- 📓 **Clickable notebook cards** with descriptions
- 📚 **Resource links** to all documentation
- 🎨 **Feature showcase** with icons
- 📱 **Responsive design** (mobile-friendly)
- 🌈 **Modern, professional look**

## 🔄 Manual Deployment

To trigger deployment manually:

1. Go to **Actions** tab
2. Click **Deploy Documentation to GitHub Pages**
3. Click **Run workflow**
4. Select `main` branch
5. Click **Run workflow**

## 🧪 Testing Locally

Before pushing, test the export locally:

```bash
# Export notebooks
marimo export html book/marimo/01-getting-started.py -o test-output/01-getting-started.html

# View in browser
open test-output/01-getting-started.html
```

## 🐛 Troubleshooting

### Pages Not Updating

1. Check **Actions** tab for workflow status
2. Click on the workflow run to see logs
3. Ensure GitHub Pages is enabled in settings
4. Wait 1-2 minutes for CDN cache

### Export Errors

If notebooks fail to export:

```bash
# Test locally
cd book/marimo
marimo export html 01-getting-started.py

# Check for errors in notebook
marimo edit 01-getting-started.py
```

### Missing Files

If files are missing from deployment:

1. Check `_site` artifact in workflow run
2. Verify file paths in workflow
3. Ensure files exist in repository

## 🎯 Custom Domain (Optional)

To use a custom domain:

1. Add `CNAME` file to `docs/`:
   ```
   docs.ontonaut.com
   ```

2. Update workflow to copy CNAME:
   ```yaml
   - name: Copy CNAME
     run: cp docs/CNAME _site/CNAME
   ```

3. Configure DNS:
   - Add CNAME record pointing to `yourusername.github.io`

4. Enable in GitHub Settings → Pages → Custom domain

## 📊 Monitoring

### Check Deployment Status

- **Actions Tab**: See all workflow runs
- **Pages Settings**: View deployment history
- **Logs**: Click on workflow run for details

### View Site

Once deployed, visit:
```
https://yourusername.github.io/ontonaut/
```

## 🔒 Security

The workflow uses:
- **Minimal permissions** - Only `contents:read` and `pages:write`
- **GitHub's official actions** - Trusted sources
- **No secrets required** - All dependencies are public

## 🚀 Advanced Configuration

### Add More Notebooks

1. Create notebook: `book/marimo/04-new-feature.py`
2. It will automatically be exported by the workflow
3. Add card to `docs/index.html`:
   ```html
   <a href="04-new-feature.html" class="notebook-card">
       <div class="notebook-icon">🎨</div>
       <div class="notebook-title">New Feature</div>
       <div class="notebook-description">
           Description here
       </div>
   </a>
   ```

### Add Assets

To include images or CSS:

1. Create `docs/assets/` directory
2. Add files: `docs/assets/logo.png`
3. Workflow automatically copies them
4. Reference in HTML: `<img src="assets/logo.png">`

### Custom Styling

Edit `docs/index.html` to customize:
- Colors (gradient, borders)
- Layout (grid, spacing)
- Typography (fonts, sizes)
- Animations (hover effects)

## 📝 Best Practices

1. **Test Locally First** - Export and view before pushing
2. **Keep Notebooks Small** - Large notebooks = slow exports
3. **Use Descriptive Names** - Help users find content
4. **Update Index** - Keep landing page in sync
5. **Monitor Actions** - Check for build failures

## 🎉 Success!

Your documentation is now live! Share the link:
```
https://yourusername.github.io/ontonaut/
```

Users can:
- 📓 Browse interactive notebooks
- 📚 Read comprehensive guides
- 🎨 See feature showcase
- 🚀 Get started quickly

## 🔗 Related Resources

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Marimo Export Docs](https://docs.marimo.io/)
- [HTML/CSS Guide](https://developer.mozilla.org/en-US/docs/Web/HTML)
