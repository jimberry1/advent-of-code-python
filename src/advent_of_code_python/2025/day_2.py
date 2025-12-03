import re
from datetime import datetime

from ..helpers import puzzle_loader as loader

pattern = r"(\d+)-(\d+)"


def is_symetrical(x: int):
    x_str = str(x)
    x_len = len(x_str)
    half_length = x_len // 2

    if x_len % 2 != 0:
        return False

    return x_str[:half_length] == x_str[half_length:]


def is_invalid_code_part_2(x: int):
    x_str = str(x)
    x_len = len(x_str)
    for substr_length in range(1, (x_len // 2) + 1):
        if x_len % substr_length == 0:
            quot = x_len // substr_length

            if (x_str[:substr_length] * quot) == x_str:
                return True

    return False


def part_1(pairs):
    invalid_numbers = []

    for match in pairs:
        first, last = match[1], match[2]
        first_int, last_int = int(first), int(last)
        for number in range(first_int, last_int + 1):
            if is_symetrical(number):
                invalid_numbers.append(number)

    print(f"part 1 answer is {sum(invalid_numbers)}")


def part_2(pairs):
    invalid_numbers = []

    for match in pairs:
        first, last = match[1], match[2]
        first_int, last_int = int(first), int(last)
        for number in range(first_int, last_int + 1):
            if is_invalid_code_part_2(number):
                invalid_numbers.append(number)

    print(f"part 2 answer is {sum(invalid_numbers)}")


pairs = [re.match(pattern, pair) for pair in loader.load_line_as_list(2, split_on=",")]

part_1(pairs)

start = datetime.now()
part_2(pairs)
elapsed = datetime.now() - start
print(f"finished part 2 in {elapsed.total_seconds():.3f} seconds")
