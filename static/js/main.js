
//tools fns
function $(s){
	return document.getElementById(s)
}
//ajax fn
function ajax(options){
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
}


//
window.onload=function(){
	//insert nav
	ajax({
		method:"get",
		url:"static/nav.html",
		data:{},
		success:function(text){
			$('nav').innerHTML=text
			//class="current"
			var url=document.location.href
			var aA=$('nav').getElementsByTagName('a');
			if(url.search('.html')==-1){
				aA[0].setAttribute('class',"current")
				return '';
			}
			for(var i=0; i<aA.length; i++){
				if(aA[i].href==url){
					aA[i].setAttribute('class',"current")
					break;
				}
			}
		},
		error: function(num){
			console.log(text)
		},
		type: "text"
	})	
}
