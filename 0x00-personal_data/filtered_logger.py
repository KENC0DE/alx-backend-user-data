#!/usr/bin/env python3
"""
Personal data
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """0. Regex-ing:"""
    for fl in fields:
        message = re.sub(f'{fl}=.*?{separator}',
                         f'{fl}={redaction}{separator}', message)
    return message
