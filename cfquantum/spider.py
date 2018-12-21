# !/usr/bin/python
# -*-coding: utf-8-*-

import re, sys, time
import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 登录模块
class Spider:
	def __init__(self): 
		self.login_url = 'https://www.cfquantum.org/api/user/login'
		self.page_url = 'https://www.cfquantum.org/api/simulator/info'
		self.value_url = 'https://www.cfquantum.org/api/simulator/latest/'
		self.create_url = 'https://www.cfquantum.org/api/simulator/create'
		self.time_url = 'https://www.cfquantum.org/api/simulator/list?type=0&page=1&pagesize=10'
	
	# 登录
	def login(self):
		# POST参数
		post_data = {
			'json': '{"username":"' + self.getConf()[0] + '","password":"' + self.getConf()[1] + '"}',
			'lan': 'en_US',
			'withCredentials': 'true'
		} 

		req.post(self.login_url, data = post_data)

	# 抓取页面
	def getPage(self):
		res = req.get(self.page_url).content

		holds = re.findall('"holds":(.*?),"rank"', res)[0]
		score = re.findall('"score":(.*?),"createdAt"', res)[0]

		return (holds, score)

	# Call或Put操作
	def create(self, type, amount, target_type):
		# POST参数
		post_data = {
			'type': 0,
			'amount': amount,
			'duration_type': 0,
			'target_type': target_type,
			'target_value': self.getValue(target_type)
		}

		if type == 'put':
			post_data['type'] = 1

		req.post(self.create_url, data = post_data).content

	# 获取target_value
	def getValue(self, target_type):
		if target_type == 0:
			self.value_url += str(0)
		else:
			self.value_url += str(1)

		res = req.get(self.value_url).content

		value = re.findall('"last":(.*?),"put"', res)[0]

		return value
	
	# 获取等待时间
	def getTime(self):
		res = req.get(self.time_url).content

		try: 
			expire_time = re.findall('"expireTime":(.*?),"createdAt"', res)[0]
		except:
			return False
		
		expire_time_hour = int(time.strftime('%H', time.localtime(int(expire_time[0:10]))))
		expire_time_min = int(time.strftime('%M', time.localtime(int(expire_time[0:10]))))

		now_time_hour = int(time.strftime('%H', time.localtime(time.time())))
		now_time_min = int(time.strftime('%M', time.localtime(time.time())))
		
		if expire_time_hour == now_time_hour:
			dur_time = expire_time_min - now_time_min
		else:
			dur_time = 60 - now_time_min + expire_time_min
		
		return dur_time

	# 读取配置文件
	def getConf(self):
		f = open('./config/conf.json')

		conf = f.read()
	
		account = re.findall(r'"account": "(.*?)"', conf)[0]
		password = re.findall(r'"password": "(.*?)"', conf)[0]

		f.close()

		return (account, password)