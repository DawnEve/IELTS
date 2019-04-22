/********************
*1. 基本功能
*2. debug，添加显示最长n个句子
********************/

//全局只暴露一个变量
var ielts={}

//返回str中单词个数和当前英文日期
ielts.calc=function(str){
	var a2,i,arr,tmp;
	//1.字符串分割成数组
	a2=str.split(/[^a-zA-Z]+/) 

	//2.排除长度在2字母以内的数组元素
	i=a2.length //数组长度
	arr=[]
	while(i>0){
		i-=1;
		if(a2[i].length>2) arr[arr.length]=a2[i];
	}

	//3.整理日期June 23, 2018
	tmp=String(new Date()).split(/\s/);
	//(7) ["Sat", "Jun", "23", "2018", "19:30:00", "GMT+0800", "(中国标准时间)"]

	//4.输出结果："Jun 23, 2018 | 17 words"
	return(tmp[1]+" "+tmp[2]+", "+tmp[3]+' | '+arr.length+" words");
}


//打印str中最长的n个句子
ielts.long=function(str,n=3){
	var s2,s3,s4,s5;
	//1.分割获取句子
	s2=str.split(/[.!?\n\r]+/)  //断句包括句号、感叹号、问号和换行符

	//2.获取每个句子的单词长度
	s3=[]
	for(var i=0; i<s2.length; i++){
		s3.push(s2[i].split(/[^a-zA-Z]/).length)
	}
	//3.对句子长度arr排序
	//深度复制s4=s3;
	s4=[];
	for(var i=0;i<s3.length;i++){
		s4[i]=s3[i];
	}
	//再对s4排序
	s4.sort(function(a,b){ return b-a; })
	//4.取出前n个
	s5=s4.slice(0,n)
	//5.输出最长的n个句子
	for(var i=0; i<s2.length; i++){
		if( s5.indexOf( s3[i] ) >=0){
			// console.log("s3[i]=",s3[i]," index: ", s5.indexOf( s3[i] )) //debug
			console.log("[sentence "+i+"]"+ s3[i] + " words>", s2[i])
		} 
	}
}

//简化函数名字为cp
var cp=function(str){
	console.log(ielts.calc(str));
	console.log("============5 Longest sentences:")
	ielts.long(str,5);
}
