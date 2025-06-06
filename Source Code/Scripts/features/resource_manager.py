from Scripts.utils import config, assets
from Scripts.features import save_editor
import time

HOFF = config.OFFSET_HEIGHT
WOFF = config.OFFSET_WIDTH

# 레벨 저장용 (처음에 다 1 레벨)
tree_level_map = [[1 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
tree_upgrade_time = [[1800 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]


uptemp, leveltemp = save_editor.file_load_time_level()
for row in range(config.HEIGHT_SIZE):
    for col in range(config.WIDTH_SIZE):
        tree_upgrade_time[row + HOFF][col + WOFF] = uptemp[row][col]
        tree_level_map[row + HOFF][col + WOFF] = leveltemp[row][col]
last_update_time = time.time()


# 인덱스 ↔ 이름 매핑
TREE_NAME = {
    3: "가문비나무",
    4: "아까시나무",
    5: "자작나무",
    6: "상수리나무"
}

# 나무 종류별 생산량 기본 정보
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

def update_tree_time(tile_objects):
    global last_update_time
    now = time.time()
    elapsed = now - last_update_time
    if elapsed >= 1: # 1초씩 시간 감소
        for row in range(config.GRID_HEIGHT):
            for col in range(config.GRID_WIDTH):
                if tile_objects[row][col] in TREE_STATS:
                    if tree_upgrade_time[row][col] > 0:
                        tree_upgrade_time[row][col] -= 1
        last_update_time = now # 마지막 시간 갱신

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
                base_oxy = TREE_STATS[obj]["oxygen"]
                base_money = TREE_STATS[obj]["money"]
                 # 레벨이 오를수록 2.5배씩 증가
                oxy = int(base_oxy * (2.5 ** (tree_level_map[row][col] - 1)))
                money = int(base_money * (2.5 ** (tree_level_map[row][col] - 1)))
                generate(oxy, money)

def get_tree_cost(tree_index):
    count = tree_counts.get(tree_index, 0)
    base_cost = TREE_COST_INFO.get(tree_index, 0)
    return int((count + 1) ** 1.5 * base_cost) # 1.5배로 증가, 난이도 조절 위함


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
