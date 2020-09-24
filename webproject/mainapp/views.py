from django.shortcuts import render
import shutil
import os
import sqlite3
from collections import Counter
from kiwipiepy import Kiwi
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    context = {}

    # History 경로 생성
    homepath = os.path.expanduser("~")
    abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
    # History 파일 복사
    shutil.copyfile(abs_chrome_path, abs_chrome_path+"_sample")
    # 복사본 데이터 추출
    con = sqlite3.connect(abs_chrome_path+"_sample")
    cursor = con.cursor()
    cursor.execute("SELECT term FROM keyword_search_terms")
    term_data = cursor.fetchall()

    # 형태소 분석
    kiwi = Kiwi()
    kiwi.prepare()
    word_list = []
    for term in term_data:
        for word, tag, _, _ in kiwi.analyze(term[0], top_n=1)[0][0]:
            if tag in ['NNG','NNP','NNB','SL']:
                word_list.append(word)
    
    # count
    counts = Counter(word_list)
    tags = counts.most_common()

    # wordcloud
    mask = plt.imread("./static/images/mask.jpg")
    wc = WordCloud(font_path='./static/webfonts/NanumBarunGothicBold.ttf',
                    background_color='white', 
                    width=800, 
                    height=800,
                    mask=mask)

    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud,  interpolation="bilinear")
    plt.savefig("./static/images/wordcloud_keyword.png", dpi=300, bbox_inches='tight')

    # 상위 9개 단어
    
    top9_list = []
    for rank in range(9):
        top9 = {}
        top9['rank'] = rank+1
        top9['word'] = tags[rank][0]
        top9['count'] = tags[rank][1]
        top9_list.append(top9)

    context['top9'] = top9_list

    return render(request, 'mainapp/index.html', context)

def generic(request):
    return render(request, 'mainapp/generic.html')

def elements(request):
    return render(request, 'mainapp/elements.html')