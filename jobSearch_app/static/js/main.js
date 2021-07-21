$(document).ready(function(){
    $(".likebutton").click(function(e){
        e.preventDefault();
        var id = $(this).attr("data-catid");
        var status = $(this).text();
        $.ajax({
            type: "GET",
            url: "/job/like",
            data: {
                job_id: id,
                status: status,
            },
            success: function(data){
                if (data['status'] == "Like"){
                    $("#like"+id).removeClass('text-warning');
                    $("#like"+id).addClass('text-success');
                    $("#like"+id).text(data['status']);
                }
                else{
                    $("#like"+id).removeClass('text-success');
                    $("#like"+id).addClass('text-warning');
                    $("#like"+id).text(data['status']);
                }
            }
        })
    })


    $(".dislikebutton").click(function(e){
        e.preventDefault();
        var id = $(this).attr("data-catid");
        var status = $(this).attr('name');
        $.ajax({
            type: "GET",
            url: "/job/dislike",
            data: {
                job_id: id,
                status: status,
            },
            success: function(data){
                if (data['status'] == "Dislike"){
                    $("#dislike"+id).removeClass('text-warning');
                    $("#dislike"+id).addClass('text-danger');
                    $("#dislike"+id).text(data['status']);
                }
                else{
                    $("#dislike"+id).removeClass('text-danger');
                    $("#dislike"+id).addClass('text-warning');
                    $("#dislike"+id).text(data['status']);
                }
            }
        })
    })



})


