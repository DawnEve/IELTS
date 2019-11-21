# main module.

# 该包内的文件所需要的包可以一次性导入。
from flask import Flask, jsonify,make_response,request
import requests
import re,time,datetime,json


# 引入模块
import sys
sys.path.append('..')


#获取数据库链接
from dawnDictLib import *
mydb=DBUtil()


print('*********** this is main module ***********')


#from main import *
#__all__ = ["word", "sentence", "statistic"]