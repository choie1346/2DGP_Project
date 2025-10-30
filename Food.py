from pico2d import load_image
from random import randrange
from state_machine import StateMachine

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
        self.x, self.y = randrange(50, 950 + 1), randrange(50, 750 + 1)
        self.size = 0
        self.Creating = True
        self.image = load_image(image[0])

    def update(self):
        if self.Creating:
            self.Craete()

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.x, self.y, self.size, self.size)

    def Craete(self):
        self.size += 5
        if self.size >= 50:
            self.Creating = False