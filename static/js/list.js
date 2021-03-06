function List(api, id, format, args) {
	this.list = $(id);
	this.arguments = args;
	this.apiName = api;
	this.format = format;
	var containerName = id+'Container';
	this.list.append("<div class='container col-md-10 col-md-offset-1' id='"+containerName.substr(1)+"'></div>");
	var pagerName = id+'Pager';
	this.list.append("<div class='pager pull-right' id='"+pagerName.substr(1)+"'><button class='previous btn btn-link'>上一页</button><button class='next btn btn-link'>下一页</button></div>");
	this.container = $(containerName);
	this.pager = {previous: $(pagerName+' .previous'), next: $(pagerName+' .next')};
	this.list.attr("previous", "").attr("next", "").attr("page", "1");
	var self = this;
	this.pager.next.click(function () {
									$(id).attr("page", parseInt($(id).attr("page"))+1);
									self.update();
									});
	this.pager.previous.click(function () {
									$(id).attr("page", parseInt($(id).attr("page"))-1);
									self.update();
									});	
}
(function(){
	var processData = function (format, obj) {
	return format.replace(/\{[\w\.]+\}/g, function (word) {
									var w = word.slice(1, word.length-1);
									var data = obj,  pattern = /\w+/g, attr = pattern.exec(w);
									while (attr!=null)
									{
										data = data[attr];
										attr = pattern.exec(w);
									}
									return data;
								});
	}
	List.prototype.update = function () {
		clearUserName();
		var self = this;
		api.page(this.apiName, function (data) {
										 self.clear();
										 if ('status' in data) {
											if (data.has_previous) {
												self.pager.previous.removeClass("disabled");
												self.list.attr("previous", "true");
											}
											else {
												self.pager.previous.addClass("disabled");
												self.list.attr("previous", "");
											}
											if (data.has_next) {
												self.pager.next.removeClass("disabled");
												self.list.attr("next", "true");
											}
											else {
												self.pager.next.addClass("disabled");
												self.list.attr("next", "");
											}
											self.list.attr("page", data.number);
											for (var i=0;i<data.objects.length;i++)
											{
												self.add(data.objects[i]);
											}
											$("#commentListContainer .popover").popover('show');
										 }
									},
				this.arguments, parseInt(this.list.attr("page")));
	};
	List.prototype.add = function (obj) {
		this.container.append(processData(this.format, obj));
		initUserName();
	};
	List.prototype.clear = function () {
		this.container.text("");
	};
})();