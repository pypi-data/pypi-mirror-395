from pathlib import Path
import json
import os

ZONES = Path(__file__).resolve().parent/"tzdata"
CONTS = [cont[:-5] for cont in os.listdir(ZONES)]
FILES = [     file for file in os.listdir(ZONES)]

def load(file):
    file_path = ZONES / file
    with open(file_path, "r") as f: return json.load(f)