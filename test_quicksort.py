"""
Test Quicksort
"""
import pytest
from quicksort import quicksort

def test_serial_quicksort():
    # Set up
    unsorted_array = [0,3,1,12,9]

    # Act
    result = quicksort(unsorted_array)

    # Assert
    assert result == [0,1,3,9,12]


@pytest.mark.parametrize("test_input,expected",  [ ([0,3,1,12,9],[0,1,3,9,12]), ([0,0,1,2,1],[0,0,1,1,2]) ] )
def test_many_serial_quicksort(test_input, expected):
    # Act
    result = quicksort(test_input)

    # Assert
    assert result == expected
