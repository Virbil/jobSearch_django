$( ".show-more" ).click(function() {
    var id = $(this).attr("name");
    $( "#"+id ).toggle( "slow", function() {
      // Animation complete.
    });
});