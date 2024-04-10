#!/usr/bin/env python3
"""
Personal data
"""
from typing import List
import re


def filter_datum(fld: List[str], rdc: str, msg: str, sep: str) -> str:
    """
    0. Regex-ing:
    """
    for fl in fld:
        msg = re.sub(f'{fl}=.*?{sep}', f'{fl}={rdc}{sep}', msg)

    return msg
