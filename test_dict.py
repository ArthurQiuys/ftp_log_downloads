#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2017/5/31


def change(a):
	dict = {'1.log': '1', '2.log': '2'}
	file = '3.log'
	md5 =  '3'
	if file in dict:
		if dict[file] == md5:
			print('yes,wo in here')
		else:
			dict[file] = md5
			print('no wo change')
	else:
		dict[file] = md5
		print('I add it')
	print(dict)
	return dict


if __name__ == '__main__':
	pass
a = 0
ad = change(a)
print(ad)

