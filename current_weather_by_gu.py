import requests
from bs4 import BeautifulSoup
import pygame as pg
import time
import datetime

gu_list = [
    '강남구', '강동구', '강북구', '강서구', '관악구',
    '광진구', '구로구', '금천구', '노원구', '도봉구',
    '동대문구', '동작구', '마포구', '서대문구', '서초구',
    '성동구', '성북구', '송파구', '양천구', '영등포구',
    '용산구', '은평구', '종로구', '중구', '중랑구'
]

# 구 선택 표 그리기
def draw_gu_table():
    x_count = 0
    y_count = 0
    if GU_TABLE == True:
        gu_select = NANUMFONT_M.render("현재 날씨 확인 - 구 선택", True, (0, 0, 0))
        SCREEN.blit(gu_select, (TABLE_X_START + 190, TABLE_Y_START - 60))
        for gu in gu_list:
            gu_name = NANUMFONT_GU_NAME.render(gu, True, (0, 0, 0))
            pg.draw.rect(SCREEN, (0, 0, 0), (TABLE_X_START + TABLE_CELL_X_SIZE * x_count, TABLE_Y_START + TABLE_CELL_Y_SIZE * y_count, TABLE_CELL_X_SIZE, TABLE_CELL_Y_SIZE), 1)
            SCREEN.blit(gu_name, (TABLE_X_START + TABLE_CELL_X_SIZE * x_count + 35, TABLE_Y_START + TABLE_CELL_Y_SIZE * y_count + 20))
            x_count += 1
            if x_count == 5:
                x_count = 0
                y_count += 1
            else:
                pass

# 선택한 구의 현재 날씨 정보 가져오기 & 선택한 구의 현재 날씨 정보 그리기
def draw_current_weather_info(gu_name):
    global GU_TABLE
    if gu_name == '':
        pass
    else:
        GU_TABLE = False # 구가 선택되었으므로 구 선택 표를 그리지 않는다.
        
        # 현재 날씨 정보 가져오기
        WEATHER_INFO_URL = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}+날씨&oquery=서울+온도&tqi=hWXeVdp0YiRsseiyB6Rssssst1o-241293'.format(gu_name)
        response_wt_info = requests.get(WEATHER_INFO_URL)
        
        html_wt = response_wt_info.content
        soup = BeautifulSoup(html_wt, 'html.parser')
        
        # 현재 온도
        temp = 'ㆍ' + soup.find(class_='temperature_text').find('strong').text + ' | 어제보다 ' + soup.find(class_='temperature_info').find('span').text
        
        # 날씨
        weather = 'ㆍ' + '날씨 : ' + soup.find(class_='weather_main').find(class_='blind').text
        
        # 체감 온도 / 습도 / 바람
        summary_term = soup.find(class_='summary_list').find_all(class_='term')
        summary_desc = soup.find(class_='summary_list').find_all(class_='desc')
        sensory_temp = 'ㆍ' + summary_term[0].text + '온도 : ' + summary_desc[0].text
        humidity = 'ㆍ' + summary_term[1].text + ' : ' + summary_desc[1].text
        wind_velocity = 'ㆍ' + summary_term[2].text + ' : ' + summary_desc[2].text
        
        # 초미세먼지 / 미세먼지 / 자외선 / 일몰 시간
        chart_list = soup.find(class_='today_chart_list').find_all('li')
        ultrafine_dust = 'ㆍ' + chart_list[0].find('strong').text + ' : ' + chart_list[0].find('span').text
        fine_dust = 'ㆍ' + chart_list[1].find('strong').text + ' : ' + chart_list[1].find('span').text
        uv_rays = 'ㆍ' + chart_list[2].find('strong').text + ' : ' + chart_list[2].find('span').text
        sunset_time = 'ㆍ' + chart_list[3].find('strong').text + ' : 오후 ' + chart_list[3].find('span').text

        # 화면에 그리기
        gu_name_txt = NANUMFONT_M.render(gu_name, True, (0, 0, 0))
        gu_reselect_txt = NANUMFONT_M.render("구 선택", True, (0, 0, 0))
        
        gu_temp_txt = NANUMFONT_M.render(temp, True, (0, 0, 0))
        gu_weather_txt = NANUMFONT_M.render(weather, True, (0, 0, 0))
        gu_sensory_temp_txt = NANUMFONT_M.render(sensory_temp, True, (0, 0, 0))
        gu_humidity_txt = NANUMFONT_M.render(humidity, True, (0, 0, 0))
        gu_wind_velocity_txt = NANUMFONT_M.render(wind_velocity, True, (0, 0, 0))
        gu_ultrafine_dust_txt = NANUMFONT_M.render(ultrafine_dust, True, (0, 0, 0))
        gu_fine_dust_txt = NANUMFONT_M.render(fine_dust, True, (0, 0, 0))
        gu_uv_rays_txt = NANUMFONT_M.render(uv_rays, True, (0, 0, 0))
        gu_sunset_time_txt = NANUMFONT_M.render(sunset_time, True, (0, 0, 0))
        
        SCREEN.blit(gu_name_txt, (25, 78))
        
        pg.draw.rect(SCREEN, (0, 0, 0), (160, 80, 130, 36), 2)
        SCREEN.blit(gu_reselect_txt, (175, 78))
        
        list_txt = [gu_temp_txt, gu_weather_txt, gu_sensory_temp_txt, gu_humidity_txt,
                    gu_wind_velocity_txt, gu_ultrafine_dust_txt, gu_fine_dust_txt, gu_uv_rays_txt,
                    gu_sunset_time_txt]
        
        for i, txt in enumerate(list_txt):
            SCREEN.blit(txt, (140, 140 + i * 50))

