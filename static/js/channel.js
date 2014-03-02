function Channel() {
	if (Channel.unique !==undefined) {
		return Channel.unique;
	}
	this.channel = sae.Channel(window.channelUrl);
	console.log(window.channelMessage);
	this.channel.onmessage = function (msg) {console.log(msg);window.channelMessage(eval('('+msg['data']+')'))};
	this.channel.onerror = window.channelError;
	this.channel.onclose = window.channelClose;
	this.channel.onopen = window.channelOpen;
}
Channel.prototype.sendMessage = function (msg) {
	this.channel.send(msg);
}
try {
	channel = new Channel();
} catch (e) {
}