from pico2d import *
from Animal import Animal
from Food import Food
# Game object class here
WIDTH = 1000
HEIGHT = 800

count_food = 50

def handle_events():
    event_list = get_events()
    for event in event_list:
        animal.handle_event(event)
    pass


def reset_world():
    pass



def update_world():
    #animal.update()
    for i in range(count_food):
        food[i].update()


def render_world():
    clear_canvas()
    #animal.draw()
    for i in range(count_food):
        food[i].draw()
    update_canvas()



open_canvas(WIDTH, HEIGHT)
animal = Animal()
food = []

for i in range(count_food):
    food.append(Food())
# game loop
while True:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
