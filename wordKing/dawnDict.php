<?php
/** 后台查词典，返回结果
* 接口方式 http://ielts.dawneve.cc/wordKing/dawnDict.php?word=good
* v0.1 必应查词，允许跨域请求翻译
* v0.2 改名字为 dawnDict 拂晓词典
* v0.3 目录不存在时递归创建
* 
* 
* 这是后台接口。详细使用请看同名js文件.
*/
//重新定义header，允许外链
header('Server: suctom-server',true);
//header('HTTP/1.1 200 OK');
header('Server: WJL_translation_server/0.2');
header('Email: jimmymall@163.com');
//header('Content-Type:text/html;charset=UTF-8');//html文件类型,UTF-8类型
header("Access-Control-Allow-Origin: *");


//接收参数
$word='';
if(isset($_GET['word'])){
	$word=$_GET['word'];
}

//如果没有词，则报错，并返回
if($word==''){
	die(json_encode(array('status'=>0, 'msg'=>"input empty word")) );
}


//调用接口，访问词典
$data['word']=$word;
$data['status']=1;

//获取完整的url
#$fromUrl= 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
//获取网址参数
//接收参数
$source='';
if(isset($_GET['source'])){
	$source=$_GET['source'];
}


//文件夹
$dir = 'backup/tmp/';
is_dir($dir) OR mkdir($dir, 0777, true); // 如果文件夹不存在，将以递归方式创建该文件夹

//把查的词写入文件
$date = date("Ym");
$file_name = 'backup/tmp/wordSearched_'.$date.'.txt'; //每天一个文件
//$wordfile_handler = fopen("backup/wordSearched.txt", "a");
$wordfile_handler = fopen($file_name, "a");
$time=time();
fwrite($wordfile_handler, $word."\t".$time.' '.date("Y/m/d h:m:s")."\t".$source."\n");
fclose($wordfile_handler);


//这里是词典
$url="https://cn.bing.com/dict/SerpHoverTrans?q=".$word; //必应词典
#$url="https://www.ldoceonline.com/dictionary/".$word; //朗文词典
#$url="https://www.oed.com/search?searchType=dictionary&q=".$word."&_searchBtn=Search"; //牛津词典

#$url="http://dict.youdao.com/w/eng/".$word."/#keyfrom=dict2.index";


//返回结果
$data['url']=$url;
$data['res']=file_get_contents($url);
echo json_encode($data);