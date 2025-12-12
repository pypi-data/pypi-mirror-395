"""Custom exceptions module"""
from collections.abc import Iterable
from datetime import datetime as dt
from math import floor, ceil, sqrt
from typing import NoReturn, Any
from . import logictools
import unicodedata
import textwrap
import time
import re

def _notify(msg:str, fg: str|None, bg: str|None, bold:bool, 
            underline:bool, inline:bool, spaced:bool, 
            centered:bool, write: str|bool, 
            _internal:bool) -> str|None|NoReturn:
    """private helper for non-flow-breaking warnings"""
    msg = color(msg, fg, bg, bold, underline)
    centered_msg = color(center(msg), fg, bg, bold)
    if inline: return msg
    if not centered:
        if spaced: msg = f"\n{msg}\n"
    else:
        if not spaced: msg = centered_msg
        else: msg = f"\n{centered_msg}\n"
    
    if not write: print(msg)
    
    if isinstance(write, str) and path.isfile(write):
        with open(write, "a") as file:
            file.write(f"\n{msg}\n")
    elif write and not _internal: 
        warning("Warning! File not found", _internal=True)
    
    return msg
    
def empty(msg:str = "No contents found",
          bg: str|None = None, bold:bool = False,
          inline:bool = False, spaced:bool = True, 
          underline:bool = False, centered:bool = True, 
          write: str|bool = False, 
          _internal:bool = False) -> str | None:
    """Prints a gray colored warning message"""
    return _notify(msg, "gray", bg, bold, underline,
                   inline, spaced, centered, write,
                   _internal)

def warning(msg:str = "Warning!", bg: str|None = None, 
            bold:bool = False, inline:bool = False, 
            spaced:bool = True, underline:bool = False, 
            centered:bool=True, write: str|bool = False,
            _internal:bool = False) -> str | None:
    """Prints a yellow colored warning message"""
    return _notify(msg, "yellow", bg, bold, underline,
                   inline, spaced, centered, write,
                   _internal)
    
def validate(*argtypes, err=None) -> bool|NoReturn:
    """
Input validator

Args:
    argtypes: normally a collect of lists with the inputs
              needing validation. Each list should be
              either like this:
              [input(s), type(s), expected], or
              [input(s), type(s), expected, condition, exp]
              If there are multiple inputs or types, they
              should be in a list.
              <expected> is a string of the input that was
              required.
              <condition>: a string representing comparison
                           operator. The strings are
                           'less' (<), 'eqless' (<=),
                           'equal' (==), 'eqgreat' (>=),
                           'greater (>). They are for
                           comparing inputs against
                           expected input.
              <exp>: Expected [starting/ending] argument.
                     e.g., input 'less' exp (input < exp)
                     checks that the input is less than
                     exp else it throws an error.
    """
    def compare(arg1, against, arg2) -> bool:
        if against ==    "less": return arg1  < arg2
        if against ==  "eqless": return arg1 <= arg2
        if against ==   "equal": return arg1 == arg2
        if against == "eqgreat": return arg1 >= arg2
        if against == "greater": return arg1  > arg2
    
    for argtype in argtypes:
        args  = argtype[0]
        types = flatten(argtype[1], to=tuple)
        req   = argtype[2]
        
        if len(argtype) < 4:
            if isinstance(args, (list, tuple)):
                for arg in args:
                    if not isinstance(arg, types):
                        err(arg, req)
                continue
            
            if not isinstance(args, types): err(args, req)
            continue
                    
        against = argtype[3]
        arg2    = argtype[4]
        if isinstance(args, (str, int, float)):
            if not isinstance(args, types) or compare(
                args, against, arg2): err(args, req)
            continue
        
        for arg in args:
            if not isinstance(arg, types) or compare(
                arg, against, arg2): err(arg, req)
    
def ExitError() -> tuple:
    """function for catching exit-type errors"""
    return (EOFError, KeyboardInterrupt,)

