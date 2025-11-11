from auxilliary_functions import *

class Game:
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
    def run_game(self):
        self.initial_session()
        while self.restart_game:
            self.play_game()
            self.show_result()
            self.restart_game = self.restart()
        return None
    def fetch_map(self):
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
    def play_game(self):
        while True:
            self.display()
            self.player_input()
            if check_game_over(self):
                break
        return None
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
        for action in actions:
            # Found in auxilliary_functions
            if check_game_over(self):
                break
            elif self.game_state['error']:
                break
            elif check_pickable_object(action, self.game_state['holding'], self.player_hidden_object):
                self.game_state['holding'] = True
                self.player_held_item = self.player_hidden_object
                self.player_hidden_object = '.'
            elif action in ("W", "A", "S", "D"):
                # Found in auxilliary_functions
                dest_row, dest_col = new_pos(action, self.player_coords['row'], self.player_coords['col'])
                check_movement(self, dest_row, dest_col, self.player_coords['row'], self.player_coords['col'])
            elif action == 'Q':
                exit_terminal()
            elif action == "!":
                self.fetch_map()
            elif action == 'F':
                self.save_game()
            else:
                print(f"Invalid Action Found: {action}")
                break
        return None
    def initial_session(self):
        save_file = get_joint_path(get_current_directory(), f'{self.file_name[0::2]}{self.file_name[1::2]}')
        self.debug = save_file
        bool_check = False
        if check_existing_file(save_file):
            bool_check = self.get_bool_input(f'Save File Detected.\nRun Save [Y/N]:')
        try:
            if bool_check:
                self.fetch_save()
            else:
                self.fetch_map()
        except:
            self.debug(f'Save File Is Corrupted. Loading Base Map')
            self.fetch_map()
    def save_game(self):
        file = open(f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}", 'w')
        file.write(f"{self.map_rows} {self.map_cols}")
        file.write(f"{self.player_coords['row']} {self.player_coords['col']}")
        file.write(f"{self.player_held_item} {self.player_hidden_object}")
        file.write(f"{self.mushroom_count['total']} {self.mushroom_count['collected']}")
        file.write(f"{self.game_state['holding']} {self.game_state['drowning']}")
        file.write(f"{self.game_state['lost']} {self.game_state['error']}")
        file.write(f"{self.restart_game}")
        for tile_line in self.map:
            file.write(tile_line.strip())
        for boulder_coords in self.boulder_hidden_objects.items():
            file.write(boulder_coords)
        file.close()
        return None
    def fetch_save(self):
        self.map = list()
        self.boulder_hidden_objects = dict()
        file = open(f"saved_states/{self.file_name[0::2]}{self.file_name[1::2]}", 'rt')
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
                self.game_state['holding'], self.game_state['drowning'] = line.strip().split(" ")
            elif row == 5:
                self.game_state['lost'], self.game_state['error'] = line.strip().split(" ")
            elif row == 6:
                self.restart_game = line.strip()
            elif 7 <= row <= self.map_rows + 6:
                self.map.append(line)
            else:
                self.boulder_hidden_objects.update(line.strip())
        file.close()
        return None
    def display(self):
        clear_screen()
        show_entire_map(self)
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
    def restart(self):
        return self.get_bool_input("Restart Map? (Y/N): ")
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
    def show_result(self):
        if self.mushroom_count['total'] == self.mushroom_count['collected']:
            clear_screen()
            show_stage_clear(self.map, self.mushroom_count)
        elif self.game_state['drowning']:
            clear_screen()
            show_game_over(self.map, self.mushroom_count)
        elif self.game_state['lost']:
            clear_screen()
            show_game_over(self.map, self.mushroom_count)
        else:
            pass # Invalid; Not possible to get
        ...
            
def menu():
    ...

if __name__ == "__main__":
    while True:
        menu()
        session = Game(choose_map())
        session.run_game()
    ...
