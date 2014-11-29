(function ($) {
    "use strict";

    // load cards

    // study cards
    //

    var i = 0;
    function nextCard() {
        console.log(i);
        console.log($.cards[i]);
        showCard($.cards[i], function () {
            i++;
            nextCard();
        });
    }

    nextCard();



    /* Displays the given card, and passes the resulting grade to the callback. */
    function showCard(card, callback) {
        $("#question-content").html(card.question.replace(/\n/g, "<br/>"));
        $("#answer-content").html(card.answer.replace(/\n/g, "<br/>"));

        // Set up answer toggle
        $("#answer-placeholder").show();
        $("#answer-content").hide();
        $("#answer-panel").click(function() {
            $("#answer-content").show();
            $("#answer-placeholder").hide();
            $(this).off();
        });

        // set click listener on grade buttons
        $("#grade-toolbar button").off('click.grade');
        $("#grade-toolbar button").on('click.grade', function() {
            callback(parseInt($(this).data("grade")));
        });
    }

    // send requests to update database as we go


})(jQuery);
