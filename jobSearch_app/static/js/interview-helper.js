$(document).ready(function(){
    $('#elevatorPitch_form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            url: '/job/interview_helper/1/elevator_pitch',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                $("#results").html(response)
            }
        })
    })
})