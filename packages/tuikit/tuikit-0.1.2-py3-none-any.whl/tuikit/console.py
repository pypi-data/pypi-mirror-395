from .textools import style_text, Align
from . import logictools  
import os

def spacer(times):
    for _ in range(times): print()

def underline(line: str="—", hue: str="", alone=False):
    term_width = logictools.get_term_size(True)
    if alone: print()
    print(style_text(line*term_width, hue))
    if alone: print()

def clear(header=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    if header: print(header)