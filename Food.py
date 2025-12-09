from pico2d import load_image, get_events, draw_rectangle
from random import randrange, uniform
import common
import game_world
from sdl2 import SDL_KEYDOWN, SDLK_m
from time import time

image =[
    "Items/foods/level1f.png",
    "Items/foods/level2f.png",
    "Items/foods/level3f.png",
    "Items/foods/level4f.png",
    "Items/foods/level5f.png",
    "Items/foods/level6f.png",
    "Items/foods/level7f.png",
    "Items/foods/level8f.png",
    "Items/foods/level9f.png",
    "Items/foods/level10f.png"
]

class Food:
    def __init__(self):
        self.x, self.y = randrange(30, 750 + 1), randrange(100, 500 + 1)
        self.size = 0
        self.current = 0
        self.creating = True
        self.image = load_image(image[0])

    def update(self):
        if self.creating:
            self.craete()

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def craete(self):
        self.size += 5
        if self.size >= 50:
            self.creating = False

    def upgrade(self):
        self.current = (self.current + 1) % len(image)
        self.image = load_image(image[self.current])
        self.creating = True
        self.size = 0

    def get_bb(self):
        return self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2

    def handle_collision(self, group, other):
        if group == 'animal:food':
            game_world.remove_object(self)
            game_world.remove_collision_object(self)
            common.FOOD_CUR_NUMBER -= 1
            # print(f'음식 개수: {common.FOOD_CUR_NUMBER}')


class FoodSpawner:
    def __init__(self):
        self.current_time = 0.0
        self.spawn_time = uniform(common.FOOD_MIN_CREATE_TIME, common.FOOD_MAX_CREATE_TIME)

    def update(self):
        if common.STAGE == 1:
            if common.FOOD_CUR_NUMBER >= common.FOOD_MAX_NUMBER: return
            # print(f'Spawn in: {self.spawn_time - self.current_time:.2f} sec')
            self.current_time += 0.05
            if self.current_time >= self.spawn_time:
                new_food = Food()
                game_world.add_object(new_food, 1)
                game_world.add_collision_pair('animal:food', None, new_food)
                self.current_time = 0.0
                self.spawn_time = uniform(common.FOOD_MIN_CREATE_TIME, common.FOOD_MAX_CREATE_TIME)
                common.FOOD_CUR_NUMBER += 1
                # print(f'음식 개수: {common.FOOD_CUR_NUMBER}')

    def draw(self):
        pass