###########################################################
# Note: This version has nested function definitions      #
# (visualizes the outline of the code to avoid confusion) #
###########################################################

from auxilliary_functions import *

game_over = False
player_char = "L"

# While the game is running run this function
def run():
    clear_screen_helper()
    while True:
        # Return list of rows in map
        def fetch_map():
            # Enter map file and return the file object
            def choose_map():
                clear_screen_helper()
                attempts = 0
                # Limit the number of tries that a person could enter map file 
                def limit_tries(n):
                    map_name = instruct_input("Enter name of the map: ")
                    file_name = f"maps/{map_name}.txt"

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
            map = [list(row) for row in file.read().split("\n")]
            for row in map:
                for element in row:
                    if element == '+':
                        mushroom_count['total'] += 1
            file.close()
            return map

        # The menu function houses all the functions of the game
        def menu():

            # Boolean that checks whether a player wants to play again
            def play_again(processed):
                # If user wants to play again reset the values in global dictionary
                if processed == 'Y':
                    game_state['pickup'] = False
                    game_state['game_over'] = False
                    mushroom_count['total'], mushroom_count['collected'] = 0, 0
                    return True
                elif processed == 'N':
                    return False
                else:
                    clear_screen_helper()
                    return None
                
            res = None
            while res is None:
                choice = instruct_input("Play again? (Y/N): ")
                processed = choice.strip().upper()
                res = play_again(processed)
                if res is None:
                    clear_screen_helper()

            if res:
                current_map = fetch_map()
                while True:
                    if not game_state['game_over']:
                        # Display the map from fetch_maps
                        def display(show_map):
                            clear_screen_helper()
                            print("\n--- Current Map ---\n")
                            for row in show_map:
                                emoji_display = [tile_ui.get(tile, tile) for tile in row]
                                print("".join(emoji_display))
                            print("---------------------")

                            # check mushrooms collected
                            def check_mushrooms_collected():
                                if mushroom_count['collected'] <= 1: # set to when all collected
                                    print(f'You have collected {mushroom_count['collected']} mushrooms!\n')
                                else:
                                    print(f'You have collected {mushroom_count['collected']} mushrooms!\n')
                            check_mushrooms_collected()

                            # check if item picked up
                            def check_item_pickup():
                                if game_state['pickup'] == True:
                                    print(f'You currently have: {pickable_items[game_state['holding']]}')
                                elif tile['prev'] in pickable_items.keys():
                                    print(f'There is a {pickable_items[tile['prev']]} below you! Input [P] to pick it up!')
                                else:
                                    print(f'You currently do not have an item!')
                                    ...
                            check_item_pickup()

                            print("\nMove Up: [W]\nMove Left: [A]\nMove Down: [S]\nMove Right: [D]")
                            print("\nTo quit: [!]")

                            return None

                        # Update map depending on user input
                        def play_game(game_map):
                            player_row, player_col = player_pos(game_map, player_char)
                            actions = instruct_input("Enter your next action: ").upper()

                            for action in actions:
                                if action not in ("!", "P", "W", "A", "S", "D"):
                                    break
                                elif action == "!":
                                    exit_terminal()
                                elif action == 'P':
                                    if game_state['pickup'] == False and tile['prev'] in pickable_items:
                                        game_state['pickup'] = True
                                        game_state['holding'] = tile['prev']
                                        tile['prev'] = '.'
                                    else:
                                        print("Invalid action. Try again.")
                                elif action in ("W", "A", "S", "D"):
                                    player_row, player_col = player_pos(game_map, player_char) # recalls for chain movement
                                    new_row, new_col = new_pos(action, player_row, player_col)
                                    check_tile_to_be_moved(game_map, new_row, new_col, player_row, player_col)

                                else:
                                    print(f"Skipping invalid action: {action}")
                            return game_map

                        display(current_map)
                        current_map = play_game(current_map)
                    if game_state['game_over']:
                        break
            else:
                exit_terminal()

        menu()

if __name__ == "__main__":
    run()