# eL-tfgen

**AI-Powered Terraform Module Generator**

Generate production-ready Terraform configurations from provider documentation using Claude AI.

## Features

- 🤖 **AI-Powered Generation**: Uses Anthropic's Claude to understand and generate Terraform code
- 📚 **Documentation Parsing**: Automatically scrapes and analyzes Terraform provider documentation
- 🖥️ **GUI & CLI**: User-friendly interface or command-line for automation
- ⚡ **Fast & Accurate**: Generates complete, working Terraform modules in seconds
- 🔧 **Customizable**: Handles various providers and resource types

## Installation

```bash
pip install eL-tfgen
```

## Quick Start

### GUI Mode
```bash
tfgen-ui
```

### CLI Mode
```bash
tfgen --help
```

## Requirements

- Python 3.8 or higher
- Anthropic API key (set in `.env` file as `ANTHROPIC_API_KEY`)

## Configuration

Create a `.env` file in your working directory:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Use Cases

- Generate Terraform modules for new cloud resources
- Quickly scaffold infrastructure code
- Learn Terraform best practices from AI-generated examples
- Automate repetitive Terraform code creation

## License

MIT

## Author

eLTitans
