# Doclayer CLI

[![PyPI version](https://badge.fury.io/py/doclayer-cli.svg)](https://badge.fury.io/py/doclayer-cli)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

The official Doclayer Command-Line Interface for interacting with the Doclayer document intelligence platform.

## Installation

### macOS

```bash
pip3 install --user doclayer-cli
```

> **Note:** If `doclayer` command is not found after install, add `~/Library/Python/3.11/bin` to your PATH.

### Linux / Windows

```bash
pip install doclayer-cli
```

## Quick Start

```bash
# Authenticate with your Doclayer account
doclayer auth login

# Process a document
doclayer ingest file invoice.pdf --project proj_123 --wait

# List available agents
doclayer agent list --category contracts

# Check billing usage
doclayer billing usage
```

## Features

- **Complete Command Set**: All Doclayer operations via CLI
- **Batch Ingestion**: Process multiple documents with resume capability
- **Rich Output**: Beautiful terminal formatting
- **Profile Management**: Multiple environment profiles support
- **Secure Authentication**: API key and OAuth support

## Commands

| Command | Description |
|---------|-------------|
| `auth` | Authentication (login, logout, API keys) |
| `agent` | Agent template management |
| `billing` | Usage tracking and billing |
| `model` | Model configuration |
| `project` | Project management |
| `document` | Document operations |
| `workflow` | Workflow management |
| `search` | Vector and graph search |
| `template` | Template gallery |
| `config` | Configuration management |
| `ingest` | Batch ingestion workflows |
| `status` | Job monitoring and verification |

## Configuration

The CLI stores configuration in `~/.doclayer/`:

```
~/.doclayer/
└── config.json      # Configuration and profile settings
```

Sensitive credentials (API keys, tokens) are stored in `~/.doclayer/config.json` on macOS, or in your system's keyring on Linux/Windows.

### Credential Storage

| Platform | Default Storage | Override |
|----------|-----------------|----------|
| macOS | Config file | `DOCLAYER_USE_KEYRING=1` to use Keychain |
| Linux | System keyring | `DOCLAYER_NO_KEYRING=1` to use config file |
| Windows | System keyring | `DOCLAYER_NO_KEYRING=1` to use config file |

> **Note:** On macOS, the system Keychain prompts for password on every CLI command, so we use file-based storage by default for better UX.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DOCLAYER_API_KEY` | API key for authentication |
| `DOCLAYER_BASE_URL` | Custom API endpoint (default: https://api.doclayer.ai) |
| `DOCLAYER_PROFILE` | Active profile name |
| `DOCLAYER_TOKEN` | Authentication token |
| `DOCLAYER_NO_KEYRING` | Set to `1` to disable system keyring (Linux/Windows) |
| `DOCLAYER_USE_KEYRING` | Set to `1` to enable system keyring (macOS) |
| `DOCLAYER_VERBOSE` | Enable verbose output |

## Requirements

- Python 3.11 or higher
- pip or pipx

## Documentation

- **Getting Started**: https://docs.doclayer.ai/cli/quickstart
- **Command Reference**: https://docs.doclayer.ai/cli/commands
- **API Documentation**: https://docs.doclayer.ai/api

## Support

- **Documentation**: https://docs.doclayer.ai
- **Email**: support@doclayer.ai
- **Website**: https://doclayer.ai

## License

Copyright © 2024-2025 Doclayer. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, modification,
distribution, or use of this software, via any medium, is strictly prohibited.

See the [LICENSE](LICENSE) file for full terms.
