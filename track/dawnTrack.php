<?php
/*
v0.1 基本可用
v0.2 能跨域
v0.3 time zone
*/


//1.允许跨域
header('Server: suctom-server',true);
//header('HTTP/1.1 200 OK');
header('Server: WJL_track_server/0.1');
header('Email: jimmymall@163.com');
//header('Content-Type:text/html;charset=UTF-8');//html文件类型,UTF-8类型
header("Access-Control-Allow-Origin: *");

# time zone
date_default_timezone_set('Asia/Shanghai');


/*2. tools: function and classes*/
########## ip
//https://www.cnblogs.com/binaryworms/articles/1947032.html
function GetIP(){
	if(!empty($_SERVER["HTTP_CLIENT_IP"])){
	  $cip = $_SERVER["HTTP_CLIENT_IP"];
	}
	elseif(!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
	  $cip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	}
	elseif(!empty($_SERVER["REMOTE_ADDR"])){
	  $cip = $_SERVER["REMOTE_ADDR"];
	}
	else{
	  $cip = "无法获取！";
	}
	return $cip;
}
$ip= GetIP();



########## url
//获取完整的url
$url= 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
//获取网址参数
$para= $_SERVER["QUERY_STRING"]; #id=1


//显示访问用户的浏览器信息
$agent=$_SERVER['HTTP_USER_AGENT'];


/*####### working begin #######*/
// 解析并生成信息
//$msg="open from: ". $ip.' '. date("Y/m/d H:m:s").' '. $url .' '. $para;
//$msg='{IP:"'. $ip.'", serverDate:"'. date("Y/m/d H:m:s").'", para:"'. $para.'"},';
$n="\n";
$msg="====================\n";
$msg .= '{IP:"'. $ip.'", '.$n.
	'serverDate:"'. date("Y/m/d H:i:s").'", '.$n.
	'para: "'. $para.'", '.$n.
	'agent:"'.$agent.'"},';
$msg .= "\n--------------------\n";


// 文件名
#$date = date("Ymd");
$date = date("Ym");
#
$dir = './tmp';
is_dir($dir) OR mkdir($dir, 0777, true); // 如果文件夹不存在，将以递归方式创建该文件夹
#
$file_name = 'tmp/'.$date.'.txt';

//记录信息
$wordfile_handler = fopen($file_name, "a");
fwrite($wordfile_handler, $msg."\n");
fclose($wordfile_handler);

echo "Hello, php";
