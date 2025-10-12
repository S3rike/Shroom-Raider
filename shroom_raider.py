from auxilliary_functions import *

def run():
    print("start")
    while(True): 
        game_status = menu()
        if not game_status: 
            break
        display()
    return None
def display():
    current_map, row, column = fetch_map()
    print("Check 2")
    return None
def menu():
    print("Check0")
    return instruct_input("Try Again (True or False): ")
def choose_map():
    file_name = instruct_input("Enter path of map (etc. Maps/Sample.txt): ")

    if not check_existing_file(file_name):
        if get_operating_system() == "nt":
            print("os clear")
        else:
            os_command("clear")
        print("File not found, try again")
        file_name = instruct_input("Enter path of map (etc. Maps/Sample.txt): ")

    return open(file_name, "rt")
def fetch_map():
    file = choose_map()
    print("check1")
    map = [list(row) for row in file.read().split("\n")]
    print(map)
    file.close()
    return map, len(map), len(map[0])

if __name__ == "__main__":
    run()