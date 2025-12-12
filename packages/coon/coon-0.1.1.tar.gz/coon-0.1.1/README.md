# COON Python SDK

[![PyPI version](https://img.shields.io/pypi/v/coon.svg?labelColor=1b1b1f&color=60a5fa)](https://pypi.org/project/coon/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-60a5fa?labelColor=1b1b1f)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-60a5fa?labelColor=1b1b1f)](../../LICENSE)

Token-efficient compression format for Dart/Flutter code, optimized for LLM contexts.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [Compression Strategies](#compression-strategies)
- [API Reference](#api-reference)
- [CLI Usage](#cli-usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [License](#license)

## Installation

```bash
# Standard installation
pip install coon

# With CLI support
pip install coon[cli]

# For development
pip install coon[dev]
```

## Quick Start

```python
from coon import compress_dart, decompress_coon

# Compress Dart code
dart_code = """
class MyWidget extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: Text('Hello')),
            body: Center(child: Text('World')),
        );
    }
}
"""

compressed = compress_dart(dart_code)
print(f"Compressed: {compressed}")
# Output: c:MyWidget<StatelessWidget>;m:b S{a:B{t:T'Hello'},b:N{c:T'World'}}

# Decompress back to Dart
restored = decompress_coon(compressed)
```

## Advanced Usage

### Using the Compressor Class

```python
from coon import Compressor, CompressionConfig

# Configure compression
config = CompressionConfig(
    strategy="aggressive",
    enable_metrics=True,
    validate_output=True
)

compressor = Compressor(config)
result = compressor.compress(dart_code)

print(f"Original tokens: {result.original_tokens}")
print(f"Compressed tokens: {result.compressed_tokens}")
print(f"Savings: {result.percentage_saved:.1f}%")
print(f"Strategy: {result.strategy_used}")
```

### Code Analysis

```python
from coon import CodeAnalyzer

analyzer = CodeAnalyzer()
analysis = analyzer.analyze(dart_code)

# Get detailed report
report = analyzer.generate_report(analysis)
print(report)

# Access metrics
print(f"Complexity: {analysis.complexity}")
print(f"Widget count: {analysis.widget_count}")
print(f"Compression opportunities: {analysis.opportunities}")
```

### Validation

```python
from coon import validate_round_trip

# Verify lossless compression
is_valid = validate_round_trip(dart_code)
print(f"Round-trip valid: {is_valid}")
```

## Compression Strategies

| Strategy | Compression | Speed | Description |
|----------|-------------|-------|-------------|
| `auto` | 50-70% | Fast | Automatic optimal selection |
| `basic` | 30-40% | Fastest | Simple abbreviations |
| `aggressive` | 60-70% | Fast | Maximum compression |
| `ast_based` | 50-65% | Moderate | Syntax tree analysis |
| `component_ref` | 70-80% | Moderate | Pattern-based references |
| `semantic` | 55-65% | Moderate | Meaning-preserving |

### Strategy Selection

```python
from coon import Compressor, CompressionStrategyType

compressor = Compressor()

# Use specific strategy
result = compressor.compress(code, strategy=CompressionStrategyType.AGGRESSIVE)

# Use auto (default)
result = compressor.compress(code, strategy=CompressionStrategyType.AUTO)
```

## API Reference

### Core Functions

#### `compress_dart(code: str, strategy: str = "auto") -> str`

Compress Dart code to COON format.

```python
compressed = compress_dart(dart_code)
compressed = compress_dart(dart_code, strategy="aggressive")
```

#### `decompress_coon(compressed: str) -> str`

Decompress COON format back to Dart code.

```python
original = decompress_coon(compressed)
```

### Classes

#### `Compressor`

Main compression class with configuration options.

```python
from coon import Compressor, CompressionConfig

config = CompressionConfig(
    strategy="auto",
    enable_metrics=True,
    validate_output=False
)

compressor = Compressor(config)
result = compressor.compress(code)
```

#### `Decompressor`

Decompression class with formatting options.

```python
from coon import Decompressor

decompressor = Decompressor(
    format_output=True,
    indent_size=2
)

result = decompressor.decompress(compressed)
```

#### `CompressionResult`

Result object containing compression output and metrics.

```python
result.compressed         # Compressed code string
result.original_tokens    # Original token count
result.compressed_tokens  # Compressed token count
result.percentage_saved   # Compression percentage
result.strategy_used      # Strategy that was used
```

## CLI Usage

```bash
# Compress a file
coon compress app.dart -o app.coon

# Decompress
coon decompress app.coon -o app.dart

# Use specific strategy
coon compress app.dart -s aggressive -o app.coon

# Analyze for compression opportunities
coon analyze app.dart

# Compare all strategies
coon stats app.dart

# Validate round-trip integrity
coon validate app.dart
```

## Architecture

```
coon/
├── core/          # Compressor, Decompressor, Config, Result
├── strategies/    # Compression strategy implementations
│   ├── base.py         # Base strategy class
│   ├── basic.py        # Basic compression
│   ├── aggressive.py   # Aggressive compression
│   ├── ast_based.py    # AST-based compression
│   └── component_ref.py # Component reference
├── data/          # Abbreviation data from shared spec
├── parser/        # Lexer, Parser, AST nodes
├── analysis/      # Code analyzer, Metrics
├── utils/         # Validator, Registry, Formatter
└── cli/           # Command-line interface
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest tests/ --cov=coon --cov-report=html

# Run conformance tests
pytest tests/test_conformance.py
```

## License

MIT - See [LICENSE](../../LICENSE) for details.
