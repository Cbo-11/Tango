    $(document).ready(function() {
        //jquery code to be added here 
$("#about-btn").click( function(event){
            alert("You Clicked the button using JQuery!");
        });

    $("p").hover( function() {
        $(this).css('color','red'); 
    },
    function(){ 
        $(this).css('color','blue');
    });

        $("#about-btn").click( function(event){
        msgstr= $("#msg").html()
        msgstr=msgstr+"ooo"
        $("#msg").html(msgstr)
    });

});