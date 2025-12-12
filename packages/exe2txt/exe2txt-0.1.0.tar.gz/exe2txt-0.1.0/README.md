# exe2txt

Convert Windows EXE/DLL files into text representations for LLM prompting.

## Installation

### Using uv (recommended)

```bash
# Install as a tool
uv tool install exe2txt

# Or run directly without installing
uvx exe2txt <file.exe>
```

### Using pip

```bash
pip install exe2txt
```

## Usage

### Command Line

```bash
# Analyze an EXE file
exe2txt example.exe

# Save output to a file
exe2txt example.exe -o output.txt
```

### As a Library

```python
from exe2txt import analyze_pe

# Analyze a PE file
info = analyze_pe("example.exe")

# Get text representation
print(info.to_text())

# Access structured data
print(f"Machine type: {info.machine_type}")
print(f"Entry point: 0x{info.entry_point:08X}")

for section in info.sections:
    print(f"Section: {section.name}")

for imp in info.imports:
    print(f"Import: {imp.dll_name}")
```

## Features

- Parse PE file headers and metadata
- Extract section information
- List imported DLLs and functions
- List exported functions
- Generate LLM-friendly text output

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/crlotwhite/exe2txt.git
cd exe2txt

# Create virtual environment and install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
uv run pytest
```

### Building

```bash
uv build
```

## License

MIT License
