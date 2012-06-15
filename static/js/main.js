$(document).ready(function() {
    $('#progress-lmuy').hide();
    $('#stats_show').click(function() {
        $('#progress-lmuy').slideToggle('slow', function() {
            // Animation complete.
        });
    });
});

