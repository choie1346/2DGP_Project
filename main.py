from pico2d import *

import common
import game_world
from Interface import Background, StartUI, Interface, EndGameUI
from Animal import Animal
from Food import Food, FoodSpawner
from sdl2 import SDL_KEYDOWN, SDLK_m, SDLK_ESCAPE, SDLK_e, SDLK_u
from Quest import Quest, Farmer, QuestSpawner
# Game object class here

interfaces = []

# 배경 음악 로드 (오류 발생 시 무시)
try:
    music = load_wav("sounds/background_music.wav")
    music.set_volume(64)
    music.repeat_play()
except:
    print("배경 음악을 로드할 수 없습니다. 게임을 계속 진행합니다.")
    music = None

def add_interface(path, info, origin_x, origin_y, box_w, box_h, draw_w, draw_h):
    interface = Interface(path, info)
    interfaces.append(interface)
    interface.location(origin_x, origin_y, box_w, box_h, draw_w, draw_h)
    game_world.add_object(interface, 1)
    # print(f"Interface added: {info}, pos: ({box_w}, {box_h}), size: ({draw_w}, {draw_h})")


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            quit()

        # STAGE 0: 시작 화면
        if common.STAGE == 0:
            if event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN:
                startui.handle_event(event)

        # STAGE 1: 게임 화면
        elif common.STAGE == 1:
            animal.handle_event(event)
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_m:
                    # game_world에서 모든 Food 객체 가져와서 업그레이드
                    all_foods = game_world.get_objects_by_type(Food)
                    for food in all_foods:
                        food.upgrade()
                elif event.key == SDLK_u:
                    common.coin_number += 1000

            if event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN:
                # 모든 인터페이스에 마우스 이벤트 전달
                for i, interface in enumerate(interfaces):
                    interface.handle_event(event)


def reset_world():
    global food, background, animal, startui, speed_up, food_spawner, quest_spawner, interfaces, endgame_ui


    # interfaces 리스트 초기화 (STAGE 변경 시 이전 인터페이스 제거)
    interfaces.clear()

    # stage == 0
    if common.STAGE == 0:
        background = Background()
        game_world.add_object(background, 0)

        startui = StartUI()
        game_world.add_object(startui, 0)

    elif common.STAGE == 1:
        # stage == 1
        background = Background()
        game_world.add_object(background, 1)

        # FoodSpawner 생성
        food_spawner = FoodSpawner()
        game_world.add_object(food_spawner, 1)

        # Food 생성
        for i in range(common.FOOD_CUR_NUMBER):
            food = Food()
            game_world.add_object(food, 1)
            game_world.add_collision_pair('animal:food', None, food)

        animal = Animal()
        game_world.add_object(animal, 1)

        game_world.add_collision_pair('animal:food', animal, None)
        game_world.add_collision_pair('animal:farmer', animal, None)

        # QuestSpawner 생성 (자동으로 일정 시간마다 퀘스트 출현)
        quest_spawner = QuestSpawner()
        game_world.add_object(quest_spawner, 1)

        add_interface("Graphic/speed_up.png", "speed_up", 108, 108, 50, 50, 50, 50)
        add_interface("Graphic/time_decrease.png", "food_spawn", 23, 38, 110, 50, 30, 50)
        add_interface("Graphic/maxcount_up.png", "food_upgrade", 24, 35, 170, 50, 50, 50)
        add_interface("Items/coins/coinchest2.png", "coinchest", 256, 256, 880, 50, 50, 50)

    elif common.STAGE == 2:
        # stage == 2 (게임 종료 화면)
        background = Background()
        game_world.add_object(background, 2)

        # EndGameUI 생성 및 추가
        endgame_ui = EndGameUI()
        game_world.add_object(endgame_ui, 2)


def update_world():
    game_world.update()
    game_world.handle_collision()

def render_world():
    clear_canvas()
    game_world.render(common.STAGE)
    update_canvas()



open_canvas(common.WIDTH, common.HEIGHT)
reset_world()
# game loop
while True:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
