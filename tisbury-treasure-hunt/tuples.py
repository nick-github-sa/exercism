"""Functions to help Azara and Rui locate pirate treasure."""


def get_coordinate(record):
    """Return coordinate value from a tuple containing the treasure name, and treasure coordinate.

    :param record: tuple - with a (treasure, coordinate) pair.
    :return: str - the extracted map coordinate.
    """

    treasure, coordinate = record
    return str(coordinate)


def convert_coordinate(coordinate):
    """Split the given coordinate into tuple containing its individual components.

    :param coordinate: str - a string map coordinate
    :return: tuple - the string coordinate split into its individual components.
    """

    return tuple(coordinate)


def compare_records(azara_record, rui_record):
    """Compare two record types and determine if their coordinates match.

    :param azara_record: tuple - a (treasure, coordinate) pair.
    :param rui_record: tuple - a (location, tuple(coordinate_1, coordinate_2), quadrant) trio.
    :return: bool - do the coordinates match?
    """

    new_coordinate = "".join(rui_record[1])
    treasure, coordinate = azara_record
    return convert_coordinate(azara_record[1]) == rui_record[1]

def create_record(azara_record, rui_record):
    """Combine the two record types (if possible) and create a combined record group.

    :param azara_record: tuple - a (treasure, coordinate) pair.
    :param rui_record: tuple - a (location, coordinate, quadrant) trio.
    :return: tuple or str - the combined record (if compatible), or the string "not a match" (if incompatible).
    """

    treasure, azara_coord = azara_record
    location, rui_coord_tuple, quadrant = rui_record

    # Combine Rui's coordinate tuple into a string (e.g., ("A", "2") → "A2")
    rui_coord = rui_coord_tuple[0] + rui_coord_tuple[1]

    # Compare Azara's coordinate with Rui's coordinate
    if azara_coord == rui_coord:
        return (treasure, azara_coord, location, rui_coord_tuple, quadrant)
    else:
        return "not a match"


def clean_up(combined_record_group):
    """Clean up a combined record group into a multi-line string of single records.

    :param combined_record_group: tuple - everything from both participants.
    :return: str - everything "cleaned", excess coordinates and information are removed.

    The return statement should be a multi-lined string with items separated by newlines.

    (see HINTS.md for an example).
    """

    lines = []
    for treasure, _coord_str, location, coord_tuple, quadrant in combined_record_group:
        # Keep treasure, location, coordinate tuple, quadrant
        cleaned = (treasure, location, coord_tuple, quadrant)
        lines.append(str(cleaned))
    result = "\n".join(lines)
    return result + ("\n" if result else "")
