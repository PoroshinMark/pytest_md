import time

import pytest
import pytest_md


def test_example_1(metrics, extras):
    metrics.append(("accuracy", 0.95))
    metrics.append(("loss", 0.05))
    time.sleep(2)
    assert True
