from functools import cache

from ..helpers import puzzle_loader as loader

puzzle_input = loader.load_lines_as_lists(7, is_example=False)

start_coord = (0, puzzle_input[0].index("S"))

diagram = puzzle_input


def progress_beam_down_one(beam_coords: tuple[int, int]):
    """Progresses the beam downwards, returning the coordinates of the next beam, or beams in a list"""
    beam_y, beam_x = beam_coords
    should_split = diagram[beam_y + 1][beam_x] == "^"

    if should_split:
        return [
            (beam_y + 1, new_x)
            for new_x in [beam_x - 1, beam_x + 1]
            if (new_x >= 0 and new_x < len(diagram[0]))
        ]
    else:
        return [(beam_y + 1, beam_x)]


def is_beam_at_bottom(beam_coords: tuple[int, int], diagram: list[list[str]]):
    beam_y, _ = beam_coords
    return beam_y == len(diagram) - 1


def part_1(starting_diagram: list[list[str]]):
    all_beam_coords = [start_coord]
    next_layer_beam_coords = set()

    total_splits = 0

    for _ in range(len(starting_diagram) - 1):
        for cur_beam_coords in all_beam_coords:
            next_beam_coords = progress_beam_down_one(cur_beam_coords)

            if len(next_beam_coords) == 2:
                total_splits += 1

            next_layer_beam_coords.update(next_beam_coords)

        all_beam_coords, next_layer_beam_coords = list(next_layer_beam_coords), set()

    return total_splits


print(f"part 1: {part_1(puzzle_input)}")


def part_2(starting_diagram: list[list[str]]):
    all_beam_coords = [start_coord]

    total_splits = 0

    while all_beam_coords:
        cur_beam_coords = all_beam_coords.pop()

        if is_beam_at_bottom(cur_beam_coords, starting_diagram):
            total_splits += 1
            continue

        all_beam_coords.extend(progress_beam_down_one(cur_beam_coords))

    return total_splits


@cache
def coord_to_path_count(beam_coord: tuple[int, int]):
    if is_beam_at_bottom(beam_coord, diagram):
        return 1

    next_beam_coords = progress_beam_down_one(beam_coord)
    return sum([coord_to_path_count(next_beam) for next_beam in next_beam_coords])


def part_2_attempt_2():
    all_beam_coords = [start_coord]

    total_paths = 0

    while all_beam_coords:
        next_beam_coord = all_beam_coords.pop()
        total_paths += coord_to_path_count(next_beam_coord)

    return total_paths


print(f"part 2 attempt 2 : {part_2_attempt_2()}")
