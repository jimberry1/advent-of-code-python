import math

from ..helpers import puzzle_loader as loader


def line_xf(line: list[str]):
    line_vals = []
    cur_val = ""
    for char in line:
        if char == " " and cur_val:
            line_vals.append(
                int(cur_val) if (cur_val != "*" and cur_val != "+") else cur_val
            )
            cur_val = ""

        if char != " ":
            cur_val += char

    line_vals.append(int(cur_val) if (cur_val != "*" and cur_val != "+") else cur_val)

    return line_vals


partially_loaded_puzzle_input = loader.load_lines_as_lists(6, is_example=False)

parsed_input_p1 = [line_xf(line) for line in partially_loaded_puzzle_input]


def solve_p1(puzzle_input: list[list[int | str]]):
    total = 0

    for equation_idx in range(len(puzzle_input[0])):
        operator = puzzle_input[-1][equation_idx]
        operands = [operand_row[equation_idx] for operand_row in puzzle_input[:-1]]

        total += math.prod(operands) if operator == "*" else sum(operands)

    return total


print(f"part 1 total : {solve_p1(parsed_input_p1)}")

# PART 2 - Going to do this separately down here because of the completely different input parsing


def get_operands(lines: list[str]):
    operands = lines[:-1]
    operands_length = len(operands[0])

    operands_for_sums = []
    cur_operands = []
    for operand_idx in range(operands_length):
        col_values = [row[operand_idx] for row in operands]

        if all(val == " " for val in col_values):
            operands_for_sums.append(cur_operands)
            cur_operands = []
            continue

        cur_operands.append(
            int(
                "".join(
                    [line[operand_idx] for line in operands if line[operand_idx] != " "]
                )
            )
        )

    operands_for_sums.append(cur_operands)

    return operands_for_sums


lines = [line.replace("\n", "") for line in loader.read_raw_lines(6)]

operators = [operator for operator in lines[-1] if operator == "+" or operator == "*"]
operands = get_operands(lines)

total = 0
for cur_operator, cur_operands in zip(operators, operands):
    total += math.prod(cur_operands) if cur_operator == "*" else sum(cur_operands)

print(f"part 2 total : {total}")
