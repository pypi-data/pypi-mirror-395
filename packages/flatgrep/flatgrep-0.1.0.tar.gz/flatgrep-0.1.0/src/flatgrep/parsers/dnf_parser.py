# parsers/dnf_parser.py
import re
from utils.responses import Responses

def parse_dnf_lines(line: str):
    match = re.match(r'^\s*([^\s:]+)', line)
    if match:
        return match.group(1)
    Responses.exitprogram()  

