from pico2d import load_image

class Background:
    def __init__(self):
        self.image = load_image("Background/background.png")

    def draw(self):
        self.image.clip_draw(0, 0, 660, 470, 500, 350, 1000, 700)