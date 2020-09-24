from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

data_list = []

def make_wordcloud(word_count):
    twitter = Twitter()
 
    sentences_tag = []
    #형태소 분석하여 리스트에 넣기
    for sentence in data_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)
 
    print(sentences_tag)
    print('\n' * 3)
 
    noun_adj_list = []
    #명사와 형용사만 구분하여 이스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)
 
    #형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print(tags)
 
    #wordCloud생성
    #한글이 깨지는 문제 해결하기 위해 font_path 지정
    wc = WordCloud(font_path='/Library/Fonts/NanumSquareLight.ttf', background_color='white', width=800, height=600)
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

import shutil
import os
import sqlite3
 
if __name__ == '__main__':
    # 경로
    homepath = os.path.expanduser("~")
    abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
    # 파일복사
    shutil.copyfile(abs_chrome_path, abs_chrome_path+"123")

    # SQL
    con = sqlite3.connect(abs_chrome_path+"123")
    cursor = con.cursor()
    cursor.execute("SELECT term FROM keyword_search_terms")

    for i in range(30):
        data = cursor.fetchone()
        data_list.append(data[0])
 
    #단어 30개까지 wordcloud로 출력
    make_wordcloud(30)


