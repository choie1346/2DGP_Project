from pico2d import *

import common
import game_world
from Interface import Background, startUI
from Animal import Animal
from Food import Food
from sdl2 import SDL_KEYDOWN, SDLK_m
# Game object class here


count_food = 10

def handle_events():
    event_list = get_events()
    for event in event_list:
        animal.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_m:
            for i in range(count_food):
                food[i].upgrade()
        if event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN:
            startui.handle_event(event)


def reset_world():
    global food, background, animal, startui

    # stage == 0
    background = Background()
    game_world.add_object(background, 0)

    startui = startUI()
    game_world.add_object(startui, 0)


    # stage == 1
    game_world.add_object(background, 1)
    food = []
    for i in range(count_food):
        food.append(Food())
        game_world.add_object(food[i], 1)
    animal = Animal()
    game_world.add_object(animal, 1)

    game_world.add_collision_pair('animal:food', animal, None)
    for f in food:
        game_world.add_collision_pair('animal:food', None, f)

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
