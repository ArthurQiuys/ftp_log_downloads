#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2017/5/25


def read_doc(conf_file):
	"""
	:param conf_file: 传入文件
	:return: 结果
	"""
	try:
		with open(conf_file) as pf:
			for line in pf.readline():
				host = line.split(':')[0]
				# path = line.split(':')[1]
				print(host)
	except IOError as e:
		print("io error")


if __name__ == '__main__':
	pass
print('input')
read_doc('conf')
print('success')