class CUIError(Exception):
    """Base class for all custom CUI exceptions."""
    def __init__(self, msg: str = "An error occurred", 
                 hue: str | None = "red"):
        super().__init__(color(msg, hue))
        self.msg = msg
        self.now = dt.now()

    def display(self, inline: bool = False, 
                centered:bool = False,fg: str|None = "red", 
                bg: str | None = None, bold: bool = False, 
                underline: bool = False) -> None:
        """
Prints the exception message in red, optionally inline, centered, or underlined
        """
        if centered: self.msg = center(self.msg)
        msg = color(self.msg, fg, bg, bold, underline)
        print(msg, end='' if inline else '\n')
    
    @staticmethod
    def mod_error_tag(error:str) -> str:
        return f"tuikit.exceptions.{error}: "
    
    @staticmethod
    def cause_req(msg:str, cause:Any, required:str) -> str:
        def resolve_cause(c:Any) -> str:
            if type(c).__name__ == "function":
                length, c = len(c.__name__), c.__name__
                if length < 8: c = c + "(...)"
                else: c = c[:4] + "...(...)"
            elif "class" in str(c): c = str(c)[8:-2]
            
            if len(str(c)) > 12: c = str(c)[:9]+"..."
            return c
        
        if not any_eq(cause, required, eq='hapana'):
            if cause != 'hapana':
                cuz = resolve_cause(cause)
                type_name = type(cause).__name__
                if type_name == "type": 
                    type_name += " or function"
                if has_unicode(cause): 
                    type_name = "unicode" if len(cuz
                            ) < 2 else f"unicoded str"
                    cuz = preserve_codes(cuz)
                    if len(cuz) > 12: cuz = cuz[:9]+"..."
        
            if not all_eq(cause, required, eq='hapana'):
                msg =(f"'{cuz}' (type: {type_name}) is "
                    + f"not a valid {required}")
            elif cause != 'hapana':
                msg =(f"'{cuz}' (type: {type_name}) is "
                    + "not a valid input")
            else: msg = f"Invalid {required}"
    
        return msg

class Exceptions:
    """Custom exception factory"""
    def __getattr__(self, name):
        class __DynamicError(CUIError):
            def __init__(self, msg:str=f"{name} occurred", 
                         hue: str|None = "red"):
                super().__init__(f"[{name}] {msg}", hue)
        return __DynamicError

class TimeError(CUIError):
    """Raised for time-related errors"""
    def __init__(self, msg: str = "Invalid time format", 
                hue:str|None = "red", cause:Any = 'hapana', 
                required: str = 'hapana'):
        name = self.mod_error_tag("TimeError")
        msg  = self.cause_req(msg, cause, required)
        msg  = wrap_text(msg, list_order=name, inline=True)
        super().__init__(msg, hue)

class ListError(CUIError):
    """Raised for list-related errors"""
    def __init__(self, msg: str = "Invalid list format", 
                hue:str|None = "red", cause:Any = 'hapana', 
                required: str = 'hapana'):
        name = self.mod_error_tag("ListError")
        msg  = self.cause_req(msg, cause, required)
        msg  = wrap_text(msg, list_order=name, inline=True)
        super().__init__(msg, hue)

class InputError(CUIError):
    """Raised for invalid user input"""
    def __init__(self, msg: str = "Invalid input", 
                hue:str|None = "red", cause:Any = 'hapana', 
                required: str = 'hapana'):
        name = self.mod_error_tag("InputError")
        msg  = self.cause_req(msg, cause, required)
        msg  = wrap_text(msg, list_order=name, inline=True)
        super().__init__(msg, hue)



# ——————————————————————《 HELPERS 》———————————————————————

# Helpers are dumped down here to avoid circular
# import errors
# I did not use a utils.py module for these helpers
# as they are core functions of other modules

def any_eq(*args, eq:Any = None) -> bool:
    for arg in args:
        if arg == eq: return True
    return False

def all_eq(*args, eq:Any = None) -> bool:
    for arg in args:
        if arg != eq: return False
    return True

