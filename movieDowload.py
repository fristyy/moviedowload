#coding:utf-8
import re
import asyncio

import requests
import aiohttp


#毒液下载，同步版
m3u8url = 'https://doubanzyv3.tyswmp.com:888/2018/12/12/UEtWtHwTc0UniIDQ/playlist.m3u8'
def m3u8D(m3u8url):	
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		      'X-Requested-With': 'ShockwaveFlash/32.0.0.114'}
	
	m3u8resp = requests.get(m3u8url,headers=headers).text
	m3u8rawlist  = m3u8resp.split()
	
	tslist = ( ts for ts in m3u8rawlist if not ts.startswith('#'))
	#for i in tslist:
		#print(i)
		
	for ts in tslist:
		tsurl = m3u8url.rsplit('/',1)[0] + '/' + ts
		#tsresp = requests.get(tsurl,headers=headers,stream = True).raw.read()
		#with open (ts, 'wb') as fd:
			#fd.write(tsresp)	
		
    #推荐以下方法下载流文件
		#http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
		tsresp = requests.get(tsurl,headers=headers,stream = True)		
		with open (ts, 'wb') as fd:
			for chunk in tsresp.iter_content(chunk_size=1024):
				fd.write(chunk)	

#以下无限战争下载		
#newurl = 'http://data.vod.itc.cn/?new=/174/103/DzyQ7HSKS2OQEEP9KqSxiH.mp4&vid=4909516&plat=17&mkey=0Df_wsApYLSepsY22aMpB3Ycg0laIHcB&ch=tv&uid=398C15121BCDD2C9D8E1CF9C8435B1CC&pt=7&prod=app&pg=1'
apiurl = 'http://api.bbbbbb.me/yunjx/api.php?xml=http://m.tv.sohu.com/v4909514.shtml&md5=ab59ec3a7b8ab5d6c6a70dccad27loij&type=auto&hd=cq&wap=0&siteuser=&lg=&sohuuid=8A92F35F8A339557D1A2753180321D06'

#同步版
def QSP(url):
	headers = {'Referer': 'http://api.bbbbbb.me/yunjx/?url=http://m.tv.sohu.com/v4909514.shtml',
	           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	           'X-Requested-With': 'ShockwaveFlash/32.0.0.114'}
	
	resp = requests.get(url,headers=headers)
	partlist = re.findall('<file>.*?(http://.*?)]]', resp.text)
	print(partlist)
	part = 0
	for url in partlist:
		tsresp = requests.get(url,headers=headers,stream = True)
		with open (f'无限战争{part}.mp4', 'wb') as fd:
			for chunk in tsresp.iter_content(chunk_size=1024):
				fd.write(chunk)		
		part += 1

#异步版
async def asyDload(apiurl):
	headers = {'Referer': 'http://api.bbbbbb.me/yunjx/?url=http://m.tv.sohu.com/v4909514.shtml',
	           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	           'X-Requested-With': 'ShockwaveFlash/32.0.0.114'}	
	resp = requests.get(apiurl,headers=headers)
	partlist = re.findall('<file>.*?(http://.*?)]]', resp.text)
	partdict = {}
	for key in range(len(partlist)):
		partdict[partlist[key]]=key
	for i in partdict:
		print(i)
	if partlist:
		conn = aiohttp.TCPConnector(limit=5)
		async with aiohttp.ClientSession(connector=conn,headers=headers) as session:
			_movielisttask = [dowload(url,session,partdict,headers) for url in partdict]			
			movielist = await asyncio.gather(*_movielisttask)
		print(f'开始下载:{len(partlist)}个部分')
	return partlist
	
async def dowload(url,session,partdict,headers):
	async with session.get(url,headers=headers) as resp:  
		
		with open(f'E:/streamDload/无限战争/InfiityWar{partdict[url]}.mp4', 'wb') as fd:
			while True:
				chunk = await resp.content.read(2048)
				if not chunk:
					break
				fd.write(chunk)

if __name__ == '__main__':
	asyncio.run(asyDload(apiurl))
