import re

from ..helpers import puzzle_loader as loader

puzzle_input = loader.load_lines(5, is_example=False)


break_index = puzzle_input.index("")

db_index_pattern = r"(\d+)-(\d+)"
db_ranges = [
    (int(m.group(1)), int(m.group(2)))
    for r in puzzle_input[:break_index]
    if (m := re.match(db_index_pattern, r))
]

items = (int(i) for i in puzzle_input[break_index + 1 :])


def part_1(db_ranges: list[tuple[int, int]], items: list[int]):
    fresh_ingredients = []
    for item in items:
        for lower, upper in db_ranges:
            if item >= lower and item <= upper:
                fresh_ingredients.append(item)
                break
    return fresh_ingredients


def part_2(db_ranges: list[tuple[int, int]]):
    valid_db_ranges = sorted(db_ranges)

    coverage_count = 0
    last_end = 0
    for start, end in valid_db_ranges:
        if end >= last_end:
            coverage_count += (end - max(start, last_end + 1)) + 1
            last_end = end

    return coverage_count


print(f"Found {len(part_1(db_ranges, items))} fresh ingrendients")
print(f"ID range was {part_2(db_ranges)} units wide")
