$(document).ready(function(){
    $('#elevatorPitch_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("elevator-pitch").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/elevator_pitch`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })

    $('#strengths_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("strengths").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/strengths`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
    
    $('#weaknessess_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("weaknessess").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/weaknessess`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
    
    $('#accomplishments_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("accomplishments").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/accomplishments`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
    
    $('#interview_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("interview").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/interview`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
    
    $('#general_form').submit(function(e) {
        e.preventDefault();
        var user_id = $(this).attr("userID");
        post = document.getElementById("general").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: `/job/interview_helper/${user_id}/general`,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
})