#!/usr/bin/python
# -*- coding: utf-8 -*-


search_time = 0.5    # 잔여백신을 해당 시간마다 한번씩 검색합니다. 단위: 초
open_delay = 0        # 잔여백신 발생 시 브라우저를 열기 전 지연시간. 단위: 초




import requests
import json
import urllib3
import os
import time
import datetime
from sys import platform
urllib3.disable_warnings()


print("예약시도할 백신 코드를 알려주세요. 예시: VEN00013 ")
print("화이자         : VEN00013")
print("모더나         : VEN00014")
print("아스크라제네카   : VEN00015")
print("얀센          : VEN00016")
VAC = str(input("예약시도할 백신 코드를 알려주세요. : "))

def pretty_print(json_string):
    json_object = json.loads(json_string)
    for org in json_object["organizations"]:
        if org.get('status') == "CLOSED" or org.get('status') == "EXHAUSTED":
            continue
        print("잔여갯수: " + str(org.get('leftCounts'))
              + "\t상태: " + org.get('status')
              + "\t기관명: " + org.get("orgName")
              + "\t주소: " + org.get("address"))

# ===================================== def ===================================== #
print("사각형 모양으로 백신범위를 지정한 뒤, 해당 범위 안에 있는 백신을 조회해서 남은 백신이 있으면 Chrome 브라우저를 엽니다.")
topx = str(input("사각형의 위쪽 좌측 x값을 넣어주세요. 127.xxxxxx   : "))
topy = str(input("사각형의 위쪽 좌측 y값을 넣어주세요 37.xxxxx      : "))
botx = str(input("사각형의 아래쪽 우측 x값을 넣어주세요 127.xxxxx    : "))
boty = str(input("사각형의 아래쪽 우측 y값을 넣어주세요 37.xxxxx     : "))
APIURL = 'https://vaccine-map.kakao.com/api/v2/vaccine/left_count_by_coords'
APIdata = '{"bottomRight":{"x":' + botx + ',"y":' + boty + '},"onlyLeft":false,"order":"latitude","topLeft":{"x":' + topx + ',"y":' + topy + '}}'
print(APIdata)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://vaccine.kakao.com",
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 9.3.8",
    "Referer":"https://vaccine.kakao.com/reservation/{a['orgCode']}?from=Map&code=VEN00013",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close"
}

done = False
while done == False:
    time.sleep(search_time)
    response = requests.post(APIURL, data=APIdata, headers=headers, verify=False)

    received_API_status_code = response.status_code
    received_API_data = response.text

    pretty_print(received_API_data)
    print(datetime.datetime.now())

    jsonloaded = json.loads(received_API_data)
    jsonData = jsonloaded["organizations"]
    found = False
    for x in jsonData:
        if x.get('status') == "AVAILABLE" or x.get('leftCounts') != 0:
            found = x
            done = True
            break
        # keys = x.keys()
        # print(keys)
        # values = x.values()
        # print(values)


print("--- found")
print(found)
orgCdCode = str(x.get('orgCode'))
latkey = str(x.get('y'))
lngkey = str(x.get('x'))

time.sleep(open_delay)
if platform == "linux" or platform == "linux2":
    os.system('/usr/bin/google-chrome "https://vaccine.kakao.com/reservation/' + orgCdCode + '?from=Map&code=' + VAC + '"')
elif platform == "darwin":
    os.system('/usr/bin/open -a "/Applications/Google Chrome.app" "https://vaccine.kakao.com/reservation/' + orgCdCode + '?from=Map&code=' + VAC + '"')
elif platform == "win32":
    os.system('start chrome.exe "https://vaccine.kakao.com/reservation/' + orgCdCode + '?from=Map&code=' + VAC + '"')
