/**
 * @author Kishor Mali
 */


jQuery(document).ready(function(){
	
	jQuery(document).on("click", ".deleteWallet", function(){
		var wallet = $(this).data("wallet"),
			hitURL = baseURL + "deleteWallet",
			currentRow = $(this);
		
		var confirmation = confirm("Are you sure to delete this wallet " + wallet +"?");
		
		if(confirmation)
		{
			jQuery.ajax({
			type : "POST",
			dataType : "json",
			url : hitURL,
			data : { wallet : wallet } 
			}).done(function(data){
				currentRow.parents('tr').remove();
				if(data.status = true) { alert("Wallet "+ wallet + " successfully deleted"); }
				else if(data.status = false) { alert("Wallet "+ wallet + " deletion failed"); }
				else { alert("Access denied..!"); }
			});
		}
	});
	
});
