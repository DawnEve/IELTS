#拂晓词典的后台
from myConfig import DBUtil

from flask import Flask
from flask import jsonify,make_response,request
import requests
import re,time

app = Flask(__name__)

#获取数据库链接
mydb=DBUtil()

#html Controler
@app.route('/')
def hello():
    return """
这是字典接口文件，能完成查字典功能，
现在本地数据库检索，有了，直接返回json；
如果没有，则查必应词典，如果有，则写入数据库，并返回json，没有，则返回json说没有。

每查一次词典，记录用户信息到数据库中。
"""

#测试接口，内部调用函数等
import time
@app.route('/api/test/<word>')
def test3(word):
    print( request.headers)
    print(request.remote_addr) #获取IP地址
    return word

#保存到数据库
def saveToDB(arr):
    tableName='word_ms'

    #双保险！先要核对确实不在数据库，然后再插入
    if len( mydb.query('select * from '+tableName+' where word="'+arr[0]+'";') )>0:
        print('S01=========>word_ms:','已经在数据库中了！')
        return False

    # SQL 语句
    add_time=int(time.time()) #1572085262 数据库保存这种格式
    #mysql 转义 content = db.escape_string(content)
    sql="insert into "+tableName+"(word,phoneticSymbol,meaning,add_time) values('%s','%s','%s',%d);" %  \
    (arr[0],mydb.db().escape_string(arr[1]),mydb.db().escape_string(arr[2]), add_time)
    print('S02=========>word_ms:sql=',sql)
    # 执行sql语句
    rs=mydb.execute(sql)
    print('S03=========>word_ms:rs=',rs)
#

#直接用必应词典查词的web页面
import time
@app.route('/api/bing/<word>')
def getwordByBingWeb(word):
    rs=getwordByBing(word)
    return jsonify(rs)
#

#从必应获取单词
def getwordByBing(word):
    status=True
    headers = {
        #"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    response=requests.get('https://cn.bing.com/dict/SerpHoverTrans?q='+word, headers=headers)

    if response.text!='':
        ##########################
        ## 正则解析内容
        #音标
        phoneticSymbol=re.findall(r'lang="en">(.*?)</span>',response.text,re.S)  #re.S 把文本信息转换成1行匹配
        if len(phoneticSymbol)<1:
            phoneticSymbol=''
        else:
            phoneticSymbol=phoneticSymbol[0]
        #print(phoneticSymbol[0])
        #意思
        meaningArr=re.findall(r'<ul>(.*?)</ul>',response.text,re.S)  #re.S 把文本信息转换成1行匹配
        meaning='<ul>'+'</ul><ul>'.join(meaningArr) +'</ul>'
        #print( meaning )
        #最后的结果
        arr=[word, phoneticSymbol.strip(), meaning]
    else:
        status=False
        arr=[]
    ##########################
    # 返回结果
    if status:
        return [1]+arr
    else:
        return [0]


#字典查询后台接口，允许跨域访问
@app.route('/api/dict/<word>', methods=['GET'])
def getword(word):
    #每查一次，都记录到数据库word_searched中
    sql='insert into word_searched(word, add_time) values("%s", %d);' %(word, int(time.time()) )
    print('001=================>searched:sql=',sql)
    rs=mydb.execute(sql)
    print('002=================>searched:rs=', rs)
    
    #sql语句
    sql='select * from word_ms where word="'+word+'";'
    print('003=================>word_ms:sql=',sql)
    # 执行sql语句
    results=mydb.query(sql)

    #如果本地没有，则请求bing，并把查到的单词插入数据库
    if len(results)==0:
        print('004========New=========>',word,': Can not find the word in local db!', '='*30)
        result=getwordByBing(word)
        if result[0]==1:
            #保存到数据库
            saveToDB(result[1:])
    else:
        result=results[0]
    #调试用
    print('005=================>',word, result)

    #准备返回值
    if result[0]!=0:
        response = jsonify({
            'status':result[0],
            'data':{
                'word': result[1], 
                'phoneticSymbol':result[2], 
                'meaning':result[3]
            }
        })
    else:
        response = jsonify({
            'status':0,
            'data':{
                'msg':'could not find the word!'
            }
        })
    #允许跨域访问
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Backend', 'wjl_dawnDict_server/0.2.0')
    return response
#

#字典查询后台接口，允许跨域访问
@app.route('/api/newWord/', methods=['POST'])
def addNewWord():
    status=1
    wordStr=request.form.get('word')
    arr=re.split('_',wordStr)
    
    if len(arr)==0:
        msg="nothing to be inserted!"
        status=0
    else:
        type=request.form.get('type')
        add_time=int(time.time())
        wrong=1
        msg=''
        #查询之前是否有，如果没有则新增，否则仅仅更新错误次数
        for i in range(len(arr)):
            word=arr[i]
            #空字符串啥也不做
            if len(word)==0:
                continue;
            print('=============>',word)
            data=mydb.query('select id,word, wrong from word_unknown where word="%s"' % word);
            #
            if len(data)==0:
                sql='insert into word_unknown(word,type,wrong,add_time) values("%s","%s",%d,%d)' %(word, type,wrong, add_time)
                rs=mydb.execute(sql)
            else:
                wrong=data[0][2]
                wrong+=1
                sql='update word_unknown set wrong=%d where id=%d;' % (wrong, data[0][0])
                rs=mydb.execute(sql)
            msg+=word+':'+str(rs)+'|';

        msg=[arr,type, msg]
    
    #response
    res=jsonify({'status':status, 'data':msg})
    #res=jsonify(arr)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res;


#启动后端程序
if __name__ == '__main__':
    print("==> pls browse http://127.0.0.1:20180/")
    app.run(debug=True, port=20180)
