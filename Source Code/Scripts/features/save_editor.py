from Scripts.utils import config
import time
#마지막으로 저장한 시간
last_save_time = time.time()

def file_save(money, oxy, ground, objects, ground_count, tutorial, tree_up_time, tree_level):  # money, oxygen, ground를 각각 str, str, 2D list로 받아 파일에 저장
    
    with open("About Game/save.txt", "w") as f:
        f.write(f"{money}\n")
        f.write(f"{oxy}\n")
        
        flat_ground = []
        flat_objects = []
        flat_tree_up_time = []
        flat_tree_level = []
        for row in range(config.OFFSET_HEIGHT, config.OFFSET_HEIGHT + config.HEIGHT_SIZE):
            for col in range(config.OFFSET_WIDTH, config.OFFSET_WIDTH + config.WIDTH_SIZE):
                flat_ground.append(str(ground[row][col]))
                flat_objects.append(str(objects[row][col]))
                flat_tree_up_time.append(str(tree_up_time[row][col]))
                flat_tree_level.append(str(tree_level[row][col]))
                
        f.write(' '.join(flat_ground))
        f.write("\n")
        f.write(' '.join(flat_objects))
        f.write("\n")
        #트리 레벨과 업그레이드 타임도 게임 내에선 2차원 리스트로 사용되는데, 저장은 1차원 리스트로 바꿔서 함.
        f.write(f"{ground_count}\n")
        f.write(f"{tutorial}\n")
        f.write(' '.join(flat_tree_up_time))
        f.write('\n')
        f.write(' '.join(flat_tree_level))
        f.write('\n')

def auto_save(money, oxy, ground, objects, ground_count, tutorial, tree_up_time, tree_level, interval):
    global last_save_time
    now = time.time()
    if now - last_save_time >= interval:
        file_save(money, oxy, ground, objects, ground_count, tutorial, tree_up_time, tree_level)
        last_save_time = now

def file_load_tile():                       #타일의 정보만 불러오기기
    with open("About Game/save.txt", "r") as f:
        #첫 두줄은 걍 읽고 버려 ㅋㅋ
        f.readline().strip()
        f.readline().strip()
        temp = f.readline().strip()
        temp = list(map(int, temp.split()))  # 1차원 리스트로 변환
        # 2차원 리스트 (10행 20열, 땅 크기)로 변환
        ground = [temp[i * 20:(i + 1) * 20] for i in range(11)]
        temp2 = f.readline().strip()
        temp2 = list(map(int, temp2.split()))
        objects = [temp2[i * 20:(i + 1) * 20] for i in range(11)]
        return ground, objects

def file_load_resource():                   #자원만 불러오기
    with open("About Game/save.txt", "r") as f:
        money = f.readline().strip()
        money = int(money)
        oxy = f.readline().strip()
        oxy = int(oxy)
        return money, oxy

def file_load_time_level():  # 나무 업그레이드 남은시간과 레벨 반환
    with open("About Game/save.txt", "r") as f:
        for i in range(6):
           f.readline()
        temp = f.readline().strip()
        temp = list(map(int, temp.split()))
        tree_up_time = [temp[i * 20:(i + 1) * 20] for i in range(11)]
        
        temp2 = f.readline().strip()
        temp2 = list(map(int, temp2.split()))
        tree_level = [temp2[i * 20: (i + 1) * 20] for i in range(11)]
        return tree_up_time, tree_level



def file_load_ground_counts():
    with open("About Game/save.txt", "r") as f:
        for i in range(4):
            f.readline()
        ground_counts = f.readline().strip()
        return ground_counts
    
def file_load_tutorial():
    with open("About Game/save.txt", "r") as f:
        for i in range(5):
            f.readline()
        tutorial = f.readline().strip()
        return tutorial
    