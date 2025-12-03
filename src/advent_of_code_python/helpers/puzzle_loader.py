import os
from pathlib import Path
from typing import Any, Callable

import requests


def _ensure_path_exists(year):
    input_path = Path(f"resources/aoc_inputs/{year}")
    if not input_path.exists():
        input_path.mkdir(parents=True, exist_ok=True)


def _get_input_file_name(day_number: int, year: int = 2025):
    return f"resources/aoc_inputs/{year}/input_{day_number}.txt"


def _fetch_input(day_number: int, year: int):
    print(f"fetching puzzle input for day {day_number} year {year}")
    headers = {"Cookie": f"session={os.getenv('AOC_SESSION')}"}
    url = f"https://adventofcode.com/{year}/day/{day_number}/input"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        _ensure_path_exists(year)

        with open(_get_input_file_name(day_number, year), "w") as f:
            f.write(response.text)
    except Exception as e:
        print(f"failed to fetch puzzle input for day {day_number} year {year}... {e}")


def load_lines(day_number: int):
    with open(_get_input_file_name(day_number), "r") as f:
        return [line.strip() for line in f]


def load_lines_as_lists(
    day_number: int, *, item_xf: Callable[[str], Any] | None = None
):
    with open(_get_input_file_name(day_number), "r") as f:
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
    with open(_get_input_file_name(day_number), "r") as f:
        line = f.readline().strip()
        groups = line.split(split_on) if split_on else [line]
        return groups if not item_xf else [item_xf(group) for group in groups]
