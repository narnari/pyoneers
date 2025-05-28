from Scripts.utils import config
import time
#마지막으로 저장한 시간
last_save_time = time.time()

def file_save(money, oxy, ground, objects, ground_count):  # money, oxygen, ground를 각각 str, str, 2D list로 받아 파일에 저장
    with open("About Game/save.txt", "w") as f:
        f.write(f"{money}\n")
        f.write(f"{oxy}\n")
        flat_ground = []
        flat_objects = []
        for row in range(config.OFFSET_HEIGHT, config.OFFSET_HEIGHT + config.HEIGHT_SIZE):
            for col in range(config.OFFSET_WIDTH, config.OFFSET_WIDTH + config.WIDTH_SIZE):
                flat_ground.append(str(ground[row][col]))
                flat_objects.append(str(objects[row][col]))

        f.write(' '.join(flat_ground))
        f.write("\n")
        f.write(' '.join(flat_objects))
        f.write("\n")

        f.write(f"{ground_count}")

def auto_save(money, oxy, ground, objects, interval):
    global last_save_time
    now = time.time()
    if now - last_save_time >= interval:
        file_save(money, oxy, ground, objects)
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


def file_load():  # 파일을 열어 money, oxygen, ground를 읽어들여 반환
    with open("About Game/save.txt", "r") as f:
        money = f.readline().strip()
        oxy = f.readline().strip()
        temp = f.readline().strip()
        temp = list(map(int, temp.split()))  # 1차원 리스트로 변환
        # 2차원 리스트 (10행 20열, 땅 크기)로 변환
        ground = [temp[i * 20:(i + 1) * 20] for i in range(11)]
        temp2 = f.readline().strip()
        temp2 = list(map(int, temp2.split()))
        objects = [temp2[i * 20:(i + 1) * 20] for i in range(11)]
        return money, oxy, ground, objects


def file_load_ground_counts():
    with open("About Game/save.txt", "r") as f:
        for i in range(4):
            f.readline()
        ground_counts = f.readline().strip()
        return ground_counts