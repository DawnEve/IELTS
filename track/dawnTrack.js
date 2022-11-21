/*
how to use:
//<script src="http://m.biomooc.com/dawnTrack.js?time="+new Date().getTime()></script>
//<script src="http://applybio.com/track/dawnTrack.js?time="+new Date().getTime()></script>

v0.1 basic
v0.2 use En comment
*/
function dawnTrack(source){
	//1.get obj
	var xmlhttp=new XMLHttpRequest(); 
	//2.set callback
	xmlhttp.onreadystatechange=function(ev){
		//console.log(ev); //shake hand 4 times
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			console.log(xmlhttp.responseText)
			//document.getElementById("text").innerHTML=xmlhttp.responseText;
		}
	}
	//3.set url
	//http://applybio.com/track/dawnTrack.php?source=http://ielts.biomooc.com/reading/index2.html&time=1577358456750
	xmlhttp.open("GET","/track/dawnTrack.php?source="+source+"&time="+new Date().getTime(),true);
	//4.send request
	xmlhttp.send();
}

dawnTrack( window.location )
