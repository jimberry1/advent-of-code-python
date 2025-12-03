from ..helpers import puzzle_loader as loader


def find_line_joltage(battery_line: list[int], n_batteries: int):
    batteries = []

    last_battery_idx = 0

    for n_additional_required_batteries in range(n_batteries - 1, -1, -1):
        if n_additional_required_batteries == 0:
            batteries.append(max(battery_line[last_battery_idx:]))
            break

        next_available_batteries = battery_line[
            last_battery_idx:-n_additional_required_batteries
        ]
        max_joltage = max(next_available_batteries)
        batteries.append(max_joltage)
        last_battery_idx += next_available_batteries.index(max_joltage) + 1

    return int("".join(str(n) for n in batteries))


puzzle_input = loader.load_lines_as_lists(3, item_xf=int)
part_1 = sum(find_line_joltage(line, 2) for line in puzzle_input)
part_2 = sum(find_line_joltage(line, 12) for line in puzzle_input)

print(f"part 1 {part_1}, part 2 {part_2}")
