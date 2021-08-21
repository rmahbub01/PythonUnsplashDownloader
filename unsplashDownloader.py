import asyncio
import os
import time

import aiofiles
import requests


class Unsplash:

    def __init__(self, search_query, perpage, quality='raw', pages=0):

        self.search_query = search_query
        self.perpage = perpage
        self.quality = quality
        self.pages = pages
        self.headers = {
            'authority': 'unsplash.com',
            'method': 'GET',
            'path': '/napi/search?query=cat&per_page=20&xp=',
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'ugid=3388302dd15d6190842ea9c55f6c96cd5430602; uuid=47f806a0-ff22-11eb-8058-3590e11a7640; xpos=%7B%22greater-uploader-limit%22%3A%7B%22id%22%3A%22greater-uploader-limit%22%2C%22variant%22%3A%22enabled%22%7D%7D; azk=47f806a0-ff22-11eb-8058-3590e11a7640; azk-ss=true; _ga=GA1.2.1043791859.1629180829; lux_uid=162945388959200680; _sp_ses.0295=*; _gid=GA1.2.1300718912.1629453890; _gat=1; _sp_id.0295=583edf47-bce8-472b-8526-fe4922ceb2cb.1629180827.2.1629454584.1629184327.18df1ad3-f791-4383-a436-c7b1f9383558'
        }

    def setUrl(self):
        return f"https://unsplash.com/napi/search/photos?query={self.search_query}&per_page={self.perpage}&page={self.pages}"

    def getUrl(self):
        res = requests.request("GET", self.setUrl(), headers=self.headers)
        return res.json()

    def downloadPath(self, imgId):
        download_path = 'unsplash'
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        return f"{download_path}/{imgId}.jpeg"

    async def saveImg(self, imgUrl, path):
        print('waiting', path)
        async with aiofiles.open(path, mode='wb') as img:
            await img.write(requests.request('GET', imgUrl,
                                             headers=self.headers).content)
            await img.flush()
        print('done', path)

    def downloadImg(self):

        response = self.getUrl()
        imgDict = {}
        for data in response['results']:
            imgId = data['id']
            imgUrl = data['urls'][self.quality]
            imgName = self.downloadPath(imgId)
            imgDict.setdefault(imgName, imgUrl)
        return imgDict
