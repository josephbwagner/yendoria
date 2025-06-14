# GitHub Pages Setup Guide

This guide will help you enable GitHub Pages for your Yendoria documentation.

## Enabling GitHub Pages

1. **Go to your GitHub repository settings**:
   - Navigate to your repository on GitHub
   - Click on the **Settings** tab
   - Scroll down to the **Pages** section in the left sidebar

2. **Configure Pages source**:
   - Under "Source", select **GitHub Actions**
   - This allows the custom workflow to deploy your documentation

3. **Verify setup**:
   - The documentation workflow will automatically run on the next push to `main`
   - Check the **Actions** tab to see the workflow progress
   - Once complete, your documentation will be available at: `https://your-username.github.io/repository-name/`

## Workflow Features

The `.github/workflows/docs.yml` workflow provides:

- **Automatic builds**: Triggered on pushes to `main` and pull requests
- **Modern tooling**: Uses Poetry for dependency management
- **Caching**: Speeds up builds by caching Python dependencies
- **Security**: Uses proper permissions and GitHub's secure deployment
- **Manual triggers**: Can be run manually from the Actions tab

## Theme and Styling

The documentation uses the **Furo** theme, which provides:
- Clean, modern appearance
- Mobile-responsive design
- Dark/light mode toggle
- GitHub integration
- Search functionality

## Customization

To customize the documentation:

1. **Theme options**: Edit `docs/conf.py` to modify colors, layout, and features
2. **Content**: Add new `.rst` files and update the table of contents
3. **Static assets**: Add CSS, JavaScript, or images to `docs/_static/`
4. **Navigation**: Update `docs/index.rst` to change the main navigation

## File Structure for Version Control

When working with Sphinx documentation, here's what should be tracked in git:

### ✅ **Track these directories/files:**
- `docs/_static/` - Custom CSS, JS, images, and other static assets
- `docs/_templates/` - Custom Sphinx templates (if you create any)
- `docs/*.rst` - All documentation source files
- `docs/conf.py` - Sphinx configuration
- `.github/workflows/docs.yml` - GitHub Actions workflow

### ❌ **Don't track these (keep in .gitignore):**
- `docs/_build/` - Generated HTML/PDF output (rebuilt by CI/CD)
- `docs/.doctrees/` - Sphinx cache files
- `docs/.buildinfo` - Build metadata

### 📝 **Why this matters:**
- **Static assets** are source files you intentionally create/customize
- **Build output** is generated and would create unnecessary repository bloat
- **CI/CD** rebuilds documentation from source, so build artifacts aren't needed

## Troubleshooting

**Build fails?**
- Check the Actions tab for error messages
- Ensure all dependencies are properly defined in `pyproject.toml`
- Verify that `docs/conf.py` is properly configured

**Pages not updating?**
- Ensure GitHub Pages source is set to "GitHub Actions"
- Check that the workflow completed successfully
- It may take a few minutes for changes to appear

**Theme not working?**
- Ensure `furo` is in your dev dependencies
- Check that `html_theme = "furo"` is set in `docs/conf.py`
