$(document).ready(function(){
	
	/*For deleting activities - probably should have separate js files but oh well */
	$(".delete_activity").click(function(){
		var name=$(this).closest("tr").find(".activityName").text();
		var count=$(this).closest("tr").find(".activityCount").text();
		var id=$(this).attr("activity_id");
		$("#myModal").find("span#activityToDelete").html(name);
		$("#myModal").find("span#activityToDeleteCount").html(count);
		$("#deleteActivityButton").attr("activity_id", id)
	});
	
	$("#deleteActivityButton").click(function(){
		var id=$(this).attr("activity_id");
		$.post("/activity/delete/", {"id":id}, function(data){
			$("#"+data).hide();
		});
			
	});
	
	/*For adding a new activity*/
	function activity_hide(){
		$("#add_activity").hide();
		$("label[for='add_activity']").hide();
	}
	function activity_show(){
		$("#add_activity").show();
		$("label[for='add_activity']").show();
	}
	function add_activity_view(){
		var option=$("#id_activity option:selected").text()
		if (option=="ADD NEW ACTIVITY"){
			activity_show();
		}
		else {
			activity_hide();
		}	
	}
	/*something's fishy with this, but oh well*/
	activity_hide();
	$("#id_activity").change(function(){
		add_activity_view();
	});
	$("#id_activity").click(function(){
		add_activity_view();
	});
	//May not actually need this functionality.  We'll see.  
	/*
	var cache={};
	var cached=false;
	$('#activity_select').autocomplete({
		'minLength':0,
		//This next part is the opposite of DRY.  Really need to find a better way!
		'select':function(event, ui){ 
			event.preventDefault();
			$("#activity_select").val(ui.item.label);
			$("#activity_original").val(ui.item.val);
		},
		'source': function(request, response){
		if (!cached){
			$.getJSON("/activity/getActivities/", function(data){
				cache=data;
				cached=true;
				response(cache);
			});		
		}
		else {  // this part does not appear to be working
			var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
			response(cache, function( item ){
				return matcher.test(item['label']);
			}) 
		}
		}
	}).on("focus", function(){
		$(this).autocomplete("search", "");
	});
	*/
});