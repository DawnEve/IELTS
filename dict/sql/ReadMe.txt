1.save the database of wang; [2023.8.6]
(1) 保存
> # cmd
> mysqldump -h y.biomooc.com -P 7070 -u root -p wang > D:\xampp\htdocs\IELTS\dict\sql\IELTS.wang.sql
(2) 删减
有点大，86M。
查看发现有些无关表，删除: 
`cell_c1`
feature_apa
`feature_gene`
`feature_gene2`
`feature_gene_h1`

剩余8M。




(2) 导入新表格中
win11 xampp 本地系统。
> mysql -u root -p wang < D:\xampp\htdocs\IELTS\dict\sql\IELTS.wang-v2.sql


(3) navicat 查看 
已经导入。



2. 尝试启动项目
(1) 安装依赖包
> pip3 install pymysql  -i https://pypi.douban.com/simple/ 

(2) 启动
D:\xampp\htdocs\IELTS\dict> python index.py
然后，字典后台就启动了。





