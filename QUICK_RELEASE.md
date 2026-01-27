# Quick Release Guide

The fastest way to build and release YouTube Downloader.

## One-Command Release

```bash
# 1. Make sure everything is committed
git add .
git commit -m "Your changes"

# 2. Tag and push (this triggers the build)
git tag v1.0.0
git push origin main --tags

# 3. That's it! GitHub Actions will:
#    - Build for macOS, Windows, Linux
#    - Create a GitHub Release
#    - Upload all executables
#    - Your landing page auto-detects and downloads
```

## Check Build Status

```bash
# Open in browser
open https://github.com/yourusername/vidgrab/actions
```

Watch the build run in real-time, takes ~5-10 minutes.

## Get Your Downloads

After build completes:
1. Go to Releases page
2. Click your new version
3. Download executables
4. Or direct users to your landing page

## Update Landing Page

Just change these in `index.html`:

```html
<!-- Replace yourusername with your actual username -->
https://github.com/yourusername/vidgrab/releases/download/latest/VidGrab.exe
```

## Enable GitHub Pages (One-time Setup)

1. Go to repo Settings → Pages
2. Select "Deploy from a branch"
3. Choose `main` branch, root folder
4. Save
5. Your site: `https://yourusername.github.io/vidgrab`

Done! Now you have:
✅ Automatic builds for all platforms
✅ Beautiful landing page with auto-detection
✅ One-click downloads for users

## Common Tag Names

```bash
git tag v1.0.0        # Initial release
git tag v1.0.1        # Bug fix
git tag v1.1.0        # New features
git tag v2.0.0        # Major version
```

## Pre-Release Builds

To test without triggering a release:

```bash
# Just commit without tagging
git add .
git commit -m "Testing changes"
git push origin main
# CI/CD won't run (only runs on tags)
```

## Full Workflow Example

```bash
# 1. Make changes
echo "version = '1.0.1'" > youtube_downloader/version.py
git add .
git commit -m "Bump to v1.0.1: Bug fixes and improvements"

# 2. Create and push tag
git tag v1.0.1
git push origin main --tags

# 3. Monitor build (opens your browser)
open https://github.com/yourusername/vidgrab/actions

# 4. Wait for completion (~5-10 min)

# 5. Go to Releases and add notes (optional)
open https://github.com/yourusername/vidgrab/releases

# 6. Share with users
echo "Download from: yourusername.github.io/vidgrab"
```

## Troubleshooting

### Build failed?
- Check Actions tab for error message
- Usually: missing dependencies or PyQt6 issue
- Fix locally, commit, tag again

### Release not created?
- Make sure you pushed the tag: `git push --tags`
- Check Actions shows successful build

### Landing page not showing?
- Enable GitHub Pages (Settings → Pages)
- Wait 1-2 minutes for deployment
- Check Actions → "pages build and deployment"

## Next Time

Just remember:
```bash
git tag vX.Y.Z
git push --tags
```

Everything else is automatic!
