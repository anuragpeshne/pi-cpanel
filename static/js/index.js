'use strict';
const TEMP_REFRESH_INTERVAL = 30 * 1000;

$(document).ready(function() {
    var cmdSubmitBtn = $("#cmdSubmit");
    var cmdOption    = $("#cmdOption");

    cmdSubmitBtn.click(function(event) {
        event.preventDefault();
        $.ajax({
            url: "/cmd",
            method: 'GET',
            data: {'command' : $('#cmdOption').val()},
            context: document.body
        }).done(function(data) {
            $('#result').html(data);
        }).fail(function(err) {
            $('#result').html(err);
        });
    });

    function update_temp() {
        $.ajax({
            url: "/temp",
            method: 'GET',
            context: document.body
        }).done(function(data) {
            $('#temp').html(data);
        });
    }
    update_temp(); // set it once and let it update periodically
    window.setInterval(update_temp, TEMP_REFRESH_INTERVAL);
});
