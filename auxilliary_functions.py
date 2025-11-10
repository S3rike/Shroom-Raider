from assets.final_state import *
from assets.tile_tags import *
import os
import sys
import copy

# global vars
game_state = {'pickup':False, 'holding':False, 'game_over':False, 'move':1}
mushroom_count = {'total':0, 'collected':0}
tile = {'prev':'', 'curr':'', 'next':''} # tile states for map updating

# rewrite aux functions
def choose_map():
    bool_invalid_input = False
    while True:
        clear_screen()
        show_list_maps()
        print(f'[P] To Refresh List')
        if bool_invalid_input:
            print(f"File Not found, Try Again")
        map_name = instruct_input("Enter Name Of Map: ")
        if map_name.upper() == 'R':
            bool_invalid_input = False
            continue
        file_name = f"maps/{map_name}.txt"
        if check_existing_file(file_name):
            clear_screen()
            return map_name        
        else:
            bool_invalid_input = True
def show_list_maps():
    curr_directory = os.getcwd()
    peek_folder = f'{curr_directory}/maps'
    map_list = [file.strip('.txt') for file in os.listdir(peek_folder) if os.path.isfile(os.path.join(peek_folder, file))]
    map_count = len(map_list)
    print(f"-------- Available Maps --------")
    for index in range(0, map_count,3):
        print(f"{map_list[index]}   {map_list[index + 1]}   {map_list[index + 2]}")
    print(f"--------------------------------\n")
    return None
def show_entire_map(session):
    print("\n--- Current Map ---\n")
    for row in session.map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print("".join(emoji_display))
    print("---------------------")
    return None
def check_pickable_object(action, holding_item, hidden_object):
    return action == 'P' and holding_item == False and hidden_object in pickable_items

def check_game_over(session):
    bool_check1 = session.mushroom_count['total'] == session.mushroom_count['collected']
    bool_check2 = session.game_state['drowning']
    bool_check3 = session.game_state['lost']
    return bool_check1 or bool_check2 or bool_check3

def check_movement(session, dest_row, dest_col, curr_row, curr_col): # dest means destination
    if pos_in_bounds(session.map_rows, session.map_cols, dest_row, dest_col):
        dest_tile = session.map[dest_row][dest_col]
    else:
        session.game_state['lost'] = True
        session.map[curr_row][curr_col] = session.player_hidden_object
        return None
    if dest_tile in movable_tiles:
        if dest_tile == '+':
            session.mushroom_count['collected'] += 1
            dest_tile = '.'
        modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
    elif dest_tile in pickable_items.keys():
        modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
    elif dest_tile in adjustable_tiles:
        to_row = dest_row - curr_row # directions of player
        to_col = dest_col - curr_col
        rock_dest_row = dest_row + to_row # where will rock go
        rock_dest_col = dest_col + to_col
        if pos_in_bounds(session.map_rows, session.map_cols, rock_dest_row, rock_dest_col): # rock in bounds
            rock_dest_tile = session.map[rock_dest_row][rock_dest_col]
            # If the tile the rock is moving to is valid
            if rock_dest_tile in {".", "-"}:
                session.boulder_hidden_objects[(rock_dest_row, rock_dest_col)] = rock_dest_tile
                session.map[rock_dest_row][rock_dest_col] = dest_tile
                dest_tile = session.boulder_hidden_objects[(dest_row, dest_col)]
                session.boulder_hidden_objects.pop((dest_row, dest_col))
                modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
            elif rock_dest_tile == '~':
                session.map[rock_dest_row][rock_dest_col] = '-' # replace water
                session.map[dest_row][dest_col] = session.boulder_hidden_objects[(dest_row, dest_col)]
                dest_tile = session.boulder_hidden_objects[(dest_row, dest_col)]
                session.boulder_hidden_objects.pop((dest_row, dest_col))
                modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
            else:
                session.game_state['error'] = True
        else:
            session.game_state['error'] = True
    elif dest_tile == '~':
        session.game_state['drowning'] = True
        session.map[curr_row][curr_col] = session.player_hidden_object
        session.player_hidden_object = '.'
    elif dest_tile == 'T':
        if session.game_state['holding']:
            use_held_item(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
        else:
            session.game_state['error'] = True
        ...
    else:
        pass #invalid but definitely will not be used
    return None

def use_held_item(session, dest_tile, dest_row, dest_col, curr_row, curr_col):
    if session.player_held_item == 'x':
        dest_tile = '.'
        modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
    elif session.player_held_item == '*':
        burn_adj_trees(session, dest_row, dest_col)
        session.map[curr_row][curr_col] = session.player_hidden_object
        session.map[dest_row][dest_col] = 'L'
        session.player_coords['row'] = dest_row
        session.player_coords['col'] = dest_col
    else:
        pass #invalid but definitely will not be used
    session.player_held_item = None
    session.game_state['holding'] = False
    return None

def burn_adj_trees(session, row, col):
    burn_stack = [(row, col)]
    checked_tiles = set()
    while burn_stack != []:
        tree_row, tree_col = burn_stack.pop()
        session.map[tree_row][tree_col] = '.'
        checked_tiles.add((tree_row, tree_col))
        burn_stack.extend(tuple(check_adj_trees(session, tree_row, tree_col)))
def check_adj_trees(session, row, col):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for shift_row, shift_col in directions:
        dest_row = row + shift_row
        dest_col = col + shift_col
        if pos_in_bounds(session.map_rows, session.map_cols, dest_row, dest_col):
            if session.map[dest_row][dest_col] == 'T':
                yield (dest_row, dest_col)
def modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col):
    session.map[curr_row][curr_col] = session.player_hidden_object
    session.player_hidden_object = dest_tile
    session.map[dest_row][dest_col] = 'L'
    session.player_coords['row'] = dest_row
    session.player_coords['col'] = dest_col
def pos_in_bounds(total_row, total_col, row, col):
    return (0 <= row < total_row) and (0 <= col < total_col)

def new_pos(action, player_row, player_col):
    dest_row, dest_col = player_row, player_col
    if action == 'W':
        dest_row -= 1
    elif action == 'S':
        dest_row += 1
    elif action == 'A':
        dest_col -= 1
    elif action == 'D':
        dest_col += 1
    return dest_row, dest_col
#-------------------------------------------------------------------
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

# Resets the map
def reset_map(current_map, original_map):
    game_state['holding'] = False
    game_state['pickup'] = False
    mushroom_count['collected'] = 0
    tile = {'prev':'', 'curr':'', 'next':''}
    current_map = copy.deepcopy(original_map)
    return current_map

#----------------------------------------------------------------
def show_game_over(map, mushroom_count):
    clear_screen()
    column = get_terminal_col_size()
    game_over_screen = game_over
    display_game_over = game_over_screen.splitlines()
    for line in display_game_over:
        print(line.center(column))
    print(f'However, you were able to collect {mushroom_count["collected"]} mushrooms!\n')
    for row in map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print(''.join(emoji_display))

def show_stage_clear(map, mushroom_count):
    clear_screen()
    column = get_terminal_col_size()
    stage_clear_screen = stage_clear
    display_stage_clear = stage_clear_screen.splitlines()
    # The issue with this is that it depends on the current terminal size
    for line in display_stage_clear:
        print(line.center(column))
    print(f'You have collected all {mushroom_count['total']} mushrooms!\n')
    for row in map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print(''.join(emoji_display))
    
def exit_terminal():
    return sys.exit()

def clear_screen():
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