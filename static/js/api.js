function ajax(url, data, method, func) {
	if (!method) {method='POST'}
	var result = "";
	$.ajax({url: url, 
					data: data, 
					type:method,
					success: function (json) {result = eval(json.responseText);func(json);},
					dataType: "json"
				});
	return result;
}
function API() {}
(function(){API.prototype.normal = function (apiName, func, args) {
		var url = '/'+apiName.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/';
		return ajax(url, args, 'POST',func);
	};

API.prototype.page = function (apiName, func,args, page) {
	var url = '/'+apiName.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/';
	if (page) {url+='?page='+page;}
	return ajax(url, args, 'POST',func);
}	
	
API.prototype.has_id = function (apiName, func, id, args) {
		var url = '/'+apiName.replace(/[A-Z][a-z]*/g, function(word){return '/'+word.toLowerCase()})+'/'+id+'/';
		return ajax(url,args, 'POST',func);
	};
})();
api = new API();