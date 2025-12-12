from .__const__ import EIGHTEENTH, UNITTHRESH
from .textools import pluralize, style_text
from .logictools import shave, format_order
from .exceptions import warning, TimeError
from typing import NoReturn, Any
from .textools import wrap_text
from datetime import datetime
from .console import clear
from math import inf

def format_time(time: int|float, set_to:str = "second", 
                hue:str|None = None, tense:str|None = None, 
                precise:bool = True, faulty:bool = True,
                only=False) -> str:
    """
Returns a fuzzy human-readable time string

Args:
       time: a positive or negative number.
             If negative, it gives out a string like
             "24 minutes and 30 seconds ago". Else it
             returns "24 minutes and 30 seconds"
     set_to: specify what order the argument 'time' 
             is in. <time=1, set_to='hour'> is greater
             than <time=56, set_to='second'>.
             Default=second
        hue: the color of the returned string
      tense: temporal reference ('future' or 'past').
             if 'future': returns "in 2 minutes"
             if 'past': returns "2 minutes ago"
             if None: returns "2 minutes"
    precise: whether or not to return the time string
             down to the second. E.g., if precise=True
             it returns "55 years, 9 months, 2 weeks, 
             3 days, 14 hours, 37 minutes and 41 
             seconds". Else returns "55 years and 9 
             months"
     faulty: used when the time is greater than a month.
             The conversion used are faulty by default
             (1 month ≠ 4 weeks) so it is used for 
             corrections. You can leave it as-is (it 
             just takes a few milliseconds longer to
             format the time)
    """
    if set_to not in UNITTHRESH:
        err(set_to, "period of time")
 
    try: past = time < 0
    except TypeError: err(time, set_to)
    
    if tense and tense not in ["future", "past"]:
        err(tense, 
            "temporal reference ('future' or 'past')")
    
    if past: 
        time  = abs(time)
        tense = "past"
    
    units = list(UNITTHRESH.keys())     
    for unit in units[:units.index(set_to)]:
        time *= UNITTHRESH[unit]

    if faulty: time = get_time_lapsed(time, num=True)
    if not precise and time > 60:
        return style_text(time_lapsed(time, tense=tense), 
               hue)
        
    def get_timeunits(time) -> list[list[int|float, str]]:
        timeunits = []
        limits    = [UNITTHRESH[u] for u in units]

        for limit, unit in zip(limits, units):
            if only:
                if unit == set_to:
                    timeunits.append([time, unit])
                    if len(timeunits) > 1:
                        timeunits = timeunits[1:]
                    break
            if time >= limit:
                time = round(time)
                shaved, time = shave(time, limit)
                timeunits.append([shaved, unit])
            else:
                timeunits.append([time, unit])
                break

        return timeunits
        
    timeunits = get_timeunits(time)
    for i, timeunit in enumerate(timeunits):
        time, unit = timeunit
        unit = pluralize(time, unit)
        timeunits[i] = [time, unit]
    
    return style_text(format_time_string(timeunits[::-1], 
           tense=tense), fg=hue)

def convert(time:str, to:str = "hours") -> int | float:
    """
Takes a 24-hour notation time string (e.g., "23:45")
Converts the time string to the specified unit:
    if to = hours: returns 23.75
    if to = minutes: returns 1425
    if to = seconds: returns 85500

The time string should be in one of these 3 formats:
    1. hh
    2. hh:mm
    3. hh:mm:ss
    """   
    units, limits = get_unit_limits(plural=True)
    try:
        parts = [int(part) for part in time.split(":")][:3]
        for part, limit, unit in zip(parts, limits[::-1], 
                                             units[::-1]):
            if part not in range(limit):
                xrange = "is below minimum" if (part 
                       < 0) else "exceeds maximum"
                raise TimeError(f"{part!r} {xrange}"
                      +f" value allowed for {unit}")
    except (AttributeError, ValueError):
        err(time, "time string (hh, hh:mm or hh:mm:ss)")
    
    length = 0        
    for i, part in enumerate(parts):
        length += part / 60**i
    
    for pos, unit in enumerate(units[::-1]):
        if to == unit: return length * (60**pos)
    
    err(to, "unit (hours, minutes or seconds)")

def timestamp(iso_str:str|datetime, date_only:bool = False, 
              short:bool = False, mini:bool = False)-> str:
    """
Converts ISO timestamp into a human-readable string.

Args:
    iso_str: ISO 8601 datetime string or object.
    date_only (bool): If True, omits time (returns date only).
    short (bool): If True, returns compact date (e.g., "14 Sep 2025").
    mini (bool): If True, returns compact date (e.g., "2025/09/14")

Returns:
    str: Formatted timestamp string.
    """
    try: iso_str = to_iso(iso_str)
    except TimeError: pass
    
    try: dt_obj = datetime.fromisoformat(iso_str)
    except (ValueError, TypeError):
        err(iso_str, 
           "iso string (YYYY-MM-DD) or datetime object")
                        
    if mini: return dt_obj.strftime("%Y/%m/%d")
    elif short: return dt_obj.strftime("%d %b %Y")
    elif date_only: return dt_obj.strftime("%A, %d %B %Y")
    return dt_obj.strftime("%A, %d %B %Y • %H:%M")

