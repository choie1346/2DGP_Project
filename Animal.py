from pico2d import load_image

image_front = [
    'Animals/Chicken/front.png',
    "Animals/Rabbit/front.png",
    "Animals/Duck/front.png",
    "Animals/Sheep/front.png",
    "Animals/Penguin/front.png",
    "Animals/Cow/front.png",
    "Animals/Ostrich/front.png",
    "Animals/Horse/front.png",
    "Animals/Unicon/front.png",
]

class Animal:
    def __init__(self):
        self.x, self.y = 400, 350
        self.route = 1
        self.current = 0
        self.frame = 0
        self.image = load_image('Animals/Chicken/front.png') # Chicken

    def update(self):
        self.frame = (self.frame + 1) % 4
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 80, self.x, self.y, 300, 300)
        pass

    def handle_event(self, event):
        pass