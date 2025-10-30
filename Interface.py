from pico2d import load_image

class startUI:
    def __init__(self):
        self.logo = load_image("Graphic/logo.png")
        self.start_button = load_image("Graphic/start_button.png")

    def draw(self):
        self.logo.clip_draw(0, 0, 500, 500, 500, 450, 400, 400)
        self.start_button.clip_draw(0, 0, 98, 38, 500, 150, 200, 100)
        #self.exit_button.clip_draw(0, 0, 400, 100, 500, 150, 200, 50)

    def update(self):
        pass

class Background:
    def __init__(self):
        self.image = load_image("Background/background.png")

    def draw(self):
        self.image.clip_draw(0, 0, 660, 470, 500, 350, 1000, 700)

    def update(self):
        pass