import math

from ..helpers import puzzle_loader as loader


def line_to_coord(line: str):
    x, y, z = line.split(",")
    return (int(x), int(y), int(z))


puzzle_input = loader.load_lines(8, line_xf=line_to_coord, is_example=False)


def calc_distance(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    base = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    distance = math.sqrt(base)
    return distance


def create_ordered_distances(junction_boxes):
    cross_product_distances = []
    for box_idx, box1 in enumerate(junction_boxes[:-1]):
        for box2 in junction_boxes[box_idx + 1 :]:
            distance = calc_distance(box1, box2)
            cross_product_distances.append((distance, box1, box2))

    return sorted(cross_product_distances, key=lambda item: item[0])


def assemble_connections(box_map):
    box_chains = []
    seen_boxes = set()

    for box in iter(box_map):
        if box in seen_boxes:
            continue

        seen_boxes.add(box)

        current_chain, connections_to_resolve = {box}, [box]
        while connections_to_resolve:
            next_box = connections_to_resolve.pop()
            connected_boxes = [
                connection
                for connection in box_map[next_box]
                if connection not in seen_boxes
            ]
            current_chain.update(connected_boxes)
            seen_boxes.update(connected_boxes)
            connections_to_resolve.extend(connected_boxes)

        box_chains.append(current_chain)

    return box_chains


def solve_p1(junction_boxes: list[tuple[int, int, int]]):
    junction_box_map = {coord: [coord] for coord in junction_boxes}
    sorted_distances = create_ordered_distances(junction_boxes)
    number_of_connections = 1000

    for _, box1, box2 in sorted_distances[:number_of_connections]:
        junction_box_map[box1].append(box2)
        junction_box_map[box2].append(box1)

    res = assemble_connections(junction_box_map)
    sorted_res = sorted(res, key=len, reverse=True)
    return math.prod([len(top_n) for top_n in sorted_res[:3]])


def solve_p2(junction_boxes):
    sorted_distances = create_ordered_distances(junction_boxes)
    connected_groups = []
    for _, box1, box2 in sorted_distances:
        indexes_containing_either_box = set(
            [
                idx
                for idx, group in enumerate(connected_groups)
                if box1 in group or box2 in group
            ]
        )

        if not indexes_containing_either_box:
            connected_groups.append({box1, box2})
            continue

        else:
            merged_set = set({box1, box2})
            for set_idx in indexes_containing_either_box:
                merged_set = merged_set | connected_groups[set_idx]

            sets_to_maintain = [
                group
                for idx, group in enumerate(connected_groups)
                if idx not in indexes_containing_either_box
            ]

            combined = [merged_set] + sets_to_maintain
            connected_groups = combined

            if len(merged_set) == len(junction_boxes):
                return box1[0] * box2[0]


print(f"part 1: {solve_p1(puzzle_input)}")
print(f"part 2: {solve_p2(puzzle_input)}")
