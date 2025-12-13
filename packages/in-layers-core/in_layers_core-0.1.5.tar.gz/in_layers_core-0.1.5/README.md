# In Layers Core

Python port of the Node-in-Layers core framework.
Supports  Domains, config and layers loading, and cross-layer logging.

Key points:
- Domains explicitly provided in config (no convention discovery)
- Layers are loaded in configured order (supports composite layers)
- Cross-layer logging with automatic id propagation and function wraps


## Contributing

### Auto-Cleaning / Checking Tools
```bash
poetry run black .
poetry run ruff check --fix .
```

### Publishing
```bash
rm -Rf ./dist/
poetry run python -m build
poetry run python -m twine upload dist/*
```
