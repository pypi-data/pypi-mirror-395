from typing import Union, List
from enum import Enum


class Color(str, Enum):
    """ANSI color codes"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class BgColor(str, Enum):
    """ANSI background color codes"""
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_GRAY = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'


class Style(str, Enum):
    """ANSI style codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'


# Style mappings for easy access
STYLES = {
    # Colors
    'black': Color.BLACK,
    'red': Color.RED,
    'green': Color.GREEN,
    'yellow': Color.YELLOW,
    'blue': Color.BLUE,
    'magenta': Color.MAGENTA,
    'cyan': Color.CYAN,
    'white': Color.WHITE,
    'gray': Color.GRAY,
    'grey': Color.GRAY,
    'brightRed': Color.BRIGHT_RED,
    'brightGreen': Color.BRIGHT_GREEN,
    'brightYellow': Color.BRIGHT_YELLOW,
    'brightBlue': Color.BRIGHT_BLUE,
    'brightMagenta': Color.BRIGHT_MAGENTA,
    'brightCyan': Color.BRIGHT_CYAN,
    'brightWhite': Color.BRIGHT_WHITE,
    
    # Background colors
    'bgBlack': BgColor.BG_BLACK,
    'bgRed': BgColor.BG_RED,
    'bgGreen': BgColor.BG_GREEN,
    'bgYellow': BgColor.BG_YELLOW,
    'bgBlue': BgColor.BG_BLUE,
    'bgMagenta': BgColor.BG_MAGENTA,
    'bgCyan': BgColor.BG_CYAN,
    'bgWhite': BgColor.BG_WHITE,
    'bgGray': BgColor.BG_GRAY,
    'bgGrey': BgColor.BG_GRAY,
    'bgBrightRed': BgColor.BG_BRIGHT_RED,
    'bgBrightGreen': BgColor.BG_BRIGHT_GREEN,
    'bgBrightYellow': BgColor.BG_BRIGHT_YELLOW,
    'bgBrightBlue': BgColor.BG_BRIGHT_BLUE,
    'bgBrightMagenta': BgColor.BG_BRIGHT_MAGENTA,
    'bgBrightCyan': BgColor.BG_BRIGHT_CYAN,
    'bgBrightWhite': BgColor.BG_BRIGHT_WHITE,
    
    # Styles
    'bold': Style.BOLD,
    'dim': Style.DIM,
    'italic': Style.ITALIC,
    'underline': Style.UNDERLINE,
    'blink': Style.BLINK,
    'inverse': Style.INVERSE,
    'hidden': Style.HIDDEN,
    'strikethrough': Style.STRIKETHROUGH,
}


def style_text(format: Union[str, List[str]], text: str) -> str:
    """
    Style text with ANSI escape codes, similar to Node.js util.styleText
    
    Args:
        format: A style name (string) or list of style names
        text: The text to style
        
    Returns:
        Styled text with ANSI codes
        
    Example:
        >>> style_text('red', 'Error!')
        >>> style_text(['bold', 'blue'], 'Important')
        >>> style_text(['bgYellow', 'black', 'bold'], 'Warning')
    """
    if isinstance(format, str):
        format = [format]
    
    codes = []
    for style_name in format:
        if style_name in STYLES:
            codes.append(STYLES[style_name])
        else:
            raise ValueError(f"Unknown style: {style_name}")
    
    if not codes:
        return text
    
    styled = ''.join(codes) + text + Style.RESET.value
    return styled


# Convenience function for chaining
class StyledText:
    """Chainable text styling"""
    
    def __init__(self, text: str):
        self.text = text
        self.styles = []
    
    def __getattr__(self, name: str):
        if name in STYLES:
            self.styles.append(name)
            return self
        raise AttributeError(f"Unknown style: {name}")
    
    def __str__(self):
        return style_text(self.styles, self.text)
    
    def __repr__(self):
        return self.__str__()


def styled(text: str) -> StyledText:
    """
    Create a chainable styled text object
    
    Example:
        >>> print(styled('Hello').red.bold)
        >>> print(styled('Warning').bgYellow.black)
    """
    return StyledText(text)
