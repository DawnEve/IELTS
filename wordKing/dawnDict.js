/*
拂晓词典：
url:http://ielts.dawneve.cc/wordKing/dawnDict.js

使用方法：
该url仅支持本机访问，自用需要架服务器并调url

1.把同名php文件放在服务器中；可以更改其中的词典链接，或者自己编写词典；
2.把本js文件放在相同文件夹中，调整本文件的trans方法中ajax的php文件地址，确保能访问到；
一旦以上步骤搞定，剩下的就简单了。

3.在需要划词翻译的网页，F12打开控制台，输入如下语句并回车即可: 
var s=document.createElement("script");s.src="http://ielts.dawneve.cc/wordKing/dawnDict.js";document.body.append(s);

tips:很多网页是https的，需要构建https服务器，
难点是证书的配置: https://blog.csdn.net/qq_35128576/article/details/81326524





//划词搜索
1.实现获取词汇
2.ajax传递给后台，获取单词
3.在悬浮窗显示单词 //todo 悬浮窗有空再做。


版本控制
#v0.2 写成一个对象，避免污染变量空间
#v0.3 抽象成一个js文件
#v0.4 添加关闭按钮
#v0.4.1 美化界面
#v0.4.2 改名为dawnDict;支持console查单词 dawnDict.trans('good');


* todo 悬浮框显示；悬浮取词；
*/

