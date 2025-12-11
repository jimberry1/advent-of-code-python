import re
from collections import defaultdict, deque

from ..helpers import puzzle_loader as loader


def parse_input_line(line: str):
    pattern = r"\[([^\]]*)\]|\(([^)]*)\)"
    desired_state, *button_rows = [
        first or [int(val) for val in second.split(",")]
        for first, second in re.findall(pattern, line)
    ]

    desired_state_binary = int(
        "".join(["1" if val == "#" else "0" for val in desired_state]), 2
    )

    buttons_binary = []
    for buttons in button_rows:
        row_str = "".join(
            [
                "1" if item_idx in buttons else "0"
                for item_idx in range(len(desired_state))
            ]
        )
        row_binary_val = int(row_str, 2)
        buttons_binary.append(row_binary_val)
    # print(f"desired state {desired_state_binary}")
    # print(f"buttons : {buttons_binary}")
    return desired_state_binary, buttons_binary


parsed = parse_input_line("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")


# Find the lowest common combination that leads to the desired state if '0 1 1 0' (from .##.)
# Do this with a breadth first search, or Dijkstra's algorithm?
# BFS would be:
# Start with a queue containing current state, number of presses and next button to press
# Read off left of queue, apply next button and enqueue all other buttons with the new state and 1+ number of presses
# When the first value that reaches the desired state is found, return

# How do we prevent cycles of button presses? e.g. A->B->C->A->B->C?
# If every item on the queue enqueues n_buttons-1 messages, this will grow with presses^number of buttons
# Store a dict of current button state : [button_idx]. If you've been at that state before don't enqueue a button if it's been seen before
# That way only unique combinations are found... should thin down the problem space nicely. Now we can grow better


def calc_min_presses(target, buttons):
    starting_state_binary_val = 0

    seen = defaultdict(set)

    my_queue = deque()
    for button in buttons:
        my_queue.append((0, starting_state_binary_val, button))

    while my_queue:
        press_count, cur_state, next_button = my_queue.popleft()
        if next_button in seen[cur_state]:
            continue

        inc_press_count = press_count + 1
        new_state = cur_state ^ next_button

        if new_state == target:
            return inc_press_count

        next_queue_items = [
            (inc_press_count, new_state, nb) for nb in buttons if nb != next_button
        ]
        my_queue.extend(next_queue_items)


def solve_p1(parsed_inputs: list[tuple]):
    total_presses = 0

    for desired_state_binary, buttons_binary in parsed_inputs:
        total_presses += calc_min_presses(desired_state_binary, buttons_binary)

    return total_presses


puzzle_input = loader.load_lines(10, line_xf=parse_input_line, is_example=False)


print(f"ans : {solve_p1(puzzle_input)}")
