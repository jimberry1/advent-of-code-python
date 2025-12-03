import re
from collections import deque
from typing import NamedTuple

from ..helpers import puzzle_loader as loader

pattern = r"(R|L)(\d+)"


class SafeMovement(NamedTuple):
    direction: str
    value: int


lines = loader.load_lines(day_number=1)

dial = deque(list(range(100)))
dial.rotate(50)

counter = 0
for line in lines:
    match = re.match(pattern, line)
    direction, value = match[1], int(match[2])

    dial.rotate(value if direction == "L" else -value)

    if dial[0] == 0:
        counter += 1

print(f"part 1 {counter}")

counter = 0

dial = deque(list(range(100)))
dial.rotate(50)

for line in lines:
    match = re.match(pattern, line)
    direction, value = match[1], int(match[2])

    for move in range(value):
        dial.rotate(1 if direction == "R" else -1)
        if dial[0] == 0:
            counter += 1

print(f"part 2 {counter}")
