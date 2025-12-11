import re
from collections import defaultdict, deque

from ..helpers import puzzle_loader as loader


def parse_input_line_p1(line: str):
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


puzzle_input = loader.load_lines(10, line_xf=parse_input_line_p1, is_example=False)


print(f"ans : {solve_p1(puzzle_input)}")


def parse_input_line_p2(line: str):
    button_pattern = r"\(([^)]*)\)"
    all_button_activation_indices = [
        tuple([int(val) for val in button_matches.split(",")])
        for button_matches in re.findall(button_pattern, line)
    ]

    joltage_pattern = r"\{(.*)\}"
    match = re.search(joltage_pattern, line)
    joltages = tuple([int(val) for val in match[1].split(",")])

    return all_button_activation_indices, joltages


def calc_joltage_min_presses(button_activation_indices: tuple, joltages: list[int]):
    starting_state = tuple([0 for _ in joltages])

    print(
        f"button_activation_indices {button_activation_indices}, joltages: {joltages}"
    )

    seen_states = {starting_state: 0}

    my_queue = deque()

    for button in button_activation_indices:
        my_queue.append((0, starting_state, button))

    while my_queue:
        cur_presses, cur_state, next_button = my_queue.popleft()

        seen_states[cur_state] = cur_presses

        if cur_state == joltages:
            return cur_presses

        inc_presses = cur_presses + 1
        # New state is going to be the current state, + value of button activation index at that array
        updated_state = tuple(
            [
                val + 1 if idx in next_button else val
                for idx, val in enumerate(cur_state)
            ]
        )

        if updated_state in seen_states and seen_states[updated_state] <= inc_presses:
            continue

        seen_states[updated_state] = inc_presses

        should_exit = False
        for idx, val in enumerate(updated_state):
            if val > joltages[idx]:
                should_exit = True
                break

        if should_exit:
            continue

        for button in button_activation_indices:
            my_queue.append((inc_presses, updated_state, button))


def solve_p2(parsed_inputs: list[tuple[list[int], list[int]]]):
    total_presses = 0

    for button_activation_indices, joltages in parsed_inputs:
        total_presses += calc_joltage_min_presses(button_activation_indices, joltages)

    return total_presses


p2_puzzle_input = loader.load_lines(10, line_xf=parse_input_line_p2, is_example=False)
print(f"p2 answer: {solve_p2(p2_puzzle_input)}")

# This works, but it's way too slow, there's probably a much better way to solve this using a lowest common multiple
# You could probably do this with a greedy algorithm and backtracking - find the button with the highest total effect and work backwards
