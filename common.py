import game_world

WIDTH, HEIGHT = 1000, 700
MAX_X, MAX_Y = WIDTH, 500
# 0-start, 1-in game
STAGE = 0

# 코인 관련
coin_number = 0
COIN_SPAWN_PROBABILITY = 50

# 음식 관련
FOOD_CUR_NUMBER = 10
FOOD_MAX_NUMBER = 30
FOOD_MIN_CREATE_TIME = 5.0
FOOD_MAX_CREATE_TIME = 10.0

# 동물 관련
ANIMAL_SPEED = 1.0
GROW_ANIMAL_NUMBER = [50, 150, 300, 50, 150, 200, 300, 500]
UNICON_UNLOCK = False

# 게임 종료 정보
final_animal_level = 0  # 게임 종료 시 동물 레벨 저장

# 업그레이드 레벨
speed_level = 1  # 속도 업그레이드 레벨
food_spawn_level = 1  # 음식 생성 시간 업그레이드 레벨
food_upgrade_level = 1  # 음식 업그레이드 레벨

# 업그레이드 비용
LEVEL_UP_COST = [50, 100, 200, 300, 400, 500, 600, 700, 800, 1000]

def change_stage(new_stage):
    global STAGE
    game_world.clear()
    STAGE = new_stage
    print("Stage changed to:", STAGE)

    # 순환 참조를 피하기 위해 여기서 import
    import main
    main.reset_world()

def upgrade_speed():
    global speed_level, ANIMAL_SPEED
    speed_level += 1
    ANIMAL_SPEED += 1.0
    print(f"Speed upgraded to level {speed_level}, speed: {ANIMAL_SPEED}")

def downgrade_speed():
    global speed_level, ANIMAL_SPEED
    if speed_level > 0:
        speed_level -= 1
        ANIMAL_SPEED = max(1.0, ANIMAL_SPEED - 1.0)
        print(f"Speed downgraded to level {speed_level}, speed: {ANIMAL_SPEED}")

def upgrade_food_spawn():
    global food_spawn_level, FOOD_MIN_CREATE_TIME, FOOD_MAX_CREATE_TIME
    food_spawn_level += 1
    FOOD_MIN_CREATE_TIME = max(1.0, FOOD_MIN_CREATE_TIME - 0.5)
    FOOD_MAX_CREATE_TIME = max(2.0, FOOD_MAX_CREATE_TIME - 0.5)
    print(f"Food spawn upgraded to level {food_spawn_level}")

def downgrade_food_spawn():
    global food_spawn_level, FOOD_MIN_CREATE_TIME, FOOD_MAX_CREATE_TIME
    if food_spawn_level > 0:
        food_spawn_level -= 1
        FOOD_MIN_CREATE_TIME += 0.5
        FOOD_MAX_CREATE_TIME += 0.5
        print(f"Food spawn downgraded to level {food_spawn_level}")

def upgrade_food_quality():
    global food_upgrade_level
    food_upgrade_level += 1
    print(f"Food quality upgraded to level {food_upgrade_level}")

def downgrade_food_quality():
    global food_upgrade_level
    if food_upgrade_level > 0:
        food_upgrade_level -= 1
        print(f"Food quality downgraded to level {food_upgrade_level}")
