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
import json
import os
import re
import socket
from Logger import Logger

try:
	import requests
	import bottle
	import geventwebsocket
	from bottle import route, run, static_file, request, response, redirect, template, error
	from bottle.ext.websocket import GeventWebSocketServer
	from bottle.ext.websocket import websocket
except ModuleNotFoundError:
	os.system('pip install requests')
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
	return static_file("login.html", root=".")


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
				try:
					u.send('服务端接收到了：' + rec)  # 发送信息给所有的客户端
				except geventwebsocket.exceptions.WebSocketError as e:
					print('发送消息时，之前建立的链接异常断掉了')
		else:
			break  # 如果有客户端断开连接，则踢出users集合


@route("/index", method=["GET", "POST"])  # method 默认GET,可以指定其他请求或者请求方式列表
def index():
	# print(request.method)  # POST
	# print(request.forms)  # post请求信息
	# print(request.query)  # get 请求数据
	# print(request.body)  # POST 请求数据
	# print(request.files)  # 上传的文件信息
	# print(request.cookies)  # cookie信息
	# print(request.environ)  # 环境信息
	# print(request.json)  #
	# print(request.params)  #
	q = {}
	for k in request.query:
		if k == 'page':
			q[k] = int(request.query[k]) - 1
		elif k == 'limit':
			q['page_size'] = int(request.query[k])
		else:
			q[k] = int(request.query[k])

	if q:  # 请求带参数，返回json
		# 获取所有订单信息
		q['type'] = 8
		print(q)
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
		}
		try:
			res = session.get(
				url='http://xcx.zitcloud.cn/api/restaurant/order/orderList', headers=headers, params=q)
			order_list = res.json()['orderVoList']
			order_size = res.json()['allOrder']
		except:
			# 登录失效了
			return json.dumps({'code': 400, 'msg': '请求失败，请重新登录'})
		d = []
		for data in order_list:
			for item in data['orderItem']:
				d.append({
					'orderId': data['orderId'],
					'code': data['orderNumber'][-4:],
					'dish_name': item['itemName'],
					'number': item['number'],
					'remark': data['remark'],
					'time': data['endTime'],
					'orderStatus': data['orderStatus'],
				})
		res = json.dumps({'code': 0, 'msg': '查询成功', 'count': order_size, 'data': d})
		return res
	else:  # 请求不带参数，返回页面
		return template("index.html")


@route("/login", method=["GET", "POST"])  # method 默认GET,可以指定其他请求或者请求方式列表
def login():
	if request.method == 'GET':
		return template("login.html")
	else:
		params = {}
		for item in request.params:
			params[item] = request.params[item]
		print(params)
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
		}
		session.post(url="http://www.zitcloud.cn/login", data=params, headers=headers)
		r1 = session.get(url="http://www.zitcloud.cn/user/profile/", headers=headers)
		resp = {}
		if '请先登录' in r1.text:
			print('登录失败')
			resp['result'] = False
			resp['text'] = '登录失败'
		else:
			print('登录成功')
			# 获取该账号下的小程序id
			xcx_list = session.get(url='http://www.zitcloud.cn/user/MiniProgram/index', headers=headers)
			pattern = re.compile(r'"miniPrograms":.*]')
			s = '{' + re.search(pattern, xcx_list.text).group() + '}'
			miniprograms = json.loads(s)['miniPrograms']
			xcx_id = miniprograms[0]['id']

			# 根据获取到的小程序id请求 小程序管理页面
			xcx_manage = session.get(url='http://www.zitcloud.cn/user/xcx/manage/' + xcx_id, headers=headers)
			restaurants_list = session.get(url='http://xcx.zitcloud.cn/api/restaurant/tables?length=10&start=0',
										   headers=headers)
			restaurants = []
			for r in restaurants_list.json()['aaData']:
				restaurants.append({'rid': r['id'], 'rname': r['name']})
			print('restaurants', restaurants)
			response.set_cookie('restaurants', str(restaurants))
			resp['result'] = True
			resp['text'] = '登录成功'
		print('resp', resp)
		return json.dumps(resp)


@route("/consumeOrderById", method=["GET"])
def consumeOrderById():
	orderId = request.query.get('orderId')
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	}
	r1 = session.get(url="http://xcx.zitcloud.cn/api/order/consumeCustomer/" + orderId,
					 headers=headers)
	if not r1.json():
		Logger.log('consumeOrderById:' + orderId)
		return json.dumps(200)
	else:
		print('出错了')


@route("/closeOrderById", method=["GET"])
def closeOrderById():
	orderId = request.query.get('orderId')
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	}
	print(request.query.get('orderId'))
	r1 = session.get(url="http://xcx.zitcloud.cn/api/order/closeOrder/" + request.query.get('orderId'),
					 headers=headers)
	if not r1.json():
		Logger.log('closeOrder:' + orderId)
		return json.dumps(200)
	else:
		print('出错了')


@route("/requestWxData", method=["GET", "POST"])  # method 默认GET,可以指定其他请求或者请求方式列表
def requestWxData():  # 接收微信小程序发来的订单
	datas = []
	for order in request.json:
		for detail in order['orderDetails']:
			print(order['id'], order['createDate'], order['number'], order['remark'], detail['number'],
				  json.loads(detail['itemInfo'])['name'])


@error(500)
def error500(code):
	return template('error.html')


if __name__ == '__main__':
	session = requests.Session()
	host = '0.0.0.0' if get_host_ip() == '10.10.9.79' else 'localhost'
	# print(host)
	run(host=host, port=10000, server=GeventWebSocketServer, debug=True, reloader=True)
