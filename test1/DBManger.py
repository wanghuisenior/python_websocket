#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: DBManger.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/17 17:31
 @Description:
"""
import sqlite3


class DBTool(object):
	def __init__(self):
		"""
		初始化函数，创建数据库连接
		"""
		self.conn = sqlite3.connect('order.db')
		self.c = self.conn.cursor()

	def executeUpdate(self, sql, ob):
		"""
		数据库的插入、修改函数
		:param sql: 传入的SQL语句
		:param ob: 传入数据
		:return: 返回操作数据库状态
		"""
		try:
			self.c.executemany(sql, ob)
			i = self.conn.total_changes
		except Exception as e:
			print('错误类型： ', e)
			return False
		finally:
			self.conn.commit()
		if i > 0:
			return True
		else:
			return False

	def executeDelete(self, sql, ob):
		"""
		操作数据库数据删除的函数
		:param sql: 传入的SQL语句
		:param ob: 传入数据
		:return: 返回操作数据库状态
		"""
		try:
			self.c.execute(sql, ob)
			i = self.conn.total_changes
		except Exception as e:
			return False
		finally:
			self.conn.commit()
		if i > 0:
			return True
		else:
			return False

	def executeQuery(self, sql, ob):
		"""
		数据库数据查询
		:param sql: 传入的SQL语句
		:param ob: 传入数据
		:return: 返回操作数据库状态
		"""
		test = self.c.execute(sql, ob)
		return test

	def close(self):
		"""
		关闭数据库相关连接的函数
		:return:
		"""
		self.c.close()
		self.conn.close()


if __name__ == '__main__':
	db = DBTool()
	ob = [('张三', '我的名字叫张三'), ('张三1', '我的名字叫张三1'), ('张三2', '我的名字叫张三2')]
	sql1 = 'insert into test (name, remark) values (?,?)'
	T = db.executeUpdate(sql1, ob)
	if T:
		print('插入成功！')
	else:
		print('插入失败！')

	print("通ID修改Student姓名信息")
	sql2 = 'UPDATE test set name = ? where ID=?'
	ob = [('张三', '6')]
	T = db.executeUpdate(sql2, ob)
	if T:
		print('修改成功！')
	else:
		print('修改失败！')

	print("通ID删除Student信息")
	sql3 = "DELETE from test where ID=?"
	ob = [(22)]
	T = db.executeDelete(sql3, ob)
	if T:
		print('删除成功！')
	else:
		print('删除失败！')

	print("通姓名查询Student信息")
	sq4 = 'select * from test where name=?'
	ob = ['张三']
	s = db.executeQuery(sq4, ob)
	st = []
	for st in s:
		print('ID:', st[0], '  Name:', st[1], '  Remark:', st[2])
	if any(st):
		pass
	else:
		print("输入有误，该学员不存在")

	# 关闭数据库连接
	db.close()
