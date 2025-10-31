
WIDTH, HEIGHT = 1000, 700
MAX_X, MAX_Y = WIDTH, 500
# 0-start, 1-in game
STAGE = 0

def change_stage(new_stage):
    global STAGE
    STAGE = new_stage
    print("Stage changed to:", STAGE)