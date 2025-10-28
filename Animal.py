from pico2d import load_image
import os

image_front = [                 # unicon -> 0 1 3 5 7 8 9
    "Animals/Chicken/front.png", # Ostrich -> 0 2 4 6
    "Animals/Rabbit/front.png",
    "Animals/Duck/front.png",
    "Animals/Sheep/front.png",
    "Animals/Penguin/front.png",
    "Animals/Cow/front.png",
    "Animals/Ostrich/front.png",
    "Animals/Horse/front.png",
    "Animals/Unicon/front.png",
]

path = "Animals/Chicken/front.png"
print("파일 존재 여부:", os.path.exists(path))

class Animal:
    def __init__(self):
        self.x, self.y = 400, 90
        self.route = 1
        self.current = 0
        self.frame = 0
        self.image = load_image("Animals/Chicken/front.png") # Chicken

    def update(self):
        self.frame = (self.frame + 1) % 4
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 100, 100, self.x, self.y)
        pass

    def handle_event(self, event):
        pass