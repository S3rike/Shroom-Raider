from auxilliary_functions import *

def run():
    print("start")
    while(True): 
        game_status = menu()
        if not game_status: 
            break
        
    # setup
    current_map, row, column = fetch_map()
    game_over = False

    while not game_over:
        display(current_map)
        play_game(current_map)

        # todo check for game over? or in diff func?
    return None

def display(show_map):
    print("\n--- Current Map ---")
    for row in show_map:
        print("".join(row))
    print("---------------------")
    print("Check: Printed")
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
    file.close()
    return map, len(map), len(map[0])
    
def play_game():
    action = instruct_input("Enter your next action: ")
    print(action)
    return None

if __name__ == "__main__":
    run()