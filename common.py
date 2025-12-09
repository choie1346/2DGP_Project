
WIDTH, HEIGHT = 1000, 700
MAX_X, MAX_Y = WIDTH, 500
# 0-start, 1-in game
STAGE = 0

FOOD_MAX_NUMBER = 20
FOOD_CUR_NUMBER = 10

FOOD_MIN_CREATE_TIME = 6.0
FOOD_MAX_CREATE_TIME = 11.0

GROW_ANIMAL_NUMBER = [10, 30, 50, 100, 20, 30, 50, 100, 200]

def change_stage(new_stage):
    global STAGE
    STAGE = new_stage
    print("Stage changed to:", STAGE)