# Imports From Standard Libraries And Assets Used
from assets.final_state import *
from assets.tile_tags import *
from assets.sound_paths import *
from assets.screen_display_text import *
from playsound3 import playsound
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from wcwidth import wcswidth
import os
import sys
import time

def play_sound(action_type):
    try:
        return playsound(f"assets/audio/{sound_files[action_type]}", block=False)
    except:
        return None
def stop_sound(curr_playing):
    if curr_playing != None:
        curr_playing.stop()
    return None

def save_to_leaderboard(self, name_input, completion_time):
    map_leaderboard_file = f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}_leaderboard.txt"
    time_of_save = time.strftime("%d - %b - %Y %H:%M")
    with open(map_leaderboard_file, 'a') as f:
        f.write(f'{name_input} | {format_completion_time(completion_time)} | {time_of_save}\n')
    ...

def format_completion_time(completion_time):
    completion_hours = int(completion_time // 3600)
    completion_mins = int(completion_time % 3600)
    completion_seconds = completion_time % 60
    if completion_hours > 0:
        return f"{completion_hours}:{completion_mins:02d}:{completion_seconds:05.2f}"
    else:
        return f"{completion_mins}:{completion_seconds:05.2f}"

# Functions For User Choosing Maps
def choose_map():
    curr_playing = play_sound('menu')
    bool_invalid_input = False
    while True:
        clear_screen()
        show_list_maps()
        print(f'[R] To Refresh List       [Q] To Quit Game')
        if curr_playing == None: print(f"Audio Backend Not Available")
        if bool_invalid_input: print(f"File Not found, Try Again")
        map_name = instruct_input("Enter Name Of Map: ")
        if map_name.upper() == 'R':
            bool_invalid_input = False
            continue
        elif map_name.upper() == 'Q':
            exit_terminal()
        else:
            file_name = f"maps/{map_name}.txt"
            if check_existing_file(file_name):
                stop_sound(curr_playing)
                clear_screen()
                return map_name        
            else:
                bool_invalid_input = True

def return_map_list():
    curr_directory = get_current_directory()
    peek_folder = get_joint_path(curr_directory, 'maps')
    map_list = [file.strip('.txt') for file in os.listdir(peek_folder) if os.path.isfile(os.path.join(peek_folder, file))]
    return map_list

def show_list_maps():
    curr_directory = get_current_directory()
    peek_folder = get_joint_path(curr_directory, 'maps')
    map_list = [file.strip('.txt') for file in os.listdir(peek_folder) if os.path.isfile(os.path.join(peek_folder, file))]
    map_count = len(map_list)
    print(f"-------- Available Maps --------")
    for index in range(0, map_count,3):
        print(f"{map_list[index]}   {map_list[index + 1]}   {map_list[index + 2]}")
    print(f"--------------------------------\n")
    return None

# Checks For Valid Inputs
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
        session.latest_action = 'water'
        return None
    if dest_tile in movable_tiles:
        if dest_tile == '+':
            session.mushroom_count['collected'] += 1
            dest_tile = '.'
            session.latest_action = 'pick'
        else:
            session.latest_action = 'move'
        modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
    elif dest_tile in pickable_items.keys():
        session.latest_action = 'move'
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
                session.latest_action = 'push'
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
        session.latest_action = 'water'
        session.game_state['drowning'] = True
        session.map[curr_row][curr_col] = session.player_hidden_object
        session.player_hidden_object = '.'
    elif dest_tile == 'T':
        if session.game_state['holding']:
            use_held_item(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
        else:
            session.game_state['error'] = True
    else:
        pass #invalid but definitely will not be used
    return None

# Using Items
def use_held_item(session, dest_tile, dest_row, dest_col, curr_row, curr_col):
    if session.player_held_item == 'x':
        dest_tile = '.'
        session.latest_action = 'cut'
        modify_movement(session, dest_tile, dest_row, dest_col, curr_row, curr_col)
    elif session.player_held_item == '*':
        burn_adj_trees(session, dest_row, dest_col)
        session.latest_action = 'burn'
        session.map[curr_row][curr_col] = session.player_hidden_object
        session.map[dest_row][dest_col] = 'L'
        session.player_coords['row'] = dest_row
        session.player_coords['col'] = dest_col
    else:
        pass #invalid but definitely will not be used
    session.player_held_item = None
    session.game_state['holding'] = False
    return None

# Flamethrower Functions
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

# Movement methods due to being redundant
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

# Showing Game State
def show_entire_map(session):
    print("\n--- Current Map ---\n")
    for row in session.map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print("".join(emoji_display))
    print("---------------------")
    return None

def show_game_over(map, mushroom_count, mins_taken, seconds_taken, completion_time):
    play_sound('game_over')
    clear_screen()
    column = get_terminal_col_size()
    game_over_screen = game_over
    display_game_over = game_over_screen.splitlines()
    for line in display_game_over:
        print(line.center(column))
    print(f'However, you were able to collect {mushroom_count["collected"]} mushrooms!\n')
    print(f'You played for {mins_taken} minutes and {seconds_taken} seconds.')
    print(f'Full time: {format_completion_time(completion_time)}\n')
    for row in map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print(''.join(emoji_display))

def show_stage_clear(self, mins_taken, seconds_taken, completion_time):
    play_sound('win')
    clear_screen()
    column = get_terminal_col_size()
    stage_clear_screen = stage_clear
    display_stage_clear = stage_clear_screen.splitlines()
    for line in display_stage_clear:
        print(line.center(column))
    print(f'You collected all {self.mushroom_count['total']} mushrooms!\n')
    print(f'You played for {mins_taken} minutes and {seconds_taken} seconds.')
    print(f'Full time: {format_completion_time(completion_time)}\n')
    for row in self.map:
        emoji_display = [tile_ui.get(tile, tile) for tile in row]
        print(''.join(emoji_display))
    name_input = instruct_input("\nEnter name for leaderboard: ")
    save_to_leaderboard(self, name_input, completion_time)

# System Commands
def exit_terminal():
    clear_screen()
    return sys.exit()

def clear_screen():
    if get_operating_system() == "nt":
        os_command("cls")
    else:
        os_command("clear")

def instruct_input(input_text):
    while True:
        try:
            return input(input_text)
        except:
            pass

def get_operating_system():
    return os.name

def get_current_directory():
    return os.getcwd()

def create_directory(name):
    os.mkdir(name)
    return None

def get_joint_path(*paths):
    file = ""
    for line in paths:
        file = os.path.join(file, line)
    return file

def check_existing_file(file_name):
    return os.path.exists(file_name)
def get_terminal_row_size():
    return os.get_terminal_size().lines
def get_terminal_col_size():
    return os.get_terminal_size().columns
def os_command(command):
    return os.system(command)

# Showing game intro and ending displays 
TERMINAL_WIDTH = get_terminal_col_size()
TERMINAL_LENGTH = get_terminal_row_size()

console = Console(width=TERMINAL_WIDTH)

# Stylize text depending on num parity
def stylize_text(list_text, num):
    text = Text(list_text[num])
    text.stylize("bold red on white" if num % 2 == 0 else "italic")
    return text

# Clear screen to show only up to two phrases
def clear_screen_if_needed(num):
    if num % 2 == 0:
        os_command('cls' if get_operating_system() == 'nt' else 'clear')

# Check the display width
def check_display_width(list_text, num):
    display_width = wcswidth(list_text[num])
    # For more information check out this link
    # https://wcwidth.readthedocs.io/en/latest/intro.html#wcwidth-wcswidth
    if display_width < 0:
        return len(list_text[num])
    else:
        return display_width
    
# Print horizontal padding
def print_horizontal_padding(num, padding_h):
    if num % 2 == 0:
        print('\n' * padding_h)

# Add a typewriter effect
def typewriter_effect(list_text):
    padding_h = (TERMINAL_LENGTH - 2) // 2

    for num in range(len(list_text)):
        clear_screen_if_needed(num)
        print_horizontal_padding(num, padding_h)

        padding_v = (TERMINAL_WIDTH - check_display_width(list_text, num)) // 2

        text_in_list = stylize_text(list_text, num)
        sys.stdout.write(" " * padding_v)
        sys.stdout.flush()

        for char in text_in_list:
            console.print(char, end="")
            sys.stdout.flush()
            if num % 2 == 0:
                time.sleep(0.2)
            else:
                time.sleep(0.15)
        print()
        time.sleep(3)

def display_intro():
    typewriter_effect(INTRO_QUOTES)
    os_command('cls' if get_operating_system() == 'nt' else 'clear')
    console.print(SHROOM_RAIDER_SIGN, style="red", justify="center")
    time.sleep(4.5)

# What Will Happen If User Runs This File
def error():
    '''
    If incorrectly running this file
    will add later
    '''
    ...
if __name__ == "__main__":
    error()