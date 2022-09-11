import json
import os
import time
from datetime import datetime
from texttable import Texttable
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import (
    has_completions,
    completion_is_selected,
)
from prompt_toolkit.application.current import get_app


def prompt_autocomplete():
    app = get_app()
    b = app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


# Override enter key to automatically perform first completion.
key_bindings = KeyBindings()
filter = has_completions & ~completion_is_selected


@key_bindings.add("enter", filter=filter)
def _(event):
    event.current_buffer.go_to_completion(0)
    event.current_buffer.validate_and_handle()


file_name = 'DB.json'


def autoComp(method, lists, preRun):
    lists = FuzzyWordCompleter(lists)
    if method in ["입고", "출고", "조정"]:
        method = f"{method}:"
    if preRun == True:
        response = prompt(f'{method}',
                          completer=lists,
                          complete_while_typing=True,
                          key_bindings=key_bindings,
                          pre_run=prompt_autocomplete
                          )
    else:
        response = prompt(f'{method}',
                          completer=lists,
                          complete_while_typing=True,
                          key_bindings=key_bindings,
                          )

    return response


def move(method, location, product, number, note):
    dic1 = json_load()
    product = product.upper()
    number = int(number)
    timeStamp = time.time()
    if method == "출고":
        number = -number
    try:
        ydata = dic1[product][0]
        ynumber = list(ydata.values())[0][4]
        nowNumber = number + ynumber
        dic1[product].insert(
            0, {timeStamp: [method, location, number, ynumber, nowNumber, note]})
    except:
        dic1[product] = []
        dic1[product].insert(
            0, {timeStamp: [method, location, number, 0, number, note]})
    json_save(dic1)


def in_put(method):
    item = item_load()
    location = autoComp(method, item["location"], True)
    x = "y"
    lst = ["제품명:", "수량:", "비고:"]
    while 1:
        mySale = []
        index = 0
        if x == 'y':
            while index < len(lst):
                if index == 0:
                    myData = autoComp(f'{lst[index]}', item["product"], False)
                else:
                    myData = input(f"{lst[index]}")
                if myData == "back":
                    if index == 0:
                        input("첫입력입니다:")
                    else:
                        index = index - 1
                else:
                    mySale.append(myData)
                    index = index + 1

                if index == len(lst):
                    break

            move(method, location, mySale[0], mySale[1], mySale[2])
        else:
            break
        x = autoComp(f'제품추가:', ["y", "n"], True)


def product():
    dic1 = json_load()
    item = item_load()
    item["location"].insert(0, "All")
    location = autoComp("명령:", item["location"], True)
    while 1:
        table = Texttable()
        tableList = [["제품명", "수량"]]
        prodic = {}
        for k, v in dic1.items():
            for i in v:
                value = list(i.values())[0]
                amount = value[2]
                if location == "All":
                    try:
                        prodic[k] = prodic[k]+amount
                    except:
                        prodic[k] = amount
                else:
                    if value[1] == location:
                        try:
                            prodic[k] = prodic[k]+amount
                        except:
                            prodic[k] = amount

        for k, v in prodic.items():
            if v > 0:
                tableList.append([k, v])
        table.add_rows(tableList)
        print(table.draw())
        answer = input("BACK:")
        break


def edit():  # 수량 조절
    pass


def times():
    now = datetime.datetime.now()
    NDT = now.strftime('%m/%d %H:%M:%S')
    return now


def history(data):  # 입출고내역
    dic1 = json_load()
    while 1:
        table = Texttable()
        tableList = [["거래처", "거래시간", "거래구분", "제품명", "수량", "전", "후", "비고"]]
        for k, v in dic1.items():
            for key in v:
                value = list(key.values())[0]
                key = list(key.keys())[0].split(".")[0]
                times = datetime.fromtimestamp(float(key))
                value.insert(0, value[1])
                value.insert(1, times)
                value[3] = k
                if data != "none":
                    if value[0] == data:
                        tableList.append(value)
                else:
                    tableList.append(value)
        table.add_rows(tableList)
        print(table.draw())
        answer = input("BACK:")
        break


def json_save(temp):
    with open(file_name, 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(temp, ensure_ascii=False))
    print(f"{file_name} Save")


def json_load():
    dic1 = {}
    with open(file_name, 'r', encoding="UTF-8-sig") as fp:
        dic1 = json.load(fp)
    print(f"{file_name} Load")
    return dic1


def item_load():
    data = {}
    with open("item.json", 'r', encoding="UTF-8-sig") as fp:
        data = json.load(fp)
    print(f"item.json Load")
    return data


while 1:
    start = {
        1: "제품현황",
        2: "입고",
        3: "출고",
        4: "조정",
        5: "입출고내역",
        6: "위치별 제품목록",
    }

    table = Texttable()
    tableList = [["No.", f"File:{file_name}"]]
    for k, v in start.items():
        tableList.append([k, v])
    table.add_rows(tableList)
    print(table.draw())
    a = input("값 입력: ")

    print()
    if a == "1":
        product()
    elif a == "2":
        in_put("입고")
    elif a == "3":
        in_put("출고")
    elif a == "4":
        edit()
    elif a == "5":
        history("none")
    elif a == "6":
        item = item_load()
        location = autoComp(f'거래처:', item["location"], True)
        history(location)
