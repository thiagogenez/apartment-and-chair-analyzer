"""Tests for the FloorPlan class and its methods."""

import os
import pytest
from floor_plan import FloorPlan, FloorPlanError


@pytest.fixture
def example_file_path():
    """Fixture that returns the path to the examples directory."""
    return os.path.join(os.path.dirname(__file__), "../examples")


@pytest.mark.parametrize(
    "file_name", ["example1.txt", "example2.txt", "example3.txt", "example4.txt", "example5.txt"]
)
def test_floor_plan_parsing(example_file_path, file_name):
    """Test parsing of floor plans for different example files.

    Args:
        example_file_path (str): Path to the examples directory.
        file_name (str): Name of the example file to test.
    """
    file_path = os.path.join(example_file_path, file_name)
    chair_types = {"C", "S", "P", "W"}
    wall_separators = {"+", "-", "|", "/", "\\"}

    floor_plan = FloorPlan(file_path, chair_types, wall_separators)
    floor_plan.parse_floor_plan()

    # Define the expected output
    expected_output = {
        "example1.txt": """\
total:
W: 14, S: 3, P: 7, C: 1
balcony:
W: 0, S: 0, P: 2, C: 0
bathroom:
W: 0, S: 0, P: 1, C: 0
closet:
W: 0, S: 0, P: 3, C: 0
kitchen:
W: 4, S: 0, P: 0, C: 0
living room:
W: 7, S: 2, P: 0, C: 0
office:
W: 2, S: 0, P: 1, C: 0
sleeping room:
W: 1, S: 1, P: 0, C: 0
toilet:
W: 0, S: 0, P: 0, C: 1
""",
        "example2.txt": """\
total:
W: 24, S: 7, P: 14, C: 1
balcony:
W: 0, S: 0, P: 2, C: 0
bathroom:
W: 0, S: 0, P: 1, C: 0
closet:
W: 0, S: 0, P: 3, C: 0
hall:
W: 0, S: 0, P: 0, C: 0
kitchen:
W: 4, S: 0, P: 0, C: 0
living room:
W: 6, S: 2, P: 0, C: 0
office:
W: 2, S: 0, P: 1, C: 0
suite:
W: 2, S: 0, P: 2, C: 0
toilet:
W: 0, S: 0, P: 0, C: 1
tv room:
W: 10, S: 5, P: 5, C: 0
""",
        "example3.txt": """\
total:
W: 0, S: 0, P: 3, C: 0
studio:
W: 0, S: 0, P: 3, C: 0
""",
        "example4.txt": """\
total:
W: 0, S: 0, P: 0, C: 0
""",
        "example5.txt": """\
total:
W: 0, S: 0, P: 1, C: 0
a:
W: 0, S: 0, P: 1, C: 0
""",
    }

    # Get the actual output
    actual_output = floor_plan.get_room_names_sorted()

    # Compare actual and expected outputs
    assert actual_output.strip() == expected_output[file_name].strip()


def test_invalid_floor_plan(example_file_path):
    """Test for an invalid floor plan file.

    Args:
        example_file_path (str): Path to the examples directory.
    """
    # Test invalid file path
    file_path = os.path.join(example_file_path, "invalid_file.txt")
    chair_types = {"C", "S", "P", "W"}
    wall_separators = {"+", "-", "|", "/", "\\"}

    with pytest.raises(FloorPlanError):
        FloorPlan(file_path, chair_types, wall_separators)
