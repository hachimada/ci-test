import pytest

from src.sample import add

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (2, 3, 5),
        (3, 4, 7),
    ],
)
def test_sample(a: int, b: int, expected: int) -> None:
    """
    Sample test to check if pytest is working.
    """
    assert add(a, b) == expected