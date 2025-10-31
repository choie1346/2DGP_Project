
WIDTH, HEIGHT = 1000, 700
# 0-start, 1-in game
stage = 0

def change_stage(new_stage):
    global stage
    stage = new_stage
    print("Stage changed to:", stage)