from ..helpers import puzzle_loader as loader
import re 
from functools import cache

pattern = r"[a-z]{3}"

def parse_line(line):
    return re.findall(pattern, line)

puzzle_input = loader.load_lines(11, line_xf=parse_line, is_example=False)


def create_connection_map(lines: list[list[str]]):
    """Parses puzzle input into a hashmap where the key is the input connection and the value is
    a list of connected output nodes"""
    lookup_table = {}
    for input_connection, *output_connections in lines:
        lookup_table[input_connection] = output_connections
    
    return lookup_table

create_connection_map(puzzle_input)

def find_paths_p1(connection_map, node_key, path_counter):
    connections = connection_map[node_key]

    if not connections:
        return 0
    
    if 'out' in connections:
        return 1
    
    return sum([find_paths_p1(connection_map, connection, path_counter) for connection in connections])

def solve_p1(puzzle_input):
    connection_map = create_connection_map(puzzle_input)
    return find_paths_p1(connection_map, 'you', 0)

print(f"p1 answer is {solve_p1(puzzle_input)}")

def solve_p2(puzzle_input):
    connection_map = create_connection_map(puzzle_input)

    @cache
    def find_paths_p2(node_key, fft, dac):
        connections = connection_map[node_key]

        if not connections:
            return 0
        
        if 'out' in connections:
            return 1 if fft and dac else 0
        
        return sum([find_paths_p2(connection, fft or node_key == 'fft', dac or node_key == 'dac')  for connection in connections])

    return find_paths_p2('svr', False, False)

print(f"p2 answer is {solve_p2(puzzle_input)}")