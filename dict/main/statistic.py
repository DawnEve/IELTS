# statistic module
#
from __init__ import *

# v0.2 做了web页面

def  add_statistic_routes(app):
    #
    # 查询统计信息
    @app.route('/api/stat/', methods=['GET'])
    def statistics():
        #总体统计
        rs1=mydb.query('select count(*) from word_ms;');
        rs2=mydb.query('select count(*) from word_unknown;');
        rs3=mydb.query('select count(*) from word_searched;');
        #
        # 昨天时间 https://www.jb51.net/article/141272.htm
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        oneWeek = today - datetime.timedelta(days=7)
        #
        today=int(time.mktime(  time.strptime(str(today), '%Y-%m-%d')   ))
        yesterday=int(time.mktime(  time.strptime(str(yesterday), '%Y-%m-%d')   ))
        oneWeek=int(time.mktime(  time.strptime(str(oneWeek), '%Y-%m-%d')   ))
        #24h内
        #yesterday=time.time()-24*3600
        #
        print('today=',today)
        td1=mydb.query('select count(*) from word_ms where add_time>%d;'%today);
        td2=mydb.query('select count(*) from word_unknown where add_time>%d;'%today);
        td3=mydb.query('select count(*) from word_searched where add_time>%d;'%today);
        #
        print('yesterday=',yesterday)
        ys1=mydb.query('select count(*) from word_ms where add_time>%d and add_time<%d;'% (yesterday,today) );
        ys2=mydb.query('select count(*) from word_unknown where add_time>%d and add_time<%d;'% (yesterday,today) );
        ys3=mydb.query('select count(*) from word_searched where add_time>%d and add_time<%d;'% (yesterday,today) );
        #
        print('oneWeek=',oneWeek)
        week1=mydb.query('select count(*) from word_ms where add_time>%d;'%oneWeek);
        week2=mydb.query('select count(*) from word_unknown where add_time>%d;'%oneWeek);
        week3=mydb.query('select count(*) from word_searched where add_time>%d;'%oneWeek);
        #
        sentence=mydb.query('select count(*) from sentence_dawn;');
        sentenceToday=mydb.query('select count(*) from sentence_dawn where add_time>%d;'%today);
        sentenceYs=mydb.query('select count(*) from sentence_dawn where add_time>%d and add_time<%d;'% (yesterday,today) );
        sentenceWeek1=mydb.query('select count(*) from sentence_dawn where add_time>%d;'%oneWeek);
        #返回值
        return cors({
            'sentence':{
                'total':sentence[0][0],
                'today':sentenceToday[0][0],
                'yesterday':sentenceYs[0][0],
                'week':sentenceWeek1[0][0]
            },
            'word_ms':{
                'total':rs1[0][0],
                'today':td1[0][0],
                'yesterday':ys1[0][0],
                'week':week1[0][0]
            },
            'word_unknown':{
                'total':rs2[0][0],
                'today':td2[0][0],
                'yesterday':ys2[0][0],
                'week':week2[0][0]
            },
            'word_searched':{
                'total':rs3[0][0],
                'today':td3[0][0],
                'yesterday':ys3[0][0],
                'week':week3[0][0]
            }
        })
    #
