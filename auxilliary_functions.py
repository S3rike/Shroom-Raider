import os
import sys
from assets.final_state import game_over
from assets.final_state import stage_clear

# global vars
movable_tiles = {'.', '-', '+'} # Set of tiles that can be moved immediately
pickable_items = {'x': "Axe", '*': "Flamethrower"} # Set of tiles that can be picked up
immovable_tiles = {'T', '~'} # Set of tiles that cannot be moved into
adjustable_tiles = {'R'}
game_state = {'pickup':False, 'holding':False, 'game_over':False, 'move':1}
mushroom_count = {'total':0, 'collected':0}
tile = {'prev':'', 'curr':'', 'next':''} # tile states for map updating
tile_ui = {'L':'🧑', '.':'　', 'T':'🌲', '+':'🍄', 'R':'🪨', '~':'🟦', '-':'⬜', 'x':'🪓', '*':'🔥'}

def new_pos(action, player_row, player_col):
    new_row, new_col = player_row, player_col
    if action == 'W':
        new_row -= 1
    elif action == 'S':
        new_row += 1
    elif action == 'A':
        new_col -= 1
    elif action == 'D':
        new_col += 1
    return new_row, new_col

# Get player position
def player_pos(game_map, player_char):
    for row_index, row_list in enumerate(game_map):
        for col_index, cell_char in enumerate(row_list):
            if cell_char == player_char:
                return (row_index, col_index)
            
def check_tile_to_be_moved(game_map, new_row, new_col, player_row, player_col):
    tile['next'] = game_map[new_row][new_col]
    next_tile = tile['next']
    # Checks if this is the first time moving
    def check_curr_tile_state():
        if tile['curr'] == '':
            tile['curr'] = '.'
        else:
            tile['curr'] = tile['prev']
        tile['prev'] = tile['next']
    if next_tile in (movable_tiles | pickable_items.keys()) :
        check_curr_tile_state()

        # Updates mushroom collected
        if next_tile == '+':
            tile['prev'] = '.'
            mushroom_count['collected'] += 1
            game_map[player_row][player_col] = tile['curr']
            game_map[new_row][new_col] = "L"

            # If the mushroom collected is equal to the total then show stage clear
            # This can be modified depending on how we'll proceed onwards
            if mushroom_count['collected'] == mushroom_count['total']:
                game_state['game_over'] = True
                show_stage_clear()
        
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
                return
    
    elif next_tile in adjustable_tiles:
        if game_map[new_row][new_col] == 'R': # tile is rock
            to_row = new_row - player_row # directions of player
            to_col = new_col - player_col
            rock_to_row = new_row + to_row # where will rock go
            rock_to_col = new_col + to_col

            if (0 <= rock_to_row < len(game_map)) and (0 <= rock_to_col < len(game_map[0])): # rock in bounds
                rock_to_tile = game_map[rock_to_row][rock_to_col]

                # If the tile the rock is moving to is valid
                if rock_to_tile in (".", "-", "~"):
                    if tile['curr'] == '': # set under rock to '.'
                        tile['curr'] = '.'
                    else:
                        tile['curr'] = tile['prev']

                    if rock_to_tile == '~':
                        game_map[rock_to_row][rock_to_col] = '-' # replace water
                    else:
                        game_map[rock_to_row][rock_to_col] = 'R' # replace previous
                # If the tile to pushed to is invalid do nothing
                else:
                    return
            else:
                return # rock not in bounds

            game_map[player_row][player_col] = tile['curr']
            game_map[new_row][new_col] = 'L'
    
    return None

def show_game_over():
    column = get_terminal_col_size()
    # I commented this part since we need to display the game map and the amount of mushrooms collected
    # clear_screen_helper()
    game_over_screen = game_over
    display_game_over = game_over_screen.splitlines()
    # The issue with this is that it depends on the current terminal size
    for line in display_game_over:
        print(line.center(column))
    

def show_stage_clear():
    column = get_terminal_col_size()
    # I commented this part since we need to display the game map and the amount of mushrooms collected
    # clear_screen_helper()
    stage_clear_screen = stage_clear
    display_stage_clear = stage_clear_screen.splitlines()
    # The issue with this is that it depends on the current terminal size
    for line in display_stage_clear:
        print(line.center(column))

def exit_terminal():
    return sys.exit()

def clear_screen_helper():
    if get_operating_system() == "nt":
        os_command("cls")
    else:
        os_command("clear")

def instruct_input(input_text):
    return input(input_text)

def get_operating_system():
    return os.name

def check_existing_file(file_name):
    return os.path.exists(file_name)

# If we want to get the terminal size row and col just call os.get_terminal_size()
def get_terminal_col_size():
    return os.get_terminal_size()[0]

def os_command(command):
    return os.system(command)

def error():
    '''
    If incorrectly running this file
    will add later
    '''
    ...
if __name__ == "__main__":
    error()