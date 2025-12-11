from ..helpers import puzzle_loader as loader


def line_xf(line: str):
    y, x = line.split(",")
    return (int(x), int(y))


puzzle_input = loader.load_lines(9, line_xf=line_xf, is_example=True)


def calc_area(edge1, edge2):
    x1, y1 = edge1
    x2, y2 = edge2

    return ((abs(x2 - x1)) + 1) * ((abs(y2 - y1)) + 1)


def solve_p1(red_tile_coords: list[tuple[int, int]]):
    max_size = 0
    for i in range(len(red_tile_coords)):
        for j in range(i + 1, len(red_tile_coords)):
            edge1, edge2 = red_tile_coords[i], red_tile_coords[j]
            max_size = max(max_size, calc_area(edge1, edge2))

    return max_size


print(f"part1: {solve_p1(puzzle_input)}")


def connect_straight_line(edge1, edge2):
    x1, y1 = edge1
    x2, y2 = edge2

    if x2 - x1 == 0:
        return [(x1, new_y) for new_y in range(min(y1, y2), max(y1, y2) + 1)]

    else:
        return [(new_x, y1) for new_x in range(min(x1, x2), max(x1, x2) + 1)]


def connect_edge_coords(red_tile_coords):
    start = red_tile_coords[0]

    edge_coords = []
    last_red_tile = start

    for next_red_tile in red_tile_coords[1:]:
        connection = connect_straight_line(last_red_tile, next_red_tile)
        edge_coords.extend(connection)
        last_red_tile = next_red_tile

    final_connection = connect_straight_line(last_red_tile, start)
    edge_coords.extend(final_connection)
    return set(edge_coords)


def find_inside_of_rectangle(connected_red_tiles: set[tuple[int, int]]):
    starting_tile = min(connect_edge_coords)
    # now travel in all directions until you find another


def get_neighbours(coord):
    x, y = coord
    new_xs = [
        (new_x, y) for new_x in range(x - 1, x + 2, 2) if new_x >= 0
    ]  # do we need a max check?
    new_ys = [(x, new_y) for new_y in range(y - 1, y + 2, 2) if new_y >= 0]
    return new_xs + new_ys


def flood_fill_initial_shape(
    start_coord: tuple[int, int], edge_coords: set[tuple[int, int]]
):
    coords_to_track = [start_coord]
    seen = edge_coords
    flood_fill = []
    iter_count = 0
    while coords_to_track:
        iter_count += 1

        if iter_count % 1000 == 0:
            print(f"iter count {iter_count * 1000}")
        cur_coord = coords_to_track.pop()
        if cur_coord in seen:
            continue
        else:
            flood_fill.append(cur_coord)
            seen.add(cur_coord)

        neighbours = [
            neighbour
            for neighbour in get_neighbours(cur_coord)
            if neighbour not in seen
        ]

        coords_to_track.extend(neighbours)

    return flood_fill


def create_rectangle_edges(edge1, edge2):
    x1, y1 = edge1
    x2, y2 = edge2
    coords = [edge1, ((abs(x2 - x1)) + 1, y1), edge2, (x1, (abs(y2 - y1)) + 1)]
    return connect_edge_coords(coords)


def is_straight_line(edge1, edge2):
    x1, y1 = edge1
    x2, y2 = edge2
    return True if x1 == x2 or y1 == y2 else False


def is_straight_line_two_high(edge1, edge2):
    x1, y1 = edge1
    x2, y2 = edge2
    return True if abs(x2 - x1) <= 1 or abs(y2 - y1) <= 1 else False


def flood_fill_validity_check(
    edge1: tuple[int, int],
    edge2: tuple[int, int],
    allowed_coords: set[tuple[int, int]],
):
    x1, y1 = edge1
    x2, y2 = edge2

    # Initial checks for straight lines...
    if is_straight_line(edge1, edge2):
        coords = connect_straight_line(edge1, edge2)
        for coord in coords:
            if coord not in allowed_coords:
                return False
        return True

    if is_straight_line_two_high(edge1, edge2):
        if abs(x2 - x1) <= 1:
            coords = connect_straight_line((x1, y1), (x1, y2)) + connect_straight_line(
                (x2, y1), (x2, y2)
            )
        else:
            coords = connect_straight_line((x1, y1), (x1, y2)) + connect_straight_line(
                (x2, y1), (x2, y2)
            )
        for coord in coords:
            if coord not in allowed_coords:
                return False
        return True

    edge_coord_set = create_rectangle_edges(edge1, edge2)
    start_x, start_y = min(x1, x2) + 1, min(y1, y2) + 1

    coords_to_track = [(start_x, start_y)]
    seen = edge_coord_set

    while coords_to_track:
        cur_coord = coords_to_track.pop()
        if cur_coord in seen:
            continue
        else:
            seen.add(cur_coord)

        if cur_coord not in allowed_coords:
            return False

        neighbours = [
            neighbour
            for neighbour in get_neighbours(cur_coord)
            if neighbour not in seen
        ]

        coords_to_track.extend(neighbours)

    return True


def solve_p2(red_tile_coords: list[tuple[int, int]]):
    # connect all tiles
    edge_coords = connect_edge_coords(red_tile_coords)

    print(f"edge coords {edge_coords}")
    # flood fill contents into a set
    first_x, first_y = red_tile_coords[0]
    starting_coord = (8, 2)
    all_contained_tiles = flood_fill_initial_shape(starting_coord, edge_coords)

    print(f"all_contained_tiles: {all_contained_tiles}")

    # for each rectangle, find all contained coords
    max_size = 0
    for i in range(len(red_tile_coords)):
        for j in range(i + 1, len(red_tile_coords)):
            edge1, edge2 = red_tile_coords[i], red_tile_coords[j]
            if flood_fill_validity_check(edge1, edge2, all_contained_tiles):
                max_size = max(max_size, calc_area(edge1, edge2))

    return max_size


print(f"p2 : {solve_p2(puzzle_input)}")
