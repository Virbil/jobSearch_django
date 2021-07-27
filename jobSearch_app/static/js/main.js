$(document).ready(function(){
    $(".likebutton").click(function(e){
        e.preventDefault();
        var id = $(this).attr("data-catid");
        var status = $(this).attr('name');
        $.ajax({
            type: "GET",
            url: "/job/like",
            data: {
                job_id: id,
                status: status,
            },
            success: function(data){
                $("#like"+id).attr('name', data['status']);
                if (data['status'] == "Like"){
                    $("#like"+id).html("<i class='bi bi-hand-thumbs-up'></i>")
                }
                else{
                    $("#like"+id).html("<i class='bi bi-hand-thumbs-up-fill'></i>");
                    $("#dislike"+id).html("<i class='bi bi-hand-thumbs-down'></i>");
                    $("#dislike"+id).attr('name', 'Dislike');
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
                $("#dislike"+id).attr('name', data['status']);
                if (data['status'] == "Dislike"){
                    $("#dislike"+id).html("<i class='bi bi-hand-thumbs-down'></i>");
                }
                else{
                    $("#dislike"+id).html("<i class='bi bi-hand-thumbs-down-fill'></i>");
                    $("#like"+id).html("<i class='bi bi-hand-thumbs-up'></i>");
                    $("#like"+id).attr('name', 'Like');
                }
            }
        })
    })

})


