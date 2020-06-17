#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: PrinterManager.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/16 14:36
 @Description:
"""
import hashlib
import threading
import time
import requests


class Printer(object):
	_instance_lock = threading.Lock()

	def __init__(self):
		self.__user = '549558353@qq.com'
		self.__ukey = 'puqDRpM6YKem4gRC'
		self.__sn = '520508940'
		self.__stime = str(int(time.time()))
		self.__sig = hashlib.sha1((self.__user + self.__ukey + self.__stime).encode('utf-8')).hexdigest()
		self.__params = {'user': self.__user, 'stime': self.__stime, 'sig': self.__sig}

	@classmethod
	def instance(cls, *args, **kwargs):
		if not hasattr(Printer, "_instance"):
			with Printer._instance_lock:
				if not hasattr(Printer, "_instance"):
					Printer._instance = Printer(*args, **kwargs)
		return Printer._instance

	def printMsg(self, content):
		self.__params['apiname'] = 'Open_printMsg'
		self.__params['sn'] = '520508940'
		self.__params['content'] = content
		return requests.get('http://api.feieyun.cn/Api/Open/', params=self.__params)


if __name__ == '__main__':
	p = Printer.instance()

	# res = p.printMsg('test msg')
