import argparse
from floor_plan import FloorPlan, FloorPlanError
import logging
import sys


def setup_logging(log_level):
    """
    Configure the logging level and format.
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main(file_path: str, separators: set, chair_chars: set, log_level: str) -> None:
    """
    Main function to process the floor plan file.

    Args:
        file_path: Path to the floor plan file.
        separators: Set of characters used as separators.
        chair_chars: Set of characters representing chairs.
        log_level: Logging level as a string.
    """

    # Configure logging based on the user's choice
    setup_logging(log_level)

    logging.debug(f"File to read: {file_path}")
    logging.debug(f"Separators: {separators}")
    logging.debug(f"Chair characters: {chair_chars}")

    try:
        # Create a FloorPlan object with the given parameters
        floor_plan = FloorPlan(file_path, chair_chars, separators)
        # Parse the floor plan to find rooms and chair counts
        floor_plan.parse_floor_plan()
        # Print the sorted room names and their chair counts
        print(floor_plan.get_room_names_sorted())
    except FloorPlanError as e:
        logging.error(f"Failed to process floor plan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a floor plan file.")

    # Define command-line arguments
    parser.add_argument("file_path", type=str, help="The path to the floor plan file.")
    parser.add_argument(
        "--separators",
        type=lambda s: set(s.split(",")),
        default={"+", "-", "|", "/", "\\"},
        help="Characters used as separators. Provide as comma-separated. Default: '+,-,|,/,\\'.",
    )
    parser.add_argument(
        "--chair_chars",
        type=lambda s: set(s.split(",")),
        default={"C", "S", "P", "W"},
        help="Characters representing chairs. Provide as comma-separated. Default: 'C,S,P,W'.",
    )
    parser.add_argument(
        "--logging",
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level. Default: 'info'.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.file_path, args.separators, args.chair_chars, args.logging)
