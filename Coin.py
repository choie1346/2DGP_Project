from pico2d import load_image
import game_world
import common
from random import randint

class Coin:
        def __init__(self, x, y):
            self.image = load_image("Items/coins/coin.png")
            self.x, self.y = x, y

        def draw(self):
            self.image.clip_draw(0, 0, 63, 54, self.x, self.y, 50, 50)

        def update(self):
            pass

        def get_bb(self):
            return self.x - 25, self.y - 25, self.x + 25, self.y + 25

        def handle_collision(self, group, other):
            if group == 'animal:coin':
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
                # print(f'코인 획득! 현재 코인 수: {common.COINS}')

class CoinSpawner:
    def __init__(self, food):
        if common.STAGE == 1:
            rad = randint(0, 100)
            print(f'Coin spawn probability: {rad:.2f}')
            if rad > common.COIN_SPAWN_PROBABILITY:
                game_world.remove_object(self)
                return
            coin = Coin(food.x, food.y)
            game_world.add_object(coin, 1)
            game_world.add_collision_pair("animal:coin", None, coin)
            game_world.remove_object(self)
