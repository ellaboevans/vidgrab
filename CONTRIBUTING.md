# Contributing to VidGrab

Thank you for your interest in contributing to VidGrab! We welcome contributions from the community. This document provides guidelines and instructions for contributing.

---

## Getting Started

### Prerequisites

- Python 3.11+
- macOS, Windows, or Linux
- Git

### Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/ellaboevans/vidgrab.git
   cd vidgrab
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r app/requirements.txt
   pip install pillow  # For splash screen generation
   ```

4. **Run the app**
   ```bash
   python3 -m app.main
   ```

---

## Development Workflow

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to functions and classes

### File Organization

```
app/
├── core/          # Core functionality (engine, queue, logger)
├── ui/            # User interface (PyQt6)
└── main.py        # Entry point
```

### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Keep commits atomic (one logical change per commit)
   - Write clear commit messages
   - Test your changes locally

3. **Commit message format**

   ```
   type: brief description

   Longer explanation if needed.
   - Point 1
   - Point 2
   ```

   Types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`

4. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

---

## Types of Contributions

### 🐛 Bug Reports

Found a bug? Please report it!

**Before submitting:**

- Check if the bug already exists in Issues
- Test on latest version
- Try to reproduce consistently

**Include in bug report:**

- macOS/Windows/Linux version
- VidGrab version
- Steps to reproduce
- Expected vs actual behavior
- Error message or screenshot
- Log file (`~/.vidgrab/logs/app.log`)

**Example:**

```
Title: Progress bar not updating during downloads

Steps:
1. Add single YouTube URL
2. Click "Start Downloads"
3. Watch progress bar

Expected: Progress updates from 0% to 100%
Actual: Progress stays at 0% until completion

System: macOS 14.2, VidGrab 1.0.0
```

### ✨ Feature Requests

Have an idea to improve VidGrab?

**Before submitting:**

- Check Roadmap in CHANGELOG.md
- Check open Issues and Discussions

**Include in feature request:**

- Clear description of the feature
- Why you think it's useful
- Example use case
- Possible implementation approach (optional)

**Example:**

```
Title: Add keyboard shortcuts for common actions

Description: Users should be able to use keyboard shortcuts instead of clicking buttons.

Requested shortcuts:
- Ctrl+A (or Cmd+A on Mac): Add URL
- Ctrl+S (or Cmd+S on Mac): Start downloads
- Ctrl+Q (or Cmd+Q on Mac): Quit app

Use case: Power users can work faster without reaching for mouse.
```

### 📖 Documentation

Improvements to docs are always welcome!

- Fix typos or unclear explanations
- Add examples
- Improve formatting
- Add screenshots or diagrams

### 🧹 Code Quality

Help improve the codebase:

- Refactor for clarity
- Add type hints
- Improve error handling
- Optimize performance
- Add unit tests

---

## Testing Your Changes

### Manual Testing Checklist

Before submitting a PR:

- [ ] Code compiles without errors
- [ ] Feature works as expected
- [ ] No UI freezing during operations
- [ ] Settings persist after restart
- [ ] Queue persists after restart
- [ ] Error messages are clear
- [ ] No new console errors/warnings

### On macOS Specifically

- [ ] App launches from `dist/VidGrab.app`
- [ ] Download works with single video
- [ ] Download works with playlist
- [ ] Settings dialog opens and saves
- [ ] View Logs button opens log file
- [ ] Stop button halts download

### Build Testing

```bash
cd app
./build.sh
open dist/VidGrab.app
```

---

## Pull Request Guidelines

### Before Submitting

1. **Sync with main branch**

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run tests locally**
   - Verify code compiles
   - Test the feature manually
   - Check error handling

3. **Update relevant docs**
   - If adding feature: update CHANGELOG.md
   - If changing setup: update BUILDING.md
   - If API change: update docstrings

### PR Description Template

```markdown
## Description

Brief description of changes.

## Related Issue

Closes #123

## Changes Made

- Change 1
- Change 2
- Change 3

## Testing

- [x] Manual testing on macOS
- [x] Feature works as expected
- [x] No regressions

## Screenshots (if applicable)
```

### Code Review Process

Your PR will be reviewed for:

- **Functionality**: Does it work as intended?
- **Code quality**: Is it clean and maintainable?
- **Tests**: Are changes properly tested?
- **Documentation**: Are docs updated?
- **Compatibility**: Does it work on all platforms?

---

## Architecture Overview

### Core Modules

**`core/engine.py`** - Download engine wrapper around yt-dlp

- Handles format selection, quality settings
- Manages FFmpeg integration
- Reports progress via hooks

**`core/hooks.py`** - Progress callback system

- Tracks download percentage
- Calculates speed and ETA
- Formats human-readable output

**`core/queue.py`** - Queue state management

- Tracks current and next items
- Manages download order

**`ui/app.py`** - Main PyQt6 window

- `DownloadWorker` thread for downloads
- `MetadataWorker` thread for title fetching
- Signal/slot connections

**`core/logger.py`** - Logging system

- Rotating file logs
- Singleton pattern

### Data Flow

```
User Input
    ↓
URLValidator (validation + duplicate check)
    ↓
MetadataWorker (fetch title)
    ↓
QueueManager (add to queue)
    ↓
DownloadWorker (download file)
    ↓
DownloadEngine (yt-dlp wrapper)
    ↓
Progress Hooks (report progress)
    ↓
UI Updates (update progress bar, status)
    ↓
QueuePersistence (save queue on exit)
```

---

## Commit Message Examples

**Good:**

```
feat: Add keyboard shortcuts for common actions

- Ctrl+A to add URL
- Ctrl+S to start downloads
- Ctrl+Q to quit
- Updated settings dialog to show shortcuts

Closes #42
```

**Good:**

```
fix: Progress bar text invisible on filled portion

Changed progress bar text color from cyan to dark
to improve readability on cyan background fill.

Fixes #38
```

**Good:**

```
docs: Clarify installation instructions for Windows

Added explicit path examples and troubleshooting
section for common Windows installation issues.
```

---

## Reporting Security Issues

**Do not** open a public issue for security vulnerabilities.

Email security concerns to: [contact info if provided]

Include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (optional)

---

## Code of Conduct

- Be respectful and inclusive
- Assume good intent
- Provide constructive feedback
- Help others learn
- Respect privacy and confidentiality

---

## Questions?

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Docs**: Check README.md, BUILDING.md, DEPLOYMENT.md

---

## Recognition

Contributors will be recognized in:

- GitHub contributors page
- Release notes (for significant contributions)
- Project README (for sustained contributions)

---

## License

By contributing to VidGrab, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to VidGrab! 🎉
