# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation Methods

### Install from PyPI (when published)

```bash
pip install streamlit-app-generator
```

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/leandrodalcortivo/streamlit-app-generator.git
cd streamlit-app-generator
```

2. Install in development mode:
```bash
pip install -e .
```

3. Or install with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Database-Specific Installation

### PostgreSQL Support

```bash
pip install streamlit-app-generator[postgresql]
```

### MySQL Support

```bash
pip install streamlit-app-generator[mysql]
```

### MongoDB Support

```bash
pip install streamlit-app-generator[mongodb]
```

### Redis Support

```bash
pip install streamlit-app-generator[redis]
```

### All Databases

```bash
pip install streamlit-app-generator[all-databases]
```

## Verify Installation

```bash
streamlit-app-generator --version
streamlit-app-generator info
```

## Next Steps

- Read the [Quick Start Guide](quickstart.md)
- Check the [Configuration Guide](configuration.md)
- See the [API Reference](api_reference.md)
