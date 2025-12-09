import common
from random import randint, uniform
from pico2d import load_image, load_font
import game_world

quests = [
    {"코인으로 이것 좀 사겠니?" : randint(common.coin_number, common.coin_number + 500)},
    {"나에게 음식 좀 줄 수 있니?": randint(10, 50)},
    {"이거랑 교환하지 않을래?": randint(1, 3)},
    {"이걸 줄게!" : 1}
]

rewards = [
    {"코인을 주마" : randint(100, 500)},
    {"이거 먹으렴!" : randint(10, common.FOOD_MAX_NUMBER)},
    {"업그레이드를 해주마" : randint(1, 3)},
    {"유니콘이 되고 싶다고?" : 1}  # 키를 일치시킴
]

# 애니메이션 상태별 이미지 범위
WALK_LEFT = (0, 3)    # 왼쪽으로 걸어나옴 (인덱스 0~4)
IDLE_FRONT = (4, 4)   # 앞을 보고 서있음 (인덱스 5~9)
WALK_RIGHT = (5, 8) # 오른쪽으로 나감 (인덱스 10~14)

farmer_images = [
    "Characters/farmer/left2.png",
    "Characters/farmer/left3.png",
    "Characters/farmer/left4.png",
    "Characters/farmer/left5.png",
    "Characters/farmer/front2.png",
    "Characters/farmer/right2.png",
    "Characters/farmer/right3.png",
    "Characters/farmer/right4.png",
    "Characters/farmer/right5.png"
]

class QuestSpawner:
    def __init__(self):
        # print("QuestSpawner initialized")
        self.current_time = 0.0
        self.spawn_time = uniform(30.0, 60.0)  # 30~60초마다 퀘스트 출현
        self.active_farmer = None  # 현재 활성화된 농부
        self.active_quest = None  # 현재 활성화된 퀘스트

    def update(self):
        if common.STAGE == 1:
            if self.active_farmer is None or self.active_farmer.state == 'hidden':
                self.current_time += 0.01
                # print(f'Next quest in: {self.spawn_time - self.current_time:.2f} sec')

                if self.current_time >= self.spawn_time:
                    self.spawn_quest()
                    self.current_time = 0.0
                    self.spawn_time = uniform(30.0, 60.0)

            if self.active_farmer and self.active_farmer.state == 'hidden':
                game_world.remove_object(self.active_farmer)
                game_world.remove_collision_object(self.active_farmer)
                self.active_farmer = None
                self.active_quest = None

    def spawn_quest(self):
        farmer = Farmer()
        game_world.add_object(farmer, 1)
        game_world.add_collision_pair('animal:farmer', None, farmer)

        # 새로운 퀘스트 생성
        quest = Quest()
        farmer.set_quest(quest)

        self.active_farmer = farmer
        self.active_quest = quest

        # print(f"New quest spawned! Next spawn in {self.spawn_time:.1f} seconds")

    def draw(self):
        pass


