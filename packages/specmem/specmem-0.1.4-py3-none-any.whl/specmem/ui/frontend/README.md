# SpecMem Web UI Frontend

React + TypeScript + Tailwind CSS frontend for SpecMem.

## Development

```bash
# Install dependencies
npm install

# Start dev server (proxies API to localhost:8765)
npm run dev

# Build for production
npm run build
```

## Building for Distribution

The build output goes to `../static/` which is served by the FastAPI backend.

```bash
npm run build
```

This creates:
- `../static/index.html`
- `../static/assets/` (JS, CSS bundles)

## Features

- Dashboard with block list and filters
- Semantic search
- Pinned blocks view
- Statistics panel
- Dark mode
- Live updates via WebSocket
- Export Agent Pack
