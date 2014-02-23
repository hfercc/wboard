function toggleInfo() {
	if (hasLogined)
	{
		clearForm("#formLogin");
		$("#formLogin").hide();
		$("#userInfo").show();
		$("#psw").attr("placeholder", '密码');
		$("#top1").show();
	}
	else
	{
		$("#formLogin").show();
		$("#userInfo").hide();
		$("#top1").hide();
	}
}
function login(){
	api.normal("accountsLogin", function (data){
										    if (data.hasOwnProperty('status'))
											{
												hasLogined = true;
												username = data.user.username;
												toggleInfo();
												changeUserName();
											}
											else
											{
												//$("#hintLogin").popover('show');
												$("#psw").attr("placeholder", "密码错误");
												$("#psw").val("");
												$("#psw").focus();
												//setTimeout(function(){$("#hintLogin").popover('hide')}, 3000);
											}
										  },
				$("#formLogin").serialize());
}
function logout(){
	api.normal("accountsLogout", function(data){
										  if (data.hasOwnProperty('status'))
											{
												hasLogined = false;
												username = '';
												$("#userName").text(username);
												toggleInfo();
											}
										  });
   jump("/");
}