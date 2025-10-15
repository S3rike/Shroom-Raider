import os
import sys

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