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

        // Set up answer toggle
        $("#answer-content").hide();
        $("#answer-panel").click(function() {
            $("#answer-content").show();
            $("#answer-placeholder").hide();
            $(this).off();
        });

        // set click listener on grade buttons
        $("#grade-toolbar button").click(function() {
            callback(parseInt($(this).data("grade")));
            $("#grade-toolbar button").off();
        });
    }

    showCard(new Card("Hello", "Bye"), function(grade) {
        console.log(grade);
    });

    // send requests to update database as we go


})(jQuery);
