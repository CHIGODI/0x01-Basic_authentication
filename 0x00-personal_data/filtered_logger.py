#!/usr/bin/env python3
""" Regex-ing """

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Redacts the specified fields in a given message.
    """
    for field in fields:
        pattern = rf'{field}=[^{separator}]+'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
