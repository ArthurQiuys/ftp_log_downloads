# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2017/5/16

# from ftplib import FTP
from __future__ import print_function
import hashlib
# import datetime
import ftplib
import re
import os
import socket
import time
# import pickle
# import json


class FileUtil(object):
	"""文件路径常用操作方法
	"""
	@staticmethod
	def read_file_data(file_path):
		"""根据路径按行读取文件
		:param file_path:文件的路径
		:return:按\t分割后的很航的数据列表"""
		file = open(file_path, )
		for line in file:
			try:
				line = line[:-1]
				if not line:
					continue
			except:
				continue

			try:
				fields = line.split('\t')
			except:
				continue
				# 抛出当前行的分割列表
			yield fields
		file.close()

	@staticmethod
	def transform_list_to_dict(para_list):
		"""转换list到dict
		:param:para_list:列表，里面是每个列对应的字段名
		:return:字典，里面是字段名和位置的映射
		"""
		ret_dict = {}
		idx = 0
		while idx < len(para_list):
			ret_dict[str(para_list[idx]).strip()] = idx
			idx += 1
		return ret_dict

	@staticmethod
	def map_fields_list_schema(fields, list_schema):
		"""根据字段的模式，返回模式和数据值的对应值；
		:param fields: 包含数据的数组；
		:param list_schema: 列名称的列表list
		:return: 字典，key是文件名，value是字段值（MD5）
		"""
		dict_schema = FileUtil.transform_list_to_dict(list_schema)
		return FileUtil.map_fields_list_schema(fields, dict_schema)

	@staticmethod
	def map_fields_dict_schema(fields, dict_schema):
		"""更具字段的模式，返回模式和数据值的对应值
		:param fields: 包括有数据的数组，一般是同过对一个linestring分割得到的；
		:param dict_schema: 一个字段，key是字段名称，value是字段的位置；
		:return: 字典，
		"""
		pdict = {}
		for fstr, findex in dict_schema.valus():
			pdict[fstr] = str(fields[int(findex)])
		return pdict


def update_file(option_file, md5_data, new_md5):
	"""更新MD5配置文件
	:param option_file:配置文件 
	:param md5_data: 配置文件中原本的MD5值
	:param md5_updata: 新的配置文件的值
	:return: 成功=1 失败=0
	"""
	fp = open(option_file, )
	all_lines = fp.readline()
	fp.close()
	fp = open(option_file, 'w')
	for each_line in all_lines:
		a = re.sub(md5_data, new_md5, each_line)
		fp.writelines(a)
	fp.close()


def create_file(option_file, file_name, md5_data):
	"""
	添加配置文件项目
	:param option_file:配置文件路径 
	:param file_name: 文件名
	:param md5_data: 文件名对应MD5值
	:return: 
	"""
	try:
		with open(option_file, 'w') as pf:
			# 打开配置文档，如果不存在就创建
			for line in pf.readlines():
				time.sleep(1)
				if line.split(':')[0] == file_name:
					line.split(':')[1] = md5_data
				else:
					pf.writelines(file_name + ':' + md5_data)
					pf.write('\n')
			pf.close()
	except IOError as e:
		print('Error:can not open option file')
	# 先寻找相同项目，如果没有就加一行，先写入再进行重复行删除
	read_file = open(option_file, )
	write_file = open(option_file, 'w')
	all_line = read_file.readlines()
	read_file.close()
	s = set()
	for i in all_line:
		s.add(i)
	for i in s:
		write_file.write(i)
	write_file.close()


def create_file1(option_file, file_name, md5_data):
	"""
	修改配置文件
	:param option_file:配置文件 
	:param file_name: 需要修改的文件
	:param md5_data: 需要修改的文件的md5值
	:return: 
	"""
	try:
		md5 = file_dic(option_file)
		md5[file_name] = md5_data
		f = open(option_file, "w")
		# pickle.dump(md5, f)
		# json1 = json.dumps(dict)
		for key, value in md5.items():
			f.write('%s:%s\n' % (key, value))
		# print('{0:<10}{1:<10}'.format(str(key), md5[key]), file=f)
		f.close()
		return 0
	except IOError as e:
		print("Error in IO")
		return


def file_dic(option_file):
	"""
	将文件转化为字典
	:param option_file:配置文件，用来读取md5值
	:return: 字典
	"""
	md5 = {'test.log': '111'}
	try:
		with open(option_file, ) as pf:
			for line in pf.readlines():
				if line != '\n':
					file_name = line.split(':')[0]
					md5_name = line.split(':')[1].strip('\r').strip('\n')
					if file_name in md5:
						continue
				# print('cunzai')
					else:
						md5[file_name] = md5_name
				# print('xiugai')
				else:
					continue
	except IOError as e:
		print('ERROR:不能打开配置文件')
	return md5


def read_doc(file_path):
	"""读取本地配置文件
	:param file_path:配置文件路径"""
	try:
		with open(file_path, ) as pf:
			# 打开配置文档
			for line in pf.readlines():
				# 逐行读取文件
				time.sleep(1)
				# 略做等待
				global HOST, PATH, USER_NAME, PASSWORD
				# 将所有参数设置为全局参数
				# print('1')
				HOST = line.split(':')[0]
				# print(HOST)
				PATH = line.split(':')[1]
				# print(PATH)
				USER_NAME = line.split(':')[2]
				# print(USER_NAME)
				PASSWORD = line.split(':')[3].strip('\r').strip('\n')
	except IOError as e:
		# 捕捉错误
		print('Error:can not open configure file')
		exit(1)


