"""
Script for some utility functions.
"""

import time
import numpy as np


MAX_TIME_REQUEST = 30


def wait() -> None:
    """
    Function to wait a random time.
    """

    time.sleep(np.max([np.random.uniform(0.75, 1.5), np.random.normal(2, 1)]))
