from datetime import datetime, timedelta, tzinfo
from .exceptions import TimeError, InputError
from .__storage__ import CONTS, FILES, load
from .listools import flatten, list_items
from .console import underline
from .textools import Align

class Timezone():
    def __init__(self, zone: str|int|float = "CAT"):
        """
Initializes a Timezone object with the specified timezone

Args:
    zone: The timezone identifier (default is "CAT").
          Can be an IANA timezone (e.g., "Africa/
          Harare"), an abbreviation (e.g., "CAT") or 
          UTC offset
        

Raises:
    TimeError: If the timezone is not recognized
        """
        self.offset = self.get_offset(zone)
        self.zone = self.ZoneInfo(self.offset)
        self.name = self.zone.tzname(datetime.now())
        self.center = Align().center
        if isinstance(zone, str): self.name = zone

    class ZoneInfo(tzinfo):
        def __init__(self, offset):
            self.offset = timedelta(hours=offset)

        def utcoffset(self, dt): return self.offset

        def dst(self, dt): return timedelta(0)

        def tzname(self, dt):
            total_min = self.offset.total_seconds()/60
            hrs = int(total_min // 60)
            mins = int(abs(total_min) % 60)
            pn = "+" if hrs >= 0 else "-"
            return f"UTC{pn}{abs(hrs):02d}:{mins:02d}"

    def get_offset(self, tz:str|int|float)->int|float:
        def error():
            raise TimeError(cause=tz, required=
                "IANA timezone (e.g., 'Africa/"
                +"Harare'), abbreviation (e.g., 'CAT'"
                +") or UTC offset (e.g., 'UTC+2')")       
        
        if isinstance(tz, (int, float)): 
            if abs(tz) < 24: return tz
            error()
        try: 
            if "/" not in tz:
                tz = load("aliases.json")[tz.upper()]
        except (KeyError, TypeError):
            if tz.startswith("UTC"):
                try: 
                    ofs = float(tz[3:])
                    if abs(ofs) < 24: return ofs
                except ValueError: pass
            error()            
            
        info = tz.split("/")  
        tz = '/'.join(info)
        cont = info[0]
        for tz_cont, file in zip(CONTS, FILES):
            if cont == tz_cont:
                try: return load(file)[tz]
                except KeyError: break
        error()
                                
    def list_zones(self, aliased: bool = False,
              sort: str = "", getter: bool = False):
        """
Lists or returns available timezones or aliases

Args:
    aliased (bool): If True, show alias keys (e.g., 
                    'CAT')
    getter (bool): If True, return list instead of 
                   printing
    sort (str): filter list by continent or 
                abbreviation

Returns:
    list[str] (if getter=True): Sorted list of zones/
                                aliases
        """
        def error():
            raise InputError(cause=sort, required=
                f"filter for {chosen}")
        
        timezones = flatten([
            load(file).keys() for file in FILES if not 
            file.startswith("a")
        ])
        aliases = list(load("aliases.json").keys())
        
        chosen = "aliases" if aliased else "timezones"
        
        try: sort = sort.upper() if aliased else sort
        except AttributeError: error()
        
        temp = aliases if aliased else timezones        
        filt = [s for s in temp if s.startswith(sort)]
        if not filt: error()        
        if getter: return sorted(filt)
        
        header = self.center(f"《 {chosen.upper()} 》", 
                 "—", "magenta", "green")
        
        print(f"\n{header}\n\n")
        list_items(sorted(filt))
        print()
        underline(hue="magenta")
    
    @property
    def now(self) -> datetime:
        """Returns the current datetime in the configured zone"""
        return datetime.now(self.zone)

    def localize(self,*args)->datetime|list[datetime]:
        """
Converts naive or string datetime(s) to this timezone
Supports:
    - A single datetime or ISO string
    - Multiple datetime/ISO arguments
    - A list or tuple of datetime/ISO values
        """
        def error(dt="hapana"):
            if dt != "hapana":
                raise TimeError(cause=dt, required=
                "iso string (YYYY-MM-DD) or datetime"
                +" object")
            raise InputError("At least one datetime"
                +" or ISO string is required")
        
        def local(dt):
            if isinstance(dt, str):
                try: dt = datetime.fromisoformat(dt)
                except ValueError: error(dt)
            elif not isinstance(dt,datetime):error(dt)
            return dt.replace(tzinfo=self.zone) if (
                dt.tzinfo is None) else dt.astimezone(
                self.zone)

        # Handle list/tuple input
        if len(args)==1 and isinstance(args[0], (list, 
          tuple)):return [local(dt) for dt in args[0]]

        # Handle multiple arguments
        elif len(args) > 1:
            return [local(dt) for dt in args]

        # Handle single argument
        elif len(args) == 1: return local(args[0])

        error()

    def convert(self, dt:datetime, to:str)->datetime:
        """Converts a datetime object to a different timezone"""
        try: return dt.astimezone(Timezone(to).zone)
        except AttributeError: 
            req = "datetime object"
            raise TimeError(cause=dt, required=req)

    @property
    def iso_now(self) -> str:
        """Returns ISO string of the current time in this zone"""
        return self.now.isoformat()
    
    def diff_seconds(self, dt1, dt2) -> float:
        """
Returns total seconds difference between two datetimes
Both will be localized to self.zone before subtraction
        """
        dt1, dt2 = self.localize(dt1, dt2)
        return (dt2 - dt1).total_seconds()

if __name__ == "__main__":
    tz = Timezone()
    print(tz.iso_now)
    print(tz.localize(datetime.now().isoformat()))
    print(datetime.now().isoformat())
    tz.list_zones(sort="Africa")
