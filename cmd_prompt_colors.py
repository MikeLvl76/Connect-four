colors = {
    'GRAY': '\033[90m',
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'PURPLE': '\033[95m',
    'CYAN': '\033[96m',
    'ENDC': '\033[0m'
}

def color_string(color: str, string: str) -> str:
    color_value = colors.get(color)
    if not color_value:
        return string
    return f"{color_value}{string}{colors.get('ENDC')}"