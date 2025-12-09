# 0 : start, 1 : in game
world = [[], [], []]

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

    print(f'월드에 존재하지 않은 객체{o}를 삭제하려고 합니다.')

def collide(a, b):
    leftA, bottomA, rightA, topA = a.get_bb()
    leftB, bottomB, rightB, topB = b.get_bb()

    if leftA > rightB: return False
    if rightA < leftB: return False
    if topA < bottomB: return False
    if bottomA > topB: return False

    return True


    return None

collision_pairs = {} #key: 충돌종류 value: [[a], [b]]

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print('새로운 그룹 추가')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def get_objects_by_type(obj_type):
    objects = []
    for layer in world:
        for o in layer:
            if isinstance(o, obj_type):
                objects.append(o)
    return objects

def get_one_object_by_type(obj_type):
    for layer in world:
        for o in layer:
            if isinstance(o, obj_type):
                return o
    return None

def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()
