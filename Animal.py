from pico2d import load_image
from state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_n

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

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class front:
    def __init__(self, animal):
        self.animal = animal

    def enter(self, e):
        self.animal.image = load_image(image_dirs[0][self.animal.current])

    def do(self):
        self.animal.frame = (self.animal.frame + 1) % 4

    def exit(self, e):
        pass

class Animal:
    def __init__(self):
        self.x, self.y = 400, 350
        self.route = 1
        self.current = 0
        self.frame = 0
        #self.image = load_image('Animals/Chicken/front.png') # Chicken
        self.FRONT = front(self)
        self.state_machine = StateMachine(
            self.FRONT,  # initial state
            {
                self.FRONT: {}
            }
        )
    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 80, self.x, self.y, 300, 300)
        pass

    def handle_event(self, event):
        pass