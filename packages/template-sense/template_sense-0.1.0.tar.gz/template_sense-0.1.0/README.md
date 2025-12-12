# Template Sense

AI-powered invoice template extraction library for structured metadata analysis.

Template Sense analyzes Excel-based invoice templates using heuristics and AI to extract structured metadata, supporting multi-language translation and fuzzy matching against canonical field dictionaries.

## Installation

### From PyPI (Recommended)

```bash
# Latest version
pip install template-sense

# Specific version
pip install template-sense==0.1.0
```

### From GitHub

```bash
# Latest release
pip install git+https://github.com/Projects-with-Babajide/template-sense.git@main

# Specific release tag
pip install git+https://github.com/Projects-with-Babajide/template-sense.git@v0.1.0
```

### For Development

```bash
git clone https://github.com/Projects-with-Babajide/template-sense.git
cd template-sense
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .[dev]
```

## Quick Start

```python
from template_sense.analyzer import extract_template_structure

# Define your canonical field dictionary
# This should match YOUR domain's field names
field_dictionary = {
    "headers": {
        "invoice_number": "Invoice number",
        "shipper": "Shipper",
        "consignee": "Consignee",
        "invoice_date": "Invoice date",
        "due_date": "Due date",
    },
    "columns": {
        "product_name": "Product name",
        "quantity": "Quantity",
        "price": "Price",
        "amount": "Amount",
    }
}

# Extract template structure
result = extract_template_structure("path/to/template.xlsx", field_dictionary)

# Access extracted metadata
print(result["normalized_output"]["headers"]["matched"])
print(result["normalized_output"]["columns"]["matched"])
```

**Note:** The `field_dictionary` should contain YOUR canonical field names. Each key is the canonical identifier you want to use, and each value is the expected label in the template. The library will use AI to match similar fields and fuzzy matching to find the best matches.

## Features

- Excel template parsing and analysis
- AI-based field and column classification (OpenAI & Anthropic)
- Multi-language translation support
- Fuzzy matching against canonical field dictionaries
- Structured JSON output

## Documentation

- [Release Process](docs/RELEASE_PROCESS.md) - How to create and publish releases
- [Development Setup](docs/dev-setup.md) - Setting up your development environment
- [Architecture](docs/architecture.md) - System design and module structure

## Requirements

- Python 3.10+
- OpenAI API key (if using OpenAI provider)
- Anthropic API key (if using Anthropic provider)

## License

MIT

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- [Issue Tracker](https://github.com/Projects-with-Babajide/template-sense/issues)
- [GitHub Discussions](https://github.com/Projects-with-Babajide/template-sense/discussions)
