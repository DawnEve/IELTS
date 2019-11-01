/*
aim:看web(如长页面或pdf)听写时加一个框，提示视线位置
Version:0.1 可用，引入页面即可出现框，刷新消失。
var s=document.createElement("script");s.src="http://ielts.biomooc.com/static/js/dragBar.js";document.body.append(s);
var s=document.createElement("script");s.src="http://ielts.dawneve.cc/static/js/dragBar.js";document.body.append(s);
可移动的元素一定是定位元素（非static定位的）
监听鼠标mousedown，mouseup 和 mousemove事件。
mousemove事件处理里获取 event 事件对象的 clientX 和 clientY属性, 通过style设置元素的 top 和 left
*/
var dragBar={
	dragFactory: function(drag1){
		var IsMousedown, LEFT, TOP;
		//var drag1=document.getElementById("drag1");
		drag1.onmousedown=function(e) {
			var _this=this;
			IsMousedown = true;
			e = e||event;
			LEFT = e.clientX - _this.offsetLeft;
			TOP = e.clientY - _this.offsetTop;
			document.onmousemove = function(e) {
				var e = e||event;
				var left=e.clientX - LEFT,top=e.clientY - TOP;
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
				//重新设置高度
				if (IsMousedown) {
					_this.style.left = left + "px";
					_this.style.top = top + "px";
				}
				return false;
			}

			document.onmouseup=function(){
				IsMousedown=false;
			}
		}
	},
	init:function(){
		var oDiv=document.createElement('div');
		oDiv.setAttribute('style','	color:blue;	position:fixed;	display:block;	width:300px;	height:100px;	bottom:0;	cursor:move;	border:2px dashed #000;	background:rgba(0,0,0,0.2);z-index:9999;');
		oDiv.setAttribute('draggable',true);
		document.body.append(oDiv);
		//
		this.dragFactory(oDiv);
	}
}
console.log('script loaded!')
dragBar.init()