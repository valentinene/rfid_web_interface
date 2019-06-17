$(document).ready(function () {
  $('#register').click(function (e) {
    e.preventDefault()
    console.log($('#username').val())
    console.log($('#password').val())
    $('#loader').show();//Show loading spinner
    $.ajax({
      url: '/auth/register',
      type: 'POST',
      data: JSON.stringify({username: $('#username').val(), password: $('#password').val(), admin: $('#admin').is(':checked'), camera: $('#camera').val()
      }),
      success: function (response) {
        setTimeout(document.getElementById("messagebox").innerHTML = "Scanati cardul asociat angajatului", 500); //0.5 sec delay to scan card
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
        }, 1500)
      },
      dataType: 'json',
      contentType: 'application/json;charset=UTF-8'
    }

    )
  })

 
})

