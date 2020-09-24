from django.shortcuts import render
import shutil
import os
import sqlite3
import pandas as pd

# Create your views here.
def download(request):
    context = {}

    # History 경로 생성
    homepath = os.path.expanduser("~")
    abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
    # History 파일 복사
    shutil.copyfile(abs_chrome_path, abs_chrome_path+"_sample")
    # 복사본 데이터 추출
    con = sqlite3.connect(abs_chrome_path+"_sample")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM downloads LEFT JOIN downloads_url_chains on downloads.id = downloads_url_chains.id")
    download_data = cursor.fetchall()
    download_db = pd.DataFrame(download_data, columns=list(map(lambda x:x[0], cursor.description)))
    
    # 파일명, 확장자 추출
    download_db['filename'] = download_db['target_path'].str.split('\\').str[-1]
    download_db['extension'] = download_db['filename'].str.split('.').str[-1].str.lower()

    # 확장자 가장 많은 순위
    extension_dict = {}
    for extension in download_db['extension']:
        extension_dict[extension] = extension_dict.get(extension, 0)+1
    
    extension_rank = sorted(extension_dict.items(), key=lambda x : x[1], reverse=True)
    
    extension_top = []
    for rank in range(10):
        extension_top.append(extension_rank[rank][0])
    
    context['extension_top'] = extension_top

    if request.method == "POST":
        # 선택한 확장자
        
        extension_selected = request.POST.getlist('extension')
        keyword = request.POST.get('keyword')

        dataset_selected_list = []
        for extension in extension_selected:
            dataset_selected_dict = {}
            data_selected_list = []

            for data in download_db.loc[(download_db['extension'] == extension) & (download_db['filename'].str.contains(keyword)), ['filename','referrer','url', 'danger_type']].values:
                data_selected_dict = {}
                data_selected_dict['filename'] = data[0]
                data_selected_dict['referrer'] = data[1]
                data_selected_dict['url'] = data[2]
                data_selected_dict['danger_type'] = data[3]
                data_selected_list.append(data_selected_dict)

            dataset_selected_dict['extension'] = extension
            dataset_selected_dict['dataset'] = data_selected_list

            dataset_selected_list.append(dataset_selected_dict)

        context['dataset_selected'] = dataset_selected_list

    return render(request, 'downloadapp/download.html', context)