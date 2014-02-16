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
	.replace(/[\n\r]/g, '<br/>')
	.replace(/\[img\=[^\]]+\]/g, function(str) {return '<img src="'+str.slice(5,-1)+'" />';});
}