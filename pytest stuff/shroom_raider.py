from argparse import ArgumentParser
import os

movable_tiles = {'.', '-', '+'} # Set of tiles that can be moved immediately
pickable_items = {'x': "Axe", '*': "Flamethrower"} # Set of tiles that can be picked up
immovable_tiles = {'T', '~'} # Set of tiles that cannot be moved into
adjustable_tiles = {'R'}
tile_ui = {'L':'🧑', '.':'　', 'T':'🌲', '+':'🍄', 'R':'🪨', '~':'🟦', '-':'⬜', 'x':'🪓', '*':'🔥'}

class Base_Game:
    def __init__(self, file_name, input_move, output_file):
        self.file_name = file_name
        self.actions = input_move
        self.output_file = output_file
        self.map = list()
        self.map_rows = 0
        self.map_cols = 0
        self.player_coords = {'row': 0, 'col': 0} #col is column
        self.player_held_item = None
        self.player_hidden_object = '.'
        self.boulder_hidden_objects = dict()
        self.mushroom_count = {'total': 0, 'collected': 0}
        self.game_state = {'holding':False, 'drowning':False, 'lost':False, 'error':False}
    def run_game(self):
        self.fetch_map()
        self.player_input()
        return self.output()

    def fetch_map(self):
        self.map = list()
        self.boulder_hidden_objects = dict()
        self.mushroom_count = {'total': 0, 'collected': 0}
        self.game_state = {'holding':False, 'drowning':False, 'lost':False, 'error':False}
        file = open(self.get_joint_path('maps', self.file_name), 'rt')
        for y_coord, tile_row in enumerate(file):
            if y_coord == 0: self.map_rows, self.map_cols = map(int, tile_row.strip().split(" "))
            else:
                self.map.append(list(tile_row))
                for x_coord, tile_char in enumerate(tile_row):
                    if tile_char == 'L':
                        self.player_coords['row'] = y_coord - 1
                        self.player_coords['col'] = x_coord
                        self.player_hidden_object = '.'
                        self.player_held_item = None
                    elif tile_char == 'R':
                        self.boulder_hidden_objects[(y_coord - 1, x_coord)] = '.'
                    elif tile_char == '+':
                        self.mushroom_count['total'] += 1
                    else:
                        pass
        file.close()
        self.map_rows = len(self.map)
        self.map_cols = len(self.map[0]) - 1
        return None
    def player_input(self):
        if self.check_game_over(): # Only occurs during backup of a finished self
            return None
        if self.game_state['error']:
            self.game_state['error'] = False
        
        for action in self.actions:
            action = action.upper()
            # Found in auxilliary_functions
            if self.check_game_over():
                break
            elif self.game_state['error']:
                break
            elif action == "P":
                if self.check_pickable_object():
                    self.game_state['holding'] = True
                    self.player_held_item = self.player_hidden_object
                    self.player_hidden_object = '.'
                else:
                    continue
            elif action in ("W", "A", "S", "D"):
                # Found in auxilliary_functions
                dest_row, dest_col = self.new_pos(action)
                self.check_movement(dest_row, dest_col, self.player_coords['row'], self.player_coords['col'])
            elif action == 'Q':
                break
            elif action == "!":
                self.fetch_map()
                self.latest_action = None
            elif action == 'F':
                self.latest_action = None
            else:
                break
        return None
    def check_pickable_object(self):
        return self.player_held_item == None and self.player_hidden_object in pickable_items.keys()
    def check_game_over(self):
        bool_check1 = self.mushroom_count['total'] == self.mushroom_count['collected']
        bool_check2 = self.game_state['drowning']
        bool_check3 = self.game_state['lost']
        return bool_check1 or bool_check2 or bool_check3
    def check_movement(self, dest_row, dest_col, curr_row, curr_col): # dest means destination
        if self.pos_in_bounds(dest_row, dest_col):
            dest_tile = self.map[dest_row][dest_col]
        else:
            self.game_state['lost'] = True
            self.map[curr_row][curr_col] = self.player_hidden_object
            self.latest_action = 'water'
            return None
        if dest_tile in movable_tiles:
            if dest_tile == '+':
                self.mushroom_count['collected'] += 1
                dest_tile = '.'
                self.latest_action = 'pick'
            else:
                self.latest_action = 'move'
            self.modify_movement(dest_tile, dest_row, dest_col, curr_row, curr_col)
        elif dest_tile in pickable_items.keys():
            self.latest_action = 'move'
            self.modify_movement(dest_tile, dest_row, dest_col, curr_row, curr_col)
        elif dest_tile in adjustable_tiles:
            to_row = dest_row - curr_row # directions of player
            to_col = dest_col - curr_col
            rock_dest_row = dest_row + to_row # where will rock go
            rock_dest_col = dest_col + to_col
            if self.pos_in_bounds(rock_dest_row, rock_dest_col): # rock in bounds
                rock_dest_tile = self.map[rock_dest_row][rock_dest_col]
                # If the tile the rock is moving to is valid
                if rock_dest_tile in {".", "-"}:
                    self.boulder_hidden_objects[(rock_dest_row, rock_dest_col)] = rock_dest_tile
                    self.map[rock_dest_row][rock_dest_col] = dest_tile
                    dest_tile = self.boulder_hidden_objects[(dest_row, dest_col)]
                    self.boulder_hidden_objects.pop((dest_row, dest_col))
                    self.latest_action = 'push'
                    self.modify_movement(dest_tile, dest_row, dest_col, curr_row, curr_col)
                elif rock_dest_tile == '~':
                    self.map[rock_dest_row][rock_dest_col] = '-' # replace water
                    self.map[dest_row][dest_col] = self.boulder_hidden_objects[(dest_row, dest_col)]
                    dest_tile = self.boulder_hidden_objects[(dest_row, dest_col)]
                    self.boulder_hidden_objects.pop((dest_row, dest_col))
                    self.modify_movement(dest_tile, dest_row, dest_col, curr_row, curr_col)
                else:
                    pass
            else:
                pass
        elif dest_tile == '~':
            self.latest_action = 'water'
            self.game_state['drowning'] = True
            self.map[curr_row][curr_col] = self.player_hidden_object
            self.player_hidden_object = '.'
        elif dest_tile == 'T':
            if self.game_state['holding']:
                self.use_held_item(dest_tile, dest_row, dest_col, curr_row, curr_col)
            else:
                pass
        else:
            pass #invalid but definitely will not be used
        return None
    def use_held_item(self, dest_tile, dest_row, dest_col, curr_row, curr_col):
        if self.player_held_item == 'x':
            dest_tile = '.'
            self.modify_movement(dest_tile, dest_row, dest_col, curr_row, curr_col)
        elif self.player_held_item == '*':
            self.burn_adj_trees(dest_row, dest_col)
            self.map[curr_row][curr_col] = self.player_hidden_object
            self.map[dest_row][dest_col] = 'L'
            self.player_coords['row'] = dest_row
            self.player_coords['col'] = dest_col
        else:
            pass #invalid but definitely will not be used
        self.player_held_item = None
        self.game_state['holding'] = False
        return None
    def burn_adj_trees(self, row, col):
        burn_stack = [(row, col)]
        checked_tiles = set()
        while burn_stack != []:
            tree_row, tree_col = burn_stack.pop()
            self.map[tree_row][tree_col] = '.'
            checked_tiles.add((tree_row, tree_col))
            burn_stack.extend(tuple(self.check_adj_trees(tree_row, tree_col)))
    def check_adj_trees(self, row, col):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for shift_row, shift_col in directions:
            dest_row = row + shift_row
            dest_col = col + shift_col
            if self.pos_in_bounds(dest_row, dest_col):
                if self.map[dest_row][dest_col] == 'T':
                    yield (dest_row, dest_col)
    def modify_movement(self, dest_tile, dest_row, dest_col, curr_row, curr_col):
        self.map[curr_row][curr_col] = self.player_hidden_object
        self.player_hidden_object = dest_tile
        self.map[dest_row][dest_col] = 'L'
        self.player_coords['row'] = dest_row
        self.player_coords['col'] = dest_col
    def pos_in_bounds(self, row, col):
        return (0 <= row < self.map_rows) and (0 <= col < self.map_cols)
    def new_pos(self, action):
        dest_row, dest_col = self.player_coords['row'], self.player_coords['col']
        if action == 'W':
            dest_row -= 1
        elif action == 'S':
            dest_row += 1
        elif action == 'A':
            dest_col -= 1
        elif action == 'D':
            dest_col += 1
        return dest_row, dest_col
    def get_joint_path(self, *paths):
        file = ""
        for line in paths:
            file = os.path.join(file, line)
        return file
    def output(self):
        if self.output_file != None:
            file = open(f"{self.output_file}", 'w')
            file.write(f"{self.show_result()}\n")
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
            row = f'{row}'
            file.write(row)
            file.close()
            return None
        else:
            return self.show_result()
    def show_result(self):
        if self.mushroom_count['total'] == self.mushroom_count['collected']:
            return "CLEAR"
        else:
            return "NO CLEAR"

if __name__ == "__main__":
    get_arguments = ArgumentParser()
    get_arguments.add_argument('-f', '--stage_name', type = str)
    get_arguments.add_argument('-m', '--move_actions', type = str)
    get_arguments.add_argument('-o', '--output_file', type = str, default=None)
    inputs = get_arguments.parse_args()

    session = Base_Game(inputs.stage_name, inputs.move_actions, inputs.output_file)
    session.run_game()