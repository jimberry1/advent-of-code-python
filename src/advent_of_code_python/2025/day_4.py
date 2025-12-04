from ..helpers import puzzle_loader as loader


def get_surrounding_cords(y_pos, x_pos):
    res = [
        (y, x) for x in range(x_pos - 1, x_pos + 2) for y in range(y_pos - 1, y_pos + 2)
    ]
    res.pop(4)
    return res


def solve_puzzle(paper_map: list[list[str]]):
    n_rows = len(paper_map)
    n_row_items = len(paper_map[0])

    removeable_coords = []

    for y, row in enumerate(paper_map):
        for x, item in enumerate(row):
            taken_space_count = 0

            item = paper_map[y][x]
            if item != "@":
                continue

            neighbour_cords = get_surrounding_cords(y, x)
            for n_y, n_x in neighbour_cords:
                if n_y < 0 or n_y >= n_rows or n_x < 0 or n_x >= n_row_items:
                    continue

                if paper_map[n_y][n_x] == "@":
                    taken_space_count += 1

            if taken_space_count < 4:
                removeable_coords.append((y, x))

    return removeable_coords


def solve_p2(floor_map: list[list[str]]):
    total_removed = 0
    iter_count = 0
    should_continue = True

    while should_continue:
        iter_count += 1
        new_removable_cords = solve_puzzle(floor_map)
        removable_count = len(new_removable_cords)
        if removable_count == 0:
            should_continue = False
        total_removed += len(new_removable_cords)
        for y, x in new_removable_cords:
            floor_map[y][x] = "."

    return total_removed


puzzle_input = loader.load_lines_as_lists(4)
print(f"part 1 {len(solve_puzzle(puzzle_input))}")
print(f"part 2 {solve_p2(puzzle_input)}")
