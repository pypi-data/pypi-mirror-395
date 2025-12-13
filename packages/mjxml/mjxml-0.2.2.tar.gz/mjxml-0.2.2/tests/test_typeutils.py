from typing import Literal
import numpy as np

import mjxml.typeutils as typeutils


def test_eps():
    assert typeutils.EPS == float(np.finfo(np.float32).eps)


def test_str_protocol():
    # builtin str should satisfy the protocol
    assert isinstance("hello", typeutils.Str)

    class S:
        def __str__(self) -> str:  # pragma: no cover - trivial
            return "x"

    assert isinstance(S(), typeutils.Str)


def test_natural_and_strict_natural():
    assert isinstance(0, typeutils.Natural)
    assert isinstance(5, typeutils.Natural)
    assert not isinstance(-1, typeutils.Natural)

    assert not isinstance(0, typeutils.StrictNatural)
    assert isinstance(1, typeutils.StrictNatural)


def test_arraylike_with_length_and_type():
    Int3 = typeutils.ArrayLike[int, Literal[3]]
    assert isinstance([1, 2, 3], Int3)
    assert not isinstance([1, 2], Int3)
    assert not isinstance([1, 2, "3"], Int3)

    IntAny = typeutils.ArrayLike[int]
    assert isinstance([0, 1, 2, 3], IntAny)
    assert not isinstance([0, 1, "2"], IntAny)


def test_arraylike_tuple_length_options():
    IntLen2or4 = typeutils.ArrayLike[int, Literal[2, 4]]
    assert isinstance([1, 2], IntLen2or4)
    assert isinstance([1, 2, 3, 4], IntLen2or4)
    assert not isinstance([1], IntLen2or4)


def test_compare_none():
    assert typeutils.compare(None, None) is True
    assert typeutils.compare(None, [1]) is False
    assert typeutils.compare([1], None) is False


def test_compare_length_mismatch():
    assert typeutils.compare([1], [1, 2]) is False
    assert typeutils.compare([1, 2], [1]) is False


def test_compare_integers():
    assert typeutils.compare([1, 2, 3], [1, 2, 3]) is True
    assert typeutils.compare([1, 2, 3], [1, 2, 4]) is False


def test_compare_strings():
    assert typeutils.compare(["a", "b"], ["a", "b"]) is True
    assert typeutils.compare(["a", "b"], ["a", "c"]) is False


def test_compare_floats_exact():
    # Since the current implementation likely falls through to strict equality
    # because T1 is not SupportsFloat at runtime, these should pass if exact.
    assert typeutils.compare([1.0, 2.0], [1.0, 2.0]) is True
    assert typeutils.compare([1.0], [1.1]) is False


def test_compare_floats_epsilon():
    # Test epsilon comparison for floats
    val = 1.0
    # A difference smaller than EPS should be considered equal
    # EPS is derived from 32bit floats, so a smaller difference is possible.
    small_diff = val + typeutils.EPS * 0.5
    
    assert typeutils.compare([val], [small_diff]) is True

    # A difference larger than EPS should be considered unequal
    large_diff = val + typeutils.EPS * 2.0
    assert typeutils.compare([val], [large_diff]) is False

def test_floatarr_to_string():
    # Test with integers
    assert typeutils.floatarr_to_str([1, 0, 0]) == "1.0 0.0 0.0"
    
    # Test with floats
    assert typeutils.floatarr_to_str([1.5, 2.0, 3.14]) == "1.5 2.0 3.14"
    
    # Test with mixed (integers that can be converted to float)
    assert typeutils.floatarr_to_str([1, 2.0, 3]) == "1.0 2.0 3.0"
    
    # Test with numpy floats or other SupportsFloat
    import numpy as np
    assert typeutils.floatarr_to_str([np.float32(1.0), 2.0]) == "1.0 2.0"