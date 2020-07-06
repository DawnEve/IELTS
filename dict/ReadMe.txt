拂晓词典v0.1

整体架构
后台：采用python3 flask + mysql的方式
前台：先用普通页面，后期考虑Vue


1.部署方式:
要不定期备份后台数据库。
数据库位置定义在文件 /dict/dawnDictLib.py 中


2.如何运行?
后台运行 /dict/index.py 
$ python index.py


3.背单词页面
http://ielts.dawneve.cc/dict/scanWord.html

记住了: 数字1，或减号
下一个: 好几个键都可以(左箭头，下箭头，数字234)

遇到错误的单词，修改: 点拂晓词典，里面有修改


修改代码:
前台页面定义在 /dict/scanWord.html中
背单词的模式定义在文件 /dict/main/word.py



4.背完单词提交到后台，js控制台输入 
$(document).trigger("feedback");
不提交就没有副作用


#### 
缺点1: 复数名词单独成词条，不好，怎么分流到已经认识的数据表中？或者冗余字段中
	doubts; tons; pigments; 
缺点2: 动词的ing, 过去式、过去分词怎么分流？
	tackling; 




大型项目的组织方式：
https://blog.csdn.net/ying847782627/article/details/51189049




####################################
英汉精简数据库：主要来自必应
CREATE TABLE `word_ms` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) DEFAULT NULL,
  `phoneticSymbol` varchar(100) DEFAULT NULL,
  `meaning` text,
  `modi_time` varchar(30) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  #Unique KEY `word` (`word`)
  KEY `word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

(1)#添加新列：牛津级别，根据ox3000和ox5000表添加，基础(A1，A2),中级（B1,B2）,高级(c1,c2)；
alter table word_ms add tag_ox varchar(10) DEFAULT NULL comment '牛津级别';
# 每类几个单词？
mysql> select tag_ox, count(*) from word_ms group by tag_ox;
+--------+----------+
| tag_ox | count(*) |
+--------+----------+
| NULL   |     1820 |
| A1     |      746 |
| A2     |      741 |
| B1     |      759 |
| B2     |     1409 |
| C1     |     1292 |
+--------+----------+

#1) 查异常值：
mysql> select id,word,tag_ox from word_ms where tag_ox like '%\.%';

# 查id断开的编号
select (id-1) as id_jump from word_ms a where not exists (select 1 from word_ms where id+1=a.id) order by id_jump;
+---------+
| id_jump |
+---------+
|       0 |
|    5499 |
|    5506 |
|    5523 |
|    5528 |
|    5535 |
|    5540 |
|    5547 |
insert into word_ms(id) values(1027);
insert into word_ms(id) values(1131);
    

#2) 查找带数字的单词
mysql> select * from word_ms where word REGEXP '[0-9]{1,}'; ## live2
#并删掉
mysql> delete from word_ms where word REGEXP '[0-9]{1,}';
Query OK, 12 rows affected (0.03 sec)

#查带空格的单词
select id, concat('|',word,"|"), tag_ox from word_ms where word like '% %' limit 10;



#3) 查找带web的词条，基本都是输入错误，改正，不能改正的删除
mysql> select * from word_ms where meaning like '%web.%';
delete from word_ms where meaning like '%web.%';



(2)添加雅思word list:
https://github.com/woshichuanqilz/others/blob/master/WindowsConfig/IELTS

添加新列，雅思词汇 tag_ielts: 第一批3000个标签为1, 默认是0；
alter table word_ms add tag_ielts int(3) DEFAULT 0 comment '雅思词汇' after tag_ox;
## ALTER TABLE word_ms DROP tag_ielts;





扫描单词：100个剩下10个以下时可以停止。
0)"select * from word_ms where id>5000 and tag_ox is null limit 100";
["futile", "numb", "pail", "rack", "stale", "wretched", "tangle"]

1)select * from word_ms where id>4000 and tag_ox is null limit 100;
["amiable", "bypass", "composite", "entail", "pedestrian", "rake", "riddle", "scorn", "tentative"]

2) select * from word_ms where id>4000 and tag_ox is null limit 100,100;
["dissipate", "lounge", "renovate", "repel", "revolt", "spontaneous", "tiresome", "wholesome", "wreath"]

4000,
#page 3 ["preclude", "agitate", "pathetic", "sly", "humid", "shaft", "tempo", "gracious", "inertia"]
#page 4 ["gasp", "shrewd", "numb", "refrain", "stale", "futile", "rack", "wretched"]
#page 5 ["fiddling", "nagging", "fraught", "episodic", "prised", "concur", "tacking", "epistemological", "disparate"]
#page 6 ["interrogate", "wig", "coerce", "penile", "platinum", "milieu", "dissect", "homeostasis", "bimodality"]

3000,
#page1 
#page2 ["envisage", "tub", "susceptible", "wrench", "strenuous", "clasp"]




####################################
查过的单词列表
CREATE TABLE `word_searched` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




####################################
生词，主要是易写的错词
CREATE TABLE `word_unknown` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) DEFAULT NULL,
  `type` char(10) DEFAULT NULL, #写错w/听错l/生词n/读音错了r/
  `right` int(10) DEFAULT 0,
  `wrong` int(10) DEFAULT 0,
  `modi_time` varchar(30) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





####################################
dawn语料库，以行为单位保存(一行可能包含很多句子)
CREATE TABLE `sentence_dawn` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `line` text,
  `source` varchar(50) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#添加新列：修改时间
alter table sentence_dawn add modi_time varchar(30) DEFAULT NULL comment '修改时间';

词典从语料库查询单词，新页面显示
select * from sentence_dawn where line like "%risk%" order by add_time DESC, id DESC limit 5;

mysql> delete from sentence_dawn where line like '%listen and then answer the following%';
Query OK, 47 rows affected (0.02 sec)







####################################
刷单词记录表，可以记录多用户的单词掌握情况
CREATE TABLE `word_scan` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `uid` int(10) NOT NULL comment '用户id号',
  `wid` int(10) NOT NULL comment '单词id号',
  `unfamiliarScore` int(5) DEFAULT 0 comment '陌生程度',
  `familiarScore` int(5) DEFAULT 0 comment '熟悉程度',
  
  `add_time` varchar(30) DEFAULT NULL,
  `modi_time` varchar(30) DEFAULT NULL,
  KEY (`id`),
  PRIMARY KEY (`uid`,`wid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
