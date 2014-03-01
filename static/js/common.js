function clearForm(id) {
$(':input', id)  
 .not(':button, :submit, :reset, :hidden')  
 .val('')  
 .removeAttr('checked')  
 .removeAttr('selected');
}
function jump(URL) {
	location.href = URL;	
}
function rand() {
    return 1;
}
function processBodyText(text) {
	return text.replace(/[<>]/g, function(word){return word=='<'?'&lt;':'&gt;';})
	.replace(/[\n\r]|(&lt;br \/&gt;)/g, '<br/>')
	.replace(/\[img\=[^\]]+\]/g, function(str) {return '<br/><a href="'+str.slice(5,-1)+'"><img style="max-width:80%;" src="'+str.slice(5,-1)+'" />';})
    .replace(/\[file=[^\]]+\]/g, function(str) {
        var list = str.slice("|");
        var url=list[0];
        var file_name=list[1];
        return '<br/><a href="'+url+'">'+file_name+'</a><br/>';
    });
}
Date.prototype.format = function(format){ 
var o = { 
"M+" : this.getMonth()+1, //month 
"d+" : this.getDate(), //day 
"h+" : this.getHours(), //hour 
"m+" : this.getMinutes(), //minute 
"s+" : this.getSeconds(), //second 
"q+" : Math.floor((this.getMonth()+3)/3), //quarter 
"S" : this.getMilliseconds() //millisecond 
} 

if(/(y+)/.test(format)) { 
format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
} 

for(var k in o) { 
if(new RegExp("("+ k +")").test(format)) { 
format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
} 
} 
return format; 
} 
if(!Array.indexOf){  
   Array.prototype.indexOf = function(Object){  
     for(var i = 0;i<this.length;i++){  
        if(this[i] == Object){  
           return i;  
         }  
     }  
     return -1;  
	}
}
Array.prototype.remove=function(dx) 
{ 
    if(isNaN(dx)||dx>this.length){return false;} 
    for(var i=0,n=0;i<this.length;i++) 
    { 
        if(this[i]!=this[dx]) 
        { 
            this[n++]=this[i] 
        } 
    } 
    this.length-=1 
} 