def time_lapsed(last:int|float, now:int|float|None = None, 
                tense:str|None = "past") -> str:
    """
Returns a fuzzy human-readable time difference
string (e.g., "3 hours and 12 minutes ago").
    """
    if tense and tense not in ["future", "past"]:
        err(tense, "temporal reference")
    
    def get_lapsed(last:int|float, now:int|float|None=None
                  ) -> tuple[str, int|float]:
        lapsed = last
        if now: lapsed = now - last
        s = pluralize(lapsed, "second")
        string = f"{int(lapsed)} {s} ago"
        return string, lapsed

    s, lapsed = get_lapsed(last, now) if now \
           else get_lapsed(last)
 
    # Checks if user has tempered with device date
    tempered = lapsed < -5
  
    if -5 <= lapsed < 1: return "Just now"
  
    # Thresholds for escalation to next unit
    units, limits = get_unit_limits("year")
    prv_unit      = "second"
    for unit, limit in zip(units[1:], limits[:-1]):
        if lapsed >= limit:
            s, lapsed = format_unit(lapsed, limit, unit,
                        prv_unit, tense)
            prv_unit  = unit
        else: break

    return s if not tempered else warning(
        'Tempered with device date', inline=True)

def format_time_string(*args, tense:str|None=None) -> str:
    def tensed(body:str) -> str:
        head = "in "  if tense == "future" else ""
        tail = " ago" if tense ==   "past" else ""
        return f"{head}{body}{tail}"

    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]

    parts = []
    try:
        parts = [f"{unit[0]} {unit[1]}" for unit in args if
                    unit[0] != 0]
    except TypeError: 
        if args[0] != 0: parts = [f"{args[0]} {args[1]}"]
    
    if len(parts) > 1: return tensed(', '.join(parts[:-1])
                            + f" and {parts[-1]}")
    elif len(parts) == 1: return tensed(parts[0])
    else: return "just now"

def format_unit(lapsed:int|float, unit:int,
                major_label:str, minor_label:str, 
                tense:str|None = None) -> tuple[str, int]:
    major = int(lapsed / unit)
    minor = round(lapsed - major * unit)
    major_str = pluralize(major, major_label)
    minor_str = pluralize(minor, minor_label)
    return format_time_string([major, major_str],[minor, 
           minor_str], tense=tense), major
        
def get_time_lapsed(iso_str:str, fuzzy:bool = True, 
                    num:bool = False, 
                    _fixed:str|None=None) -> str|int|float:
    try: before = datetime.fromisoformat(iso_str)
    except (TypeError, ValueError):
        if num: pass
        else: err(iso_str, "iso string (YYYY-MM-DD)")
              
    now   = EIGHTEENTH if _fixed else datetime.now()
    years = 0
    if not num:
        diff   = now - before
        years  = int(diff.days / 365)
        lapsed = diff.total_seconds()
    else:
        years  = int(iso_str / 60 / 60 / 24 / 365)
        lapsed = iso_str
        fuzzy  = False
    if years: lapsed -= lapsed - 29030400 * years
    return time_lapsed(lapsed) if fuzzy else lapsed

def to_iso(iso_str:str) -> str:
    if isinstance(iso_str, datetime): 
        return iso_str.isoformat()
    try:
        timestamp = datetime.fromisoformat(iso_str)
        return timestamp.isoformat()
    except (ValueError, TypeError):
        err(iso_str, "iso string (YYYY-MM-DD)")

def get_age(b_day:str, years:bool = True, 
            _fixed:bool = False) -> int|str:
    try: b_day = datetime.fromisoformat(b_day)
    except (ValueError, TypeError):
        err(b_day, "iso string (YYYY-MM-DD)")
    
    today = EIGHTEENTH if _fixed else datetime.now()
    if years: return int((today - b_day).days / 365)
    lapsed = get_time_lapsed(to_iso(b_day),0,_fixed=_fixed)
    return format_time(lapsed, "second", faulty=False)
    
def get_unit_limits(upto:str = "hour", plural:bool = False
                   ) -> tuple[str, int]:
    if upto not in UNITTHRESH.keys():
        err(upto, "unit of time")
    
    units, limits = [], []
    for unit, limit in UNITTHRESH.items():
        u = pluralize(0, unit) if plural else unit
        units.append(u)
        limits.append(limit)
        if unit == upto: return units, limits

def clock(time: str|int|float, notation:str = "24", 
          meridiem: str|None = None) -> str:
    try: time = float(time)
    except ValueError: err(time, "number") 
    
    if notation != "24":
        if notation == "12":
            am = ["am", "a.m", "a.m."]
            pm = ["pm", "p.m", "p.m."]
            if meridiem and meridiem in am + pm:
                if meridiem in pm: time += 12
            else: err(meridiem, "meridiem (a.m or p.m)")
        else: err(notation,"hour notation (12 or 24)")
        
    hours   = int(time)
    minutes = float(round((time - hours) * 60, 7))
    seconds = int(round((minutes - int(minutes)) * 60, 7))
    
    times = [hours, minutes, seconds]
    units, limits = get_unit_limits(plural=1)
    unitlimits = list(zip(units, limits))[::-1]
    for time, (unit, limit) in zip(times, unitlimits):
        if int(time) not in range(limit):
            xrange = "is below minimum" if time < 0 \
                else "exceeds maximum"            
            raise TimeError(f"{time!r} {xrange} value "
                          + f"allowed for {unit}")
    
    hrs  = format_order(hours)
    mins = format_order(int(minutes))
    sec  = format_order(seconds)
    
    if seconds: return f"{hrs}:{mins}:{sec}"
    return f"{hrs}:{mins}"

def err(cause:Any, required:str) -> NoReturn:
    raise TimeError(cause=cause, required=required)
