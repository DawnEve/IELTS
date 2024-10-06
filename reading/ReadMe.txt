
1.小说阅读器[深色] reading/novelReader.html

支持本地和远程txt
http://ielts.dawneve.cc/reading/novelReader.html?url=novel/HarryPoter_1-7.txt
http://ielts.dawneve.cc/reading/novelReader.html?url=http://y.biomooc.com:8000/file/docs/HarryPoter_1-7.txt

带百分比，可以显示和设置百分比。
大致正确，不是十分精确。不同高度时，同一个百分比显示文本有差异。
纠正了上个错误，但是读完不是100%，勉强接受吧。

改进的地方: 自动统计阅读速度，几百词一分钟?




2. 英文文章阅读器[浅色] reading/dawnReader.html

(1) 单词数统计
1) 位置 http://ielts.dawneve.com/reading/index2.html
2) 词频统计
该页面 F12 console: > cp(``) //词频首字母
在两个反引号中间粘贴txt内容，回车出现统计信息，和最长句子top5

Mar 09, 2024 | 1170 words
ielts.js:65 ============5 Longest sentences:
ielts.js:57 [sentence 42]64 words>  There Microsoft had to become the un-Microsoft - pricing at rock bottom instead of charging hundreds of dollars for its Windows operating system and Office applications; abandoning the centerpiece of its public-policy approach elsewhere, the protection of its intellectual property at all costs; and closely partnering with the government instead of fighting it as in the U.S., a stance that has opened the company to criticism from human rights groups.


(2)添加文章的方法:在reading/目录中
1) 打开 index2.html，顶部添加目录信息
	2024/10/x.txt 是年月日信息，也对应目录结构，月份和日期2位数，比如 01，12
	精听(可选): 给出 music.163.com 的链接
	bingo(可选)：给出精彩一句话

2) 文本文件 x.txt 的格式
第一行：杂志名 | 标题
第二行：阅读日期 | 单词数
第三行：作者和发表日期。

如:
<span class=light>Mar 11, 2024 | 232 words
By AFP - Agence France Presse | February 25, 2024</span>

结尾放链接：
<span class=light>
https://fortune.com/2018/11/02/ballmer-china-windows-piracy/
</span>

中间可以使用html标签，如<b>