import random
import os

def get_random_value(list):
    if list:
        return random.choice(list)
    else:
        return None
    
def get_random_index(list):
    return random.randint(0, len(list) - 1)

def check_file_path(file_path):
    return os.path.exists(file_path)