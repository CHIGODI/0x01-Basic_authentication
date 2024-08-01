#!/usr/bin/env python3
""" Regex-ing """

from typing import List, Tuple
import re
import logging
import os
import mysql.connector
from mysql.connector import Error


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Redacts the specified fields in a given message.
    """
    for field in fields:
        pattern = rf'{field}=[^{separator}]+'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List) -> None:
        """Init"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Redacting formater"""
        original_log = super().format(record)
        redacted_log = filter_datum(self.fields, self.REDACTION,
                                    original_log, self.SEPARATOR)
        return redacted_log


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named "user_data".
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db():
    """"""
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=passwd,
        database=db_name
    )
    return conn