使用复合主键，必须是MyISAM  引擎？

mysql> desc word_scan;
+-----------------+-------------+------+-----+---------+----------------+
| Field           | Type        | Null | Key | Default | Extra          |
+-----------------+-------------+------+-----+---------+----------------+
| id              | int(10)     | NO   | MUL | NULL    | auto_increment |
| uid             | int(10)     | NO   | PRI | NULL    |                |
| wid             | int(10)     | NO   | PRI | NULL    |                |
| unfamiliarScore | int(5)      | YES  |     | 0       |                |
| familiarScore   | int(5)      | YES  |     | 0       |                |
| add_time        | varchar(30) | YES  |     | NULL    |                |
| modi_time       | varchar(30) | YES  |     | NULL    |                |
+-----------------+-------------+------+-----+---------+----------------+

陌生打分，见一次不认识，则陌生程度加1，貌似不会减少；
熟悉打分，直接斩杀加3分，见一次后再斩杀加1分，此后不再加分。最后剩下的10个左右单词，陌生程度加1分。

#添加新列: viewed 只要提交，所有看过的都加1
alter table word_scan drop viewed;
alter table word_scan add viewed int(5) DEFAULT 0 comment '过遍数' after familiarScore;

(1) 查看最熟悉的单词
select a.id, a.word,a.phoneticSymbol,a.meaning,b.familiarScore from word_ms a left join ( select * from  word_scan where uid=1 ) b on a.id=b.wid order by familiarScore DESC, b.add_time DESC limit 10\G

(2)查看最陌生的单词
select a.id, a.word,a.phoneticSymbol,a.meaning,b.familiarScore, b.unfamiliarScore from word_ms a left join ( select * from  word_scan where uid=1 ) b on a.id=b.wid order by unfamiliarScore DESC, b.add_time DESC limit 10\G

(3)按照目的刷单词
http://ielts.dawneve.cc/dict/scanWord.html?page=1&aim=0  默认刷单词......: 按照 (familiarScore+0.5*unfamiliarScore) 选择没见过面的单词 
aim=1: 

(4)查一个词，联合两个表
select a.id, a.word,a.phoneticSymbol,a.meaning,familiarScore,unfamiliarScore,viewed from word_ms a left join ( select * from  word_scan where uid=1 ) b on a.id=b.wid where a.word="posture";


####################################

1.写一个简易的接口，使用web页面或js输入错误单词列表，默认是生词，

2.提供状态的接口
/api/status/  提供状态，数据表条目数，昨天新增条目数


3.背单词app，怎么优化？

查看生词，按照错误率排名，相同排名的按照时间正序
select *, wrong/(`right`+ wrong) as ratio  from word_unknown order by ratio desc, add_time limit 20;



4.过单词软件，一天过几百单词，只为眼熟。 scanWord.html
(1) 词汇表
https://github.com/Deemoore/zieckey-study-code/tree/319fd3914a9abc0e617f96409de6062e9ec4b98c/eclipseworkspace/python/dictparser/src/zieckey/dict/wordlist
只有46级可能齐全。


(2)话题的单词列表
https://www.cambridgeenglish.org/Images/22105-ket-vocabulary-list.pdf




5.报错
(1)
(2013, 'Lost connection to MySQL server during query ([WinError 10054] 远程主机强迫关闭了一个现有的连接。)')




6.备份表
mysqldump -u 用户名 -p 数据库名 表名> 导出的文件名
G:\xampp\mysql\bin\mysqldump -h y.biomooc.com -P 7070 -u root -p wang word_unknown > G:\xampp\htdocs\IELTS\dict\backup\tb_word_unknown_20191127.sql
有更好用的脚本： tools/backup_DB_tables.py
备份到 backup/目录下，git不跟踪，自行发送到Email中。





v0.2 修正高亮显示例句问题
v0.3 添加背单词工具
v0.4 语料库可以孤立web页修改
v0.5 添加修改单词功能
v0.6 扫单词功能基本可用
v1.0 代码重构，分成好几个小py文件
	__init__ 好像不会用
	__all__ =[] 也不好用
v1.1 反馈结果新增 viewed 字段，影响筛选单词时的排序;
v1.2 备份脚本//todo


todo
1.浏览语料库，删除质量不高的部分
2.
