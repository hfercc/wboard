function clickMf(obj) {
	obj = $(obj);
	var is_friend = obj.hasClass("btn-default");
	alert(is_friend);
	api.normal("accountsMf", function(data) {
									 	if ('status' in data) {
											is_friend = !is_friend;
											is_friend?obj.text("已关注"):obj.text("关注");
											obj.toggleClass("btn-default").toggleClass("btn-success");
										}
									  }, {id:obj.attr("data-id"), action: is_friend?'remove':'add'});
}
function initUserName() {
	$(".user-name").each(function(){
		var element = $(this);
		element.attr("data-html", "true")
		.attr("data-trigger", "hover")
		.attr("data-delay", {show: '0', hide: '5000'})
		.attr("data-toggle", "popover")
		.attr("data-content", " ")
		.attr("data-placement", "top")
		.attr("data-container", "body")
		.on("show.bs.popover", function(){
			api.has_id("accountsInfo", function (data) {
				var str = '';
				if ('status' in data) {
					data = data.object
					str += '<h5><strong>'+data.nick_name+
					'</strong>&nbsp;(<small>'+data.username+
					'</small>)</h5>'+'<button onclick="clickMf(this)" data-id="'+data.id+'" class="btn btn-xs btn-'+(data.is_friend?'default">取消关注':'success">关注')+'</button>';
				} else { str = '加载失败，请检查网络配置'; }
				element.attr("data-content", str);
			}, element.attr("data-id"));		
		}).popover("hide");
	});
}
//$(document).ready(function(){initUserName()});