拂晓词典v0.1

整体架构
后台：采用python3 flask + mysql的方式
前台：先用普通页面，后期考虑Vue


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


查过的单词列表
CREATE TABLE `word_searched` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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






dawn语料库，以行为单位保存(一行可能包含很多句子)
CREATE TABLE `sentence_dawn` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `line` text,
  `source` varchar(50) DEFAULT NULL,
  `add_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


词典从语料库查询单词，新页面显示
select * from sentence_dawn where line like "%risk%" order by add_time DESC, id DESC limit 5;



1.写一个简易的接口，使用web页面或js输入错误单词列表，默认是生词，


2.提供状态的接口
/api/status/  提供状态，数据表条目数，昨天新增条目数


v0.2 修正高亮显示例句问题
v0.3 添加背单词工具




todo
1.浏览语料库，删除质量不高的部分
2.
