from inspect import getfile
import os
import re
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import json

overlap = []
url_list = "https://seoulboard.seoul.go.kr/front/bbs.json?bbsNo=163&schTy=&schData=&curPage="
url_page = "https://seoulboard.seoul.go.kr/humanframe/Json/view/163_"
# https://seoulboard.seoul.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=378438&fileTy=ATTACH&fileNo=1&bbsNo=163

def get_download(url, fname, directory):
    if not os.path.isdir(directory): #폴더가 존재하지 않는다면 폴더 생성
        os.mkdir(directory)

    try:
        request.urlretrieve(url, directory+ fname)
        print(fname+' successfully downloaded\n')
    except HTTPError as e:
        print('Error')
        return

def main():
    pageoffset = 1
    num = 500
    while num>0 :
        r = requests.get(url_list+str(pageoffset))
        rj = json.loads(r.text)

        for item in rj['listVO']['listObject']:
            # print(item['nttNo'])
            r2 = requests.get(url_page+str(item['nttNo'])+".json")
            # print(r2.text)
            if r2.ok:
                r2j = json.loads(r2.text)
                for index, fileitem in enumerate(r2j['bbsTypeVO']['bbsFileList']):
                    if fileitem['orginlFileNm'][-4:]==".hwp":
                        url2 = "https://seoulboard.seoul.go.kr/comm/getFile?srvcId=BBSTY1&fileTy=ATTACH&bbsNo=163&fileNo="+str(index+1)+"&upperNo="+str(item['nttNo'])
                        print(url2)
                        get_download(url2, fileitem['orginlFileNm'], "./download/")
            
        pageoffset += 1
        num -= 10

main()