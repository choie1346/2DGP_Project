from pico2d import *
from Animal import *


# Game object class here

animal = Animal()

def handle_events():
    # event_list = get_events()
    # for event in event_list:
            # Animal.handle_event(event)
    pass


def reset_world():
    pass



def update_world():
    animal.update()
    pass


def render_world():
    clear_canvas()
    animal.draw()
    update_canvas()



open_canvas()
# game loop
while True:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
