#!/usr/bin/python
#-*-coding:utf-8-*-

from distutils.core import setup
import glob
import py2exe


options = {"py2exe": {	
		"compressed": 1, #压缩  
		"optimize": 2, 
		"bundle_files": 3 #1、所有文件打包成一个exe文件，但Tkinter有问题
	}
}   

setup(
    windows = [{"script": "buildsdk.py"}],
	options = options,
	data_files = [
		('.', ['buildsdk.json']),
	]
) 