def flatten(data:Iterable, to:type = list) -> list|tuple:
    """
Recursively flattens any iterable (except str/bytes) into a flat list.

Args:
    data (Iterable): Input iterable, possibly nested.
    to (list or tuple): what to return the flattened
                        data as

Returns:
    list/tuple: Flattened version of the iterable.
    data: If input is not an iterable.
    """
    if not isinstance(data, Iterable) or isinstance(
        data, (str, bytes)): return data

    flat = []
    for item in data:
        if isinstance(item, Iterable) and not (
           isinstance(item, (str, bytes))):
           flat.extend(flatten(item))
        else: flat.append(item)
    
    return to(flat)

def strip_ansi(s: str) -> str:
    if not isinstance(s, str): __err__(s, "string") 
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',s)

def visual_width(s: str) -> int:
    clean = strip_ansi(s)
    width = 0
    for ch in clean:
        width += 2 if unicodedata.east_asian_width(ch) in [
                 'F', 'W'] else 1
    return width

def preserve_codes(s: str) -> str:
    codes = {
          "\n": "\\n",
          "\r": "\\r",
          "\t": "\\t",
        "\x1b": "\\x1b",
        "\033": "\\033"
    }
        
    preserved = [ch for ch in s]
    for c, r in codes.items():
        for i, ch in enumerate(preserved):
            if ch == c: preserved[i] = r
                
    return "".join(preserved)

def has_unicode(s: str) -> bool:
    try:      
        for ch in s:
            if isunicode(ch): return True
    except TypeError: return False
    return False

def isunicode(s: str) -> bool:
    return ord(s) in [9, 10, 13, 27]

def underline() -> None:
    term_width = logictools.get_term_width()
    print(color("—"*term_width, "magenta")) 

def color(text, fg: str|None = None, bg: str|None = None, 
          bold:bool = False, underline:bool = False)-> str:
    colors = {
        "black": 30, "red": 31, "green": 32, 
        "yellow": 33, "blue": 34, "magenta": 35,
        "cyan": 36, "white": 37,
        "gray": 90, "lightred": 91, "lightgreen": 92,
        "lightyellow": 93, "purple": 94,
        "lightmagenta": 95, "lightcyan": 96
    }

    if fg and fg not in colors:
        raise InputError(cause=fg)
    
    styles = []
    
    if bold: styles.append("1")
    if underline: styles.append("4")
    if fg in colors: styles.append(str(colors[fg]))
    if bg in colors: styles.append(str(colors[bg]+10))

    if styles: 
        return f"\033[{';'.join(styles)}m{text}\033[0m"
    return text

def center(text, lined:bool = False, doubled:bool = False, 
           line_hue: str|None = None, hue: str|None = None
           ) -> str:
    term_width  = logictools.get_term_size(True)
    display_len = visual_width(text)
    total_pad   = max(term_width - display_len, 0)
    left_pad    = total_pad // 2    
    right_pad   = total_pad - left_pad
    
    if lined or doubled:
        line   = "—" if lined else "="
        left   = color(line *  left_pad, fg=line_hue)
        right  = color(line * right_pad, fg=line_hue)
        middle = color(text, fg=hue)
        return f"{left}{middle}{right}"
    return " " * left_pad + color(text, fg=hue)

def wrap_text(text:str, indent:int = 0, pad:int = 0, 
              inline:bool = False, list_order:str = ''
              ) -> str:
    width = logictools.get_term_size()
    styled_words = text.split()
    
    length   = len(list_order) if inline else 0
    trailing = length / (10 ** len(str(length))
               ) if not inline else 0
    edge = 1 + trailing
    if length > 9 and not inline:
        trailing = length * 2 / 10
    margin = 1 + trailing if length > 9 else edge
    
    line_len = len(list_order)
    result   = list_order if not inline else ""
    if pad:
        result   = " " * (pad-1)
        line_len = pad
    for i, word in enumerate(styled_words):
        used = line_len + visual_width(word)
        if used + margin > width:
            result += '\n' + ' ' * indent + word
            line_len = indent + visual_width(word)
        else:
            result += (' ' if result else '') + word
            line_len += visual_width(
                word) + margin / (2 if margin >= 2 
                else 1)
    
    return result