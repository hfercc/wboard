function NavController() {
	if (NavController.unique !== undefined) {
		return NavController.unique;
	}
	this.tabs = [];
}
function Tab(obj) {
    this.unread?(this.unread = 0):1;
	var b = typeof obj == 'number';
	b?(this.data = {id:obj,nick_name: obj}):(this.data = obj);
	var id = (!b)?obj.id:obj;
	$("#tabHeader").append('<li><a href="#tab'+id+'" data-toggle="pill" id="tabItem'+id+'">'+this.data.nick_name+'<button type="button" class="inline close" aria-hidden="true">&nbsp;&nbsp;&times;</button></a></li>');
	this.tabHeader = $("#tabItem"+id);
	$("#tabContent").append('<div class="tab-pane fade" style="border:1px solid #ddd;" id="tab'+id+'"><div style="overflow-y:auto;height:300px;margin:10px;" class="chatContent"><p class="history-bar text-center" style="background-color:#eee;"><small>加载</small><button class="history btn btn-link btn-sm">历史记录</button></p><dl></dl></div><hr/><div style="padding:0px 10px 40px 10px;"><span class="pull-left files"></span><div class="form-group"><textarea class="form-control" style="width:100%;height:90px;"></textarea></div><input type="hidden" name="attachment" value="" /><div class="btn-group pull-left"><button class="upload-picture btn btn-default btn-sm"><span class="glyphicon glyphicon-picture"></span></button><button class="upload-file btn btn-default btn-sm"><span class="glyphicon glyphicon-upload"></span></button></div><div class="btn-group pull-right"><button class="submit btn btn-success btn-sm">发送</button></div></div>');
	this.tab = $("#tab"+id);
	this.submit = this.tab.find("button.submit");
	this.textarea = this.tab.find("textarea");
	this.content = this.tab.find(".chatContent")[0];
	this.chatList = this.tab.find("dl");
	this.attachments = $(this.tab.find("input[name=attachment]")[0]);
	this.files = $(this.tab.find(".files")[0]);
	this.uploadState = '';
	var self = this;
	if (b) {
		api.has_id("accountsInfo", 
			function (data) {
				if ('status' in data) {
					self.data = data.object;
					self.tabHeader.html(self.data.nick_name+'<button type="button" class="close" aria-hidden="true">&nbsp;&nbsp;&times;</button>');
					window.friends.push(data.object);
	self.tabHeader.find(".close").click(function () {
		self.close();										  
	});
				}
			}, id);
	}
	this.tabHeader.find(".close").click(function () {
		self.close();										  
	});
	this.tabHeader.on("shown.bs.tab",
		function (e) {
			controller.activeTab = self;
            self.markRead();
	});
	self.int = 0;
	self.interval = function () {
		if (self.int == 9) {
			clearInterval(self.intervalId);
			self.int = 0;
			return;
		}
		self.int++;
		var css = self.int%2==0?"":"red";
		self.tabHeader.css("background-color", css);
	}
	self.tab.find(".upload-picture").click(
		function () {
			self.uploadState = 'picture';
			showFileUploadDialog();
		}
	);
	self.tab.find(".upload-file").click(
		function () {
			self.uploadState = 'file';
			showFileUploadDialog();
		}
	);
	self.tab.find(".history").click(
		function () {
			api.normal('pmHistory', 
				function (data) {
					if ('status' in data) {
						$(data.objects).each(
							function () {
								self.prepend(this);
						});
						self.since_id = data.objects[data.objects.length-1].id;
						if (data.objects.length<20)
							self.tab.find(".history-bar").hide();
						self.tab.find(".history-bar small").text("查看");
						self.tab.find(".history").text("历史记录");
					} else {
						self.tab.find(".history-bar small").text("加载失败，请");
						self.tab.find(".history").text("重试");
					}
				}, {since_id: self.since_id, id: self.data.id});
		}
	);
	self.submit.click(
	function () {
		var text = self.textarea.val();
		if (!text) {
			self.textarea.parent().addClass("has-error");
			self.textarea.attr("placeholder", "输入不为空");
			return;
		}
		text = self.formatMessage();
		channel.sendMessage(JSON.stringify(text));
		text.created_time = new Date().format("MM-dd hh:mm");
		self.append(text);
		self.content.scrollTop = self.content.scrollHeight;
		self.textarea.val("");
		self.attachments.val("");
		self.files.text("");
	});
	self.textarea.keypress(
		function (e) {
			$(this).parent().removeClass("has-error");
			$(this).attr("placeholder", "");
			if (e.ctrlKey && (e.which == 13 || e.which == 10)) {
				self.submit.click();	
			}
		}
	);
	resize();
}
Tab.prototype.flash = function () {
	self = this;
	this.intervalId = setInterval("self.interval()", 300);	
}
Tab.prototype.markRead = function () {
    window.messages -= this.unread;
    this.unread = 0;
    console.log("unread"+this.unread);
    this.tabHeader.css("background-color", "");
}
Tab.prototype.formatMessage = function() {
	return {to:this.data.id, message: this.textarea.val(), attachments: this.attachments.val()};	
}
Tab.prototype.close = function () {
	this.tab.remove();
	this.tabHeader.remove();
	controller.tabs.remove(controller.tabs.indexOf(this));
}
Tab.prototype.messageToHTML = function (msg) {
	var name = ('to' in msg)?username:getDataObject(msg['from']).nick_name;
	var attachments = '';
	var style = 'color:'+('to' in msg?'green':'blue');
	var b = msg.attachments.split("|");
	if (msg.attachments)
	for (i in b) {
        if (typeof b[i] != "string") continue;
console.log(b[i]);
		var a = b[i].split("*");
		attachments += '<br/><a target="_blank" href="'+a[0]+'">'+a[1]+'</a>';
	}
	return "<dt style='"+style+"'>"+name+'&nbsp;'+msg.created_time+"</dt><dd>"+processBodyText(msg.message)+attachments+"</dd>";
}
Tab.prototype.prepend = function (msg) {
	this.chatList.prepend(this.messageToHTML(msg));	
}
Tab.prototype.append = function (msg) {
	this.chatList.append(this.messageToHTML(msg));	
}
NavController.prototype.get = function (obj) {
	var id = (typeof obj == 'object')?obj.id:obj;
	for (var i=0;i<this.tabs.length;i++){
		if (this.tabs[i].data.id == id) return this.tabs[i];
	}
	var tab = new Tab(obj);
	this.tabs.push(tab);
	return tab;
}

