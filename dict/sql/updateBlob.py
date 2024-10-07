# -*- coding: utf-8 -*-

# 这是示例，自己编写请另存为，修改运行后删除。

import pymysql, sys, re
from pymysql.converters import escape_string

def updateBlob(textBlog, msg_id):
	db = pymysql.connect(host='10.10.117.156',port=8070,user='root', password='123456', \
	                         database='wang', charset='utf8')

	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	sql="update `msg_English` set msg_content='%s' where msg_id=%d" % (escape_string(textBlog), msg_id);
	#print(sql)

	try:
	    cursor.execute(sql) # 执行sql语句
	    db.commit() # 提交到数据库执行
	    print("commit successfully")
	except:
	    rsponse=db.rollback() # 发生错误时回滚
	    print("rollback")
	    print( sys.exc_info() )

	# 关闭数据库连接
	cursor.close()
	db.close()

text2="""
<span class="light">Oct 06, 2024 | 3428 words
Tue 10 Sep 2024 05.00 BST | By Seán Columb</span>

<b>I spoke to dozens of people – from ‘donors’ to brokers – to find out how this exploitative trade thrives on chaos and desperation</b>
More from this series: Rights and Freedom

They travelled at night, for what seemed like hours, but it was difficult to tell. Yonas was blindfolded and drowsy from the Xanax he had been given. He wasn’t sure where he was, but he could smell salt in the air when the car stopped. Yonas heard Ali, the other passenger, wind down his window and light a cigarette. The driver sat motionless, breathing heavily. Several minutes passed in silence. Then Yonas heard a pinging noise. Someone’s phone had received a message.

...
"""

#print(text2)
#updateBlob(text2, 618)


def addHtmlTagP(text2):
    arr=re.split("\n{2,}", text2)
    print(len(arr))

    str2=""
    for i in range(len(arr)):
        ele = arr[i]
        if not ele.startswith("<hr"):
            ele = "<p>%s</p>" % (ele);
        str2 += ele + "<p><br></p>";
        print("[%d] %s" % (i, ele) )
    return str2;

updateBlob(addHtmlTagP(text2), 618)
