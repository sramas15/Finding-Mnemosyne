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
        $("#grade-toolbar button").off('click.grade');
        $("#grade-toolbar button").on('click.grade', function() {
            callback(card, parseInt($(this).data("grade")));
        });
    }

    var aLotOfCardsThreshold = 50;

    function nextCard(cards, i) {
        if (i >= cards.length) {
            $("#no-cards-alert").show();
            return;
        }

        if (i > aLotOfCardsThreshold) {
            $("#a-lot-threshold").html(aLotOfCardsThreshold);
            $("#a-lot-alert").show();
            $("#keep-going-btn").off("click.keepGoing").on("click.keepGoing", function () {
                $("#a-lot-alert").hide();
                aLotOfCardsThreshold += 30;
                nextCard(cards, i);
            });
            return;
        }

        showCard(cards[i], function (card, grade) {
            // send requests to update database as we go
            $.get("/json/new_log/" + card.id + "/" + grade);
            // FIXME proper error checking?
            nextCard(cards, i + 1);
        });
    }

    // Start here
    $("#a-lot-alert").hide();
    $("#no-cards-alert").hide();
    $("#add-cards-btn").click(function() {
        $("#no-cards-alert").hide();
        $.getJSON("/json/get_study_queue/new", function(cards) {
            nextCard(cards, 0);
        });
    });
    $.getJSON("/json/get_study_queue", function(cards) {
        nextCard(cards, 0);
    });

})(jQuery);
