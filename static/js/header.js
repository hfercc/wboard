function toggleInfo() {
	if (hasLogined)
	{
		/*clearForm("#formLogin");
		$("#userName").text(username);
		$("#formLogin").hide();
		$("#userInfo").show();
		$("#psw").attr("placeholder", '密码');*/
		$("#loginNav").hide();
		$("userInfo").show();
	}
	else
	{
		/*$("#formLogin").show();
		$("#userInfo").hide();*/
		$("#loginNav").show();
		$("#userInfo").hide();
	}
}
(function (){
function login(){
	api.normal("accountsLogin", function (data){
										    if (data.hasOwnProperty('status'))
											{
												hasLogined = true;
												username = data.user.nick_name;
												toggleInfo();
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
												toggleInfo();
											}
										  });
}
})();