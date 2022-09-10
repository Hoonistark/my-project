import json
import time,datetime
from itertools import chain
from collections import defaultdict


dic1 = {}

dic2 = {}




dic3 = defaultdict(list)

file_name1 = '입고.json'
file_name2 = '출고.json'

def move(method,location,product,number,note):
    global dic1
    aa = location
    bb = product.upper()                                # 대문자 변경
    cc = number
    dd = note
    if method == '입고':
        dic1[time()] = {aa:[method,time(),bb,cc,note]}
    else:
        dic2[time()] = {aa:[method,time(),bb,-cc,note]}

def in_put(method):
    location = input(f"{method}처를 입력: ")
    product = input("제품명 입력: ")
    number = int(input("수량 입력: "))
    note = input("비고 입력: ")
    move(method,location,product,number,note)
    while 1:
        x = input("제품 추가입력 y or n :")
        if x == 'y':
            product = input("제품명 입력: ")
            number = int(input("수량 입력: "))
            note = input("비고 입력: ")
            move(method,location,product,number,note)
        elif x == 'n':
            break
    

def product():
    for k,v in dic1.items():
        for i in v:
            print(v[i][1],v[i][2],v[i][3],v[i][4])

def adjustment(): #수량 조절
    pass
    
def time():
    now = datetime.datetime.now()
    NDT = now.strftime('%m/%d %H:%M:%S')
    return NDT

def histoty(): #입출고내역
    global dic1,dic2,dic3
    for k, v in chain(dic1.items(), dic2.items()):
        dic3[k].append(v)
    x = sorted(dic3)
    for i in range(len(x)):
        print(dic3[x[i]])

def json_save1():
    with open(file_name1,'w') as f:
        json.dump(dic1, f)

def json_save2():
    with open(file_name2,'w') as f:
        json.dump(dic1, f)

def json_load1():
    with open(file_name1, 'r') as f:
        dic11 = json.load(f, encoding = 'utf-8')

def json_load2():
    with open(file_name1, 'r') as f:
        dic22 = json.load(f, encoding = 'utf-8')
        
    
while 1:
    start = '''
    1. 제품목록
    2. 입고
    3. 출고
    4. 조정
    5. 입출고내역
    6. 위치별 재품목록
    7. 저장
    8. 로드
    '''
    print(start)

    a = int(input("값 입력: "))
    print()
    if a == 1:
        product()
    elif a == 2:
        in_put("입고")
    elif a == 3:
        in_put("출고")
    elif a == 4:
        adjustment()
    elif a == 5:
        histoty()
    elif a == 6:
        in_put("출고")
    elif a == 7:
        json_save1()
        json_save2()
    elif a == 8:
        json_load1()
        json_load2()
        