# 현재 시간 그리기
def draw_time():
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second = now.strftime('%S')

    time_now = NANUMFONT_M.render(f"{year}년 {month}월 {day}일 {hour}시 {minute}분 {second}초", True, (0, 0, 0))
    SCREEN.blit(time_now, (10, 10))

# 현재 뉴스 헤드라인 가져오기 & 현재 뉴스 헤드라인 그리기
def draw_headline():
    global count, headline
    # 현재 뉴스 헤드라인 가져오기
    if count == 100:
        NEWS_URL = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
        response_news = requests.get(NEWS_URL, headers={'User-Agent':'Mozilla/5.0'})
        if response_news.status_code == 200:
            html_news = response_news.content
            soup = BeautifulSoup(html_news, 'html.parser')

            headline = soup.find(class_='cluster_group _cluster_content').find(class_='cluster_text_headline').text
        else:
            print("Error")
        count = 0
    
    # 현재 뉴스 헤드라인 그리기
    news_headline = NANUMFONT_S.render(headline, True, (0, 0, 0))
    SCREEN.blit(news_headline, (10, 600))

WIDTH = 850
HEIGHT = 650
TABLE_X_START = 75
TABLE_Y_START = 180
TABLE_CELL_X_SIZE = 140
TABLE_CELL_Y_SIZE = 70
MAIN_SCREEN = True
GU_TABLE = True
GU_SELECTED = ''

count = 100

pg.init()
pg.display.set_caption("Current weather by gu")
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

# 폰트
NANUMFONT_GU_NAME = pg.font.Font("nanum-gothic/NanumGothic.ttf", 20)
NANUMFONT_S = pg.font.Font("nanum-gothic/NanumGothic.ttf", 24)
NANUMFONT_M = pg.font.Font("nanum-gothic/NanumGothic.ttf", 32)
NANUMFONT_L = pg.font.Font("nanum-gothic/NanumGothic.ttf", 64)

# 프로그램 메인 루프
PROGRAM_RUNNING = True
while PROGRAM_RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            PROGRAM_RUNNING = False
        # 구가 선택되지 않은 경우(구 선택 표 O)
        elif GU_TABLE == True and GU_SELECTED == '':
            x_count = 0
            y_count = 0
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pg.mouse.get_pos()
                    for gu in gu_list:
                        x_standard = TABLE_X_START + TABLE_CELL_X_SIZE * x_count
                        y_standard = TABLE_Y_START + TABLE_CELL_Y_SIZE * y_count
                        if x_standard < pos[0] < x_standard + TABLE_CELL_X_SIZE and y_standard < pos[1] < y_standard + TABLE_CELL_Y_SIZE:
                            GU_SELECTED = gu
                            GU_TABLE = False
                        else:
                            pass

                        x_count += 1
                        if x_count == 5:
                            x_count = 0
                            y_count += 1
                        else:
                            pass
        
        # 구가 선택된 경우(구 선택 표 X)
        elif GU_TABLE == False and GU_SELECTED != '':
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pg.mouse.get_pos()
                    if  160 < pos[0] < 290 and 80 < pos[1] < 116:
                        MAIN_SCREEN = True
                        GU_TABLE = True
                        GU_SELECTED = ''
    
    # 배경 그리기
    SCREEN.fill((127, 127, 255))

    # 오브젝트 계산 및 그리기
    draw_headline()
    draw_time()
    draw_gu_table()
    draw_current_weather_info(GU_SELECTED)

    count += 1

    # 화면 업데이트 및 업데이트 간격 설정
    pg.display.update()
    time.sleep(0.03)
pg.quit()