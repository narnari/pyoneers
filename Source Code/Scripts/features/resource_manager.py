from Scripts.utils import config, assets
from Scripts.features import save_editor
import time
import math


# 인덱스 ↔ 이름 매핑
TREE_NAME = {
    3: "가문비나무",
    4: "아까시나무",
    5: "자작나무",
    6: "상수리나무"
}

# 나무 종류별 생산량 정보
TREE_STATS = {
    3: {"oxygen": 15, "money": 2},
    4: {"oxygen": 12, "money": 8},
    5: {"oxygen": 8, "money": 12},
    6: {"oxygen": 2, "money": 15}
}

# 기본 심기 비용
TREE_COST_INFO = {
    3: 50,
    4: 80,
    5: 80,
    6: 50
}

# 나무 인덱스별 심은 개수 저장용 딕셔너리
tree_counts = {
    3: 0,  # 가문비나무
    4: 0,  # 아까시나무
    5: 0,  # 자작나무
    6: 0   # 상수리나무
}

land_count = int(save_editor.file_load_ground_counts())

resources = {
    "stored_oxygen": 50, # 기본 제공 50
    "stored_money": 100, # 기본 제공 100
    "produce_oxygen": 0,
    "produce_money": 0,
    "last_update_time": time.time()  # 마지막으로 보유량 업데이트한 시간
}
resources["stored_money"],resources["stored_oxygen"] = save_editor.file_load_resource()
# 인덱스로 이름 얻기
def get_tree_name(index):
    return TREE_NAME.get(index, "Unknown")
# 나무 개수가 달라지니까 생산량 초기화하고 다시 계산
def reset_income():
    resources["produce_oxygen"] = 0
    resources["produce_money"] = 0

def generate(oxy, money):
    resources["produce_oxygen"] += oxy
    resources["produce_money"] += money

def update_resources():
    now = time.time()
    elapsed = now - resources["last_update_time"]

    if elapsed >= 1.0:
        seconds = int(elapsed)
        resources["stored_oxygen"] += resources["produce_oxygen"] * seconds
        resources["stored_money"] += resources["produce_money"] * seconds
        resources["last_update_time"] += seconds


def can_spend(oxy=0, money=0):
    # 자원 부족하면 False 반환
    if resources["stored_oxygen"] < oxy or resources["stored_money"] < money:
        return False
    
    resources["stored_oxygen"] -= oxy
    resources["stored_money"] -= money
    return True


def check_resource(tile_objects):
    reset_income()
    
    for idx in tree_counts:
        tree_counts[idx] = 0

    for row in range(4, config.GRID_HEIGHT - 1):
        for col in range(5, config.GRID_WIDTH - 5):
            obj = tile_objects[row][col]
            if obj in TREE_STATS:
                tree_counts[obj] += 1
                oxy = TREE_STATS[obj]["oxygen"]
                money = TREE_STATS[obj]["money"]
                generate(oxy, money)

def get_tree_cost(tree_index):
    count = tree_counts.get(tree_index, 0)
    base_cost = TREE_COST_INFO.get(tree_index, 0)
    return int((count + 1) ** 1.5 * base_cost) # 1.5배로 증가, 난이도 조절 위함
    #return int(math.sqrt(count + 1) * base_cost) # count + 1 인 이유는 처음 심을 때도 돈 쓰게 하기 위함


def draw_resources(screen):
    font = assets.load_font("Jalnan.ttf", 38)
    stored_oxy_text = font.render(f"{resources['stored_oxygen']} 개", True, config.BLACK)
    stored_money_text = font.render(f"{resources['stored_money']} 원", True, config.BLACK)
    produce_oxy_text = font.render(f"1초당 {resources['produce_oxygen']} 개", True, config.BLACK)
    produce_money_text = font.render(f"1초당 {resources['produce_money']} 원", True, config.BLACK)
    screen.blit(stored_oxy_text, (340, 40))
    screen.blit(stored_money_text, (340, 115))
    screen.blit(produce_oxy_text, (940, 40))
    screen.blit(produce_money_text, (940, 115))
