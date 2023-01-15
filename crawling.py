import os
from urllib import request
from urllib.error import HTTPError
import requests
import json



def url_list(bbsNo, curPage): return "https://seoulboard.seoul.go.kr/front/bbs.json?bbsNo="+str(bbsNo)+"&schTy=&schData=&curPage="+str(curPage)
def url_page(bbsNo, nttNo) : return "https://seoulboard.seoul.go.kr/humanframe/Json/view/"+str(bbsNo)+"_"+str(nttNo)+".json"
def url_file(bbsNo, upperNo, fileNo): return "https://seoulboard.seoul.go.kr/comm/getFile?srvcId=BBSTY1&upperNo="+str(upperNo)+"&fileTy=ATTACH&fileNo="+str(fileNo)+"&bbsNo="+str(bbsNo)

def get_download(url, fname, directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

    print(url)
    try:
        request.urlretrieve(url, directory+ fname)
        print(fname+' successfully downloaded')
    except HTTPError as e:
        print('Error')
        return False
    return True

def main():
    pageoffset = 1
    num = 500

    bbsNo = 163
    fileTotalSize = 0
    while fileTotalSize < 4 * 1024**12 :
        r = requests.get(url_list(bbsNo,pageoffset))
        rj = json.loads(r.text)

        for item in rj['listVO']['listObject']:
            # print(item['nttNo'])
            r2 = requests.get(url_page(bbsNo, item['nttNo']))
            # print(r2.text)
            if r2.ok:
                r2j = json.loads(r2.text)
                for index, fileItem in enumerate(r2j['bbsTypeVO']['bbsFileList']):
                    if fileItem['orginlFileNm'][-4:]==".hwp":
                        fileURL=url_file(bbsNo, fileItem['upperNo'], index+1)
                        if(get_download(fileURL, fileItem['orginlFileNm'], "./download/")):
                            fileTotalSize += fileItem['fileSize']
                            print(fileItem['fileSize'],"Byte\nTotal:",fileTotalSize,"Byte\n")
            
        pageoffset += 1
        num -= 10

main() 