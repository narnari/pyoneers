from Scripts.utils import config, assets
import time

resources = {
    "stored_oxygen": 0,
    "stored_money": 0,
    "produce_oxygen": 0,
    "produce_money": 0,
    "last_update_time": time.time()  # 마지막으로 보유량 업데이트한 시간
}

font = assets.load_font("Jalnan.ttf", 38)

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
        # 경과 시간 동안 얻은 산소/돈 계산 (1초 단위로만)
        seconds = int(elapsed)
        resources["stored_oxygen"] += resources["produce_oxygen"] * seconds
        resources["stored_money"] += resources["produce_money"] * seconds
        resources["last_update_time"] = now  # 시간 갱신

def spend(oxy=0, money=0):
    resources["stored_oxygen"] -= oxy
    resources["stored_money"] -= money

def check_resource(tile_objects):
    reset_income()
    for row in range(4, config.GRID_HEIGHT - 1):
        for col in range(5, config.GRID_WIDTH - 5):
            obj = tile_objects[row][col]
            if obj == 3:  # 가문비
                generate(15, 2)
            elif obj == 4:  # 아까시
                generate(12, 8)
            elif obj == 5:  # 자작
                generate(8, 12)
            elif obj == 6:  # 상수리
                generate(2, 15)

def draw_resources(screen):
    stored_oxy_text = font.render(f"{resources['stored_oxygen']} 개", True, config.BLACK)
    stored_money_text = font.render(f"{resources['stored_money']} 원", True, config.BLACK)
    produce_oxy_text = font.render(f"1초당 {resources['produce_oxygen']} 개", True, config.BLACK)
    produce_money_text = font.render(f"1초당 {resources['produce_money']} 원", True, config.BLACK)
    screen.blit(stored_oxy_text, (340, 40))
    screen.blit(stored_money_text, (340, 115))
    screen.blit(produce_oxy_text, (940, 40))
    screen.blit(produce_money_text, (940, 115))
