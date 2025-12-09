from pico2d import load_image, draw_rectangle, load_font

import common
from state_machine import StateMachine
import game_world
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, SDL_KEYUP, SDLK_LEFT, SDLK_n
from Food import Food
from random import randint

# 0-front, 1-back, 2-left, 3-right
# route1 - 3까지, route2 - 4부터 8까지
image_dirs = [
    ["Animals/Chicken/front.png",
    "Animals/Duck/front.png",
    "Animals/Penguin/front.png",
    "Animals/Ostrich/front.png",
    "Animals/Rabbit/front.png",
    "Animals/Sheep/front.png",
    "Animals/Cow/front.png",
    "Animals/Horse/front.png",
    "Animals/Unicon/front.png"
    ],
    ["Animals/Chicken/back.png",
    "Animals/Duck/back.png",
    "Animals/Penguin/back.png",
    "Animals/Ostrich/back.png",
    "Animals/Rabbit/back.png",
    "Animals/Sheep/back.png",
    "Animals/Cow/back.png",
    "Animals/Horse/back.png",
    "Animals/Unicon/back.png"
        ],
    ["Animals/Chicken/left.png",
    "Animals/Duck/left.png",
    "Animals/Penguin/left.png",
    "Animals/Ostrich/left.png",
    "Animals/Rabbit/left.png",
    "Animals/Sheep/left.png",
    "Animals/Cow/left.png",
    "Animals/Horse/left.png",
    "Animals/Unicon/left.png"
    ],
    ["Animals/Chicken/right.png",
    "Animals/Duck/right.png",
    "Animals/Penguin/right.png",
    "Animals/Ostrich/right.png",
    "Animals/Rabbit/right.png",
    "Animals/Sheep/right.png",
    "Animals/Cow/right.png",
    "Animals/Horse/right.png",
    "Animals/Unicon/right.png"
    ]
]

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def key_n(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_n

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

class run:
    def __init__(self, animal):
        self.animal = animal
        self.frame_time = 0

    def enter(self, e):
        # 키 누름 - 해당 방향의 상태만 업데이트
        if down_down(e):
            self.animal.key_down_pressed = True
        elif up_down(e):
            self.animal.key_up_pressed = True
        elif left_down(e):
            self.animal.key_left_pressed = True
        elif right_down(e):
            self.animal.key_right_pressed = True
        # 키 뗌 - 해당 방향의 상태만 해제
        elif down_up(e):
            self.animal.key_down_pressed = False
        elif up_up(e):
            self.animal.key_up_pressed = False
        elif left_up(e):
            self.animal.key_left_pressed = False
        elif right_up(e):
            self.animal.key_right_pressed = False
        elif key_n(e):
            self.animal.current = (self.animal.current + 1) % len(image_dirs[0])

        # 키 상태에 따라 속도 계산
        self.animal.velocity_x = 0
        self.animal.velocity_y = 0

        if self.animal.key_left_pressed:
            self.animal.velocity_x -= 1
        if self.animal.key_right_pressed:
            self.animal.velocity_x += 1
        if self.animal.key_down_pressed:
            self.animal.velocity_y -= 1
        if self.animal.key_up_pressed:
            self.animal.velocity_y += 1

        # 방향 결정 (스프라이트 이미지용) - 이동 중일 때만 업데이트
        if self.animal.velocity_x != 0 or self.animal.velocity_y != 0:
            # 우선순위: 수직 > 수평
            if abs(self.animal.velocity_y) > abs(self.animal.velocity_x):
                if self.animal.velocity_y < 0:
                    self.animal.dir = 0  # down
                else:
                    self.animal.dir = 1  # up
            else:
                if self.animal.velocity_x < 0:
                    self.animal.dir = 2  # left
                else:
                    self.animal.dir = 3  # right

        self.animal.image = load_image(image_dirs[self.animal.dir][self.animal.current])

    def do(self):
        # 이동 처리
        self.animal.x += self.animal.velocity_x * self.animal.speed
        self.animal.y += self.animal.velocity_y * self.animal.speed

        # 애니메이션 프레임 업데이트
        self.frame_time += 0.01
        if self.frame_time > 0.1:
            self.animal.frame = (self.animal.frame + 1) % 4
            self.frame_time = 0

    def draw(self):
        self.animal.image.clip_draw(self.animal.frame * 80, 0, 80, 80, self.animal.x, self.animal.y, self.animal.size, self.animal.size)

    def exit(self, e):
        self.animal.velocity_x = 0
        self.animal.velocity_y = 0

class Animal:
    def __init__(self):
        self.x, self.y = 400, 350
        self.route = 1
        self.current = 0
        self.frame = 0
        self.dir = 0
        self.size = 200
        self.speed = common.ANIMAL_SPEED  # 이동 속도
        self.velocity_x = 0  # X 방향 속도
        self.velocity_y = 0  # Y 방향 속도

        # 각 방향키의 눌림 상태 추적
        self.key_up_pressed = False
        self.key_down_pressed = False
        self.key_left_pressed = False
        self.key_right_pressed = False

        self.RUN = run(self)
        self.state_machine = StateMachine(
            self.RUN,  # initial state
            {
                self.RUN: {up_down: self.RUN, down_down: self.RUN, left_down: self.RUN, right_down: self.RUN, key_n: self.RUN,
                           up_up: self.RUN, down_up: self.RUN, left_up: self.RUN, right_up: self.RUN}
            }
        )

    def grow(self):
        self.current += 1
        if self.current >= len(image_dirs[0]):
            self.current = len(image_dirs[0]) - 1
            # print('최대 성장 도달')
            return
        self.size = 200
        self.image = load_image(image_dirs[self.dir][self.current])
        # print(f'Animal grew to stage {animal.current}')

    def update(self):
        self.state_machine.update()
        if self.speed != common.ANIMAL_SPEED:
            self.speed = common.ANIMAL_SPEED
            # print(f'Animal speed updated: {self.speed}')

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        # size 기본값 200을 기준으로 비율 계산
        ratio = self.size / 200.0
        # 기본 박스 크기: 너비 80 (좌우 각 40), 높이 80 (상하 40, 120)
        half_width = 40 * ratio
        bottom_offset = 120 * ratio
        top_offset = 40 * ratio
        return self.x - half_width, self.y - bottom_offset+ 20, self.x + half_width, self.y - top_offset

    def handle_collision(self, group, other):
        if group == 'animal:food':
            food = game_world.get_one_object_by_type(Food)
            self.size += (food.current + 1)
            if self.size >= common.GROW_ANIMAL_NUMBER[self.current] + 200:
                self.grow()
            if randint(0, 100) < common.COIN_SPAWN_PROBABILITY:
                common.coin_number += 10
            # print(f'size up: {self.size}')
