$(document).ready(function () {
  $('#register').click(function (e) {
    e.preventDefault()
    //Validate the form
    username = document.getElementById('username');
    password = document.getElementById('password');
    camera = document.getElementById('camera');
    error = document.getElementById('username_error');

    if (username.value.length <= 4 || username.value.length > 32) {
      error.innerHTML = "Numele de utilizator trebuie sa fie intre 4 si 32 de caractere."
      return false;
    }
    error.innerHTML = "";
    error = document.getElementById('password_error');
    if (password.value.length <= 6 || password.value.length > 40) {
      error.innerHTML = "Parola trebuie sa fie intre 8 si 40 de caractere."
      return false;
    }
    error.innerHTML = "";
    error = document.getElementById('camera_error');

    if (camera.value > 4) {
      error.innerHTML = "Camera selectata nu exista."
      return false;
    }
    error.innerHTML = "";
    $('#loader').show();//Show loading spinner
    //Registration form inputs are valid at this point, continue with the registration
    $.ajax({
      url: '/auth/register',
      type: 'POST',
      data: JSON.stringify({username: $('#username').val(), password: $('#password').val(), admin: $('#admin').is(':checked'), camera: $('#camera').val()
      }),
      success: function (response) {
        if (response['error'] != null) {
          error = document.getElementById( String(response["input"]).concat("_error") );
          error.innerHTML = response['error'];
          return false;
        }
        $("#register_form :input").prop('readonly', true); // Disable form while waiting for RFID card
        document.getElementById("messagebox").innerHTML = "Scanati cardul asociat angajatului"; //0.5 sec delay to scan card
        polling = setInterval(function () {
          $.ajax({
            url: '/auth/get_angajat',
            type: 'GET',
            data: {
              username: response['username'],
              camera: response['camera']
            },
            dataType: 'json',
            success: function (response) {
              if (response['message'] === 'Found') {
                clearInterval(polling)
                //After a successful register redirect to the login page
                if(response['redirect']) { 
                  document.getElementById("messagebox").innerHTML = "Utilizatorul a fost inregistrat.\nVeti fi redirectionati la pagina de login.";
                  setTimeout(function () { window.location.href = response['redirect'] } , 1500);//Redirect after 2 seconds
                }
              }
            }
          })
        }, 1000)
      },
      dataType: 'json',
      contentType: 'application/json;charset=UTF-8'
    }

    )
  })

 
})

