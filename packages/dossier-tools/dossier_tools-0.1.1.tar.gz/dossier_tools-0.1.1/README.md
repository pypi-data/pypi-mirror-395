# dossier-tools

Validation, signing, and verification tools for `.ds.md` files.

A `.ds.md` file is a markdown document with structured YAML frontmatter containing metadata like title, version, checksum, and cryptographic signature. This package provides tools to validate the frontmatter schema, verify content integrity via SHA256 checksums, and sign/verify files using Ed25519.

```markdown
---
schema_version: "1.0.0"
title: Deploy to Production
version: "1.0.0"
status: stable
objective: Deploy application to production with validation
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: a3b5c8d9...
signature:
  algorithm: ed25519
  public_key: RWT...
  signed_by: alice@example.com
---

# Deploy to Production

Your markdown content here...
```

## Installation

```bash
pip install dossier-tools
```

Or with uv:

```bash
uv add dossier-tools
```

## Quick Start

```bash
# Initialize and generate keys
dossier init
dossier generate-keys

# Create a dossier from markdown
dossier create workflow.md --title "My Workflow" --objective "Do something" --author "you@example.com"

# Validate, sign, and verify
dossier validate workflow.ds.md
dossier sign workflow.ds.md --signed-by "you@example.com"
dossier verify workflow.ds.md
```

## Registry

Browse and download dossiers from the public registry:

```bash
# List available dossiers
dossier list

# Get metadata for a dossier
dossier get myorg/deploy

# Download a dossier
dossier pull myorg/deploy
```

Publish your own dossiers (requires GitHub authentication):

```bash
dossier login
dossier publish workflow.ds.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DOSSIER_REGISTRY_URL` | Registry API URL | `https://dossier-registry-mvp.vercel.app` |
| `DOSSIER_SIGNING_KEY` | Default signing key name | `default` |
| `DOSSIER_LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) | `WARNING` |

## Documentation

See [docs/](./docs/) for detailed documentation:

- [CLI Reference](./docs/cli.md) — All commands and options
- [Python API](./docs/api.md) — Using dossier-tools as a library
- [Schema Reference](./docs/schema.md) — Frontmatter field reference
- [Signing Guide](./docs/signing.md) — Signing and verification workflow

## Development

```bash
# Clone and setup
git clone https://github.com/tal-liberio/dossier-tools.git
cd dossier-tools
make setup    # Install dependencies with uv

# Run tests
make test

# Format code
make format

# Check formatting and lint
make check
```

## License

MIT
