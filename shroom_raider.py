# Import functions to be used
from auxilliary_functions import *

class Game:
    # Initializations
    def __init__(self, file_name):
        self.file_name = file_name
        self.map = list()
        self.map_rows = 0
        self.map_cols = 0
        self.player_coords = {'row': 0, 'col': 0} #col is column
        self.player_held_item = None
        self.player_hidden_object = '.'
        self.boulder_hidden_objects = dict()
        self.mushroom_count = {'total': 0, 'collected': 0}
        self.game_state = {'holding':False, 'drowning':False, 'lost':False, 'error':False}
        self.debug = None
        self.restart_game = True
        self.latest_action = None
        self.start_time = None
        self.pause_time = None # for save_states
        self.end_time = None
    # Basically int(main) 
    def run_game(self):
        self.initial_session()
        while self.restart_game:
            self.save_game()
            self.play_game()
            self.show_result()
            self.restart_game = self.restart()
        return None
    
    # Either Loads Base Map File or Previous Save State
    def initial_session(self):
        folder = get_joint_path(get_current_directory(),'saved_states')
        save_file = get_joint_path(folder,f'{self.file_name[0::2]}{self.file_name[1::2]}.txt')
        bool_check = False
        if check_existing_file(save_file.strip()):
            bool_check = self.get_bool_input(f'Save File Detected.\nRun Save [Y/N]: ')
        try:
            if bool_check:
                self.fetch_save()
            else:
                self.fetch_map()
        except:
            self.debug = f'Save File Is Corrupted. Loading Base Map'
            self.fetch_map()

    # Loads Base Map File
    def fetch_map(self):
        self.start_time = time.time()
        self.pause_time = 0
        self.map = list()
        self.boulder_hidden_objects = dict()
        self.mushroom_count = {'total': 0, 'collected': 0}
        self.game_state = {'holding':False, 'drowning':False, 'lost':False, 'error':False}
        file = open(f"maps/{self.file_name}.txt", 'rt')
        for y_coord, tile_row in enumerate(file):
            self.map.append(list(tile_row))
            for x_coord, tile_char in enumerate(tile_row):
                if tile_char == 'L':
                    self.player_coords['row'] = y_coord
                    self.player_coords['col'] = x_coord
                    self.player_hidden_object = '.'
                    self.player_held_item = None
                elif tile_char == 'R':
                    self.boulder_hidden_objects[(y_coord, x_coord)] = '.'
                elif tile_char == '+':
                    self.mushroom_count['total'] += 1
                else:
                    pass
        file.close()
        self.map_rows = len(self.map)
        self.map_cols = len(self.map[0]) - 1
        return None
    
    # Saves Game State To A txt File
    def save_game(self):
        try:
            file = open(f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}.txt", 'w')
        except FileNotFoundError:
            create_directory("saved_states")
            file = open(f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}.txt", 'w')
        elapsed_time = 0
        if self.start_time:
            elapsed_time = time.time() - self.start_time - self.pause_time
        file.write(f"{self.map_rows} {self.map_cols}\n")
        file.write(f"{self.player_coords['row']} {self.player_coords['col']}\n")
        file.write(f"{self.player_held_item} {self.player_hidden_object}\n")
        file.write(f"{self.mushroom_count['total']} {self.mushroom_count['collected']}\n")
        file.write(f"{int(self.game_state['holding'])} {int(self.game_state['drowning'])}\n")
        file.write(f"{int(self.game_state['lost'])} {0}\n")
        file.write(f"{int(self.restart_game)}\n")
        file.write(f"{elapsed_time}\n")
        for tile_line in self.map[:-1]:
            row = tile_line[0]
            for char in tile_line[1:-1]:
                row = f'{row} {char}' 
            row = f'{row} \n'
            file.write(row)
        tile_line = self.map[-1]
        row = tile_line[0]
        for char in tile_line[1:]:
            row = f'{row} {char}' 
        row = f'{row} \n'
        file.write(row)
        for boulder_coords in self.boulder_hidden_objects.items():
            loc, char = boulder_coords
            x, y = loc
            file.write(f'{x} {y} {char}\n')
        file.close()
        return None
    
    # Loads Saved State
    def fetch_save(self):
        saved_elapsed_time = 0
        self.map = list()
        self.boulder_hidden_objects = dict()
        file = open(f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}.txt", 'rt')
        for row, line in enumerate(file):
            if row == 0:
                self.map_rows, self.map_cols = map(int, line.strip().split(" "))
            elif row == 1:
                self.player_coords['row'], self.player_coords['col'] = map(int, line.strip().split(" "))
            elif row == 2:
                self.player_held_item, self.player_hidden_object = line.strip().split(" ")
            elif row == 3:
                self.mushroom_count['total'], self.mushroom_count['collected'] = map(int, line.strip().split(" "))
            elif row == 4:
                self.game_state['holding'], self.game_state['drowning'] = map(int, line.strip().split(" "))
            elif row == 5:
                self.game_state['lost'], self.game_state['error'] = map(int, line.strip().split(" "))
            elif row == 6:
                self.restart_game = bool(line.strip())
            elif row == 7:
                try:
                    saved_elapsed_time = float(line.strip())
                except ValueError:
                    saved_elapsed_time = 0
            elif 7 < row <= self.map_rows + 7:
                self.map.append(list(line.split(" ")))
            else:
                x, y, char = line.strip().split(' ')
                self.boulder_hidden_objects.update({(int(x),int(y)): char})
        file.close()

        self.start_time = time.time() # reset timer after fetching save
        self.pause_time = -saved_elapsed_time # negative so subtracted at final calculation

        return None
    
    # The actual int(main) but runs for each move of the user
    def play_game(self):
        while True:
            self.display()
            self.player_input()
            if check_game_over(self):
                break
        return None
    # Main Sreen During Session
    def display(self):
        clear_screen()
        show_entire_map(self)
        if self.start_time:
            elapsed = time.time() - self.start_time - self.pause_time
            mins = int(elapsed // 60)
            seconds = int(elapsed % 60)
            print(f'Time Elapsed: {mins:02d}:{seconds:02d}\n')
        print(f'You have collected {self.mushroom_count['collected']} mushrooms!\n')
        if self.game_state['holding']:
            print(f'You currently have: {pickable_items[self.player_held_item]}')
        elif self.player_hidden_object in pickable_items.keys():
            print(f'There is a {pickable_items[self.player_hidden_object]} below you! Input [P] to pick it up!')
        else:
            print(f'You currently do not have an item!')
        print("\nMove Up: [W]\nMove Left: [A]\nMove Down: [S]\nMove Right: [D]")
        print(f"\nTo Reset: [!]  To Quit: [Q]  To Save: [F]")
        return None
    
    # Validates and Runs User Inputs
    def player_input(self):
        if check_game_over(self): # Only occurs during backup of a finished session
            return None
        if self.debug != None:
            print(self.debug)
            self.debug = None
        if self.game_state['error']:
            print(f"Invalid Action")
            self.game_state['error'] = False
        actions = instruct_input("Enter your next action: ").upper()
        self.latest_action = None
        for action in actions:
            # Found in auxilliary_functions
            if check_game_over(self):
                break
            elif self.game_state['error']:
                break
            elif action == "P":
                if check_pickable_object(action, self.game_state['holding'], self.player_hidden_object):
                    self.game_state['holding'] = True
                    self.player_held_item = self.player_hidden_object
                    self.player_hidden_object = '.'
                    self.latest_action = 'pick'
                else:
                    pass
            elif action in ("W", "A", "S", "D"):
                # Found in auxilliary_functions
                dest_row, dest_col = new_pos(action, self.player_coords['row'], self.player_coords['col'])
                check_movement(self, dest_row, dest_col, self.player_coords['row'], self.player_coords['col'])
            elif action == 'Q':
                exit_terminal()
            elif action == "!":
                self.fetch_map()
                self.latest_action = None
            elif action == 'F':
                self.save_game()
                self.latest_action = None
            else:
                print(f"Invalid Action Found: {action}")
                break
        if self.latest_action and not check_game_over(self):
            play_sound(self.latest_action)
        return None
    
    # Shows Possible Ending Game States
    def show_result(self):
        completion_time = time.time() - self.start_time - self.pause_time
        mins_taken = int(completion_time // 60)
        seconds_taken = int(completion_time % 60)
        self.save_game()
        if self.mushroom_count['total'] == self.mushroom_count['collected']:
            clear_screen()
            show_stage_clear(self, mins_taken, seconds_taken, completion_time)
        elif self.game_state['drowning']:
            clear_screen()
            show_game_over(self.map, self.mushroom_count, mins_taken, seconds_taken, completion_time)
        elif self.game_state['lost']:
            clear_screen()
            show_game_over(self.map, self.mushroom_count, mins_taken, seconds_taken, completion_time)
        else:
            pass # Invalid; Not possible to get
        return None
    
    # Extra Functions Cause why not
    def restart(self):
        user_input = self.get_bool_input("Restart Map? (Y/N): ")
        if user_input:
            self.fetch_map()
        else:
            pass
        return user_input
    
    def get_bool_input(self, instruct):
        while True:
            if self.game_state['error']:
                print(f"Invalid Action")
                self.game_state['error'] = False
            choice = instruct_input(instruct).strip().upper()
            if choice == 'Y' or choice == "!":
                bool_check = True
                break
            elif choice == 'N':
                bool_check = False
                break
            else:
                self.game_state['error'] = True
        if bool_check:
            return True
        else:
            return False      
           
def menu():
    ...
    
if __name__ == "__main__":
    # display_intro()
    while True:
        menu()
        session = Game(choose_map())
        session.run_game()
    ...