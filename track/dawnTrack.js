/*
引入方式:
//<script src="http://m.biomooc.com/dawnTrack.js?time="+new Date().getTime()></script>
//<script src="http://applybio.com/track/dawnTrack.js?time="+new Date().getTime()></script>

v0.1 基本可用
*/
function dawnTrack(source){
	var xmlhttp=new XMLHttpRequest(); //1.获取对象
	//2.绑定回调函数
	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			//console.log(xmlhttp.responseText)
			//document.getElementById("text").innerHTML=xmlhttp.responseText;
		}
	}
	//3.设定访问的url
	//http://applybio.com/track/dawnTrack.php?source=http://ielts.biomooc.com/reading/index2.html&time=1577358456750
	xmlhttp.open("GET","http://applybio.com/track/dawnTrack.php?source="+source+"&time="+new Date().getTime(),true);
	//4.发送请求
	xmlhttp.send();
}

dawnTrack( window.location )
