Aim: 拂晓预料库 txt 版

使用 /reading/年/月/日.txt 资料，查找包含给定关键词的句子。
txt 定期保存到sqlite3: /dict/dustbin/，然后再查。
	更新db的关键函数在 /dict/main/sentence3.py

1. API 格式
最新的在page1
url: http://127.0.0.1:20180/api/sentence3/word/good?page=1
[    [
        263,
        "https://mp.weixin.qq.com/s?__biz=MzI0NDcxNzc5Mg==&mid=2247485194&idx=1&sn=3d484220ff1cb1bb28eac77dacfaac2b&chksm=e958c685de2f4f93c07a626392c08f689f7bf37b291cacdb40589cffbfd94c1ad6255e9001e3#rd",
        "xx报",
        "20180925",
        3338,
        "Guardian|Solving the genome puzzle",
        "The 100,000 Genomes Project was launched in England in 2012 by the then prime minister David Cameron, whose son Ivan was born with a rare neurological disorder that baffled doctors and eventually claimed his life."
    ],
	[id(编号), 原文url(可为空), 原文来源(正文第一行|前的部分), 日期，单词数，标题，匹配句子],
]



2. 前台
/dict/sentence3.html

