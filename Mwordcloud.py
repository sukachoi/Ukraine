from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import os

class Mwc():
    def __init__(self):
        print("Mwc init call")
        pass
        

    def execute(self):
        self.path_dir = "C:/Users/USER/Desktop/workspace/Ukraine/data"
        self.file_list = os.listdir(self.path_dir)
        self.full_text = ""

        for i in self.file_list:
            f = open(self.path_dir+"/"+i, 'r') #C:/Users/USER/Desktop/workspace/Ukraine/data    0.txt
            text = f.read()
            #print(text)
            self.full_text=self.full_text+text+"\n"
            f.close()
        self.okt = Okt()
        nouns = self.okt.nouns(self.full_text) # 명사만 추출
        print(nouns)

        words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외
        c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
        #print(c)

        wc = WordCloud(font_path='C:/Windows/Fonts/H2HDRM.TTF', width=400, height=400, scale=2.0, max_font_size=250)
        gen = wc.generate_from_frequencies(c)
        plt.figure()
        plt.imshow(gen)
        wc.to_file('word_cloud.png')