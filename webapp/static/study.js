(function ($) {
    "use strict";

    // load cards

    // study cards
    //

    function Card(question, answer) {
        this.question = question;
        this.answer = answer;
    }

    /* Displays the given card, and passes the resulting grade to the callback. */
    function showCard(card, callback) {
        $("#question-content").html(card.question);
        $("#answer-content").html(card.answer);


        // set click listener on grade buttons
        // rehide answer, then call callback
    }

    $("#answer-content").hide();

    $("#answer-panel").click(function() {
        $("#answer-content").show();
        $("#answer-placeholder").hide();
    });

    showCard(new Card("Hello", "Bye"));



    // send requests to update database as we go


})(jQuery);
