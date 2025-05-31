import time
from Scripts.utils import config
from Scripts.features import trash_editor, resource_manager

def ignite(tile_objects, x, y, fspread, tile_map):                #위치, 오브젝트 2차원 리스트를 인자로 받아 불로 바꿔줌.
    tile_objects[y][x] = 2                              #시간 재는 것은 fire_func 스크립트에서 진행.
    #땅도 다시 잠가버리고 땅 카운트도 낮춰버리기기
    tile_map[y][x] = 0
    resource_manager.land_count -= 1
    trash_editor.trash_count = trash_editor.decrease_count_when_ignite(trash_editor.trash_count)
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
        now = tile_objects[ny][nx]
        if (nx<lx or nx >= lx+config.WIDTH):          #탈출조건 1: x가 땅 범위 벗어남
            continue
        if (ny<ly or ny >= ly+config.HEIGHT_SIZE):          #탈출조건 2: y가 땅 범위 벗어남
            continue
        if (tile_map[ny][nx] == False):     #탈출조건 3: 땅이 열려있지 않음
            continue
        if (now == 2):     #탈출조건 4: 이미 불이 번져있음음
            continue
        if (now == 1):     #쓰레기에 불이 번지지면 쓰레기 카운트 -1
            trash_editor.trash_count = trash_editor.decrease_count_when_ignite(trash_editor.trash_count)
        #나머지 경우: (나무가 심겨있거나 땅이 비어있음) 해당 타일을 불로 만듦
        tile_objects[ny][nx] = 2
        #땅 잠구고 카운트 줄이깅
        tile_map[ny][nx] = 0
        resource_manager.land_count -= 1
        resource_manager.check_resource(tile_objects)
        if not any(f.x == nx and f.y == ny for f in fspread):   #이미 fspread에 좌표가 존재할 시 중복 append 방지
            fspread.append(config.Fire(nx, ny, time.time()))

def fire_on_load(x,y, fspread, tile_map):
    if not any(f.x == x and f.y == y for f in fspread):
        fspread.append(config.Fire(x,y,time.time()))

def control_fire(t_to_f, fspread, tile_objects, tile_map):
    #trash to fire process
    if len(t_to_f):         #t_to_f 리스트 사이즈가 0이 아니면 실행
        t = time.time()     #현재 시간
        current = t_to_f[0]
        if t - current.tick >= config.IGNITION_SEC:    #현재 시간과 비교: 1800초가 지나면 쓰레기가 불로 점화
            ignite(tile_objects, current.x, current.y, fspread, tile_map)
            del(t_to_f[0])              #점화한 쓰레기는 삭제.

    #fire spreading process
    if len(fspread):        #fspread 리스트 사이즈가 0이 아니면 실행
        t = time.time()
        for current in fspread.copy():
            if t - current.tick >= config.SPREAD_SEC:     #현재 시간과 비교: 600초가 지나면 쓰레기가 주변으로 번짐
                spread(tile_objects, current.x, current.y, tile_map, fspread)
                del(fspread[0])
                #불 번지는건 바로 삭제하지 않음(불이 여러번 퍼질 수 있는 예외가 존재). 
                #!!향후 불을 끄는 함수 구현할 때 삭제할 예정!!

def remove_fire(x,y, fspread, oxygen):  #fspread에서 x,y좌표에 해당하는 불을 제거(리스트 컴프리헨션)
    fspread[:] = [f for f in fspread if not (f.x == x and f.y == y)]
    oxygen -= 100
    return oxygen