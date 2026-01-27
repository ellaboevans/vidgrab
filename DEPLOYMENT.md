# Deployment Guide

This guide explains how to set up CI/CD builds and deploy the landing page.

## GitHub Actions CI/CD Setup

### What It Does

The CI/CD pipeline (`.github/workflows/build.yml`) automatically:
1. **Triggers on tag push** (e.g., `git tag v1.0.0 && git push --tags`)
2. **Builds executables** for macOS, Windows, and Linux
3. **Creates a DMG** for macOS distribution
4. **Uploads artifacts** to GitHub Actions
5. **Creates a release** on GitHub with all executables

### Requirements

- GitHub repository (public or private)
- No special setup needed - GitHub Actions is free

### How to Use

1. **Push a new tag to trigger a build:**
```bash
# Make your changes and commit
git add .
git commit -m "Version 1.0.0"

# Tag the release
git tag v1.0.0

# Push tag to GitHub
git push --tags
```

2. **View the build progress:**
   - Go to your GitHub repo
   - Click "Actions" tab
   - Watch the build run in real-time

3. **Download built executables:**
   - After build completes, click the workflow
   - Scroll to "Artifacts" section
   - Download macOS, Windows, or Linux builds

4. **Create a GitHub Release:**
   - Go to "Releases" on GitHub
   - Should see the auto-created release with all executables
   - Edit to add release notes

### Build Artifacts

After a successful build, you'll have:
- `VidGrab.dmg` - macOS installer
- `VidGrab.exe` - Windows executable
- `VidGrab` - Linux executable
- `VidGrab.app` - macOS app bundle

## GitHub Pages Landing Page

### Setup (One-time)

1. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Select "Deploy from a branch"
   - Branch: `main` (or your default branch)
   - Folder: `/ (root)`
   - Click Save

2. **Wait for deployment:**
   - GitHub builds and deploys automatically
   - Takes ~1 minute
   - Will show deployment status in Actions tab

3. **Your site is live at:**
   ```
   https://yourusername.github.io/vidgrab
   ```

### Customizing the Landing Page

Edit `index.html`:

1. **Update GitHub repo links:**
   - Replace `yourusername` with your actual GitHub username
   - Example: `https://github.com/YOUR_USERNAME/vidgrab`

2. **Update download links:**
   - Links point to releases: `releases/download/latest/`
   - Change `yourusername` in all URLs

3. **Customize text:**
   - Edit title, description, features
   - Add your own branding

4. **Deploy:**
   - Just commit and push
   - GitHub Pages updates automatically

### Example Download Link Format

```
https://github.com/yourusername/vidgrab/releases/download/v1.0.0/VidGrab.exe
```

Replace:
- `yourusername` - Your GitHub username
- `v1.0.0` - Your release tag
- `VidGrab.exe` - The file name

## Full Release Workflow

Here's the complete process for releasing a new version:

### 1. Prepare Release
```bash
# Update version in code (if applicable)
# Commit changes
git add .
git commit -m "Release v1.0.0: New features and bug fixes

- Feature 1
- Feature 2
- Bug fix 1"
```

### 2. Create Tag
```bash
git tag -a v1.0.0 -m "Version 1.0.0 Release"
```

### 3. Push to GitHub
```bash
git push origin main
git push origin v1.0.0
# Or push all tags: git push --tags
```

### 4. Wait for Build
- Go to Actions tab
- Watch workflow complete (5-10 minutes)
- Check for any build errors

### 5. Review Release
- Go to Releases page
- Edit the auto-created release
- Add release notes
- Upload any additional files if needed
- Click "Publish release"

### 6. Update Landing Page (Optional)
- Edit `index.html` to point to new version
- Or use "latest" tag for automatic updates

## Troubleshooting CI/CD

### Build Fails on macOS

Common issue: PyQt6 installation
```bash
# Solution: Ensure requirements.txt has correct versions
pip install --upgrade PyQt6
```

### Build Fails on Windows

Common issue: Long file paths
```bash
# Solution: Enable long paths in Windows
# Run as Admin: git config --system core.longpaths true
```

### Build Fails on Linux

Common issue: Missing libraries
```bash
# Solution: Install system dependencies
sudo apt-get install libxkbcommon-x11-0 libxkbcommon0
```

### Release Not Created

Check:
1. Tag was pushed (not just committed): `git push --tags`
2. Workflow completed successfully
3. Check Actions tab for errors

## Advanced Customization

### Custom Release Notes

Edit `.github/workflows/build.yml`:

```yaml
- name: Create Release
  if: startsWith(github.ref, 'refs/tags/v')
  uses: softprops/action-gh-release@v1
  with:
    files: |
      dist/VidGrab.dmg
      dist/VidGrab.exe
      dist/VidGrab
    body: |
      ## YouTube Downloader v1.0.0

      ### Features
      - New download queue system
      - Enhanced error handling
      
      ### Downloads
      - macOS: VidGrab.dmg
      - Windows: VidGrab.exe
      - Linux: VidGrab
```

### Additional Platforms

To add more platforms (e.g., ARM-based Mac):

```yaml
strategy:
  matrix:
    include:
      # Add this for ARM64 macOS:
      - os: macos-latest
        arch: arm64
        # ... rest of config
```

### Code Signing

For production, add code signing:

**macOS:**
```bash
# Create signing certificate
codesign -s - dist/VidGrab.app
```

**Windows:**
```bash
# Requires code signing certificate
signtool sign /f cert.pfx dist/VidGrab.exe
```

## Monitoring

### GitHub Actions

- Check workflow runs: Settings → Actions → General
- Enable notifications for failures
- Review logs for any issues

### Release Analytics

- Track downloads from GitHub Releases page
- See download counts per file
- Monitor release traffic

## Support

Having deployment issues?

1. **Check GitHub Actions logs** - most detailed info
2. **Review BUILDING.md** - covers manual build issues
3. **Check release downloads** - verify files are there
4. **Test locally** - build on your machine first

Common resources:
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub Pages Docs](https://docs.github.io/en/pages)
- [PyInstaller Docs](https://pyinstaller.org/)

