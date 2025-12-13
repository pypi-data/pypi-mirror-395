# -*- coding: utf-8 -*-
# helpers.py

"""
Utility functions
"""

import pandas as pd


def whitespaceCleanup(text):
    try:
        if pd.isnull(text):
            return ""
    except ValueError:
        if all([pd.isnull(elem) for elem in text]):
            return ""
    return " ".join(str(text).split())
