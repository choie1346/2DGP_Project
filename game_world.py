# 0 : start, 1 : in game
world = [[], []]

# world object 추가
def add_object(o, stage):
    world[stage].append(o)

# world object update
def update():
    for layer in world:
        for o in layer:
            o.update()

def render(stage):
    for o in world[stage]:
        o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    print('월드에 존재하지 않은 객체를 삭제하려고 합니다.')