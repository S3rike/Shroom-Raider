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
                # If user wants to play again reset the values in global dictionary
                if processed == 'Y':
                    game_state['pickup'] = False
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

                            # Check if the user has picked up an item
                            def check_item_pickup():
                                if game_state['pickup'] == True:
                                    print(f'You currently have an item')
                                else:
                                    # line about not having an item
                                    ...

                            # Check the number of mushrooms collected
                            def check_mushrooms_collected():
                                if game_state['mushrooms'] <= 1:
                                    print(f'You have collected {game_state['mushrooms']} mushrooms!')
                                else:
                                    print(f'You have collected {game_state['mushrooms']} mushrooms!')

                            check_item_pickup()
                            check_mushrooms_collected()
                            print("\nMove Up: [W]\nMove Left: [A]\nMove Down: [S]\nMove Right: [D]\n")
                            print(f'prev: {tile["prev"]}')
                            print(f'curr: {tile["curr"]}')

                            # Check if the user has picked up an item
                            def check_item_pickup():
                                if game_state['pickup'] == True:
                                    print(f'You currently have: {game_state['holding']}')
                                else:
                                    print(f'You currently do not have an item!')
                                    print(f'Pickup Item on Current Tile: [P]')
                                    ...

                            check_item_pickup()
                            print("\nCheck: Map & Controls Printed")
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

                            movable_tiles = {'.', '-', '+'} # Set of tiles that can be moved immediately
                            pickable_items = {'x', '*'} # Set of tiles that can be picked up
                            immovable_tiles = {'T', '~'} # Set of tiles that cannot be moved into
                            
                            if action == 'Q':
                                exit_terminal()

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
                                if game_state['pickup'] == False and tile['prev'] in pickable_items:
                                    game_state['pickup'] = True
                                    game_state['holding'] = tile['prev']
                                    tile['prev'] = '.'
                            else:
                                print("Invalid action. Try again.")
                                return game_map

                            # Checks the tile to be moved if valid
                            def check_tile_to_be_moved():
                                tile['next'] = game_map[new_row][new_col]
                                next_tile = tile['next']

                                # Checks if this is the first time moving
                                def check_curr_tile_state():
                                    if tile['curr'] == '':
                                        tile['curr'] = '.'
                                    else:
                                        tile['curr'] = tile['prev']

                                    tile['prev'] = tile['next']

                                if next_tile in (movable_tiles | pickable_items) :
                                    check_curr_tile_state()
                                    # Updates mushroom collected
                                    if next_tile == '+':
                                        tile['prev'] = '.'
                                        game_state['mushrooms'] += 1
                                        game_map[player_row][player_col] = tile['curr']
                                        game_map[new_row][new_col] = "L"
                                    
                                    # Update map upon moving
                                    else:
                                        game_map[player_row][player_col] = tile['curr']
                                        game_map[new_row][new_col] = 'L'


                                elif next_tile in immovable_tiles:
                                    # If the tile stepped into is water
                                    if game_map[new_row][new_col] == '~':
                                        game_state['game_over'] = True
                                        show_game_over()
                                    # If the tile stepped into is a tree
                                    elif game_map[new_row][new_col] == 'T':
                                        if game_state['pickup']: # has item
                                                                                    
                                            if game_state['holding'] == 'x': # axe, set tree to empty
                                                check_curr_tile_state()
                                                tile['prev'] = '.'
                                                game_map[player_row][player_col] = tile['curr']
                                                game_map[new_row][new_col] = "L"
                                            
                                            elif game_state['holding'] == '*': # flamethrower, check and destroy adj trees
                                                check_curr_tile_state()

                                                def burn_adj_trees(r_start, c_start):
                                                    r_max, c_max = len(game_map), len(game_map[0])

                                                    stack = [(r_start, c_start)]
                                                    checked = set([(r_start, c_start)])

                                                    while stack:
                                                        r, c = stack.pop()
                                                        game_map[r][c] = '.' # burn
                                                        # check neighbours
                                                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                                            nr, nc = r + dr, c + dc # check adj

                                                            if (0 <= nr < r_max) and (0 <= nc < c_max) and (game_map[nr][nc] == "T") and ((nr, nc) not in checked):
                                                                # idk how to make this shorter
                                                                checked.add((nr, nc))
                                                                stack.append((nr, nc))
                        
                                                burn_adj_trees(new_row, new_col)
                                                tile['prev'] = '.'
                                                game_map[player_row][player_col] = tile['curr']
                                                game_map[new_row][new_col] = "L"

                                            game_state['holding'] = False
                                            game_state['pickup'] = False

                                        else: # no item, so return to previous state
                                            game_map[player_row][player_col]

                            check_tile_to_be_moved()
                        
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
    game_state = {'pickup':False, 'holding':False, 'game_over':False, 'mushrooms':0, 'move':1}
    item = {'x':False, '*':False}
    tile = {'prev':'', 'curr':'', 'next':''}
    
    run()