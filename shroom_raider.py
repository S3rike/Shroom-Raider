import sys

input = sys.stdin.readline

def run():
    while(display()): pass

def display():
    current_map, row, column = fetch_map()

def fetch_map(file = menu()):
    map = [list(row) for row in file.read().split("\n")]
    '''
    you may add addl checks if map is legal
    '''
    return map, len(map), len(len(map))

def menu():
    file_name = "maps/Sample.txt"
    '''
    function intended for menu
    currently just returns sample.txt
    '''
    ...
    return open(file_name, "rt")


if __name__ == "__main__":
    run()