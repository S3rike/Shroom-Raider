###########################################################
# Note: This version has nested function definitions      #
# (visualizes the outline of the code to avoid confusion) #
###########################################################

from auxilliary_functions import *
from assets.gameover import game_over_text

# While the game is running run this function
def run():
    clear_screen_helper()
    print("start")
    while True:
        # Return list of rows in map
        def fetch_map():
            # Enter map file and return the file object
            def choose_map():
                clear_screen_helper()
                attempts = 0
                # Limit the number of tries that a person could enter map file 
                def limit_tries(n):
                    file_name = instruct_input("Enter path of map (etc. Maps/Sample.txt): ")

                    if check_existing_file(file_name):
                        clear_screen_helper()
                        return open(file_name, 'rt')
                    
                    else:
                        # Limit it to three tries
                        if n == 2:
                            print('Sorry, you have reached the limit. Please try again.')
                            exit_terminal()
                        else:
                            clear_screen_helper()
                            n += 1
                            print(f"File not found, try again. You have {3 - n} tries left")
                            limit_tries(n)

                raw_file = limit_tries(attempts)
                return raw_file
            
            file = choose_map()
            print("Check: Map Chosen")
            map = [list(row) for row in file.read().split("\n")]
            file.close()
            return map

        # The menu function houses all the functions of the game
        def menu():
            print("Check: Menu Loaded")
            choice = instruct_input("Play Again? (Y/N): ")
            processed = choice.strip().upper()

            # Boolean that checks whether a player wants to play again
            def play_again():
                if processed == 'Y':
                    game_state['game_over'] = False
                    game_state['mushrooms'] = 0
                    return True
                elif processed == 'N':
                    return False
                else:
                    clear_screen_helper()
                    menu()

            if play_again():
                current_map = fetch_map()
                while not game_state['game_over']:
                    # If the player stepped into water the current_map returns None
                    if current_map == None:
                        show_game_over()
                        game_state['game_over'] = True
                    else:
                        # Display the map from fetch_maps
                        def display(show_map):
                            clear_screen_helper()
                            print("\n--- Current Map ---\n")
                            for row in show_map:
                                print("".join(row))
                            print("---------------------")

                            def check_item_pickup():
                                if game_state['pickup'] == True:
                                    print(f'You currently have an item')

                            def check_mushrooms_collected():
                                if game_state['mushrooms'] <= 1:
                                    print(f'You have collected {game_state['mushrooms']} mushroom!')
                                else:
                                    print(f'You have collected {game_state['mushrooms']} mushrooms!')

                            check_item_pickup()
                            check_mushrooms_collected()
                            print("Move Up: [W/U]\nMove Left: [A/L]\nMove Down:[S/D]\nMove Right:[D/R]\n")
                            print("Pickup Item on Current Tile: [P]")
                            print("Check: Map & Controls Printed")
                            return None

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

                            if action == 'Q':
                                exit_terminal()

                            # todo deal with invalid actions, chained actions
                            new_row, new_col = player_row, player_col
                            if action == 'W':
                                new_row -= 1
                            elif action == 'S':
                                new_row += 1
                            elif action == 'A':
                                new_col -= 1
                            elif action == 'D':
                                new_col += 1
                            elif action == 'P':
                                if game_state['pickup'] != True:
                                    game_state['pickup'] = True
                                else:
                                    game_state['pickup'] = False
                            else:
                                print("Invalid action. Try again.")
                                return game_map
                            
                            # Track the type of tile on the new space to move so that when it moves 
                            # It gets reverted to its original state
                            prev_state_tile = game_map[new_row][new_col]

                            # If the tile stepped into is water
                            if game_map[new_row][new_col] == '~':
                                return
                            # If the tile stepped into is a tree, return to current state
                            elif game_map[new_row][new_col] == 'T':
                                game_map[player_row][player_col]
                            # Updates mushroom collected
                            elif game_map[new_row][new_col] == '+':
                                game_state['mushrooms'] += 1
                                game_map[player_row][player_col] = "."
                                game_map[new_row][new_col] = "L"
                            # If the tile stepped into is empty, proceed
                            else:
                                game_map[player_row][player_col] = "." # todo account for running over different tiles
                                game_map[new_row][new_col] = "L"

                            return game_map

                        # Show game over screen
                        def show_game_over():
                            column = get_terminal_col_size()
                            clear_screen_helper()
                            game_over_screen = game_over_text
                            display_game_over = game_over_screen.splitlines()
                            # The issue with this is that it depends on the current terminal size
                            for line in display_game_over:
                                print(line.center(column))

                        display(current_map)
                        current_map = play_game(current_map)
            else:
                exit_terminal()

        menu()

if __name__ == "__main__":
    game_state = {'pickup':False, 'game_over':False, 'mushrooms':0}
    item = {'x':False, '*':False}
    run()