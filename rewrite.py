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
        self.debug = tuple()
        self.restart_game = True
    def run_game(self):
        while self.restart_game:
            self.fetch_map()
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
        if self.debug != None:
            print(self.debug)
        if self.game_state['error']:
            print(f"Invalid Action")
            self.game_state['error'] = False
        actions = instruct_input("Enter your next action: ").upper()
        for action in actions:
            # Found in auxilliary_functions
            if check_pickable_object(action, self.game_state['holding'], self.player_hidden_object):
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
            else:
                print(f"Skipping Invalid Action: {action}")
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
        print("\nTo reset map: [!]\nTo quit: [Q]")
        return None
    def restart(self):
        while True:
            if self.game_state['error']:
                print(f"Invalid Action")
                self.game_state['error'] = False
            choice = instruct_input("Restart Map? (Y/N): ").strip().upper()
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
