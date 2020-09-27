#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# win 压缩文件
# https://www.jb51.net/article/167861.htm

import os
import re
import time
import zipfile


# 1. 获取路径下的文件
def get_zip_file(input_path, result):
  """
  对目录进行深度优先遍历
  :param input_path:
  :param result:
  :return:
  """
  files = os.listdir(input_path)
  for file in files:
    if os.path.isdir(input_path + '/' + file):
      get_zip_file(input_path + '/' + file, result)
    else:
      result.append(input_path + '/' + file)

# 2. 开始压缩
def zip_file_path(input_path, output_path, output_name):
  """
  压缩文件
  :param input_path: 压缩的文件夹路径
  :param output_path: 解压（输出）的路径
  :param output_name: 压缩包名称
  :return:
  """
  f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
  filelists = []
  get_zip_file(input_path, filelists)
  i=0
  for file in filelists:
    # filter 1
    if file.endswith('.sql'):
      # fileter 2
      if len( re.findall('/', file) )==1:
        i=i+1
        print(i, file)
        f.write(file)
  # 调用了close方法才会保证完成压缩
  f.close()
  return output_path + r"/" + output_name


# 主程序
if __name__ == '__main__':
  # 工作目录
  os.chdir(r"G:\xampp\htdocs\IELTS\dict\backup");
  print('Working path:', os.getcwd())
  
  # 生成压缩文件的名字: 当前年月日-时分秒
  today = time.strftime("%Y%m%d-%H%M%S", time.localtime())  #"20191127_1110" #备份时间戳 '20190517-140223'
  zipFileName=today+'.zip'
  print("zipFileName:",zipFileName)
  zip_file_path(r".", '.', zipFileName)

  #
  print('==end==')