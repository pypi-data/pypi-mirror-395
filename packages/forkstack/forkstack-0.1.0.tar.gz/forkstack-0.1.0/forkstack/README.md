# forkstack

**Instant, isolated development environments using zero-copy database and storage forks.**

forkstack is a CLI tool for creating fully isolated development environments in seconds. Each developer gets their own copy of your entire stack—database and object storage—without duplicating data or slowing down.

## Installation

```bash
# Recommended: install script
curl -LsSf https://forkstack.xyz/install.sh | sh

# Or with pip/uv
pip install forkstack
uv pip install forkstack

# Or with cargo
cargo install forkstack --bin forks
```

## Why forkstack?

Traditional development environments share databases or require expensive duplication:
- ❌ **Shared dev DB**: Developers step on each other's data
- ❌ **DB per developer**: Expensive, slow to provision, hard to keep in sync
- ❌ **Local-only**: Can't test with production-like data

forkstack gives you the best of all worlds:
- ✅ **Instant creation**: New environments in seconds, not minutes
- ✅ **Zero cost**: Fork-on-write means no data duplication charges
- ✅ **Full isolation**: Each environment has its own DB and storage
- ✅ **Production parity**: Fork from production to test with real data
- ✅ **Easy cleanup**: Delete environments instantly when done

## Quick Start

### 1. Create a config file

Create `.forkstack.toml` in your project:

```toml
[database]
provider = "turso"
organization = "your-org"
production = "my-app-prod"

[storage.uploads]
provider = "tigris"
bucket = "my-app-uploads"
endpoint = "https://fly.storage.tigris.dev"
```

### 2. Set credentials

```bash
export TURSO_API_TOKEN="your-token"
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

### 3. Create a fork

```bash
$ forks create -n alice
Created fork: alice
Database: libsql://alice-your-org.turso.io
Storage:  uploads: s3://my-app-uploads/forks/alice/
```

### 4. Use your fork

Point your app at the fork URLs, work in isolation, then clean up:

```bash
$ forks delete alice
Deleted fork: alice
```

## CLI Reference

```bash
forks create           # Create fork with random name
forks create -n alice  # Create fork with specific name
forks list             # List all forks
forks delete alice     # Delete a fork
```

## How It Works

```
forks create
    │
    ├── Turso API: Create database branch
    │   └── Zero-copy fork from production DB
    │
    └── S3 API: Copy objects to fork prefix
        └── Full copy (or use Tigris bucket forks)
```

**Database branching** uses Turso's native branching—instant, zero-copy regardless of database size.

**Storage forking** copies objects to a fork-specific prefix. For zero-copy storage, use Tigris bucket forks.

## Supported Services

**Databases** (pick one):
- [Turso](https://turso.tech) - SQLite branches (recommended)
- More coming soon (Neon, PlanetScale)

**Object Storage** (pick one):
- [Tigris](https://www.tigrisdata.com) - S3-compatible with bucket forks (recommended)
- Any S3-compatible storage

## Pattern Benefits

### For Individual Developers
- Test risky changes in isolation
- Work on multiple features simultaneously
- Fork from prod to debug with real data
- Clean up experiments instantly

### For Teams
- No database conflicts between developers
- Easy code review with deployable branches
- Staging environments on-demand
- Safe production debugging

### For CI/CD
- Ephemeral preview environments per PR
- Cost-effective testing at scale
- Automatic cleanup after merge

## Documentation

Full documentation at [forkstack.xyz](https://forkstack.xyz)

- [Getting Started Guide](https://forkstack.xyz/getting-started)
- [Architecture Deep Dive](https://forkstack.xyz/architecture)
- [Database Options](https://forkstack.xyz/databases)
- [Storage Options](https://forkstack.xyz/storage)

## Contributing

Contributions welcome! Submit issues and PRs at [github.com/russellromney/forkstack](https://github.com/russellromney/forkstack)

## License

Apache 2.0 - Use it however you want.
