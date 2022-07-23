from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from random import *


###############################################
###############  크롤링 부분   #################
###############################################

class Mcrawl():

    def __init__(self):
        #div가 1이면 네이버지식인 크롤링, 2이면 네이버 블로그 ...
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        #browser = webdriver.Chrome(options=options)
        #여기의 options을 아래 driver만들때 넣어줌
        self.driver = webdriver.Chrome('C:/Users/USER/Desktop/workspace/Ukraine/chromedriver',options=self.options)
        # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
        self.driver.implicitly_wait(3)


    # 네이버 지식인 크롤링
    # keyword에 크롤링하고 싶은 단어 선택. space 는 + 로 치환
    def get_keyword(self,text):
        return text.replace(" ", "%20")

    # 정렬 방식 선택
    # 1: 추천순
    # 2: 최신순
    # 기타: 정확도 순
    def sort_kind(self,index):
        # 추천
        if index == 1:
            return 'vcount'
        # 최신순
        elif index == 2:
            return 'date'
        # 정확도
        else:
            return 'none'

    def excute(self,keyword="연세대",start_dt='2022.07.15',from_dt='2022.07.17',limit=20):
        self.keyword = keyword#'서울대'
        self.driver.get('https://kin.naver.com/search/list.nhn?query=' + self.get_keyword(keyword)) #함수 
        time.sleep(uniform(0.1, 1.0))

        page_index = 1
        # 크롤링 시작 일자
        f = start_dt#'2022.07.01'
        # 크롤링 종료 일자
        t = from_dt#'2022.07.03'
        period_txt = "&period=" + f + ".%7C" + t + "."

        _sort_kind = self.sort_kind(2) # 함수 날짜 return
        date = str(datetime.now()).replace('.', '_')
        date = date.replace(' ', '_')

        # URL 저장
        f = open("url_list.txt", 'w')
        page_url = []
        while True:
            time.sleep(uniform(0.01, 1.0))
            self.driver.get('https://kin.naver.com/search/list.nhn?' + "&sort=" + _sort_kind + '&query=' + self.get_keyword(keyword) + period_txt + "&section=kin" + "&page=" + str(page_index))
            html = self.driver.page_source
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
            #print("파인드엘리먼트바이클래스네임전")
            post_number = self.driver.find_element(By.CLASS_NAME,'number').text
            #print("파인드엘리먼트바이클래스네임후")
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
            self.driver.get(i)
            title = self.driver.find_element(By.CLASS_NAME,'title').text
            print("=========질문======")
            print(title)
            try:
                question_txt = self.driver.find_element(By.CLASS_NAME,'c-heading__content').text
                
            except:
                question_txt = ""

            # 답변 리스트
            answer_list = self.driver.find_elements(By.CLASS_NAME,"se-main-container")
            
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
            if count >= limit:
                break
            print(count)


        