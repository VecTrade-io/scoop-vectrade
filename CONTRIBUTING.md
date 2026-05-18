# Contributing to scoop-vectrade

## Overview

This repository contains the official [Scoop](https://scoop.sh/) bucket for the VecTrade CLI on Windows.

**This bucket is auto-generated.** Manifest files are pushed by [GoReleaser](https://goreleaser.com/) when a new [vectrade-cli](https://github.com/VecTrade-io/vectrade-cli) release is published. Manual edits to `bucket/vectrade.json` will be overwritten.

## Repository Structure

```
scoop-vectrade/
├── bucket/
│   └── vectrade.json         # Scoop manifest (auto-generated)
├── .github/
│   └── workflows/
│       └── ci.yml            # CI validation pipeline
├── tests/
│   └── test_manifest.py     # Manifest structure validation
├── pytest.ini                # Test configuration
├── CONTRIBUTING.md           # This file
├── README.md                 # User-facing docs
├── LICENSE                   # MIT
└── .gitignore
```

## How Releases Work

1. A new tag is pushed to `vectrade-cli` (e.g., `v0.2.0`).
2. GoReleaser builds binaries for all platforms.
3. GoReleaser generates `bucket/vectrade.json` with correct URLs and hashes.
4. GoReleaser pushes the manifest to this repo's `main` branch.

## Running Tests Locally

```bash
# Install pytest
pip install pytest

# Run all validation tests
pytest tests/ -v
```

## What the Tests Validate

- Manifest file exists and is valid JSON
- Required fields: `version`, `description`, `homepage`, `license`, `architecture`, `bin`, `checkver`, `autoupdate`
- Correct metadata (semver version, MIT license, vectrade.exe binary)
- Architecture support (64bit + arm64)
- URLs point to GitHub releases with `.zip` format
- Autoupdate configuration with `$version` templates
- Checkver uses GitHub releases API
- JSON formatting (2-space indent, no BOM, trailing newline)

## When to Manually Edit

You should only edit this repo to:

- Update CI workflows
- Add/improve validation tests
- Fix README or docs

**Never** manually edit `bucket/vectrade.json` — it will be overwritten on next release.
