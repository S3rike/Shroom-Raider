from auxilliary_functions import *

def clear_screen_helper():
    if get_operating_system() == "nt":
        print("os clear")
    else:
        os_command("clear")

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
            current_map = play_game(current_map)

            # todo check for game over or in diff func
    return None

def display(show_map):
    clear_screen_helper()
    print("\n--- Current Map ---")
    for row in show_map:
        print("".join(row))
    print("---------------------")
    print("Move Up: [W/U]\nMove Left: [A/L]\nMove Down:[S/D]\nMove Right:[D/R]\n")
    print("Pickup Item on Current Tile: [P]")
    print("Check: Map & Controls Printed")
    return None

def menu():
    print("Check: Menu Loaded")
    choice = instruct_input("Play Again? (Y/N): ")
    processed = choice.strip().upper()
    if processed == 'Y':
        return True
    elif processed == 'N':
        return False
    else: # todo add invalid check
        pass

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
    print("Check: Map Chosen")
    map = [list(row) for row in file.read().split("\n")]
    file.close()
    return map, len(map), len(map[0])
    
def play_game(game_map):
    def player_pos(game_map, player_char="R"):
        for row_index, row_list in enumerate(game_map):
            for col_index, cell_char in enumerate(row_list):
                if cell_char == player_char:
                    return (row_index, col_index)
        

    player_row, player_col = player_pos(game_map)
    print(f"You are at ({player_row}, {player_col})\n")
    action = instruct_input("Enter your next action: ").upper()
    if action == 'Q':
        return None

    # todo deal with invalid actions, chained actions
    # according to sir jerome @ cs11 discord, only choose 1 between WASD or UDLR
    new_row, new_col = player_row, player_col
    if action == 'W':
        new_row -= 1
    elif action == 'S':
        new_row += 1
    elif action == 'A':
        new_col -= 1
    elif action == 'D':
        new_col += 1
    else:
        print("Invalid action. Try again.")
        return game_map
    # going up from top loops around
    # going down from bottom crashes
    game_map[player_row][player_col] = "." # todo account for running over different tiles
    game_map[new_row][new_col] = "R"

    return game_map

if __name__ == "__main__":
    run()