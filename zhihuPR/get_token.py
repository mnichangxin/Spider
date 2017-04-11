# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 17:04:59 2017

@author: mnichangxin
"""

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient, SearchType
from multiprocessing import Pool
import os, sys, codecs

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8') 

# 登录
TOKEN_FILE = 'token.pkl'

client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
	client.load_token(TOKEN_FILE)
else:
	client.login_in_terminal()
	client.save_token(TOKEN_FILE)

followers = client.topic(19564812).followers

people = client.search('章佳杰', SearchType.PEOPLE)

for i in people:
	# print(dir(i.obj))
	print(i.obj._id)

# # 进程调用函数
# def Process(i):	
# 	f = open('followers.csv', 'a')

# 	try: 
# 		if followers[i].follower_count >= 5000:
# 			f.write(','.join((followers[i].id,)) + '\n')
# 	except:
# 		pass
	
# 	f.close()

# # 进程创建函数
# def main():
# 	pool = Pool(10) # 创建进程池

# 	print(u'正在爬取......')

# 	# 写入文件
# 	f = open('followers.csv', 'a')    
# 	f.write(codecs.BOM_UTF8) # 防止csv文件乱码
# 	f.write(','.join(('UserId',)) + '\n')
# 	f.close()

# 	# 创建多进程
# 	for i in range(10000):
# 		pool.apply_async(Process, (i, ))

# 	pool.close()
# 	pool.join() 

# 	print(u'爬取完毕！')

# if __name__ == '__main__':
# 	main()

