"""
Module for all list-related tools
"""
from .logictools import format_order, visual_width, any_is
from .exceptions import ListError, ExitError, warning
from collections.abc import KeysView as keys
from .textools import style_text, wrap_text
from collections.abc import Iterable
from typing import Any, Callable
from . import console

def choose(options:dict, cursor:str = ">>> ",
          hue:str = "magenta", getch:bool = False,
          src=None, proxy:bool = False):
    """
Custom input menu for choosing an option from a list

Usage:
  - This function does not list the options.
  - The values of options (dict) should be functions. If
    not, use pick_from(...) instead.
  - Write 'clear' to reset the source screen.
  - This function works best when paired with the 
    function list_items(...)
  - For a real-world usage example of this function,
    check out my CLI app Habitrax on GitHub:
    https://github.com/2kDarki/Habitrax

Args:
    options (dict): A dictionary with functions as values
    cursor   (str): The prompt cursor
    hue      (str): Color of the prompt cursor
    getch   (bool): If true returns the index position of
                    the chosen function rather than calling
                    it. NB: if needed, you can use this
                    flag for options that are lists or
                    non-callable dictionary values to 
                    return their index position then use
                    pick_from(...) to get the value
    src (callable): The name of the function/method where
                    this function was called from. Needed
                    for clearing the screen and recalling
                    where you were
    proxy   (bool): Needed in rare cases where the
                    function/method that called this
                    function was called by another
                    function/method and it needs to know
                    that. See Habitrax for example
    """
    print(f"{format_order(len(options)+1,form=' ')}. Back")
    while True:
        try:
            choice = input(style_text(cursor, hue))
            choice = int(choice) - 1
            if 0 <= choice < len(options):
                if getch: return choice
                elif proxy: pick_from(options, choice)(1)
                else: pick_from(options, choice)()
                break
        except BaseException as e:
            if isinstance(e, ExitError()): 
                if isinstance(e, EOFError): print()
                print(end="\n")
                console.underline(hue=hue)
                return                
            if choice == "clear" and src:
                if proxy:
                    console.clear()
                    src(1)
                    return
                console.clear()
                src()
                return
        if choice == len(options):
            if src:
                print()
                console.underline(hue=hue)
            return
        warning("Choose a number between 1 and "
              +f"{len(options)+1}.")

def pick_from(storage: list|tuple|dict, choice:int,
              index: int | None = None) -> Any:
    """
Takes a dictionary/list/tuple/dict keys and a numeric index

Args:
    storage: A dictionary, list, tuple, or dict keys
    choice: Index position of value needed
    index: If None (default), raises StopIteration when the 
           provided choice is greater than storage's 
           index positions. Otherwise use index as fallback 
           choice
           

Returns:
    - corresponding value
    - rather than throwing
    """
    if choice < 0: choice = len(storage) - abs(choice)
    if isinstance(storage, (list, tuple, keys)):
        return list(storage[choice])
    return next((storage[opt] for pos, opt in
           enumerate(storage) if pos == int(choice)))

def format_items(items:list) -> list:
    """Format items to give out true name"""
    return [item.__name__ if callable(item) else item for
            item in items]

def list_items(items:list, guide: str|None = None,
               style: str|None = "number",
               spaced:bool = False) -> None:
    """
Displays all items in <items> as an ordered list

Args:
    items: A list, tuple or dictionary
    guide: Optional header for the items
    spaced: Adds empty lines between items
    style: Style of the ordered list:
           number, roman, alpha, and bullet
    """
    items = format_items(items)
    deno, indent, sfx, order = 0, 0, "", ""
    styles = ["number", "roman", "alpha", "bullet"]
    if style and style not in styles:
        err(style, f"list order style {tuple(styles)}")
    elif style:
        if styles.index(style) < 3: sfx = "."
        style  = ListOrder(style, suffix=sfx)
        deno   = max((visual_width(style(i+1))-1 for i, x in
                 enumerate(items)))
        deno   = max(2, deno)
        indent = deno + 2

    if guide:
        print(style_text(guide, underline=True)+":")
    for opt, item in enumerate(items):
        if style: order = format_order(style(opt),deno," ")
        print(wrap_text(item, indent, order=order))
        if spaced: print()

def flatten(data:Iterable, to:type = list) -> list|tuple:
    """
Recursively flattens any iterable (except str/bytes) into a flat list or tuple.

Args:
    data (Iterable): Input iterable, possibly nested.
    to (list or tuple): What to return the flattened
                        data as

Returns:
    Flattened version of the iterable.
    data: If input is not an iterable.
    """
    
    if not any_is(list, tuple, eq=to):
        err(to, "function (list or tuple)")
    if not isinstance(data, Iterable) or isinstance(
        data, (str, bytes)): return data

    flat = []
    for item in data:
        if isinstance(item, Iterable) and not (isinstance(
           item, (str, bytes))): flat.extend(flatten(item))
        else: flat.append(item)

    return to(flat)

def normalize(array:list, use:Callable|None = None)-> list:
    normalized = []
    
    for obj in array:
        el = obj
        if use is not None: el = use(obj)
        if el not in normalized: normalized.append(el)
    
    return normalized

class ListOrder:
    """Class for turning an index into a list style"""
    def __init__(self, style:str = "number", prefix:str="",
                 suffix:str = ".", start:int = 1):
        self.style  = style
        self.prefix = prefix
        self.suffix = suffix
        self.start  = start
        self.styles = {
            "number": self._number,
            "roman": self._roman,
            "alpha": self._alpha,
            "bullet": self._bullet
        }

    def format(self, index:int) -> str:
        """Format index to list style"""
        base = self.styles.get(self.style, self._number)(
               index + self.start)
        return f"{self.prefix}{base}{self.suffix}"

    @staticmethod
    def _number(n:int) -> str: return str(n)

    @staticmethod
    def _roman(n: int) -> str:
        """Turn a number into a roman numeral"""
        romans = [
            (1000,'M'), (900,'CM'), (500,'D'), (400,'CD'),
            (100,'C'), (90,'XC'), (50,'L'), (40,'XL'),
            (10,'X'), (9,'IX'), (5,'V'), (4,'IV'), (1,'I')
        ]
        result = ""
        for val, sym in romans:
            while n >= val:
                result += sym
                n -= val
        return result

    @staticmethod
    def _alpha(n: int) -> str:
        """Turn a number into an alpha numeral"""
        # 1 -> A, 2 -> B, ..., 26 -> Z, 27 -> AA
        result = ""
        n -= 1
        while n >= 0:
            result = chr(n % 26 + 65) + result
            n = n // 26 - 1
        return result

    @staticmethod
    def _bullet(_) -> str:  return "•"

    def __call__(self, index):
        return self.format(index)

def err(cause, required):
    """Helper for raising list-related errors"""
    raise ListError(cause=cause, required=required)
