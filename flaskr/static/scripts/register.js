$(document).ready(function() {
	$("#register").click( function(e) {
                e.preventDefault();
		console.log($("#username").val());
		console.log($("#password").val());

		$.ajax({
			url: "/auth/register",
			type: "POST",
			data: JSON.stringify({username: $("#username").val(), password: $("#password").val(), admin: $("#admin").is(":checked"), camera: $("#camera").val()
			}),
			success: function(response) {
				polling = setInterval(function(){
					$.ajax({
						url: "/auth/get_angajat",
						type: "GET",
						data: {
                                                username: response['username'],
                                                camera: response['camera']
                                                },
						dataType: "json",
						success: function(response) { if (response["message"] == "Found") clearInterval(polling); }
					});
				}, 3000);
			},
			dataType: "json",
			contentType: "application/json;charset=UTF-8"
			}

		);
		return false;
	});

});
