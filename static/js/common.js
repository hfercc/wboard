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
function uploadFile(formID, func) {

}
function processBodyText(text) {
	return text.replace(/[<>]/g, function(word){return word=='<'?'&lt;':'&gt;';})
	.replace(/[\n\r]|(&lt;br \/&gt;)/g, '<br/>')
	.replace(/\[img\=[^\]]+\]/g, function(str) {return '<br/><img style="max-width:100%;" src="'+str.slice(5,-1)+'" />';});
}
function rand() {
	var temp="0123456789qwertyuiopasdfghjklzxcvbnm";
	var i, s = '';
	for (i=0;i<10;i++) s+=temp[parseInt(Math.random()*35+1)];
	return s;
}