# -*- coding: utf-8 -*-

#module import
import os
import requests
import numpy as np
import xmltodict, json
import datetime
import pickle
import webbrowser
import service_key as sv_key

#방법1.

#방법2. 서울 = 11

loc_code_list = [
    {'종로구': '11110'},
    {'중구': '11140'},
    {'용산구': '11170'},
    {'성동구': '11200'},
    {'광진구': '11215'},
    {'동대문구': '11230'},
    {'중랑구': '11260'},
    {'성북구': '11290'},
    {'강북구': '11305'},
    {'도봉구': '11320'},
    {'노원구': '11350'},
    {'은평구': '11380'},
    {'서대문구': '11410'},
    {'마포구': '11440'},
    {'양천구': '11470'},
    {'강서구': '11500'},
    {'구로구': '11530'},
    {'금천구': '11545'},
    {'영등포구': '11560'},
    {'동작구': '11590'},
    {'관악구': '11620'},
    {'서초구': '11650'},
    {'강남구': '11680'},
    {'송파구': '11710'},
    {'강동구': '11740'}
]

monthly_list = []

def trade_load(month):
    global Trade
    with open('trade'+str(month).zfill(2)+'.pickle', 'rb') as handle:
        Trade = pickle.load(handle)
    return Trade

def trade_save(month):
    with open('trade'+str(month).zfill(2)+'.pickle', 'wb') as handle:
        pickle.dump(Trade, handle, protocol=pickle.HIGHEST_PROTOCOL)

def crawling_init(input_date, input_area_code):
    service_key = sv_key.set_service_key()

    main_url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD='+input_area_code+'&DEAL_YMD='+str(input_date)+'&serviceKey='+service_key+''
    response = requests.get(url=main_url)
    print(response.status_code)

    result = json.dumps(xmltodict.parse(response.text), ensure_ascii=False)

    try:
        tmp_dict = json.loads(result)
        result_dict = tmp_dict["response"]["body"]["items"]["item"]
        print(result_dict)

        monthly_list.append(result_dict)

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)
        # ex는 발생한 에러의 이름을 받아오는 변수
        # 바로 stackoverflow 로 슥
        url = "http://stackoverflow.com/search?q=[python]+" + str(ex)
        webbrowser.open(url, new=2)  # new=2 means new tab


def main(input_year, input_area_code):
    # Trade[input_year] = {}

    # trade_load(1)

    for i in range(1, 13):

        input_date = input_year+str(i).zfill(2)
        # Trade["%s" % input_year]["%d" % str(i).zfill(2)] = {}
        print(input_date)
        #
        crawling_init(input_date, input_area_code)

    final_time = datetime.datetime.now().strftime('%H:%M')
    print("크롤링 완료 - %s" % final_time)
    print(len(monthly_list))
    print(monthly_list)

### 메인 함수 실행
if __name__ == "__main__":

    input_area_code = input("실거래가를 크롤링 할 지역을 고르세요.(ex: 11110): ")
    input_date = input("실거래가를 크롤링 할 년도를 입력하세요(ex: 2018): ")

    print(len(loc_code_list))

    main(input_date, input_area_code)