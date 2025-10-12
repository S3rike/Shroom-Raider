import sys

def run():
    while(display()): pass

def display():
    current_map, row, column = fetch_map()
    for row in current_map:
        print("".join(row))

def menu():
    file_name = input("Enter path of map (etc. maps/Sample.txt): ")
    '''
    function intended for menu/map selection
    '''
    ...
    if FileNotFoundError:
        print("File not found, try again")
        file_name = input("Enter path of map (etc. maps/Sample.txt): ")
    return open(file_name, "rt")

def fetch_map(file = menu()):
    map = [list(row) for row in file.read().split("\n")]
    file.close()
    '''
    you may add addl checks if map is legal
    '''
    if not map:
        return [], 0, 0
    
    return map, len(map), len(map[0])

if __name__ == "__main__":
    run()