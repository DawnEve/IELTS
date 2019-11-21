拂晓词典v0.1

整体架构
后台：采用python3 flask + mysql的方式
前台：先用普通页面，后期考虑Vue



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


(2) 添加新列，陌生程度1-4级别，1是记住了，4是没见过。
alter table word_ms add strangeness int(5) DEFAULT 4 comment '陌生程度';


(3)添加雅思word list:
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
生词，易错词
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







v0.2 修正高亮显示例句问题
v0.3 添加背单词工具
v0.4 语料库可以孤立web页修改
v0.5 添加修改单词功能
v0.6 扫单词功能基本可用
v1.0 代码重构，分成好几个小py文件
	__init__ 好像不会用
	__all__ =[] 也不好用



todo
1.浏览语料库，删除质量不高的部分
2.
