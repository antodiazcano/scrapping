import time
import numpy as np


def wait() -> None:
    time.sleep(np.max([np.random.uniform(0.75, 1.5), np.random.normal(2, 1)]))
