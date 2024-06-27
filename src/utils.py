import time
import numpy as np


def wait() -> None:
    time.sleep(np.max([np.random.uniform(1, 1.5), np.random.normal(3, 1.5)]))
