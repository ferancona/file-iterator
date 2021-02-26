import pytest

from file_iterator.Exceptions import ExceptionRaiser


@pytest.fixture
def stop_iteration_raiser():
    return ExceptionRaiser(StopIteration)

def test_raise_exception(stop_iteration_raiser):
    with pytest.raises(StopIteration):
        stop_iteration_raiser.raise_ex()