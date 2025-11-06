# sentence3 module
# .txt 检索方案
# 保存到sqlite3中，定期更新DB，默认增量更新。

# v0.2 no letter before word


from __init__ import *



# 1.建表
# 不用分词，不用倒排，第一版直接 LIKE 就够。
sql_create_table="""
-- 一个 sentence 就一条记录
-- CREATE TABLE sentences (
CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,     -- 2025-11-05
    path TEXT,     -- /data/2025/11/05.txt
    title TEXT,    -- 第一行
    src_url TEXT,  -- 可空，若文章本身元信息有
    word_count INTEGER,
    sentence TEXT
);
""";

sql_create_table_index="CREATE INDEX idx_sentences_sentence ON sentences(sentence);";


# 2.预处理器（每天/周/启动 跑一次）

from pathlib import Path
import sqlite3
import re

db="dustbin/txt_sentences.db"
conn=sqlite3.connect(db)
cur=conn.cursor()

# 每个.txt文件，拆分为句子，保存到sqlite
def process_file(p:Path):
    #txt = p.read_text(encoding="utf-8", errors="ignore")
    txt = p.read_text(encoding="utf-8")
    lines = txt.splitlines()
    title = lines[0].strip()
    body = "\n".join(lines[1:])
    date = p.stem     # 05
    # better：dirname/dirname/file变为 2025-11-05
    dt = f"{p.parts[-3]}-{p.parts[-2]}-{p.stem}"
    words = len(body.split())

    sentences = re.split(r'(?<=[.!?])\s+', body)
    for s in sentences:
        cur.execute("INSERT INTO sentences(date,path,title,src_url,word_count,sentence) VALUES(?,?,?,?,?,?)",
            (dt,str(p),title,None,words,s))
    conn.commit()

# 初始化数据库，如果有新txt，依赖路径，增量式更新db
def init_DB(force_new_table=0):
    # 新建表: 是否强制新建表。默认不强制，但是没有表会新建
    if(force_new_table==1):
        cur.execute("DROP TABLE IF EXISTS sentences")

        cur.execute(sql_create_table);
        cur.execute(sql_create_table_index);
        # delete_path():    cur.execute("DELETE FROM sentences WHERE path=?", (path_str,))
        conn.commit()
    
    # 逐个txt文件扫描
    print("-> incremental add to sqlite DB: /dict/dustbin/txt_sentences.db")
    for p in Path("../reading/").rglob("*.txt"):
        # 跳过 novel/
        if "novel" in p.parts or "wechat" in p.parts:   # 排除掉
            continue
        
        # 判定年份
        # 用 p.parts[-3] 正好是 YYYY
        year = p.parts[-3]
        if not (len(year)==4 and year.isdigit()):
            continue
        
        # 查看路径是否已经在数据库：
        cur.execute("""
            SELECT *
            FROM sentences
            WHERE path=?
        """,( str(p), ))
        rows=cur.fetchall()
        
        # 保存到数据库
        if(len(rows)==0):       
            # 处理句子并保存到DB
            print("--> process: ", p) #--> process:  ..\reading\2025\11\04.txt
            print("\t insert to DB")
            process_file(p)



# 3.Flask API
#from flask import Flask, request, jsonify
#import sqlite3
#app = Flask(__name__)

#DB="sentences.db" #用之前定义的
init_DB() #不加参数，默认不需要清空DB，只是增量添加txt到DB



def  add_sentence3_routes(app):

    # http://127.0.0.1:20180/api/sentence3/word/good?page=1
    @app.route("/api/sentence3/word/<word>")
    def search(word):
        page=int(request.args.get("page",1))
        ps=10
        offset=(page-1)*ps
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        # 简洁版: 大写小写都匹配
        cur.execute("""
            SELECT id, path, title, date, word_count, sentence
            FROM sentences
            WHERE lower(sentence) LIKE ?
            ORDER BY date DESC, id DESC
            LIMIT ? OFFSET ?
        """,(f"% {word.lower()}%",ps,offset))
        rows=cur.fetchall()
        # 组装成你要的 8列格式
        r=[]
        for (id,path,title,date,word_count,sentence) in rows:
            r.append([
                id,
                "/reading/dawnReader.html?text="+date.replace("-","/"),
                title.split("|")[0] if "|" in title else title,
                date.replace("-",""),
                word_count,
                title,
                sentence
            ])
        return cors(r)


    @app.route("/api/sentence3/id/<id>")
    def get_one(id):

        conn=sqlite3.connect(db)
        cur=conn.cursor()
        # 简洁版: 大写小写都匹配
        cur.execute("""
            SELECT id, path, title, date, word_count, sentence
            FROM sentences
            WHERE id=?
        """,(id,))
        rows=cur.fetchall()

        # 组装成你要的 8列格式
        r=[]
        for (id,path,title,date,word_count,sentence) in rows:
            r.append([
                id,
                "/reading/dawnReader.html?text="+date.replace("-","/"),
                title.split("|")[0] if "|" in title else title,
                date.replace("-",""),
                word_count,
                title,
                sentence
            ])
        return cors(r)
