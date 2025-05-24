import time
from Scripts.utils import config

def ignite(tile_objects, x, y, fspread):                #위치, 오브젝트 2차원 리스트를 인자로 받아 불로 바꿔줌.
    tile_objects[y][x] = 2                              #시간 재는 것은 fire_func 스크립트에서 진행.
    if not any(f.x == x and f.y == y for f in fspread): #이미 fspread에 좌표가 존재할 시 중복 append 방지
        fspread.append(config.Fire(x,y,time.time()))

def spread(tile_objects, x, y, tile_map, fspread):
    lx = config.OFFSET_WIDTH    #lx = limit x
    ly = config.OFFSET_HEIGHT   #ly = limit y
    dx = [0,1,0,-1]
    dy = [1,0,-1,0]
    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if (nx<lx or nx >= lx+20):          #탈출조건 1: x가 땅 범위 벗어남
            continue
        if (ny<ly or ny >= ly+10):          #탈출조건 2: y가 땅 범위 벗어남
            continue
        if (tile_map[ny][nx] == False):     #탈출조건 3: 땅이 열려있지 않음
            continue
        if (tile_objects[ny][nx] == 2):     #탈출조건 4: 이미 불이 번져있음음
            continue
        tile_objects[ny][nx] = 2            #모든 조건 만족 시 불(id: 2)로 만듦
        if not any(f.x == nx and f.y == ny for f in fspread):   #이미 fspread에 좌표가 존재할 시 중복 append 방지
            fspread.append(config.Fire(nx, ny, time.time()))


def control_fire(t_to_f, tile_objects, tile_map, fspread):
    #trash to fire process
    if len(t_to_f):         #t_to_f 리스트 사이즈가 0이 아니면 실행
        t = time.time()     #현재 시간
        current = t_to_f[0]
        if t - current.tick >= 1800:    #현재 시간과 비교: 1800초가 지나면 쓰레기가 불로 점화
            ignite(tile_objects, current.x, current.y, fspread)
            del(t_to_f[0])              #점화한 쓰레기는 삭제.

    #fire spreading process
    if len(fspread):        #fspread 리스트 사이즈가 0이 아니면 실행
        t = time.time()
        for current in fspread.copy():
            if t - current.tick >= 600:
                # spread 호출 시 fspread 전달
                spread(tile_objects, current.x, current.y, tile_map, fspread)
                #불 번지는건 바로 삭제하지 않음(불이 여러번 퍼질 수 있는 예외가 존재). 향후 불을 끄는 함수 구현할 때 삭제할 예정


#   Fire 객체는 x, y, tick 멤버로 이루어져있으며, 셋 다 int. x와 y는 좌표를 나타내며 tick은 생성 시간을 나타냄. config.py에 정의하였음음
