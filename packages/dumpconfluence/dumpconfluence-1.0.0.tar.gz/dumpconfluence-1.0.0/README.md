# DumpConfluence

<div align="center">

**A modern CLI tool to backup Confluence pages with images and attachments**

[![Python](https://img.shields.io/pypi/pyversions/dumpconfluence)](https://pypi.org/project/dumpconfluence/)
[![Version](https://img.shields.io/pypi/v/dumpconfluence)](https://pypi.org/project/dumpconfluence/)
[![License](https://img.shields.io/github/license/danilipari/dumpconfluence)](https://github.com/danilipari/dumpconfluence/blob/main/LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/danilipari/dumpconfluence/tests.yml?label=tests)](https://github.com/danilipari/dumpconfluence/actions)

*Fast, reliable, and user-friendly Confluence backup solution*

</div>

---

## ✨ Features

- 📥 **Complete Page Backup** - Download Confluence pages with all images and attachments
- 💾 **Self-Contained HTML** - Generate beautiful, standalone HTML files with embedded CSS
- 🔐 **Secure Profile Management** - Store and manage multiple credential profiles safely
- 📦 **Batch Processing** - Backup multiple pages from URL lists efficiently
- 🎨 **Beautiful CLI Interface** - Rich terminal UI with progress indicators and colored output
- 📁 **Smart Directory Management** - Flexible output directory options with auto-creation
- 🚀 **Auto-Profile Selection** - Intelligent credential selection for seamless workflows
- 🛡️ **Robust Error Handling** - Comprehensive validation and helpful error messages
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🔧 **Developer Friendly** - Full type hints, comprehensive tests, and clean architecture

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/danilipari/dumpconfluence.git
cd DumpConfluence

# Install in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install dumpconfluence
```

## Quick Start

### Basic Usage

Backup a single Confluence page:

```bash
dumpconfluence backup "https://company.atlassian.net/wiki/spaces/SPACE/pages/123456/Page+Title"
```

You'll be prompted for:
- Confluence URL (e.g., https://company.atlassian.net)
- Your email address
- API token

### Save Credentials as Profile

Save your credentials for future use:

```bash
dumpconfluence backup "URL" --save-profile work
```

Use saved profile:

```bash
dumpconfluence backup "URL" --profile work
```

### Specify Output Directory

By default, pages are saved in the current directory. To specify a different location:

```bash
dumpconfluence backup "URL" --output-dir /path/to/backups
```

## Advanced Usage

### Profile Management

Create a new profile:

```bash
dumpconfluence config add myprofile
```

List all profiles:

```bash
dumpconfluence config list
```

Remove a profile:

```bash
dumpconfluence config remove myprofile
```

### Batch Processing

Create a text file with URLs (one per line):

```txt
https://company.atlassian.net/wiki/spaces/SPACE/pages/111/Page1
https://company.atlassian.net/wiki/spaces/SPACE/pages/222/Page2
https://company.atlassian.net/wiki/spaces/SPACE/pages/333/Page3
```

Process all URLs:

```bash
dumpconfluence batch urls.txt --profile work
```

### Command Line Options

```bash
dumpconfluence backup [OPTIONS] PAGE_URL

Options:
  -u, --url TEXT        Confluence base URL
  -e, --email TEXT      Confluence account email
  -t, --token TEXT      Confluence API token
  -o, --output-dir TEXT Output directory (default: current)
  -p, --profile TEXT    Use saved profile
  --save-profile TEXT   Save credentials as profile
  --help               Show this message and exit
```

## Getting an API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a descriptive name
4. Copy the token immediately (you won't see it again)

## Output Structure

Each page creates its own directory:

```
Page_Title/
├── Page_Title.html    # Self-contained HTML with embedded CSS
├── metadata.json      # Page metadata and export info
└── images/           # Downloaded images
    ├── image1.png
    ├── image2.jpg
    └── ...
```

## Configuration

Profiles are stored in:
- Linux/Mac: `~/.config/dumpconfluence/config.json`
- Windows: `%APPDATA%\dumpconfluence\config.json`

⚠️ **Security Note**: Credentials are stored in plain text. Ensure proper file permissions.

## Requirements

- Python 3.8+
- Confluence Cloud account with API access
- Read permissions for target pages

## Troubleshooting

### Authentication Failed

- Verify your API token is correct
- Ensure your email matches the Confluence account
- Check you have read permissions for the page

### Images Not Downloading

- Some images may require special permissions
- Check if images are from external sources
- Verify API token has proper scope

### Page Not Found

- Verify the URL is correct
- Ensure you have access to the page
- Check if the page exists in the specified space

## Development

### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/danilipari/dumpconfluence.git
cd DumpConfluence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with extras
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black dumpconfluence/
ruff check dumpconfluence/
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/danilipari/dumpconfluence/issues) page.