# parsers/flathub_parser.py
import re
from utils.responses import Responses

def parse_flathub_lines(line):
    parts = re.split(r'\t+', line)
    if len(parts) > 2:
        return parts[2]
    else:
        Responses.exitprogram()

def parse_local_flatpaks_lines(line):
    parts = re.split(r'\t+', line)
    if len(parts) > 2:
        return parts[1]
    else:
        Responses.exitprogram()

