from colorama import Fore, Style

def colorize(text, fore):
    return fore + text + Fore.WHITE

def dim(text):
    return Style.BRIGHT + text + Style.NORMAL