class Farmer:
    def __init__(self):
        self.images = [load_image(img) for img in farmer_images]
        self.font = load_font("Galmuri11.ttf", 16)
        self.current_image_index = 0
        self.frame_counter = 0
        self.x, self.y = 1200, 300  # 화면 오른쪽 밖에서 시작
        self.target_x = 850  # 목표 위치 (화면 오른편)

        # 상태: 'walk_in' -> 'idle' -> 'walk_out' -> 'hidden'
        self.state = 'walk_in'
        self.anim_start, self.anim_end = WALK_LEFT
        self.anim_index = 0

        self.talking_box_image = load_image("Graphic/textbox/talking_popup.png")
        self.reward_image = load_image("Characters/farmer/chest.png")
        self.quest = None  # Quest 객체를 저장할 변수
        self.can_complete = False

    def set_quest(self, quest):
        self.quest = quest

    def draw(self):
        if self.state != 'hidden':
            current_image = self.images[self.current_image_index]
            current_image.clip_draw(0, 0, 80, 80, self.x, self.y, 150, 150)

            if self.state == 'idle' and self.quest:
                # 말풍선 그리기
                self.talking_box_image.clip_draw(0, 0, 47, 28, self.x, self.y + 150, 250, 180)

                # Quest 정보 텍스트 그리기
                # 퀘스트 이름
                quest_text = f"{self.quest.quest_name}"
                self.font.draw(self.x - 110, self.y + 200, quest_text, (100, 50, 50))

                # 요구사항
                requirement_text = self.quest.get_requirement_text()
                self.font.draw(self.x - 110, self.y + 180, requirement_text, (100, 50, 50))

                # 보상
                reward_text = self.quest.get_reward_text()
                self.font.draw(self.x - 110, self.y + 140, reward_text, (50, 100, 50))

                if self.can_complete:
                    self.reward_image.clip_draw(0, 0, 32, 32, self.x + 80, self.y + 140, 40, 40)


    def update(self):
        if self.state == 'walk_in':
            # 왼쪽으로 걸어 들어옴
            self.x -= 3
            self._update_animation(WALK_LEFT)

            if self.x <= self.target_x:
                self.x = self.target_x
                self.state = 'idle'
                self.current_image_index = 4
                self.frame_counter = 0

        elif self.state == 'idle':
            self.can_complete = self.can_complete_quest()
            pass

        elif self.state == 'walk_out':
            # 오른쪽으로 걸어 나감
            self.x += 3
            self._update_animation(WALK_RIGHT)

            if self.x >= 1200:
                self.state = 'hidden'

    def _update_animation(self, anim_range):
        self.frame_counter += 1

        if self.frame_counter >= 5:  # 5프레임마다 이미지 변경
            start, end = anim_range
            self.anim_index = (self.anim_index + 1) % 4  # 4개의 이미지만 있으므로 % 4
            self.current_image_index = start + self.anim_index
            self.frame_counter = 0
            print(f'{self.x, self.y}')

    def can_complete_quest(self):
        """퀘스트 완료 가능 여부 확인 (차감하지 않고 확인만)"""
        if self.quest is None:
            return False

        # quest_type에 따라 요구사항 확인 (차감하지 않음!)
        if self.quest.quest_type == 0:  # 코인으로 이것 좀 사겠니?
            return common.coin_number >= self.quest.requirement

        elif self.quest.quest_type == 1:  # 나에게 음식 좀 줄 수 있니?
            from Food import Food
            foods = game_world.get_objects_by_type(Food)
            return len(foods) >= self.quest.requirement

        elif self.quest.quest_type == 2:  # 이거랑 교환하지 않을래?
            # 디버프 요구사항 확인
            if self.quest.requirement == 1:
                return common.speed_level > 0  # 속도 레벨이 0보다 커야 다운그레이드 가능
            elif self.quest.requirement == 2:
                return common.food_spawn_level > 0  # 음식 생성 레벨이 0보다 커야 다운그레이드 가능
            elif self.quest.requirement == 3:
                return common.food_upgrade_level > 0  # 음식 품질 레벨이 0보다 커야 다운그레이드 가능
            return True

        elif self.quest.quest_type == 3:  # 이걸 줄게!
            return True  # 무료 선물

        return False

    def complete_quest(self):
        if self.state == 'idle':
            self.state = 'walk_out'
            self.anim_start, self.anim_end = WALK_RIGHT
            self.anim_index = 0

    def get_bb(self):
        return self.x - 75, self.y - 75, self.x + 75, self.y + 75

    def handle_collision(self, group, other):
        print(f"Farmer 충돌 감지! group: {group}, other: {other}")

