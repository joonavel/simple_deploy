import random

def create_target_number():
    return random.randint(1, 100)

def check_answer(answer: int, target: int):
    return answer == target

def calculate_diff(answer: int, target: int):
    return target - int(answer)
