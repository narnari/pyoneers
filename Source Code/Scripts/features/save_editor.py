

def file_save(money, oxy, ground, objects):  # money, oxygen, ground를 각각 str, str, 2D list로 받아 파일에 저장
    with open("About Game/save.txt", "w") as f:
        f.write(f"{money}\n")
        f.write(f"{oxy}\n")
        # 2차원 리스트를 1차원 리스트로 평탄화한 후 문자열로 변환하여 저장
        flat_ground = [str(cell) for row in ground for cell in row]
        f.write(' '.join(flat_ground))
        flat_objects = [str(cell) for row in objects for cell in row]
        f.write(' '.join(flat_objects))


def file_load():  # 파일을 열어 money, oxygen, ground를 읽어들여 반환
    with open("About Game/save.txt", "r") as f:
        money = f.readline().strip()
        oxy = f.readline().strip()
        temp = f.readline().strip()
        temp = list(map(int, temp.split()))  # 1차원 리스트로 변환
        # 2차원 리스트 (10행 20열, 땅 크기)로 변환
        ground = [ground[i * 20:(i + 1) * 20] for i in range(10)]
        temp2 = f.readline().strip()
        temp2 = list(map(int, temp2.split()))
        objects = [objects[i * 20:(i + 1) * 20] for i in range(10)]
        return money, oxy, ground, objects
    
#ground : 땅의 열림 유무를 저장하는 리스트, tile_map 리스트에 대응
#objects : 땅에 놓여진 오브젝트 ID를 저장하는 리스트, tile_objects 리스트에 대응응