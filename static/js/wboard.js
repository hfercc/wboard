function ajax(url, data, method) {
	if (!method) {method='POST'}
	var result = "";
	$.ajax({url: url, 
					data: data, 
					type:method,
					success: function (json) {if(typeof json=='string'){result = eval('('+json+')')}else{result=json}},
					async: false
				});
	return result;
}
function clearForm(id) {
$(':input', id)  
 .not(':button, :submit, :reset, :hidden')  
 .val('')  
 .removeAttr('checked')  
 .removeAttr('selected');
}
function API() {
}
var intf = {
	normal: ['accountsLogin', 'accountsFriends', 'accountsMf', 'webboardList',
		'webboardAdd', 'webboardCommentAdd','pmList', 'pmWrite', 'saeUpload', 'saeChatStart'],
	has_id: ['accountsInfo', 'webboard', 'webboardModify', 'webboardVerify', 'webboardDelete',
		'webboardCommentDelete', 'pm', 'pmDelete'],
	notification: ['notificationList', 'notification', 'notificationDelete']
	};
API.prototype.normal = function (data, args) {
		var url = '/'+data.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/';
		return ajax(url, args, 'POST');
	};

API.prototype.page = function (data, args, page) {
	var url = '/'+data.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/';
	if (page) {url+='?page='+page;}
	return ajax(url, args, 'POST');
}	
	
API.prototype.has_id = function (data, id, args) {
		var url = '/'+data.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/'+id+'/';
		return ajax(url,args, 'POST');
	};
	
API.prototype.notification = function (data, kind, id, args) {
		var url = '/'+data.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/'+kind+'/'+id+'/';
		return ajax(url, args, 'POST');
	};
api = new API();