
WIDTH, HEIGHT = 1000, 700
MAX_X, MAX_Y = WIDTH, 500
# 0-start, 1-in game
STAGE = 0

ANIMAL_SPEED = 1

FOOD_MAX_NUMBER = 20
FOOD_CUR_NUMBER = 10

FOOD_MIN_CREATE_TIME = 6.0
FOOD_MAX_CREATE_TIME = 11.0

food_level = 0

GROW_ANIMAL_NUMBER = [10, 30, 80, 150, 30, 50, 100, 200, 500] # 각 단계별 성장에 필요한 음식 양

LEVEL_UP_COST = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]  # 각 레벨업에 필요한 코인 양
COIN_SPAWN_PROBABILITY = 30.0  # 음식 먹었을 때 코인 나올 확률 (%)
coin_number = 50

def change_stage(new_stage):
    global STAGE
    STAGE = new_stage
    # print("Stage changed to:", STAGE)