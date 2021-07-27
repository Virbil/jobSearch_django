$(document).ready(function(){
    $('#elevatorPitch_form').submit(function(e) {
        e.preventDefault();

        post = document.getElementById("elevator-pitch").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/elevator_pitch',
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

        post = document.getElementById("strengths").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/strengths',
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

        post = document.getElementById("weaknessess").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/weaknessess',
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

        post = document.getElementById("accomplishments").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/accomplishments',
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

        post = document.getElementById("interview").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/interview',
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

        post = document.getElementById("general").value;
        document.getElementById("results").innerHTML = post;

        $.ajax({
            url: '/job/interview_helper/1/general',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                console.log(response)
                // $("#results").html(response)
            }
        })
    })
})