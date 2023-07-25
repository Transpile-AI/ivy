import sys
import os
import contextlib
import pytest
from ivy.utils.assertions import (
    check_elem_in_list,
    check_equal,
    check_exists,
    check_false,
    check_greater,
    check_isinstance,
    check_less,
    check_true,
)
import ivy


@pytest.mark.parametrize(
    "x1, x2, allow_equal",
    [
        (5, 10, False),
        (10, 5, False),
        (5, 5, True),
        (10, 5, True),
    ],
)
def test_check_less(x1, x2, allow_equal):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_less(x1, x2, allow_equal)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if x1 > x2 and allow_equal:
        assert "lesser than or equal" in lines.strip()

    if x1 > x2 and not allow_equal:
        assert "lesser than" in lines.strip()

    if x1 < x2:
        assert not lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "x1, x2, allow_equal",
    [
        (5, 10, False),
        (10, 5, False),
        (5, 5, True),
        (10, 5, True),
    ],
)
def test_check_greater(x1, x2, allow_equal):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_greater(x1, x2, allow_equal)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if x1 < x2 and allow_equal:
        assert "greater than or equal" in lines.strip()

    if x1 < x2 and not allow_equal:
        assert "greater than" in lines.strip()

    if x1 > x2:
        assert not lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "x1, x2, inverse",
    [
        (5, 10, False),
        (10, 10, False),
        (5, 5, True),
        (10, 5, True),
    ],
)
def test_check_equal(x1, x2, inverse):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_equal(x1, x2, inverse)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if inverse:
        if x1 == x2:
            assert "must not be equal" in lines.strip()

        if x1 != x2:
            assert not lines.strip()

    if not inverse:
        if x1 != x2:
            assert "must be equal" in lines.strip()

        if x1 == x2:
            assert not lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "x, allowed_types",
    [(5.0, float), (ivy.array(5), type(ivy.array(8))), (5, float), ([5, 10], tuple)],
)
def test_check_isinstance(x, allowed_types):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_isinstance(x, allowed_types)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if not isinstance(x, allowed_types):
        assert "must be one of the" in lines.strip()

    if isinstance(x, allowed_types):
        assert not lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "x, inverse",
    [(None, False), ([], False), (None, True), ("abc", True)],
)
def test_check_exists(x, inverse):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_exists(x, inverse)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if not inverse:
        if x is None:
            assert "must not be" in lines.strip()

        if x:
            assert not lines.strip()

    if inverse:
        if x is None:
            assert not lines.strip()

        if x:
            assert "must be None" in lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "elem, list, inverse",
    [
        (1, [1, 2], False),
        ("a", [1, 2], False),
        (1, [2, 3], True),
        (0, ["a", "b", "c"], True),
    ],
)
def test_check_elem_in_list(elem, list, inverse):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_elem_in_list(elem, list, inverse)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if not inverse:
        if elem not in list:
            assert "must be one" in lines.strip()

        if elem in list:
            assert not lines.strip()

    if inverse:
        if elem not in list:
            assert not lines.strip()

        if elem in list:
            assert "must not be one" in lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "expression",
    [
        (True),
        "a",
        (None),
        (False),
    ],
)
def test_check_true(expression):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_true(expression)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if not expression:
        assert "True" in lines.strip()

    if expression:
        assert not lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


@pytest.mark.parametrize(
    "expression",
    [
        (True),
        "a",
        (None),
        (False),
    ],
)
def test_check_false(expression):
    filename = "except_out.txt"
    orig_stdout = sys.stdout
    f = open(filename, "w")
    sys.stdout = f
    lines = ""
    try:
        check_false(expression)
    except Exception as e:
        print(e)
    sys.stdout = orig_stdout
    f.close()

    with open(filename) as f:
        lines += f.read()

    if not expression:
        assert not lines.strip()

    if expression:
        assert "False" in lines.strip()

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)
