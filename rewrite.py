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
        self.restart_game = True
    def run_game(self):
        while self.restart_game:
            self.fetch_map()
            self.play_game()
            self.show_result()
            self.restart_game = self.restart()
        return None

    def play_game(self):
        while True:
            self.display()
            self.player_input()
            if check_game_over(self):
                break
        return None
    def player_input(self):
        if self.game_state['error']:
            print(f"Invalid Action")
            self.game_state['error'] = False
        actions = instruct_input("Enter your next action: ").upper()
        for action in actions:
            # Found in auxilliary_functions
            if check_pickable_object(action, self.game_state['holding'], self.player_hidden_object):
                game_state['holding'] = True
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
    def restart(self):
        while True:
            if self.game_state['error']:
                print(f"Invalid Action")
                self.game_state['error'] = False
            choice = instruct_input("Restart Map Again? (Y/N): ").strip().upper()
            if choice == 'Y':
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
    def fetch_map(self):
        file = open(f"maps/{self.file_name}.txt", 'rt')
        for y_coord, tile_row in enumerate(file):
            self.map.append(list(tile_row))
            for x_coord, tile_char in enumerate(tile_row):
                if tile_char == 'L':
                    self.player_coords['row'] = y_coord
                    self.player_coords['col'] = x_coord
                    self.player_hidden_object = '.'
                elif tile_char == 'R':
                    self.boulder_hidden_objects[(x_coord, y_coord)] = '.'
                elif tile_char == '+':
                    self.mushroom_count['total'] += 1
                else:
                    pass
        file.close()
        self.game_state = {'holding':False, 'drowning':False, 'lost':False, 'error':False}
        self.map_rows = len(self.map)
        self.map_cols = len(self.map[0])
        return None
    def display(self):
        clear_screen()
        self.show_entire_map()
        print(f'You have collected {self.mushroom_count['collected']} mushrooms!\n')
        if self.game_state['holding'] == True:
            print(f'You currently have: {pickable_items[game_state['holding']]}')
        elif self.player_hidden_object in pickable_items.keys():
            print(f'There is a {pickable_items[self.player_hidden_object]} below you! Input [P] to pick it up!')
        else:
            print(f'You currently do not have an item!')
        print("\nMove Up: [W]\nMove Left: [A]\nMove Down: [S]\nMove Right: [D]")
        print("\nTo reset map: [!]\nTo quit: [Q]")
        return None
    def show_entire_map(self):
        print("\n--- Current Map ---\n")
        for row in self.map:
            emoji_display = [tile_ui.get(tile, tile) for tile in row]
            print("".join(emoji_display))
        print("---------------------")
        return None
    def show_result(self):
        ...

def choose_map():
    while True: 
        map_name = instruct_input("Enter path of map (etc. Map1): ")
        file_name = f"maps/{map_name}.txt"
        if check_existing_file(file_name):
            clear_screen()
            return map_name        
        else:
            clear_screen()
            print(f"File not found, try again")
def menu():
    ...

if __name__ == "__main__":
    while True:
        menu()
        session = Game(choose_map())
        session.run_game()
    ...
