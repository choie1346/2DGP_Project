from pico2d import *

import game_world
from Interface import Background
from Animal import Animal
from Food import Food
from sdl2 import SDL_KEYDOWN, SDLK_m
# Game object class here
WIDTH = 1000
HEIGHT = 700

# 0-start, 1-in game
stage = 0
count_food = 50

def handle_events():
    event_list = get_events()
    for event in event_list:
        animal.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_m:
            for i in range(count_food):
                food[i].upgrade()


def reset_world():
    global food, background, animal

    background = Background()
    game_world.add_object(background, 0)
    game_world.add_object(background, 1)

    animal = Animal()
    game_world.add_object(animal, 1)
    food = []
    for i in range(count_food):
        food.append(Food())
        game_world.add_object(food[i], 1)


def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render(stage)
    update_canvas()



open_canvas(WIDTH, HEIGHT)
reset_world()
# game loop
while True:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