def lo1_md5(my_name, my_md5, option_file):
	"""
	比较md5
	:param my_name:我的文件名 
	:param my_md5: 我的md5之
	:param option_file: 配置文件
	:return: 相等为1，不想等为2
	"""
	try:
		md5 = file_dic(option_file)
		if my_name in md5:
			if md5[my_name] == my_md5:
				return 1
			else:
				return 0
		else:
			return 0
	except Exception as e:
		print("Error in md5")


def lo_md5(my_name, my_md5, pwd_file):
	"""对比双方文件MD5
	:param my_name:读取的文件名
	:param my_md5:读取的文件的md5值
	:param pwd_file:读取的本地配置文件
	:return 判断是否相等 相等=1 不相等=0"""
	try:
		with open(pwd_file, ) as pf:
			# 打开本地配置文件
			for line in pf.readlines():
				# 逐行读取文件及其md5
				time.sleep(1)
				# 等待
				file_name = line.split(':')[0]
				# 文件名
				md5_name = line.split(':')[1]
				#  md5值
				if file_name == my_name:
					# 对比本地配置中的文件名和读取的文件名
					if md5_name == my_md5:
						# 对比已经比对上上文件的md5值
						pf.close()
						return 1
						# 如果相等返回值为文件名和判断值1
					else:
						pass
				else:
					continue
				# print('[+] Trying: ' + file_name + ':' + md5_name)
				# try:
				# 	pass
				# except Exception as e:
				# 	pass
		pf.close()
	except IOError as e:
		print('Error:the 配置 has error!')
	return 0


def extract_md5(file_path):
	"""以文件为参数，返回文件的md5值
	:param file_path:文件路径
	:return 文件md5值(以16进制返回摘要，32位）
	"""
	# m = open(file_path, )
	# 需要使用二进制格式读取文件内容
	# my_file = open(file_path, 'rb')
	# 读取文件"没有读取文件的必要"
	# m.update(my_file.read())
	# 更新字典值
	# my_file.close()
	# 关闭文件指示
	try:
		m = hashlib.md5()
		# print(m.hexdigest)
		f = open(file_path, 'rb')
		m.update(f.read())
		while True:
			b = f.read(8096)
			if not b:
				break
			m.update(b)
		f.close()
		return m.hexdigest()
	except IOError as e:
		print("have IO error")


def my_download(option_file):
	""" 下载的主函数
	:param option_file:配置参数文件
	:return"""
	try:
		f = ftplib.FTP(HOST)
		# 进行ftp连接
		# print(HOST)
	except(socket.error, socket.gaierror)as e:
		# 捕捉连接错误
		print('ERROR:cannot reach %s' % HOST)
		return
	print('-----------Connected to host %s' % HOST)

	try:
		f.login(USER_NAME, PASSWORD)
		# 进行登录动作conco
		# print(USER_NAME + PASSWORD)
	except ftplib.error_perm:
		print('ERROR:Con not Login USER_NAME = %s,PWD = %s' % (USER_NAME, PASSWORD))
		# to know what error about login in
		return
	print(' Login in as %s ' % HOST)

	"""try:
		f.cwd(PATH)
	except ftplib.error_perm:
		print('ERROR:cannot CD to %s' % PATH)
		# to know what error about mulu
		f.quit()
		# if error then quit
		return
"""
	try:
		my_list = f.nlst()
		for file_name in my_list:
			# 遍历所有文件
			match = re.match(r'(.*)\.log$', file_name)
			# 挑选.log文件进行比对
			if match:
				the_md5 = extract_md5(file_name)
				# 获取md5值
				i = lo1_md5(file_name, the_md5, option_file)
				# 验证md5值
				if 0 == i:
					f.retrbinary("RETR %s" % file_name, open(file_name, 'wb').write)
					create_file1(option_file, file_name, the_md5)
					print('Downloaded success')
					print("***Downloaded %s to %s" % (file_name, os.getcwd()))
				else:
					print('%s未变化' % file_name)
					continue
			else:
				continue
	except ftplib.error_perm:
		# 测试文件读取错误
		print('ERROR:cannot read file')
		# os.unlink(file_name)
	# else:
	# print("***Downloaded %s to %s" % (file_name, os.getcwd()))
	f.quit()
	return


def is_running(process):
	""" this is a running python用来测试是否出现已运行的程序
	:process : 查看pid提取
	"""
	try:
		pids = os.popen("ps -ef|e grep 'python.*%s'|grep -v grep|awk'{print $2}'" % process)
		# 进行ps进程查询
		for pid in pids.readlines():
			# 对查询结果进行遍历，寻找是否已经有相同的进程
			if pid != "and int(pid) != os.getpid()":
				return True
			return False
	except Exception as e:
		return False


if __name__ == '__main__':
	if is_running('download.py'):
		print('download.py is running ,exit.')
		exit(1)
	else:
		print('start download.py')
	print('please input configuration file')
	configuration_file = input()
	read_doc(configuration_file)
	print('please input option file path')
	option_name = input()
	my_download(option_name)
