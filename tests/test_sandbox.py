import time

import pytest
import pytest_md


def test_example_1(extras):
    extras.append('Hello')
    extras.append('1')
    time.sleep(3)
    assert True


def test_example_2(extras):
    extras.append('Hello')
    extras.append('2')
    assert True
