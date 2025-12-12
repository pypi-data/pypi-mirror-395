import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from oddoreven.checker import is_even, is_odd

def test_is_even():
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_even(0) is True

def test_is_odd():
    assert is_odd(3) is True
    assert is_odd(2) is False
    assert is_odd(1) is True
