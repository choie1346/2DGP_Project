import os

from pico2d import load_image, get_events, load_font
from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import common
from common import *
from Food import Food
import game_world

def y_transformation(y):
    y = HEIGHT - y
    return y

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
                # print("click")
                change_stage(1)

class Interface:
    def __init__(self, path, info):
        self.image = load_image(path)
        self.info = info
        self.popup_box = None
        self.is_hovered = False
        self.font = load_font("Galmuri11.ttf", 16)

    def location(self, origin_w, origin_h, x, y, w, h):
        self.origin_w = origin_w
        self.origin_h = origin_h
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        self.image.clip_draw(0, 0, self.origin_w, self.origin_h, self.x, self.y, self.w, self.h)

        if self.info == "coinchest":
            coin_text = str(common.coin_number)
            text_width = len(coin_text) * 8
            self.font.draw(self.x - text_width // 2 + 50, self.y - 5, coin_text, (255, 255, 255))

        # 팝업이 있으면 그리기
        if self.popup_box is not None:
            self.popup_box.draw()

            if self.info == "speed_up":
                text = f"Level {common.speed_level}"
                text_width = len(text) * 8
                self.font.draw(self.x - text_width // 2, self.y + 100, text, (255, 255, 255))

                if common.speed_level >= 5:
                    self.font.draw(self.x - 40, self.y + 60, "Max Level", (255, 215, 0))
                    return
                cost_text = str(common.LEVEL_UP_COST[common.speed_level - 1])
                cost_width = len(cost_text) * 8
                # 코인 이미지를 비용 텍스트 왼쪽에 배치
                coin_image = load_image("Items/coins/coin.png")
                coin_image.clip_draw(0, 0, 63, 54, self.x - cost_width // 2 - 15, self.y + 60, 25, 25)
                self.font.draw(self.x - cost_width // 2 + 10, self.y + 60, cost_text, (255, 255, 255))

            elif self.info == "food_spawn":
                text = f"Level {common.food_spawn_level}"
                text_width = len(text) * 8
                self.font.draw(self.x - text_width // 2, self.y + 100, text, (255, 255, 255))

                if common.food_spawn_level >= 5:
                    self.font.draw(self.x - 40, self.y + 60, "Max Level", (255, 215, 0))
                    return
                cost_text = str(common.LEVEL_UP_COST[common.food_spawn_level - 1])
                cost_width = len(cost_text) * 8
                coin_image = load_image("Items/coins/coin.png")
                coin_image.clip_draw(0, 0, 63, 54, self.x - cost_width // 2 - 15, self.y + 60, 25, 25)
                self.font.draw(self.x - cost_width // 2 + 10, self.y + 60, cost_text, (255, 255, 255))

            elif self.info == "food_upgrade":
                text = f"Level {common.food_upgrade_level}"
                text_width = len(text) * 8
                self.font.draw(self.x - text_width // 2, self.y + 100, text, (255, 255, 255))

                if common.food_upgrade_level >= 10:
                    self.font.draw(self.x - 40, self.y + 60, "Max Level", (255, 215, 0))
                    return
                cost_text = str(common.LEVEL_UP_COST[common.food_upgrade_level - 1])
                cost_width = len(cost_text) * 8
                coin_image = load_image("Items/coins/coin.png")
                coin_image.clip_draw(0, 0, 63, 54, self.x - cost_width // 2 - 15, self.y + 60, 25, 25)
                self.font.draw(self.x - cost_width // 2 + 10, self.y + 60, cost_text, (255, 255, 255))

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            if self.info == "coinchest": return
            mouse_y = y_transformation(event.y)
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
                if self.info == "speed_up":
                    if common.speed_level >= 5: return
                    if common.coin_number >= common.LEVEL_UP_COST[common.speed_level - 1]:
                        common.coin_number -= common.LEVEL_UP_COST[common.speed_level - 1]
                        common.ANIMAL_SPEED += 1
                        common.speed_level += 1
                        # print(f'New ANIMAL_SPEED: {common.ANIMAL_SPEED}')
                        # print('동물 스피드 업')
                elif self.info == "food_upgrade":
                    if common.food_upgrade_level >= 10: return
                    if common.coin_number >= common.LEVEL_UP_COST[common.food_upgrade_level - 1]:
                        common.coin_number -= common.LEVEL_UP_COST[common.food_upgrade_level - 1]
                        common.food_upgrade_level += 1
                        # print('음식 업그레이드')
                        all_foods = game_world.get_objects_by_type(Food)
                        for food in all_foods:
                            food.upgrade()
                elif self.info == "food_spawn":
                    if common.food_spawn_level >= 5: return
                    if common.coin_number >= common.LEVEL_UP_COST[common.food_spawn_level - 1]:
                        common.coin_number -= common.LEVEL_UP_COST[common.food_spawn_level - 1]
                        common.food_spawn_level += 1  # 이 줄이 빠져있었습니다!
                        # print('음식 생성 시간 단축')
                        common.FOOD_MIN_CREATE_TIME = max(0.5, common.FOOD_MIN_CREATE_TIME - 1.0)
                        common.FOOD_MAX_CREATE_TIME = max(1.0, common.FOOD_MAX_CREATE_TIME - 1.0)
                        # print(f'New FOOD_MIN_CREATE_TIME: {common.FOOD_MIN_CREATE_TIME}, FOOD_MAX_CREATE_TIME: {common.FOOD_MAX_CREATE_TIME}')

class Background:
    def __init__(self):
        self.image = load_image("Background/background.png")

    def draw(self):
        self.image.clip_draw(0, 0, 660, 470, 500, 350, 1000, 700)

    def update(self):
        pass