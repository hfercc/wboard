function clickMf(obj) {
	obj = $(obj);
	var is_friend = obj.hasClass("btn-default");
	api.normal("accountsMf", function(data) {
									 	if ('status' in data) {
											is_friend = !is_friend;
											is_friend?obj.text("取消关注"):obj.text("关注");
											obj.toggleClass("btn-default").toggleClass("btn-success");
										}
									  }, {id:obj.attr("data-id"), action: is_friend?'remove':'add'});
}
function clearUserName() {
	$(".user-name").each(function ()
	{
		$(this).popover("hide");
	});
}
function initUserName() {
	$(".user-name").each(function(){
		var element = $(this);
		var id = rand();
		element.attr("data-html", "true")
		.attr("data-trigger", "click")
		.attr("data-toggle", "popover")
		.attr("data-content", "<div id='"+id+"'></div>")
		.attr("data-placement", "bottom")
		.attr("data-container", "body")
		.on("show.bs.popover", function(){
			api.has_id("accountsInfo", function (data) {
				var str = '';
				if ('status' in data) {
					data = data.object;
					str += '<h5><strong>'+data.nick_name+
					'</strong>&nbsp;(<small>'+data.username+
					'</small>)</h5>';
                    if (data.username == username) {
                        str += '<p>自己</p>';
                    } else {
                    	str+='<button onclick="clickMf(this)" data-id="'+data.id+'" class="btn btn-xs btn-'+(data.is_friend?'default">取消关注':'success">关注')+'</button>'
                    }
				} else { str = '加载失败，请检查网络配置'; }
				$("#"+id).html(str);
			}, element.attr("data-id"));		
		}).popover();
	});
}
$(document).ready(function(){initUserName()});