# scoop-vectrade

[![CI](https://github.com/VecTrade-io/scoop-vectrade/actions/workflows/ci.yml/badge.svg)](https://github.com/VecTrade-io/scoop-vectrade/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/VecTrade-io/scoop-vectrade)](LICENSE)

Official [Scoop](https://scoop.sh/) bucket for the [VecTrade CLI](https://github.com/VecTrade-io/vectrade-cli) on Windows.

## Quick Start

```powershell
# Add the bucket
scoop bucket add vectrade https://github.com/VecTrade-io/scoop-vectrade

# Install the CLI
scoop install vectrade
```

## Usage

```powershell
# Verify installation
vectrade version

# Get help
vectrade --help

# Example: fetch a quote
vectrade quote AAPL
```

## Upgrade

```powershell
scoop update vectrade
```

## Uninstall

```powershell
scoop uninstall vectrade
scoop bucket rm vectrade
```

## Platform Support

| OS      | Architecture | Status |
|---------|-------------|--------|
| Windows | x86_64      | ✅ |
| Windows | arm64       | ✅ |

## Auto-Update

This bucket supports Scoop's autoupdate mechanism. When a new CLI version is released:

1. `scoop update` refreshes bucket metadata
2. `scoop update vectrade` downloads the new version
3. Hashes are verified against the release checksums

## How It Works

This bucket is automatically updated by [GoReleaser](https://goreleaser.com/) when a new CLI version is released. Manifest files are pushed here by the CI pipeline — do not edit them manually.

## Issues & Support

Please file bugs and feature requests on the **[vectrade-cli](https://github.com/VecTrade-io/vectrade-cli/issues)** repository.

## Links

- [VecTrade CLI](https://github.com/VecTrade-io/vectrade-cli) — source repository
- [Documentation](https://docs.vectrade.io/sdks/cli) — CLI usage guide
- [Releases](https://github.com/VecTrade-io/vectrade-cli/releases) — all CLI versions
- [Contributing](CONTRIBUTING.md) — how this repo is structured

## License

MIT — see [LICENSE](LICENSE).
