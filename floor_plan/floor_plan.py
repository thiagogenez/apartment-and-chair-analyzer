"""This module defines the FloorPlan class for representing and working with floor plans."""

import re
import logging
from collections import deque
from typing import Optional


class FloorPlanError(Exception):
    """Custom exception class for FloorPlan related errors."""


class FloorPlan:
    """Represents a floor plan and provides methods for working with it."""

    def __init__(self, file_path: str, chair_types: set[str], wall_separators: set[str]):
        """
        Initialize the FloorPlan object by reading and padding the floor plan from a file, and
        initializing the visited matrix.

        Args:
            file_path (str): Path to the file containing the floor plan.
            chair_types (set[str]): A set of characters that represent chair types.
            wall_separators (set[str]): A set of characters that represent non-visitable cells.
        """

        # Sanity check for inputs
        self._validate_inputs(chair_types, wall_separators)

        try:
            logging.debug(f"Reading and padding the floor plan from {file_path}")
            self.floor_plan: list[list[str]] = self._read_and_pad_floor_plan(file_path)

            # Immediately set rows and cols based on the the padded floor plan dimensions
            self.rows, self.cols = len(self.floor_plan), len(self.floor_plan[0])
            logging.debug(f"Floor plan dimensions: {self.rows} rows, {self.cols} columns")

        except IOError as e:
            logging.error(f"Failed to read the floor plan from {file_path}: {e}")
            raise FloorPlanError(f"Failed to initialize FloorPlan from {file_path}") from e

        # Validate that we don't have an empty floor plan matrix
        if self.rows == 0:
            raise FloorPlanError(
                "Failed to initialize FloorPlan: The padded floor plan is an empty matrix."
            )

        # Initialize instance variables
        self.visited: list[list[bool]] = [[False] * self.cols for _ in range(self.rows)]
        self.wall_separators: set[str] = wall_separators
        self.chair_types: set[str] = chair_types
        self.room_mappings: dict[str, dict[str, int]] = {}

        # logging
        logging.debug("Visited matrix:")
        for row in self.visited:
            logging.debug(" ".join("X" if cell else "." for cell in row))
        logging.debug(f"Wall separators: {self.wall_separators}")
        logging.debug(f"Chair types: {self.chair_types}")

    def _validate_inputs(self, chair_types: set[str], wall_separators: set[str]):
        """
        Validates the input sets for chair types and wall separators to ensure they are not empty.

        This method checks if the provided sets for chair types and wall separators
        contain any elements. If any of these sets are found to be empty, it logs an
        error message indicating which input set is empty and raises a ValueError to
        prevent further execution with invalid input parameters.

        Args:
            chair_types (set[str]): A set of characters representing different types of chairs.
            wall_separators (set[str]): A set of characters used to represent walls or barriers
                that cannot be crossed.

        Raises:
            ValueError: If either 'chair_types' or 'wall_separators' is empty,
                indicating invalid input.
        """
        # Validate that the chair_types set is not empty
        if not chair_types:
            logging.error("Validation Error in _validate_inputs: 'chair_types' cannot be empty.")
            raise ValueError("Chair types cannot be empty.")

        # Validate that the wall_separators set is not empty
        if not wall_separators:
            logging.error(
                "Validation Error in _validate_inputs: 'wall_separators' cannot be empty."
            )
            raise ValueError("Wall separators cannot be empty.")

    def _read_and_pad_floor_plan(self, file_path: str) -> list[list[str]]:
        """
        Reads a floor plan from a file, removing trailing whitespace from each line, and pads each
        line with spaces to ensure all have the same length.

        Uses 'utf-8-sig' encoding to correctly handle files with a UTF-8 BOM.

        Args:
            file_path (str): The path to the file containing the floor plan.

        Returns:
            A list of lists, where each inner list represents a row in the floor plan
            with equal length, padded with spaces to ensure all have the same length.
        """
        try:
            with open(file_path, encoding="utf-8-sig") as f:
                # Create a list of lists from the file, stripping trailing whitespace
                floor_plan = [list(line.rstrip()) for line in f]

                # Determine the maximum length of rows for padding
                max_length = max(len(row) for row in floor_plan)

                # Pad each row to ensure uniform length across the floor plan
                return [row + [" "] * (max_length - len(row)) for row in floor_plan]

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{file_path}' not found.") from e

        except Exception as e:
            raise FloorPlanError(f"Error reading floor plan from '{file_path}': {e}") from e

    def _print_floor_plan(self) -> None | str:
        logging.debug("=" * self.rows * 2)
        for row in self.visited:
            logging.debug(" ".join("X" if cell else "." for cell in row))
        logging.debug("%" * self.rows * 2)

    def is_visitable(self, cell: tuple[int, int]) -> bool:
        """
        Determines if a given cell in the floor plan is visitable.

        Args:
            cell (tuple[int, int]): The (x, y) coordinates of the cell to check.

        Returns:
            bool: True if the cell is visitable, False otherwise.
        """
        x, y = cell
        return (
            0 <= x < self.rows
            and 0 <= y < self.cols
            and not self.visited[x][y]
            and self.floor_plan[x][y] not in self.wall_separators
        )

    @staticmethod
    def get_room_name(row_str: str, y: int) -> str | None:
        """
        Extracts a room name from a row string based on the horizontal position (y) using regex.

        Searches for the nearest pair of parentheses surrounding the y position and
        extracts the substring enclosed within. If the position is not within a valid
        room name boundary or if parentheses are not properly matched, returns None.

        Args:
            row_str (str): The string representation of the floor plan's row.
            y (int): The horizontal position (column index) within the row.

        Returns:
            str or None: The extracted room name if found, otherwise None.
        """

        # Compile a regex pattern to find all substrings enclosed in parentheses
        pattern = re.compile(r"\(([^)]+)\)")

        # Find all matches of the pattern in the row string
        matches = pattern.finditer(row_str)

        for match in matches:

            # Check if the given y position falls within the current match's span
            if match.start() <= y < match.end():

                # Return the matched group (room name) without parentheses
                return match.group(1)

        # Return None if no valid room name is found surrounding the y position
        return None

    def _bfs(
        self,
        start_cell: tuple[int, int],
    ) -> tuple[Optional[str], dict[str, int]]:
        """
        Explores the floor plan from a starting cell using Breadth-First Search (BFS) to count
        chairs by type and identify the room name, considering specified wall_separators to identify
        walls and chair types.

        Args:
            start_cell (tuple[int, int]): The starting cell coordinates (x, y) as a tuple.

        Returns:
            A tuple containing the room name (str or None) and a dictionary of chairs found,
            mapping chair types (str) to their counts (int). Each chair type is initialized
            with a count of 0.

        Raises:
            InvalidCellContentError: If a cell's content is neither a recognized chair type
            nor a wall separator.
        """

        # Return immediately if the floor plan is empty, indicating there's nothing to explore.
        if not self.floor_plan or not self.floor_plan[0]:
            return None, []

        # Initialize the queue with the starting cell and prepare containers for results.
        queue = deque([start_cell])
        chairs: dict[str, int] = {chair: 0 for chair in self.chair_types}
        area_name: Optional[str] = None

        # Mark the starting cell as visited.
        self.visited[start_cell[0]][start_cell[1]] = True

        # Continue exploring until there are no more cells to visit in a room.
        while queue:
            x, y = queue.popleft()  # Current cell being visited
            cell_value = self.floor_plan[x][y]  # Value of the current cell

            # If the current cell's value is in chair_types, count it to the chairs list.
            if cell_value in self.chair_types:
                chairs[cell_value] += 1

            # If we haven't identified the area name yet,
            # and the cell indicates a room name start, extract the name.
            elif not area_name and cell_value == "(":
                # Convert the current row to a string and attempt to extract the room name
                area_name = self.get_room_name("".join(self.floor_plan[x]), y)

            # Explore adjacent cells in all four directions (up, down, left, right).
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = (
                    x + dx,
                    y + dy,
                )  # Calculate coordinates of the next cell to visit

                # If the next cell is visitable (within bounds, not visited,
                # and not a wall), mark it as visited and add to the queue.
                if self.is_visitable((nx, ny)):
                    self.visited[nx][ny] = True
                    queue.append((nx, ny))

        # Return the discovered room name (if any) and the list of chairs
        # found during the exploration.
        return area_name, chairs

    def parse_floor_plan(self):
        """
        Parses the entire floor plan to find all rooms and count chair types within each room.

        Stores the result in self.room_mappings as {"room_name": {"chair_type": count}}.
        """

        logging.debug("Starting to parse the floor plan.")

        # Reinitialize the visited matrix to ensure a fresh start for parsing.
        self.visited = [[False] * self.cols for _ in range(self.rows)]

        # Iterate over each cell in the floor plan
        for x in range(self.rows):
            for y in range(self.cols):
                self._explore_cell(x, y)

        logging.debug("Finished parsing the floor plan.")

    def _explore_cell(self, x: int, y: int) -> None:
        """
        Explore a single cell in the floor plan, updating room mappings if a room is discovered.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        # Skip over cells that have been visited or are marked as wall separators.
        if not self.visited[x][y] and self.floor_plan[x][y] not in self.wall_separators:
            logging.debug(f"Exploring from cell ({x}, {y}).")

            # Perform BFS from each unvisited cell that is not a wall to discover rooms
            area_name, chairs = self._bfs((x, y))

            if area_name:
                if area_name in self.room_mappings:
                    logging.debug(f"Updating room: {area_name} with chairs: {chairs}")

                    # Merge chair counts if the room was already discovered
                    for chair, count in chairs.items():
                        self.room_mappings[area_name][chair] = (
                            self.room_mappings[area_name].get(chair, 0) + count
                        )
                else:
                    logging.debug(f"Discovered new room: {area_name} with chairs: {chairs}")
                    self.room_mappings[area_name] = chairs
            else:
                logging.debug(f"Encountered an unnamed area starting at cell ({x}, {y}); skipping.")

        logging.debug(f"Last explored cell ({x}, {y}).")
        self._print_floor_plan()

    def _format_chair_counts(self, chair_counts: dict) -> str:
        """
        Formats the chair counts into a sorted, comma-separated string, ensuring that all chair
        types defined in the class, as well as those found in specific rooms, are included in the
        output. Chair types not found in the room will have a count of 0.

        Args:
            chair_counts (dict): A dictionary mapping chair types to their counts in a room.

        Returns:
            str: A formatted string of chair counts, sorted alphabetically by chair type.
        """
        # Ensure all chair types are included, even if their count is zero, for consistent output.
        all_chair_types = sorted(set(self.chair_types) | set(chair_counts.keys()), reverse=True)

        # Construct the output string by iterating over all chair types.
        # For each chair type, retrieve its count from chair_counts,
        # defaulting to 0 if not found. This ensures that all known chair
        # types are included in the output, even if not present in the room.
        formatted_chair_counts = [
            f"{chair}: {chair_counts.get(chair, 0)}" for chair in all_chair_types
        ]

        # Join the individual chair count strings with commas to form the final output.
        return ", ".join(formatted_chair_counts)

    def get_room_names_sorted(self) -> str:
        """Returns a string representation of the room names stored in room_mappings and their chair
        counts, in alphabetical order, including a total count of chairs at the beginning."""
        # Initialize total chairs dictionary with zeros for all chair types.
        total_chairs = {chair: 0 for chair in self.chair_types}

        # Calculate total chair counts across all rooms.
        for chairs in self.room_mappings.values():
            for chair, count in chairs.items():
                total_chairs[chair] += count

        # Format the total counts.
        total_counts_str = self._format_chair_counts(total_chairs)
        output_lines = ["total:", total_counts_str]

        # Format counts for each room, ensuring room names are sorted alphabetically.
        for room_name in sorted(self.room_mappings.keys()):
            room_chairs = self.room_mappings[room_name]
            chairs_str = self._format_chair_counts(room_chairs)
            output_lines.extend([f"{room_name}:", chairs_str])

        return "\n".join(output_lines)
