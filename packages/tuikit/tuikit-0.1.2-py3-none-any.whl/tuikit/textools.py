from .exceptions import validate, InputError
from typing import Any, NoReturn
from . import logictools
import unicodedata
import textwrap
import time
import re
import os

class Align:
    def right(self, arg:str) -> str:
        try: return wrap_text(arg.strip())
        except AttributeError: err(arg, "string")
    
    def center(self, arg:Any, line:str = " ", 
               hue:str|None = None, 
               line_hue:str|None = None, pad:int = 0, 
               get_pad: bool = False) -> str | tuple:
        # Validate parameters
        validate([line, str, "string"],
                 [pad, int, "natural number", "less", 0],
                 err=err)
        
        arg = str(arg)
        
        term_width = logictools.get_term_size(69) # ;)
        vis_width  = logictools.visual_width(arg)
    
        total_pad = max(term_width - vis_width, 0)
        left_pad  = total_pad // 2
        right_pad = total_pad - left_pad
    
        if get_pad:
            return left_pad, total_pad, right_pad

        left   = style_text(line *  left_pad, line_hue)
        right  = style_text(line * right_pad, line_hue)
        middle = style_text(arg, hue)
        
        if len(arg) > term_width:
            if pad: total_pad += pad * 2
            return wrap_text(middle, from_center=[hue, 
                   line, line_hue, total_pad]) 
        
        return f"{left}{middle}{right}"
    
    def left(self, arg, pad: int = 4) -> str:
        validate([pad, int,  "natural number", "less", 0],
                 err=err)
        return wrap_text(str(arg), pad, pad)

def keep_split(text:str, sep=" "):
    parts = text.split(sep)
    if len(parts) < 2: return parts
    elif len(parts) == 2:
        if parts[1] == "": return [parts[0]+sep]
        else: return [parts[0]+sep, parts[1]]
    if parts[-1] == "":
        parts[-2] += sep
        parts = parts[:-1]
    
    final = []
    for i, part in enumerate(parts):
        if not part.endswith(sep):
            if i != len(parts) - 1: part += sep
        final.append(part)
    return final

def transmit(*msg:str, speed: int|float = 0.1,
             hold: int|float = 0.3,
             hue: str|None = None,
             inline:bool = False, inlined=None) -> None|str:
    validate([[speed, hold], [int, float], 
             "positive number", "less", 0], err=err)

    if len(msg) == 1: msg = str(msg[0])
    else: msg = " ".join([str(p) for p in msg])
    
    paragraphs = msg.split("\n\n")
    text       = ""
    para_len   = len(paragraphs)
    for pi, paragraph in enumerate(paragraphs):
        lines = paragraph.split("\n")
        for li, line in enumerate(lines):
            styled_words = keep_split(line, "[0m")
            sentence     = ""
            for word in styled_words:
                styled_word = style_text(word, hue)
                sentence += styled_word
            if not inlined: sentence = wrap_text(sentence)
            else: sentence = wrap_text(sentence, *inlined)
            if inline: 
                text += sentence
                if li != len(lines) - 1: text += "\n"
                continue
            for ch in sentence:
                delay = speed
                if ch == " ": delay = hold
                if logictools.any_in(ch, 
                    eq=["[", "0", "m"]): delay = 0
                print(ch, end="", flush=True)
                time.sleep(delay)
            if len(lines) > 1 and li != len(lines) - 1: 
                print()
        
        if inline: 
            if pi != len(paragraphs) - 1: text += "\n\n"
        elif para_len > 1 and pi != para_len-1: print()
    
    if inline: return text
    if len(paragraphs) == 1: print()

def strip_ansi(s:str) -> str:
    if not isinstance(s, str): err(s, "string") 
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)

def visual_width(s:Any) -> int:
    clean = strip_ansi(str(s))
    width = 0
    for ch in clean:
        width += 2 if unicodedata.east_asian_width(
                 ch) in ['F', 'W'] else 1
    return width

def pluralize(n: int|float, word:str) -> str:
    # Validate parameters
    validate([n, [int, float], "integer or float"],err=err)
    strip_ansi(word) # relegating validation
    
    if n == 1: return word
    else:
        if word.endswith('y') and len(word) > 3: 
            return word[:-1]+"ies"
        return word + 's'

def styled(text:str, get:bool = False) -> bool|list:
    def append(hues:list, array:list) -> list:
        for i, hue in enumerate(hues):
            if hue in codes: array.append(hues[i])
        return array
    
    validate([text, str, "string"], err=err)
    if not logictools.any_in("\033", "\x1b[", eq=text): 
        return False if not get else []
    if not get: return True
    if logictools.any_eq("\033", "\x1b[", eq=text): 
        return []
    
    chars = text.split()
    try: start = chars.index("[") + 1
    except ValueError: return []
    end   = chars.index("m")
    parts = [p for p in chars[start: end]]
    codes = "".join(parts).split(";")
    codes = [int(c) if len(c) == 2 else c for c in codes]
    
    bold      = "1"
    underline = "4"
    fgs       = [n for n in range(30, 38)]
    bgs       = [n for n in range(90, 97)]
    
    styles = []
    if bold in codes: styles.append(bold)
    if underline in codes: styles.append(underline)
    styles = append(fgs, styles)
    return   append(bgs, styles)

