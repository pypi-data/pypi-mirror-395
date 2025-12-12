# styletext

A Python library providing a `style_text()` function similar to Node.js `util.styleText()`. Style your terminal output with ANSI escape codes using a simple, intuitive API.

## Installation

```bash
uv add styletext
```

Or with pip:
```bash
pip install styletext
```

Or simply copy `styletext.py` to your project - **zero dependencies required**!

## Usage

### Basic Usage

```python
from styletext import style_text

# Single style
print(style_text('red', 'Error message'))
print(style_text('green', 'Success message'))

# Multiple styles
print(style_text(['bold', 'blue'], 'Important text'))
print(style_text(['bgYellow', 'black', 'bold'], 'Warning'))
```

### Chainable API (Bonus)

```python
from styletext import styled

print(styled('Hello World').red.bold)
print(styled('Success!').green.underline)
print(styled('Warning').bgYellow.black)
```

## Available Styles

### Colors
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `gray`/`grey`
- `brightRed`, `brightGreen`, `brightYellow`, `brightBlue`, `brightMagenta`, `brightCyan`, `brightWhite`

### Background Colors
- `bgBlack`, `bgRed`, `bgGreen`, `bgYellow`, `bgBlue`, `bgMagenta`, `bgCyan`, `bgWhite`, `bgGray`/`bgGrey`
- `bgBrightRed`, `bgBrightGreen`, `bgBrightYellow`, `bgBrightBlue`, `bgBrightMagenta`, `bgBrightCyan`, `bgBrightWhite`

### Text Styles
- `bold`, `dim`, `italic`, `underline`, `blink`, `inverse`, `hidden`, `strikethrough`

## Examples

### Log Messages

```python
from styletext import style_text

# Success
print(style_text(['bold', 'green'], '✓') + ' Test passed')

# Error
print(style_text(['bold', 'red'], '✗') + ' Test failed')

# Info
print(style_text(['bgBlue', 'white', 'bold'], ' INFO ') + ' Server started')

# Warning
print(style_text(['bgYellow', 'black', 'bold'], ' WARN ') + ' Deprecated API')

# Error with details
error_msg = (
    style_text(['bold', 'red'], 'Error: ') +
    'Could not find file ' +
    style_text(['italic', 'cyan'], 'config.json')
)
print(error_msg)
```

### Progress Indicators

```python
from styletext import styled

print(styled('⠋').cyan + ' Loading...')
print(styled('⠙').cyan + ' Processing...')
print(styled('✓').green.bold + ' Complete!')
```

## Comparison with Node.js

**Node.js:**
```javascript
import { styleText } from 'node:util';

console.log(styleText('red', 'Error!'));
console.log(styleText(['bold', 'blue'], 'Important'));
```

**Python (this library):**
```python
from styletext import style_text

print(style_text('red', 'Error!'))
print(style_text(['bold', 'blue'], 'Important'))
```

## Requirements

- Python 3.11+
- **Zero external dependencies** - just pure Python and ANSI escape codes!

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
