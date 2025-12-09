import os

from pico2d import load_image, get_events, load_font
from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
from common import *
import game_world

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
    def __init__(self, path, info):
        self.image = load_image(path)
        self.info = info
        self.popup_box = None
        self.is_hovered = False
        self.font = load_font("Galmuri11.ttf", 16)
        self.level = 0

    def location(self, origin_w, origin_h, x, y, w, h):
        self.origin_w = origin_w
        self.origin_h = origin_h
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        self.image.clip_draw(0, 0, self.origin_w, self.origin_h, self.x, self.y, self.w, self.h)
        # 팝업이 있으면 그리기
        if self.popup_box is not None:
            self.popup_box.draw()
            # 팝업 위에 텍스트 그리기 (중앙 정렬)
            text = "Level " + str(self.level)
            text_width = len(text) * 8  # 폰트 크기 16의 경우 대략 절반 너비
            self.font.draw(self.x - text_width // 2, self.y + 80, text, (255, 255, 255))

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            mouse_y = y_transformation(event.y)
            # 마우스가 인터페이스 위에 있는지 확인
            if (self.x - self.w / 2) <= event.x <= (self.x + self.w / 2) and (self.y - self.h / 2) <= mouse_y <= (self.y + self.h / 2):
                if not self.is_hovered:
                    self.is_hovered = True
                    # 팝업 생성
                    self.popup_box = Interface("Graphic/textbox/item_popup.png", "popup")
                    self.popup_box.location(59, 64, self.x, self.y + 80, 118, 128)
                    # print(f"{self.info} hovered - pos: ({self.x}, {self.y}), size: ({self.w}, {self.h}), mouse: ({event.x}, {mouse_y})")
            else:
                if self.is_hovered:
                    self.is_hovered = False
                    # 팝업 제거
                    self.popup_box = None

        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_y = y_transformation(event.y)
            if (self.x - self.w / 2) <= event.x <= (self.x + self.w / 2) and (self.y - self.h / 2) <= mouse_y <= (self.y + self.h / 2):
                print(f"{self.info} clicked")



class Background:
    def __init__(self):
        self.image = load_image("Background/background.png")

    def draw(self):
        self.image.clip_draw(0, 0, 660, 470, 500, 350, 1000, 700)

    def update(self):
        pass