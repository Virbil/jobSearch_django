$(document).ready(function(){
    $('#email').keyup(function(){
        var data = $("#reg_form").serialize()   // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",
            url: "/email",
            data: data
        })
        .done(function(res){
             $('#email_Msg').html(res)  // manipulate the dom when the response comes back
        })
    })
})