import os
from pathlib import Path
from typing import Any, Callable

import requests


def _get_input_path(day_number: int, year: int = 2025):
    return Path(f"resources/aoc_inputs/{year}/input_{day_number}.txt")


def _fetch_input(day_number: int, year: int):
    print(f"fetching puzzle input for day {day_number} year {year}")
    headers = {"Cookie": f"session={os.getenv('AOC_SESSION')}"}
    url = f"https://adventofcode.com/{year}/day/{day_number}/input"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        with open(_get_input_path(day_number, year), "w") as f:
            f.write(response.text)
    except Exception as e:
        print(f"failed to fetch puzzle input for day {day_number} year {year}... {e}")


def get_input_file(day_number: int, year: int = 2025):
    file_path = _get_input_path(day_number, year)
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        _fetch_input(day_number, year)
    return file_path


def load_lines(day_number: int, year: int = 2025):
    with open(get_input_file(day_number), "r") as f:
        return [line.strip() for line in f]


def load_lines_as_lists(
    day_number: int, year: int = 2025, *, item_xf: Callable[[str], Any] | None = None
):
    with open(get_input_file(day_number), "r") as f:
        return [
            [char if not item_xf else item_xf(char) for char in line.strip()]
            for line in f
        ]


def load_line_as_list(
    day_number: int,
    *,
    split_on: str | None = None,
    item_xf: Callable[[str], Any] | None = None,
):
    with open(get_input_file(day_number), "r") as f:
        line = f.readline().strip()
        groups = line.split(split_on) if split_on else [line]
        return groups if not item_xf else [item_xf(group) for group in groups]
