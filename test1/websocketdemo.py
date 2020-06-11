#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: websocketdemo.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/10 13:57
 @Description:
"""
# websocketdemo.py
# pip install bottle-websocket
import os
import socket

import bottle

try:
	from bottle import route, run, static_file, request
	from bottle.ext.websocket import GeventWebSocketServer
	from bottle.ext.websocket import websocket
except ModuleNotFoundError:
	os.system('pip install bottle-websocket')


def get_host_ip():
	"""
	获取本地IP地址
	:return:
	"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip


bottle.TEMPLATE_PATH.append("/")  # 指定模板目录


@route("/")
def callback():
	# return static_file("demo.html", root=".")
	return static_file("simple.html", root=".")


@route("/assets/<path:path>")
def callback(path):
	return static_file(path, "assets")  # 指定静态文件目录assets


users = set()  # 连接进来的websocket客户端集合


@route("/websocket", apply=[websocket])
def callback(ws):
	users.add(ws)
	while True:  # 持续进行连接
		rec = ws.receive()
		if rec:
			print('rec:', rec)
			for u in users:
				u.send('服务端接收到了：' + rec)  # 发送信息给所有的客户端
		else:
			break  # 如果有客户端断开连接，则踢出users集合


@route("/index", method=["GET", "POST"])  # method 默认GET,可以指定其他请求或者请求方式列表
def index():
	print('index', request.GET)


if __name__ == '__main__':
	host = '0.0.0.0' if get_host_ip() == '10.10.9.79' else 'localhost'
	print(host)
	run(host=host, port=10000, server=GeventWebSocketServer)
