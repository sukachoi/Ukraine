from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import time



from random import *


###############################################
###############  크롤링 부분   #################
###############################################

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#browser = webdriver.Chrome(options=options)
#여기의 options을 아래 driver만들때 넣어줌
driver = webdriver.Chrome('C:/Users/USER/Desktop/workspace/Ukraine/chromedriver',options=options)
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)
# 네이버 지식인 크롤링
# keyword에 크롤링하고 싶은 단어 선택. space 는 + 로 치환
def get_keyword(text):
    return text.replace(" ", "%20")

# 정렬 방식 선택
# 1: 추천순
# 2: 최신순
# 기타: 정확도 순
def sort_kind(index):
    # 추천
    if index == 1:
        return 'vcount'
    # 최신순
    elif index == 2:
        return 'date'
    # 정확도
    else:
        return 'none'


keyword = '서울대'
driver.get('https://kin.naver.com/search/list.nhn?query=' + get_keyword(keyword)) #함수 
time.sleep(uniform(0.1, 1.0))

page_index = 1
# 크롤링 시작 일자
f = '2022.07.01'
# 크롤링 종료 일자
t = '2022.07.03'
period_txt = "&period=" + f + ".%7C" + t + "."

_sort_kind = sort_kind(2) # 함수 날짜 return
date = str(datetime.now()).replace('.', '_')
date = date.replace(' ', '_')

# URL 저장
f = open("url_list.txt", 'w')
page_url = []
while True:
    time.sleep(uniform(0.01, 1.0))
    driver.get('https://kin.naver.com/search/list.nhn?' + "&sort=" + _sort_kind + '&query=' + get_keyword(keyword) + period_txt + "&section=kin" + "&page=" + str(page_index))
    html = driver.page_source
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    tags = soup.find_all('a', class_="_nclicks:kin.txt _searchListTitleAnchor")
    for tag in tags:
        url = str(tag).split(' ')[3]
        url = url.replace('href=', "")
        url = url.replace('"', "")
        url = url.replace('amp;', '')
        page_url.append(url)
        f.write(url + "\n")
    print("파인드엘리먼트바이클래스네임전")
    post_number = driver.find_element(By.CLASS_NAME,'number').text
    print("파인드엘리먼트바이클래스네임후")
    post_number = str(post_number).replace("(", "")
    post_number = str(post_number).replace(")", "")
    #(101-110/136)
    current_number = post_number.split('/')[0].split('-')[1]
    current_number = current_number.replace(',', '')
    total_number = post_number.split('/')[1]
    total_number = total_number.replace(',', '')

    if int(current_number) == int(total_number):
        break
    else:
        page_index += 1
print("여기까지는 성공,.......")


f.close()


count =0
for i in page_url:
    file_name="C:/Users/USER/Desktop/workspace/Ukraine/data/"+str(count)+".txt"
    f = open(file_name, 'w')
    driver.get(i)
    title = driver.find_element(By.CLASS_NAME,'title').text
    print("=========질문======")
    print(title)
    try:
        question_txt = driver.find_element(By.CLASS_NAME,'c-heading__content').text
        
    except:
        question_txt = ""

    # 답변 리스트
    answer_list = driver.find_elements(By.CLASS_NAME,"se-main-container")
    
    for n, answer in enumerate(answer_list):
        texts = answer.find_elements(By.TAG_NAME,'span')
        
        t = ""
        for i in texts:
            t += i.text
        print(t)

        if n == 0:
            pass
            #sheet.append([title, question_txt, t])
        else:
            pass
            #sheet.append(["", "", t])
        f.write(str(t) + "\n")
    f.close()
    count += 1
    if count >= 20:
        break
    print(count)


###############################################
###############  word cloud 구현  #############
###############################################
"""
1. 읽어야할 파일 목록을 구한다
2. 파일을 읽는다
3. 워드 클라우드 마음데로 그려보거나 블로그 하나 아무거나 읽기
4. word count 기반
"""
import os
 
path_dir = "C:/Users/USER/Desktop/workspace/Ukraine/data"
 
file_list = os.listdir(path_dir)

full_text = ""

for i in file_list:
    f = open(path_dir+"/"+i, 'r') #C:/Users/USER/Desktop/workspace/Ukraine/data    0.txt
    text = f.read()
    #print(text)
    full_text=full_text+text+"\n"
    f.close()

#print(full_text)


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np


okt = Okt()
nouns = okt.nouns(full_text) # 명사만 추출
#print(nouns)

words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외
c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
#print(c)

wc = WordCloud(font_path='C:/Windows/Fonts/H2HDRM.TTF', width=400, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure()
plt.imshow(gen)
wc.to_file('word_cloud.png')


#################################
# 1. 복습
# 2. 이쁘게 리팩토링
# 3. 깃 업로드
#################################