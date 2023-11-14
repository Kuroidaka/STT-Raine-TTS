import random

def get_random_value(list):
    if list:
        return random.choice(list)
    else:
        return None