function getDataObject(id) {
	for (i in window.friends) {
		if (window.friends[i].id==id) {
			return window.friends[i];
		}
	}
}

function uploadCallback(obj) {
	var tab = controller.activeTab;
	var state = tab.uploadState;
	if (state == 'picture') {
		tab.textarea.val(tab.textarea.val()+'[img='+obj.url+']');
	} else {
		var val = tab.attachments.val();
		var splitter = val?"|":"";
		tab.attachments.val(val+splitter+obj.url+'*'+obj.file_name);
		tab.files.append("<p href='"+obj.url+"'>"+obj.file_name+'<button type="button" class="close" aria-hidden="true" onclick="deleteFile(this)">&nbsp;&nbsp;&times;</button></p>');
	}
}

function deleteFile(obj) {
	var p = $(obj).parent();
	var tab = controller.activeTab;
	var fs = tab.attachments.val().split();
	for (var i=0;i<fs.length;i++) {
		if (fs[i].indexOf(p.attr("href")>=0)) {
			fs.remove(i);
			break;
		}
	}
	p.remove();
	tab.attachments.val(fs.join('|'))
}

function showFileUploadDialog() {
	$("#fileUploadDialog").modal("show");	
}

function listItemClick(obj) {
	controller.get(friends[parseInt(obj.attr("data-id"))]).tabHeader.tab('show');
}
function updateFriendsList() {
		$("#friendsList").html("");
		api.normal("accountsFriends", function (data) {
													if ('status' in data) {
														$(data.objects).each(function(i, obj){
														$("#friendsList").append('<li class="list-group-item"><button class="btn btn-link btn-xs" data-id="'+i+'" onclick="listItemClick($(this));">'+obj.nick_name+'</button></li>');
																					  });
														window.friends = data.objects;
													}
												});
}
$(document).ready(
	function() {
        window.messages = 0;
        flashId = 0;
		updateFriendsList();
		controller = new NavController();
		$("#friendsListBadge").click(function() {
			api.normal('pmHistory',
				function (data) {
					if ('status' in data) {
						$(data.objects).each(
							function () {
								var id = this.to?this.to:this.from;
								var tab = controller.get(id);
								tab.append(this);
								tab.tabHeader.tab("show");
                                tab.markRead();
							});
					}
				}, {limit:unread});
				$(this).hide();
            	window.messages = 0;
		});
	}
);
function flashTitleCallback() {
    if (window.messages==0) {
        console.log("callback"+window.messages+" "+flashId);
        clearInterval(flashId);
        flashId = 0;
        document.title = "聊天 － 华附模联公告板";
        return;
    }
    if (document.title.indexOf("新")>=0) {
        document.title = "【     】 聊天 - 华附模联公告板";
    } else {
        document.title = "【新消息】 聊天 - 华附模联公告板";
    }
}
function flashTitle() {
    if (flashId != 0) return;
    if (window.focused) return;
    console.log("prepare");
    flashId = setInterval("flashTitleCallback()", 500);
}
function messageCount(count) {
    if (count == undefined) {
        return window.messages;
    }
    window.messages = count;
    console.log(window.messages);
    count?flashTitle():1;
}        
function channelMessage(msg) {
	if ("p" in msg) {      
		$("#friendsListBadge").text(msg.p?msg.p:'');
		unread = msg.p;
        messageCount(unread);
		return;
	}
    window.messages++;
    messageCount(window.messages);
	var tab = controller.get(msg.to?msg.to:msg.from);
    tab.unread++;
    tab.flash();
	tab.append(msg);
	tab.content.scrollTop = tab.content.scrollHeight;
}