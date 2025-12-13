"""Utility helpers and shared constants for the python_jsm_asset package.

This module centralizes the package logger and small constants used by
multiple modules to avoid import cycles.
"""

from __future__ import annotations
import logging

# Centralized logger and constants for the package to avoid import cycles.
logging.basicConfig(
    filename='python_jsm_asset.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

attribute_default_types = {
    0: 'Text',
    1: 'Integer',
    2: 'Boolean',
    3: 'Double',
    4: 'Date',
    5: 'Time',
    6: 'DateTime',
    7: 'Url',
    8: 'Email',
    9: 'Textarea',
    10: 'Select',
    11: 'IP Address',
}

JSM_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
