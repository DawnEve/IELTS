# word module
#
from __init__ import *



def  add_word_routes(app):
    
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
        return rs;
    #
    
    #直接用必应词典查词的web页面
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
                result[0]=saveToDB(result[1:]) #返回值是插入db的id
        else:
            result=results[0]
        #调试用
        print('005=================>',word, result)

        #准备返回值
        if result[0]!=0:
            response = jsonify({
                'status':result[0],
                'data':{
                    'id': result[0], 
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
    
    
    
    #背单词： 获取没记住的单词，按照错误率排序
    #艾宾浩斯记忆曲线怎么实现呢？ todo
    @app.route('/api/unknown/<type>')
    def unknownWord(type=''):
        #MySQL不支持子查询里有limit解决办法 https://blog.csdn.net/qq_15076569/article/details/83787108
        sql='select word,meaning,phoneticSymbol from word_ms where word in ( select tb.word from (select * from word_unknown where type="'+type+'" order by wrong/(wrong+`right`) DESC, modi_time DESC,id DESC limit 5) as tb );'
        if type=='all':
            sql='select word,meaning,phoneticSymbol from word_ms where word in ( select tb.word from (select * from word_unknown order by wrong/(wrong+`right`) DESC, modi_time DESC,id DESC limit 5) as tb ) ;'
        arr=mydb.query(sql)
        print('===========>>',arr)
        return cors(arr)
    #


    #背过的单词，保存到数据库中
    @app.route('/api/wordRecited/', methods=['POST'])
    def wordRecited():
        status=1
        wordStr=request.form.get('word')
        oDict=json.loads(wordStr);
        msg=''
        modi_time=int(time.time())   
        
        for word in oDict:
            sql='select id,word, wrong,`right` from word_unknown where word="%s";' % word
            data=mydb.query(sql);
            print('===========>',data)
            wrong=data[0][2]
            right=data[0][3]
            if right==None:
                right=0
            #
            if oDict[word]==1:
                wrong+=1
                sql='update word_unknown set modi_time=%d, wrong=%d where id=%d;' % (modi_time, wrong, data[0][0])
            else:
                right+=1
                sql='update word_unknown set modi_time=%d, `right`=%d where id=%d;' % (modi_time, right, data[0][0])
            print('update=============>word_unknown:',word,sql)
            rs=mydb.execute(sql)
            #
            msg+=word+':'+ str(oDict[word] ) +':'+str(rs)+'|';
        #response
        return cors({'status':status, 'data':msg})
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
            msg=''
            #查询之前是否有，如果没有则新增，否则仅仅更新错误次数
            for i in range(len(arr)):
                wrong=1
                word=arr[i]
                #空字符串啥也不做
                if len(word)==0:
                    continue;
                
                #感觉需要查一下这个单词，保证词库中有，以后词库足够大了就可以省略这一步了
                getword(word);
                #查次数
                data=mydb.query('select id,word, wrong from word_unknown where word="%s"' % word);
                #
                if len(data)==0:
                    sql='insert into word_unknown(word,type,wrong,add_time) values("%s","%s",%d,%d)' %(word, type,wrong, add_time)
                    print('add=============>word_unknown:',word,sql)
                    rs=mydb.execute(sql)
                else:
                    wrong=data[0][2]
                    wrong+=1
                    sql='update word_unknown set wrong=%d, modi_time=%d where id=%d;' % (wrong, add_time, data[0][0])
                    print('update=============>word_unknown:',word,sql)
                    rs=mydb.execute(sql)
                msg+=word+':'+str(rs)+'|';

            msg=[arr,type, msg]
        
        #response
        return cors({'status':status, 'data':msg})


    #过单词 刷单词神器 刷遍数 过遍数
    # 扫描单词接口：返回dict格式数据
    @app.route('/api/wordScan/', methods=['GET'])
    def wordScan():
        page=3 # >=1
        sql="select * from word_ms where id>4000 and tag_ox is null limit "+ str((page-1)*100) +",100;";
        print('scan======>', sql)
        rs=mydb.query(sql)
        
        #array to dict
        json={}
        re_h=re.compile('</?\w+[^>]*>', flags=re.S)#HTML标签
        for word in rs:
            json[word[1]]={
                'meaning':re_h.sub('',word[3]),
                'phonetic':word[2]
            }
        #
        return cors(json)
    #


    # 按照单词id，返回单词接口
    @app.route('/api/word/id/<id>', methods=['GET'])
    def wordById(id):
        sql="select * from word_ms where id="+id;
        rs=mydb.query(sql)
        return cors(rs)
    #


    # 更新单词
    @app.route('/api/updateWord/', methods=['POST'])
    def updateWord():
        status=1
        id=int(request.form.get('id'))
        word=request.form.get('word')
        phonetic=request.form.get('phonetic')
        meaning=request.form.get('meaning')
        modi_time=int(time.time());
        #
        if len(word)==0:
            msg="no word!"
            status=0
        else:
            #整行写到db
            tableName='word_ms';
            sql="update "+tableName+" set word='%s', phoneticSymbol='%s', meaning='%s', modi_time=%d where id=%d;" % \
                (word, mydb.db().escape_string(phonetic), mydb.db().escape_string(meaning), modi_time, id)
            rs=mydb.execute(sql);
            msg=[id,rs,word]
        return cors({
            'status':status,
            'data':msg
        })
    #