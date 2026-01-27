# Monorepo Structure

This project uses a monorepo structure with separate folders for web and desktop apps:

```
/
├── www/                          # Next.js landing page + docs
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── pnpm-lock.yaml
│
├── app/                          # PyQt6 desktop application
│   ├── core/                     # Download engine (yt-dlp wrapper)
│   ├── ui/                       # Qt UI components
│   ├── resources/                # Assets, icons
│   ├── macos/                    # macOS-specific configs
│   ├── main.py                   # Entry point
│   ├── requirements.txt           # Python dependencies
│   ├── build.sh / build.bat      # Build scripts
│   ├── BUILDING.md
│   └── ...
│
├── MONOREPO_SETUP.md             # This file
├── README.md
├── MACOS_INSTALLATION.md
└── .gitignore                    # Covers both Python + Node
```

## Development Workflow

### Setup Both Apps

**Python (Desktop):**
```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Node.js (Landing Page):**
```bash
cd www
pnpm install
```

### Running Locally

| Task | Command |
|------|---------|
| Desktop app | `cd app && python -m main` |
| Landing page | `cd www && pnpm dev` (opens on `localhost:3000`) |
| Build desktop | `cd app && ./build.sh` |
| Build landing page | `cd www && pnpm build` |

## Deployment

### Desktop App
- Built in CI/CD → GitHub Releases
- See `app/BUILDING.md` and `app/DEPLOYMENT.md`

### Landing Page
- Deploy `www/` folder to Vercel, Netlino, or GitHub Pages
- Environment: Set via `.env.local` (not committed)
- No build step needed for testing locally

## CI/CD Structure

Each build pipeline is independent:
- **Desktop**: Builds PyQt6 app for macOS/Windows/Linux (Python)
- **Landing Page**: Builds Next.js site (Node.js)

See `.github/workflows/` for details.

## Git Workflow

- Keep Python and Node dependencies separate
- `.gitignore` covers both `.venv/`, `node_modules/`, and `.next/`
- Releases coordinate both: `v1.0.0` = desktop app + updated landing page

---

**Quick Links:**
- [Desktop Build Instructions](./app/BUILDING.md)
- [macOS Installation](./MACOS_INSTALLATION.md)
- [Deployment Guide](./app/DEPLOYMENT.md)
