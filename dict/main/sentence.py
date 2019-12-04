# sentence module
#
from __init__ import *



def  add_sentence_routes(app):

    # 按照单词id，返回句子接口
    @app.route('/api/sentence/id/<id>', methods=['GET'])
    def sentenceById(id):
        sql="select * from sentence_dawn where id="+id;
        rs=mydb.query(sql)
        return cors(rs)

    # 按照单词，返回句子接口
    @app.route('/api/sentence/word/<word>', methods=['GET'])
    def sentenceByWord(word):
        # 获取分页，默认是第一页
        page=int(request.args.get('page',1))
        size=10 #每页条目
        
        if word=='null2':
            sql="select * from sentence_dawn order by add_time DESC, id DESC limit %d,%d;" % ( (page-1)*size, size );
        else:
            initSite=(page-1)*size
            sql="select * from sentence_dawn where line like '%"+word+"%' order by add_time DESC, id DESC limit "+str(initSite)+","+str(size)+";";
            #sql=sql % ( (page-1)*size, size );
        #print('************>>>word=',word,sql)
        rs=mydb.query(sql)
        return cors(rs)


    # 插入新语料库2 debug use only
    @app.route('/api/newSentence2/', methods=['POST'])
    def addNewSentences2():
        status=1
        wordStr=request.form.get('str')
        arr=re.split('_____',wordStr)
        #
        source=request.form.get('source')
        
        return cors({
            'arr':arr,
            'source':source
        })

    # 插入新语料库
    @app.route('/api/newSentence/', methods=['POST'])
    def addNewSentences():
        status=1
        wordStr=request.form.get('str')
        lines=re.split('_____',wordStr)
        #
        msg=""
        
        if len(lines)==0:
            msg="nothing to be inserted!"
            status=0
        else:
            source=request.form.get('source','dict') #默认来自于字典
            add_time=int(time.time())
            ###########
            #过滤
            i=0
            j=0
            res=''
            for lineR in lines:
                i+=1
                line=lineR.strip()
                arr=re.split('[.?!]+',line) #一行分割成句子
                marker='OK'
                #过滤空行
                if len(line)==0:
                    continue;
                #过滤带汉字的行
                if re.search(r'[\u4e00-\u9fa5\|]+',line)!=None:
                    marker='No_汉字';
                    continue;
                #过滤重复的行
                if re.search('Listen to the tape then answer the question below',line)!=None:
                    marker='No_重复';
                    continue;
                if re.search('https{0,1}://www',line)!=None or re.search('doi: ',line)!=None:
                    marker='No_URL'
                    continue;
                if len(arr)==1 and len(re.split('\s+',arr[0]) )<5:
                    marker='No_仅有一句，且这一句不到5个单词'
                    continue
                #整句的保存到数据库中
                j+=1
                rs=0
                #防重复：检查数据库是否存在
                tableName='sentence_dawn'         
                if len( mydb.query( 'select * from '+tableName+' where line="%s";'%  mydb.db().escape_string(line)  ))>0:
                    rs=-1
                else:
                    sql="insert into "+tableName+"(line,source,add_time) values('%s','%s',%d);" % ( mydb.db().escape_string(line), source,add_time)
                    rs=mydb.execute(sql)
                #print(j,line)
                res+=str(rs)+' | '+line+"<br>"
            print('==end== 实际插入行数 j=',j, '; 总行数 i=',i)
            msg=[i,j,res]
        return cors({
            'status':status,
            'data':msg
        })

    # 更新语料库
    @app.route('/api/updateSentence/', methods=['POST'])
    def updateNewSentences():
        status=1
        wordStr=request.form.get('str')
        lines=re.split('_____',wordStr)
        #
        msg=""
        if len(lines)==0:
            msg="nothing to be inserted!"
            status=0
        else:
            source=request.form.get('source')
            id=int(request.form.get('id'))
            modi_time=int(time.time())
            ###########
            #过滤
            res=''
            for lineR in lines:
                line=lineR.strip()
                #过滤空行
                if len(line)==0:
                    continue;
                #整行写到db
                tableName='sentence_dawn'
                sql="update "+tableName+" set source='%s', line='%s', modi_time=%d where id=%d;" % \
                    (source, mydb.db().escape_string(line),modi_time, id)
                msg=sql
                rs=mydb.execute(sql)
                res+=str(rs)+' | '+line+"<br>"
            msg=[id,res]
        return cors({
            'status':status,
            'data':msg
        })
    #

    