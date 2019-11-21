#拂晓词典的后台
from flask import Flask
app = Flask(__name__)


##########
# 引入模块
import sys
sys.path.append('main/')

# word 模块
from main.word import *
add_word_routes(app)

# sentence 模块
from main.sentence import *
add_sentence_routes(app)

# statistic 模块
from main.statistic import *
add_statistic_routes(app)

##########


#test Controler
@app.route('/')
def hello():
    return """<pre>
1.单词增删改查
这是字典接口文件，能完成查字典功能，
现在本地数据库检索，有，直接返回json；
没有，则查必应词典，查到，则写入数据库，并返回json，查不到，则返回json说没有。

每查一次词典，记录用户信息到数据库中。

2.单词写背诵；刷单词

3.例句增删改查

4.统计，
todo: 记录用户信息
"""

#测试接口，内部调用函数等
@app.route('/api/test/<word>')
def test3(word):
    time.sleep(2)
    print( request.headers)
    print(request.remote_addr) #获取IP地址
    return cors(word+'____')

#启动后端程序
if __name__ == '__main__':
    print("This is dawnDict ==> pls browse http://127.0.0.1:20180/")
    app.run(debug=True, port=20180) #
    #app.run(debug=True, host='0.0.0.0', port=20180) #
#