# NDF - Note Data Format

Write data like notes, parse like lightning. A simple, compact, model-optimized data format.

## Features

- **40-70% smaller** than JSON
- **Write like taking notes** - minimal syntax
- **Optimized for AI/ML** - token efficient
- **Fast parsing** - single-pass parser
- **Bidirectional** - parse and serialize

## Installation
```bash
pip install notedf
```

## Quick Start
```python
from notedf import NoteDataFormat

parser = NoteDataFormat()

# Parse NDF
data = parser.parse("""
user:
  name: Alice
  age: 30
  tags: python ai ml
""")

# Serialize to NDF
ndf_text = parser.dumps(data)
```

## Syntax Examples

### Simple Values

name: John Doe
age: 30
active: yes
score: 95.5

### Lists
tags: python ai machine-learning
colors: red, blue, green

### Nested Objects
user:
name: Alice
settings:
theme: dark
notifications: yes

### Multi-line Text
description: |
This is a multi-line description.
It preserves line breaks.

## Why NDF?

| Feature | JSON | YAML | TOML | NDF |
|---------|------|------|------|-----|
| Write Speed | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Parse Speed | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Size | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Token Efficiency | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Documentation

Full documentation available at [GitHub](https://github.com/Dysporium/note-data-format)

## License

MIT License - see LICENSE file for details.