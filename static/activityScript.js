$(document).ready(function(){
	var cache={};
	var cached=false;
	$('#activity_select').autocomplete({
		'minLength':0,
		//This next part is the opposite of DRY.  Really need to find a better way!
		'select':function(event, ui){ 
			event.preventDefault();
			$("#activity_select").val(ui.item.label);
			$("#activity_hidden").val(ui.item.val);
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
	
});