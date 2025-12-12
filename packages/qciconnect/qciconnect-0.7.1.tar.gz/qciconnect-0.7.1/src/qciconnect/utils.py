"""Provides utility functions for the qciconnect package."""
import datetime
import json
from pathlib import Path


def timestamp_to_datetime(timestamp):
    """Converts a timestamp string to a datetime object.

    Args:
       timestamp (str): The timestamp string in the format "%Y-%m-%dT%H:%M:%S.%f"
    """
    try:
        result = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        result = timestamp
    return result


def read_json(file_path):
    """Reads a JSON file and returns the data."""
    with Path.open(file_path) as fp:
        return json.load(fp)
