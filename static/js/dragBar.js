/*
aim:看web(如长页面或pdf)听写时加一个框，提示视线位置
Version:
v0.1 可用，引入页面即可出现框，刷新消失。
v0.2 添加键盘移动功能，暴露接口，可以设置大小、颜色等

使用：
var s=document.createElement("script");s.src="http://ielts.biomooc.com/static/js/dragBar.js";document.body.append(s);
var s=document.createElement("script");s.src="http://ielts.dawneve.cc/static/js/dragBar.js";document.body.append(s);
可移动的元素一定是定位元素（非static定位的）
监听鼠标mousedown，mouseup 和 mousemove事件。
mousemove事件处理里获取 event 事件对象的 clientX 和 clientY属性, 通过style设置元素的 top 和 left
*/
var dragBar={
	fixLeftTop:function(_this,left,top){
		//会拖出去产生进度条，要防止需要写判断
		if(left<0){
			left=0;
		}else if(left >window.innerWidth-_this.offsetWidth){
			left = window.innerWidth-_this.offsetWidth;
		}
		if(top<0){
			top=0;
		}else if(top >window.innerHeight-_this.offsetHeight){
			top = window.innerHeight-_this.offsetHeight;
		}
		return [left,top]
	},
	dragFactory: function(obj){
		var IsMousedown, LEFT, TOP;
		var _this=this;
		obj.onmousedown=function(e) {
			IsMousedown = true;
			e = e||event;
			LEFT = e.clientX - obj.offsetLeft;
			TOP = e.clientY - obj.offsetTop;
			document.onmousemove = function(e) {
				var e = e||event;
				var left=e.clientX - LEFT,top=e.clientY - TOP;
				var rs=_this.fixLeftTop(obj,left,top)
				left=rs[0];
				top=rs[1]
				//重新设置高度
				if (IsMousedown) {
					obj.style.left = left + "px";
					obj.style.top = top + "px";
				}
				return false;
			}

			document.onmouseup=function(){
				IsMousedown=false;
			}
		}
	},
	moveFactory:function(obj){
		var _this=this;
		document.onkeydown=function(e){
			if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.key)<0){
				return false;
			}
			//记录开始位置
			var left=obj.offsetLeft,top=obj.offsetTop;
			//普通移动，一次5px，按下shift则精细调整微1px
			var range=5;
			if(e.shiftKey==1){
				range=1
			}
			if('ArrowUp'==e.key) top-=range;
			if('ArrowDown'==e.key) top+=range;
			if('ArrowLeft'==e.key) left-=range;
			if('ArrowRight'==e.key) left+=range;
			//不能移动出去
			var rs=_this.fixLeftTop(obj,left,top)
			left=rs[0];
			top=rs[1]
			
			//重新设置高度
			obj.style.left = left + "px";
			obj.style.top = top + "px";
			return false;
		}
	},
	init:function(){
		var oDiv=document.createElement('div');
		oDiv.setAttribute('style','	color:blue;	position:fixed;	display:block;	width:600px;	height:250px;	bottom:0;	cursor:move;	\
		border-radius: 20px; box-shadow: 5px 5px 5px #000; font-size:5em;	\
		background:#A349A4;		z-index:9999;');
		
		oDiv.setAttribute('draggable',true);
		document.body.append(oDiv);
		//功能
		this.dragFactory(oDiv); //添加可拖动属性
		this.moveFactory(oDiv); //添加响应键盘移动功能		
		this.obj=oDiv;//暴露出去，方便该颜色、大小等
		console.log('dragBar.js script loaded! help> dragBar.help()')
	},
	help:function(){
		console.log('1.设置大小 > dragBar.obj.style.width="500px";  \n2.能鼠标拖动位置，或者键盘按键移动位置，按下shift和箭头一次移动1px，仅用箭头一次移动5px；');
	}
};
dragBar.init();