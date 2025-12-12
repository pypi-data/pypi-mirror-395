from styletext import style_text, styled

# Basic usage - similar to Node.js styleText
print("=== Basic Usage ===")
print(style_text('red', 'This is red text'))
print(style_text('green', 'This is green text'))
print(style_text('blue', 'This is blue text'))

# Multiple styles
print("\n=== Multiple Styles ===")
print(style_text(['bold', 'red'], 'Bold red text'))
print(style_text(['underline', 'cyan'], 'Underlined cyan text'))
print(style_text(['bgYellow', 'black', 'bold'], 'Warning message'))

# All available colors
print("\n=== Colors ===")
colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
for color in colors:
    print(style_text(color, f'{color} text'))

print("\n=== Bright Colors ===")
bright_colors = ['brightRed', 'brightGreen', 'brightYellow', 'brightBlue', 
                 'brightMagenta', 'brightCyan', 'brightWhite']
for color in bright_colors:
    print(style_text(color, f'{color} text'))

# Background colors
print("\n=== Background Colors ===")
print(style_text('bgRed', 'Red background'))
print(style_text('bgGreen', 'Green background'))
print(style_text('bgBlue', 'Blue background'))
print(style_text(['bgYellow', 'black'], 'Yellow background with black text'))

# Text styles
print("\n=== Text Styles ===")
print(style_text('bold', 'Bold text'))
print(style_text('dim', 'Dim text'))
print(style_text('italic', 'Italic text'))
print(style_text('underline', 'Underlined text'))
print(style_text('strikethrough', 'Strikethrough text'))

# Chainable API (bonus feature)
print("\n=== Chainable API (Bonus) ===")
print(styled('Hello World').red.bold)
print(styled('Success!').green.bold)
print(styled('Error!').red.underline)
print(styled('Warning').bgYellow.black.bold)

# Real-world examples
print("\n=== Real-world Examples ===")
print(style_text(['bold', 'green'], '✓') + ' Test passed')
print(style_text(['bold', 'red'], '✗') + ' Test failed')
print(style_text(['bgBlue', 'white', 'bold'], ' INFO ') + ' Application started')
print(style_text(['bgYellow', 'black', 'bold'], ' WARN ') + ' Deprecated function used')
print(style_text(['bgRed', 'white', 'bold'], ' ERROR ') + ' Connection failed')

# Complex styling
print("\n=== Complex Styling ===")
error_msg = (
    style_text(['bold', 'red'], 'Error: ') +
    'Could not find file ' +
    style_text(['italic', 'cyan'], 'config.json')
)
print(error_msg)

success_msg = (
    style_text(['bold', 'green'], '✓ Success: ') +
    'Deployed to ' +
    style_text(['bold', 'blue'], 'production')
)
print(success_msg)
