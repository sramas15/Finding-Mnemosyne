(function ($) {
    "use strict";

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
        $("#grade-toolbar button").on('click.grade', function() {
            $("#grade-toolbar button").off('click.grade');
            callback(card, parseInt($(this).data("grade")));
        });
    }


    /* Wrapper function */
    function study(cards) {
        nextCard(cards, 0, 50);
    }

    /* Start studying the ith card in cards, stopping at threshold */
    function nextCard(cards, i, threshold) {
        if (i >= cards.length) {
            $("#no-cards-alert").show();
            return;
        }

        if (i > threshold) {
            $("#a-lot-threshold").html(threshold);
            $("#a-lot-alert").show();
            $("#keep-going-btn").off("click.keepGoing").on("click.keepGoing", function () {
                $("#a-lot-alert").hide();
                nextCard(cards, i, threshold + 30);
            });
            return;
        }

        showCard(cards[i], function (card, grade) {
            // send log updates to database as we go
            $.get("/json/new_log/" + card.id + "/" + grade);
            // FIXME proper error checking?
            nextCard(cards, i + 1, threshold);
        });
    }

    // Start here
    $("#a-lot-alert").hide();
    $("#no-cards-alert").hide();
    $("#add-cards-btn").click(function() {
        $("#no-cards-alert").hide();
        $.getJSON("/json/get_study_queue/new", function(cards) {
            study(cards);
        });
    });
    $.getJSON("/json/get_study_queue", function(cards) {
        study(cards);
    });

})(jQuery);
