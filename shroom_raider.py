import sys
import os

def run():
    while(display()): pass

def display():
    current_map, row, column = fetch_map()
    for row in current_map:
        print("".join(row))

def menu():
    # Uncomment this if we want to not include dir and just type the filename
    # file_name = "Maps/"" + input("Enter path of map (etc. Sample.txt): ")

    # Code if we want to include the dir and map filename
    file_name = input("Enter path of map (etc. Maps/Sample.txt): ")
    '''
    function intended for menu/map selection
    '''
    ...
    if not os.path.exists(file_name):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print("File not found, try again")
        file_name = input("Enter path of map (etc. Maps/Sample.txt): ")
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