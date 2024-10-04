import os,time

# 单文件备份数据库
# https://blog.csdn.net/ever_peng/article/details/80088994
# shell 版： https://www.cnblogs.com/cuisi/p/7300463.html

###################################
# 备份相关 mysql table 的流程:
###################################
# 已备份 ./dict/sql/**-v2.sql

# 1.生成日期，表名字；开始备份为 .sql 文件；
# $ python backup_DB_tables.py
# 2.删掉几个不用的sql表(与单词无关的3个sql文件)，压缩 /backup 文件夹内的 sql文件 为 zip 文件; 
# $ python get_zip.py
# 3.核对后，手动删除 sql 文件，手动删除超过规定天数的zip备份文件

# 推荐每个季度备份一次，发到邮箱 (title: IELTS 英语单词语料数据库备份文件, google and vip1@163)，发到 github 版本中
# IELTS_tables_20220525-135332.zip 2.6M



#1. settings 
today = time.strftime("%Y%m%d-%H%M%S", time.localtime())  #"20191127_1110" #备份时间戳 '20190517-140223'
db_backup_dir =r"G:\xampp\htdocs\IELTS\dict\backup"; # 本地备份目录
BACKUP_SAVE_DAYS='20'

# 指定要备份的表名字
tb_arr1=['word_ms', 'word_unknown', 'word_searched','word_scan', 'sentence_dawn','user', 'msg_English',]
tb_arr2=['cell_c1', 'feature_apa', 'feature_gene', ]
#
tb_arr=tb_arr1+tb_arr2;



#2.备份主命令
cmd=r"G:\xampp\mysql\bin\mysqldump -h y.biomooc.com -P 7070 -u root -p123456 wang %s > %s\tb_%s_%s.sql";
# G:\xampp\mysql\bin\mysqldump -h y.biomooc.com -P 7070 -u root -p123456 wang word_unknown > G:\xampp\htdocs\IELTS\dict\backup\tb_word_unknown_20191127_1040.sql
#循环执行
i=0
for tbName in tb_arr:
    i+=1
    cmd2=cmd %(tbName, db_backup_dir, today, tbName);
    if i==1:
        print(today, 'Backup cmd sample: \n',cmd2,'\n');
    print(i,'===> Begin to save table: ',tbName);
    os.popen(cmd2); #执行
    print('## Saved:', tbName)
    if i>1:
        #break;
        pass;
#3. 压缩刚才备份的文件 


#4. 删除过期的sql文件

print('==end of backup to .sql files==')
