#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: Logger.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/15 16:56
 @Description: 记录敏感操作
 # from Logger import Logger
"""
import datetime
import sys


class Logger(object):
	def __init__(self):
		"""Do nothing, by default."""

	@staticmethod
	def log(msg):
		time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with open('log.txt', 'a+') as f:
			f.write(
				time + ' = ' + msg + '\n')


if __name__ == '__main__':
	Logger.log('test msg')
