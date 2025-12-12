# Doclayer CLI

[![PyPI version](https://badge.fury.io/py/doclayer-cli.svg)](https://badge.fury.io/py/doclayer-cli)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

The official Doclayer Command-Line Interface for interacting with the Doclayer document intelligence platform.

## Installation

```bash
# Via pip
pip install doclayer-cli

# Or via pipx (recommended for isolated installation)
pipx install doclayer-cli
```

## Quick Start

```bash
# Authenticate with your Doclayer account
doclayer auth login

# Process a document
doclayer ingest file invoice.pdf --project proj_123 --wait

# List available agents
doclayer agent list --category contracts

# Check billing status
doclayer billing status
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
├── config.yaml      # Global configuration
├── credentials      # Encrypted credentials
└── profiles/        # Environment profiles
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DOCLAYER_API_KEY` | API key for authentication |
| `DOCLAYER_API_URL` | Custom API endpoint |
| `DOCLAYER_PROFILE` | Active profile name |

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
