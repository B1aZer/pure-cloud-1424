$(document).ready(function() {
    $('#progress-lmuy').hide();
    $('#stats_show').click(function() {
        $('#progress-lmuy').slideToggle('slow', function() {
            if ($('#stats_show').text() != "Hide Results") {
                $('#stats_show').text('Hide Results').prepend('<i class="icon-hand-up"></i>');
            }
            else {
                $('#stats_show').text('Show Results').prepend('<i class="icon-hand-down"></i>');
            }
        });
    });
});

