from auxilliary_functions import *

# Main function that houses all the functions
def run():
    clear_screen_helper()
    print("start")
    while True: 
        game_status = menu()

        if not game_status: 
            break
        # setup
        current_map = fetch_map()
        game_over = False

        while not game_over:
            # If the player stepped into water the current_map returns None
            if current_map == None:
                print('\nGame over\n')
                game_over = True
            else:
                display(current_map)
                current_map = play_game(current_map)

        # todo check for game over or in diff func
    return None

# Display the map from fetch_maps
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

# Gets input from user if they want to continue, loop for invalid input
def menu():
    print("Check: Menu Loaded")
    choice = instruct_input("Play Again? (Y/N): ")
    processed = choice.strip().upper()
    if processed == 'Y':
        return True
    elif processed == 'N':
        return False
    else:
        clear_screen_helper()
        return menu()

# Option A for choose_map() --- no limit
# Get map file from user and open it
'''
def choose_map():
    clear_screen_helper()
    file_name = instruct_input("Enter path of map (etc. Maps/Sample.txt): ")

    # I think we should just limit the amount of tries they enter invalid inputs
    while not check_existing_file(file_name):
        clear_screen_helper()
        print("File not found, try again")
        file_name = instruct_input("Enter path of map (etc. Maps/Sample.txt): ")

    return open(file_name, "rt")
'''
# Option B for choose_map() --- there's a limit
# Option when we want to limit the amount of tries for entering the map file
def choose_map():
    retries = 0
    max_retries = 2
    success = False

    clear_screen_helper()
    file_name = instruct_input("Enter path of map (etc. maps/map1.txt): ")

    # If file exists return it using open
    if check_existing_file(file_name):
        return open(file_name, 'rt')
    
    # Else, test it until it reaches three tries
    else:
        while retries < max_retries and not success:
            try:
                open(file_name, 'rt')
                if check_existing_file(file_name):
                    success = True
                    
            except FileNotFoundError:
                retries += 1
                clear_screen_helper()
                print(f"File not found, try again. You have {3 - retries} tries left")
                file_name = instruct_input("Enter path of map (etc. maps/map1.txt): ")

        if success:
            return open(file_name, 'rt')
        else:
            print('Sorry, you have reached the limit. Please try again.')
            exit_terminal()
        
# Return the map as a list
def fetch_map():
    file = choose_map()
    print("Check: Map Chosen")
    map = [list(row) for row in file.read().split("\n")]
    file.close()
    return map

# Get player position
def player_pos(game_map, player_char):
    for row_index, row_list in enumerate(game_map):
        for col_index, cell_char in enumerate(row_list):
            if cell_char == player_char:
                return (row_index, col_index)

# Update map depending on user input
def play_game(game_map):
    player_char = "L"
    player_row, player_col = player_pos(game_map, player_char)
    print(f"You are at ({player_row}, {player_col})\n")
    action = instruct_input("Enter your next action: ").upper()

    # If we want to directly quit terminal we could call this function,
    # however, if we want to load back to menu, we need to find a way to break
    # out of the nested loops and get away with the data types
    if action == 'Q':
        exit_terminal()

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

    # If the tile stepped into is water
    if game_map[new_row][new_col] == '~':
        return
    # If the tile stepped into is a tree, return to current state
    elif game_map[new_row][new_col] == 'T':
        game_map[player_row][player_col]
    # If the tile stepped into is empty, proceed
    else:
        game_map[player_row][player_col] = "." # todo account for running over different tiles
        game_map[new_row][new_col] = "L"

    return game_map

if __name__ == "__main__":
    run()