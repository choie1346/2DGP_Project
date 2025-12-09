import os

from pico2d import load_image, get_events
from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
from common import *

def y_transformation(y):
    y = HEIGHT - y
    return y

# class Interface:
#     def __init__(self, path):
#         path = head_path + path
#         self.image = load_image(path)
#         self.push = False
#         self.Isbutton = False
#
#     def location(self, x, y, w, h):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#
#     def draw(self):
#         self.image.clip_draw(0, 0, self.w, self.h, self.x, self.y, self.w, self.h)
#
#     def update(self):
#         pass
#
#     def handle_event(self, event):
#         pass

class StartUI:
    def __init__(self):
        self.logo = load_image("Graphic/logo.png")
        self.start_button = load_image("Graphic/start_button.png")
        self.push_button = False

    def draw(self):
        self.logo.clip_draw(0, 0, 500, 500, 500, 450, 400, 400)
        self.start_button.clip_draw(0, 0, 98, 38, 500, 150, 200, 100)

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            event.y = y_transformation(event.y)
            if 400 <= event.x <= 600 and 100 <= event.y <= 200:
                if not self.push_button:
                    self.push_button = True
                    self.start_button = load_image("Graphic/start_button_push.png")
            else:
                if self.push_button:
                    self.push_button = False
                    self.start_button = load_image("Graphic/start_button.png")
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            event.y = y_transformation(event.y)
            if 400 <= event.x <= 600 and 100 <= event.y <= 200:
                print("click")
                change_stage(1)


class Interface:
    def __init__(self, path):
        path = "Graphic/" + path
        self.image = load_image(path)

    def location(self, origin_w, origin_h, x, y, w, h):
        self.origin_w = origin_w
        self.origin_h = origin_h
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        self.image.clip_draw(0, 0, self.origin_w, self.origin_h, self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def handle_event(self, event):
        pass



class Background:
    def __init__(self):
        self.image = load_image("Background/background.png")

    def draw(self):
        self.image.clip_draw(0, 0, 660, 470, 500, 350, 1000, 700)

    def update(self):
        pass