//替换文本前与后的空格
;String.prototype.trim = function (){
	return this.replace(/(^\s*)|(\s*$)/g, "");
}
var dawnDict={
	version:"v0.4.2",
	$: function(s){
		return document.getElementById(s);
	},
	
	//判断子元素 
	//http://demo.jb51.net/js/2012/isParent/ 该页面有高亮代码
	//v0.2 fix bug, add && obj.tagName!=undefined
	isParent: function(obj,parentObj){
		while (obj != undefined && obj != null && obj.tagName!=undefined && obj.tagName.toUpperCase() != 'BODY'){
			if (obj == parentObj){
				return true;
			}
			obj = obj.parentNode;
		}
		return false;
	},
	/**
$(document).click(function(event){
    alert(isParent(event.target, $(".floatLayer")[0]));
});
	*/

	/*封装的ajax函数
	* v0.1 https://www.cnblogs.com/wang-zhang/p/9883654.html
	* v0.2 添加了json类型自动转换
	* v0.3 如果data为空，则不处理url
	*/
	ajax:function(options){
		//创建一个ajax对象
		var xhr = new XMLHttpRequest() || new ActiveXObject("Microsoft,XMLHTTP");
		//数据的处理 {a:1,b:2} a=1&b=2;
		var str = "";
		for(var key in options.data){
			str+="&"+key+"="+options.data[key];
		}
		str = str.slice(1)
		if(options.method == "get"){
			var url = options.url+"?"+str;
			if(str==""){
				url=options.url;
			}
			xhr.open("get",url);
			xhr.send();
		}else if(options.method == "post"){
			xhr.open("post",options.url);
			xhr.setRequestHeader("content-type","application/x-www-form-urlencoded");
			xhr.send(str)
		}
		//监听
		xhr.onreadystatechange = function(){
			//当请求成功的时候
			if(xhr.readyState == 4 && xhr.status == 200){
				var text = xhr.responseText;
				if(options.type=="json"){
					text=JSON.parse(text);
				}
				//将请求的数据传递给成功回调函数
				options.success&&options.success(text)
			}else if(xhr.status != 200){
				//当失败的时候将服务器的状态传递给失败的回调函数
				options.error&&options.error(xhr.status);
			}
		}
	},

	//给obj增加事件的自定义函,兼容IE/chrome/ff
	addEvent:function(obj,ev,fn){
		if(obj.addEventListener){
			//ff:addEventListener
			obj.addEventListener(ev,fn,false);
		}else{
			//IE:attachEvent
			obj.attachEvent('on'+ev,fn);
		}
	},

	//获取选择范围
	SelectText:function(){
		//console.log(2,this)
		try{
			var selecter = window.getSelection().toString();//chrome
			if (selecter != null && selecter.trim() != ""){
				return selecter.trim();
			}
		} catch (err){
			var selecter = document.selection.createRange();//IE
			var s = selecter.text;
			if (s != null && s.trim() != "")
			{
				return s.trim();
			}
		}
	},
	//做了冗余，可以在控制台查单词
	trans:function(word,oDiv){
		var self=this;
		//console.log('word==>'+word+';')
		self.ajax({
			method:"get",
			url:"https://ielts.dawneve.cc/wordKing/dawnDict.php?word="+word, //访问后台 //todo: 修改时要保证能访问到php文件
			success:function(data){
				if(data.status){
					if(data.res==''){
						data.res="没有查到，请调整再试";
					}
					console.log(data.res)
					if(oDiv && typeof oDiv =='object'){
						oDiv.innerHTML=data.res
					}
					if(self.$("ht_pop")){
						self.$("ht_pop").style.display='block';
					}
				}
			},
			error: function(num){
				console.log(num);
			},
			type: "json"
		})
		//ajax end;
	},
	init:function(){
		var self=this
		//嵌入dom
		var oDiv2=document.createElement("div");
		oDiv2.id='ht_pop';
		oDiv2.class='hts_pop';
		var oDiv=document.createElement("div");
		oDiv.id='ht_content';
		oDiv2.append(oDiv);
		var oClose=document.createElement("div");
		oClose.innerHTML='拂晓词典 | X';
		oClose.title="Close this box";
		oClose.id='ht_close';
		oDiv2.append(oClose);
		//
		document.body.append(oDiv2);
		
		//嵌入style表
		var oCSS=document.createElement('style');
		oCSS.innerHTML=`
#ht_pop {
	overflow: auto;
	position: fixed;
	background: #fff;color:#000;
	display:none;
	z-index: 99999;
	border:1px solid #eee;
	border-radius:5px;
	bottom:0;left:0;
	margin:5px;
	opacity:0.8;
	max-height:500px;
	font-size:1em;

	transition: box-shadow 0.35s;
    /*box-shadow: 2px -2px 10px rgba(0,0,0,0.1);*/
	box-shadow:3px -3px 10px 3px rgba(0,0,0,0.2);
}
#ht_pop:hover{
	transition:box-shadow .25s;
	box-shadow:3px -3px 20px 5px rgba(255,0,0,0.3);
}
#ht_pop h4,#ht_pop div,#ht_pop ul{margin:0;padding:0;}
#ht_pop div{padding:5px 10px;}
#ht_close{
	border-top:1px dashed #eee;
	color:#999;
	background:#ddd;
	text-align: right;
	cursor: pointer;
	padding:0 10px;
}
`
		document.body.append(oCSS);

		//step1:划词，包括单击拖动抬起鼠标，还包括单击选中词
		var word=""
		var starobj
		//双击，啥也不做
		document.ondblclick=function(){
			//console.log('1',this)
		}
		//鼠标滑动选取，分为鼠标点下，鼠标抬起
		document.onmousedown=function(){
			starobj=event.srcElement;
		}
		//鼠标抬起，开始查词
		document.onmouseup=function(){
			//如果是复制解释框，则忽略掉
			//console.log(event.srcElement, self.$("ht_pop") )
			if( self.isParent(event.srcElement, self.$("ht_pop"))  ){
				return false;
			}
			//console.log(starobj) 不是一个dom，则不起作用
			if(event.srcElement.tagName!="A" && event.srcElement.tagName!="INPUT" && starobj == event.srcElement){
				//如果没有选中的内容，则啥都不做。针对双击时的第一次鼠标抬起
				word=self.SelectText();
				if(word==undefined || word==''){
					return false;
				}
				//查单词
				self.trans(word,oDiv);
			}
		}
		//单击消失
		self.$("ht_close").onclick=function(){
			//console.log('002=====>',this)
			this.parentElement.style.display='none'
		}
	}
};
dawnDict.init();
console.log('load dawnDict: done!');