class Quest:
    def __init__(self):
        quest_type = randint(0, 3)
        reward_type = randint(0, 3)

        quest_dict = quests[quest_type]
        self.quest_name = list(quest_dict.keys())[0]
        self.requirement = list(quest_dict.values())[0]
        self.quest_type = quest_type


        reward_dict = rewards[reward_type]
        self.reward_name = list(reward_dict.keys())[0]
        self.reward = list(reward_dict.values())[0]
        self.reward_type = reward_type
        self.is_completed = False


    def get_requirement_text(self):
        if self.quest_type == 0:  # 코인으로 이것 좀 사겠니?
            return f"요구: 코인 {self.requirement}개"
        elif self.quest_type == 1:  # 나에게 음식 좀 줄 수 있니?
            return f"요구: 음식 {self.requirement}개"
        elif self.quest_type == 2:  # 이거랑 교환하지 않을래?
            if self.requirement == 1:
                return "요구: 속도 감소"
            elif self.requirement == 2:
                return "요구: 먹이 생성 시간 증가"
            elif self.requirement == 3:
                return "요구: 음식 다운그레이드"

        elif self.quest_type == 3:  # 이걸 줄게!
            return "요구: 없음"
        return f"요구: {self.requirement}"

    def get_reward_text(self):
        if self.reward_type == 0:  # 코인을 주마
            return f"보상: 코인 {self.reward}개"
        elif self.reward_type == 1:  # 이거 먹으렴!
            return f"보상: 음식 {self.reward}개"
        elif self.reward_type == 2:  # 업그레이드를 해주마
            if self.reward == 1:
                return "보상: 속도 업그레이드"
            elif self.reward == 2:
                return "보상: 먹이 생성 시간 단축"
            elif self.reward == 3:
                return "보상: 음식 업그레이드"

        elif self.reward_type == 3:  # 유니콘이 되고 싶다고?
            return "보상: 유니콘 변신!"
        return f"보상: {self.reward_name}"

    def complete_quest(self):
        self.is_completed = True

        # 요구사항 처리 (차감 또는 디버프 적용)
        if self.quest_type == 0:  # 코인으로 이것 좀 사겠니?
            common.coin_number -= self.requirement
            print(f"코인 {self.requirement}개 지불")

        elif self.quest_type == 1:  # 나에게 음식 좀 줄 수 있니?
            # game_world에서 Food 객체 제거
            from Food import Food
            foods = game_world.get_objects_by_type(Food)
            for i in range(min(self.requirement, len(foods))):
                food = foods[i]
                game_world.remove_object(food)
                game_world.remove_collision_object(food)
            print(f"음식 {self.requirement}개 제공")

        elif self.quest_type == 2:  # 이거랑 교환하지 않을래?
            # 디버프 적용
            if self.requirement == 1:
                common.downgrade_speed()
            elif self.requirement == 2:
                common.downgrade_food_spawn()
            elif self.requirement == 3:
                common.downgrade_food_quality()

        # 보상 지급
        if self.reward_type == 0:  # 코인을 주마
            common.coin_number += self.reward
            print(f"코인 {self.reward}개 획득!")

        elif self.reward_type == 1:  # 이거 먹으렴!
            # 음식 생성
            from Food import Food
            for i in range(self.reward):
                food = Food()
                game_world.add_object(food, 1)
                game_world.add_collision_pair('animal:food', None, food)
            print(f"음식 {self.reward}개 획득!")

        elif self.reward_type == 2:  # 업그레이드를 해주마
            if self.reward == 1:
                common.upgrade_speed()
            elif self.reward == 2:
                common.upgrade_food_spawn()
            elif self.reward == 3:
                common.upgrade_food_quality()

        elif self.reward_type == 3:  # 유니콘이 되고 싶다고?
            # 유니콘으로 변신 (동물의 current를 최대치로)
            from Animal import Animal
            animal = game_world.get_objects_by_type(Animal)
            if animal:
                animal[0].current = 8  # 유니콘은 인덱스 8
                animal[0].image = load_image(f"Animals/Unicon/{['front', 'back', 'left', 'right'][animal[0].dir]}.png")
            print("유니콘으로 변신!")

        return f"Quest '{self.quest_name}' completed! Reward: {self.reward}"
