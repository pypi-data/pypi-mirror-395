# TUI-Toolkit

A compact set of terminal-focused utilities: console helpers, text processing, list tools, logic evaluators, and timezone utilities backed by bundled JSON tzdata.

Designed as a library, not a framework. No global state, no magic, no TUI “engine”—just focused primitives.

---

## Installation

```bash
pip install tuikit
```

---

## Features

### Console Utilities

Structured terminal output helpers:
1. clearing screen
2. seperating screen
3. spacing


### Text Tools

Simple but practical utilities:
1. wrapping
2. alignment
3. tokenization helpers


### List Tools

Operations on sequences:
1. flattening
2. grouping
3. chunking
4. transformations

### Logic Tools

Small logic helpers:
1. truth checks
2. implication evaluation
3. safe comparisons

### Time & Zone Tools

Timezone-aware utilities using packaged JSON tzdata:
1. Africa, America, Asia, Europe, Pacific, Australia
2. zone alias resolution
3. offset lookup
4. conversions
5. formating to fuzzy human-readable

---

## Quick Start

1. Console
```
from tuikit.console import clear

print("Hello World")
clear(sleep=2) # clears screen after 2 seconds
```

2. Lists
```
from tuikit.listools import flatten

nested = [1, [2, 3, [4, 5, 6], [7], 8], [9]]
flat = flatten(nested)

```Text
from tuikit.textools import wrap

print(wrap("Long text here...", width=40))
```

3. Logic
```
from tuikit.logictools import any_in

nested = [1, [2, 3, [4, 5, 6], [7], 8], [9]]
a_list = ["Hello", "World", "by Darki", 2, 5]

if any_in(a_list, eq=nested):
    print("Hell yeah!")
```

4. Time & Zones
```
from tuikit.zonetools import Timezone
from tuikit.timetools import timestamp
from datetime import datetime

zone = Timezone("Africa/Harare")
print(zone.offset)

now = datetime.now().isoformat()
print(timestamp(now))
```

---

## Package Structure

tuikit/
  console.py
  exceptions.py
  listools.py
  logictools.py
  textools.py
  timetools.py
  zonetools.py
  tzdata/
    Africa.json
    America.json
    ...
    
---

## Why This Exists

Most libraries either:
1. force a full TUI framework,
2. over-abstract simple tasks,
3. or hide logic behind globals.

This toolkit does the opposite:
1. explicit imports
2. predictable functions
3. small focused modules
4. timezone data bundled locally

---

License

MIT. See [LICENSE](LICENSE) for more details.
