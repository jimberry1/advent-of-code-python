import os
from pathlib import Path
from typing import Any, Callable

import requests


def _get_input_path(day_number: int, year: int = 2025):
    return Path(f"resources/aoc_inputs/{year}/input_{day_number}.txt")


def _get_example_path(day_number: int, year: int = 2025):
    return Path(f"resources/aoc_inputs/{year}/example_{day_number}.txt")


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


def get_input_file(day_number: int, year: int = 2025, *, is_example: bool = False):
    """Returns the pathlib.Path to the input file.

    Options:
    `is_example` - controls whether to load the example provided in the advent of code description. This should be manually copied in by the user"""
    if is_example:
        return _get_example_path(day_number, year)

    file_path = _get_input_path(day_number, year)
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        _fetch_input(day_number, year)
    return file_path


def load_lines(
    day_number: int,
    year: int = 2025,
    *,
    line_xf: Callable[[str], any] = None,
    is_example: bool = False,
):
    with open(get_input_file(day_number, year, is_example=is_example), "r") as f:
        lines = [line.strip() for line in f]
        return [line_xf(line) for line in lines] if line_xf else lines


def load_lines_as_lists(
    day_number: int,
    year: int = 2025,
    *,
    item_xf: Callable[[str], Any] | None = None,
    is_example: bool = False,
):
    with open(get_input_file(day_number, year, is_example=is_example), "r") as f:
        return [
            [char if not item_xf else item_xf(char) for char in line.strip()]
            for line in f
        ]


def read_raw_lines(day_number, year: int = 2025, *, is_example: bool = False):
    with open(get_input_file(day_number, year, is_example=is_example), "r") as f:
        return [line for line in f]


def load_line_as_list(
    day_number: int,
    *,
    split_on: str | None = None,
    item_xf: Callable[[str], Any] | None = None,
    is_example: bool = False,
):
    with open(get_input_file(day_number, is_example=is_example), "r") as f:
        line = f.readline().strip()
        groups = line.split(split_on) if split_on else [line]
        return groups if not item_xf else [item_xf(group) for group in groups]
