
from pico2d import load_image, get_events
from random import randrange
from common import STAGE
import game_world
from sdl2 import SDL_KEYDOWN, SDLK_m

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

    def craete(self):
        self.size += 5
        if self.size >= 50:
            self.creating = False

    def upgrade(self):
        self.current = (self.current + 1) % len(image)
        self.image = load_image(image[self.current])
        self.creating = True
        self.size = 0