def style_text(text, fg: str = "", bg: str = "",
               underline: bool = False,
               bold: bool = False) -> str:
    def append(array:list, _type:str="fg") -> list:
        try:
            start, end = 30, 38
            if _type == "bg": start, end = 90, 97
            for n in range(start, end):
                if n in styles: array.append(str(n))
            return array
        except TypeError: return array
       
    validate([[underline, bold], bool, "boolean"], err=err)
    
    special = "\n" in str(text)
    clean  = strip_ansi(str(text))
    style  = []
    styles = styled(str(text), get=True)
    if not styles: clean = str(text)
    colors = {
        "black": 30, "red": 31, "green": 32, 
        "yellow": 33, "blue": 34, "magenta": 35,
        "cyan": 36, "white": 37,
        "gray": 90, "lightred": 91, "lightgreen": 92,
        "lightyellow": 93, "purple": 94,
        "lightmagenta": 95, "lightcyan": 96
    }

    for c in [fg, bg]:
        if c and c not in colors: err(c, "color")
    
    if special: 
        return transmit(str(text), hue=fg, inline=True)
    
    if bold or "1" in styles: style.append("1")
    if underline or "4" in styles: style.append("4")
    if fg: style.append(str(colors[fg]))
    else: style = append(style)
    if bg: style.append(str(colors[bg] + 10))
    else: style = append(style, "bg")
    
    if style:
        return f"\033[{';'.join(style)}m{clean}\033[0m"
    return clean

def iswhitespace(text:str) -> bool:
    for ch in text:
        if ch != " ": return False
    return True

def flatten(text: str):
    words = text.split()
    return " ".join(words)

def wrap_text(text: str, 
              indent: int = 0, 
              pad: int = 0, 
              inline: bool = False, 
              order: str = '', 
              from_center: list = [],
              _internal: bool = False
) -> str:
    # Validate parameters
    validate(
      [order, str, "string"],
      [[indent, pad], int, "natural number","less",0],
      [[inline, _internal], bool, "boolean"],
      [from_center, list, "list"], err=err)
    
    width = logictools.get_term_size()
    if not text: return ""
    if isinstance(text, str) and "\n" in text:
        args = [indent, pad, inline, order]
        return transmit(text, inline=True, inlined=args)
    if _internal:
        if isinstance(text, list):
            styled_words   = text[0].split()
            rest           = text[1:]
        else:
            text  = str(text)
            styled_words = text.split()
    else:
        text = str(text)
        styled_words = text.split()
        lines = text.split("\n")
        if len(lines) > 1:
            _internal    = True
            styled_words = lines[0].split()
            rest         = lines[1:]
    
    if from_center:
        h, l, lh, total_pad = from_center
        width -= total_pad
        centered, res = "", ""
        pos = 0
    
    # Adjust margin based on length of order
    # order is a tag for an ordered list (e.g., 1., a., 
    # IV., 10. etc)
    length = visual_width(order)
    margin = 1
    
    # Insert line breaks
    line_len = visual_width(order)
    result = order if not inline else ""
    
    if pad:
        if not inline: result = " " * pad
        if isinstance(text, str):
            text = " " * pad + text
        line_len = pad
    
    if isinstance(text, str):
        if visual_width(text) <= width and not order:
            return text

    for i, word in enumerate(styled_words):
        used = line_len + visual_width(word)
        if used + margin > width:
            first_line = False
            if from_center:
                text = " ".join(styled_words[pos:i])
                centered += align.center(text.strip(), 
                    line=l, hue=h, line_hue=lh) + "\n"
                pos = i
                res = word
            else: result += '\n' + ' ' * indent + word
            line_len = indent + visual_width(word)
        else:
            if iswhitespace(result): result += '' + word
            else: result += (' ' if result else '') + word
            if from_center: res += ' ' + word
            line_len += visual_width(word) + margin
    
    if _internal:
        rest = wrap_text(rest, indent, pad, inline, 
               order, from_center, _internal)
        result += f"\n{rest}" if rest else rest
    if not from_center: return result
    return centered + align.center(res, l, h, lh)

def pathit(path_str: str) -> str:
    """Abbreviates a path if it becomes too long"""
    if not path_str: return path_str
    path_str = str(path_str)
    prefix   = f"{os.sep}...{os.sep}"
    cwd      = path_str
    if len(cwd.split(os.sep)) < 3: return cwd
    return prefix + os.sep.join(cwd.split(os.sep)[-2:])

def to_list(array: list) -> str:
    if not isinstance(array, list): err(array, "list")
    text = ""   
    for i, item in enumerate(array):
        pfx   = f"     {i+1}. "
        i     = len(pfx) + 1
        end   = "\n" if i < len(array) - 1 else ""
        text += pfx + wrap_text(f"{item}{end}", i, 
                inline=True, order=pfx)    
    return text

def has_unicode(s:str) -> bool:
    strip_ansi(s)
    for ch in s:
        if isunicode(ch): return True
    return False

def isunicode(s:str) -> bool:
    strip_ansi(s)
    return ord(s) in [9, 10, 13, 27]

def preserve_codes(s:str) -> str:
    strip_ansi(s)
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

def label(iterable: list|tuple|dict, hue:str = "cyan",
          ordered: bool = False) -> list[str]:
    if ordered: return [color(f"{i+1}. {head}", hue) 
                for i, head in enumerate(iterable)]
    return [style_text(head, fg=hue) for head in iterable]

def iter_print(text, times: int, end: str = "\n", 
               delay: int|float = 0):
    
    validate(
        [times, int, "positive integer", "eqless", 0],
        [end, str, "string"],
        [delay, [int, float], "natural number", "less", 0],
        err=err)
    
    for _ in range(times):
        time.sleep(delay)
        print(text, end=end, flush=True)

def pad_args(*args) -> list[str]:
    return [str(n).zfill(2) for n in args]
    
def err(cause:Any, required: str) -> NoReturn:
    raise InputError(cause=cause, required=required)
 