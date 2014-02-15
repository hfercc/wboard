(function(){
function verifyAddForm() {
	if (!$("#addFormTitle").val()) {
		$("#addFormTitle").popover('show');
		return false;
	}
	if (!$("#addFormBodyText").val()) {
		$("#addFormBodyText").popover('show');
		return false;
	}	
	return true;
}
$(document).ready(function () {
	$("[data-toggle='popover']").popover();
	$("#addFormSubmit").click(function() {
		if (!verifyAddForm()) return;
		var form = $("#addForm"), statusID;
		if (form.attr("data-action")=="add"){
			api.normal("webboardAdd", function(data){
											   $("#addDialog").modal("hide");
											   if ('status' in data) {
												   statusID = data.object.id;
												   jump('/webboard/'+statusID);
											   }
										}, form.serialize());
		} else {
			api.has_id("webboardModify", function(data){
											   $("#addDialog").modal("hide");
											   if ('status' in data) {
												   statusID = data.object.id;
												   jump('/webboard/'+statusID);
											   }
										}, form.attr("data-id"), form.serialize());	
		}	
	});
	$("#addForm textarea,input").focus(function(){$(this).popover('hide');});
});
})();
function showAddForm(action) {
	$("#addForm").attr("data-action", action);
	if (action == 'add') {
		clearForm("#addForm");
	}
	$("#addDialog").modal('show');
}
function uploadCallback(obj) {
	$("#addFormUpload").popover("hide");
	$("#addFormBodyText").val($("#addFormBodyText").val()+'[img='+obj.url+']');
}