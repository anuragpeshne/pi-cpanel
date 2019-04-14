'use strict';
const TEMP_REFRESH_INTERVAL = 30 * 1000;
const REQ_TIMEOUT           = 15 * 1000;

$(document).ready(function() {
    var cmdSubmitBtn = $("#cmdSubmit");
    var cmdOption    = $("#cmdOption");

    var playBtn      = $("#playBtn");
    var playLink     = $("#playLink");
    var pauseBtn     = $('#play-pause');

    pauseBtn.click(function(event) {
      event.preventDefault();
      $.ajax({
        url: "/control",
        method: "POST",
        data: {'command': "pause"},
        timeout: REQ_TIMEOUT,
        beforeSend: function() {
          pauseBtn.addClass('loading');
        }
      }).always(function() {
        pauseBtn.removeClass('loading');
      });
    });

    cmdSubmitBtn.click(function(event) {
        event.preventDefault();
        $.ajax({
            url: "/cmd",
            method: 'GET',
            data: {'command' : $('#cmdOption').val()},
            context: document.body,
            timeout: REQ_TIMEOUT,
            beforeSend: function() {
              cmdSubmitBtn.addClass('loading');
            }
        }).done(function(data) {
            $('#result').html(data);
        }).fail(function(err) {
            $('#result').html(err);
        }).always(function() {
          cmdSubmitBtn.removeClass('loading');
        });
    });

    playBtn.click(function(event) {
      event.preventDefault();
      $.ajax({
        url: "/play_link",
        method: 'POST',
        data: {'link' : $('#playLink').val()},
        context: document.body,
        timeout: REQ_TIMEOUT,
        beforeSend: function() {
          playBtn.addClass('loading');
        }
      }).done(function(data) {
        $('#result').html(data);
      }).fail(function(err) {
        $('#result').html(err);
      }).always(function() {
        playBtn.removeClass('loading');
      });
    });

    function update_temp() {
        $.ajax({
            url: "/temp",
            method: 'GET',
            context: document.body,
            timeout: 5000,
        }).done(function(data) {
            $('#temp').html(data);
        });
    }

    function update_temp_sensor() {
        $.ajax({
            url: "/temp_sensor",
            method: 'GET',
            context: document.body,
            timeout: 5000,
        }).done(function(data) {
            $('#tempSensor').html(data);
        });
    }
    update_temp(); // set it once and let it update periodically
    update_temp_sensor();
    window.setInterval(update_temp, TEMP_REFRESH_INTERVAL);
});
