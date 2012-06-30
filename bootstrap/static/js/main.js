$(document).ready(function() {
    $('#progress-lmuy').hide();
    $('#stats_show').click(function() {
        $('#progress-lmuy').slideToggle('slow', function() {
            if ($('#stats_show').text() != "Hide Results") {
                $('#stats_show').text('Hide Results').prepend('<i class="icon-hand-left"></i>');
            }
            else {
                $('#stats_show').text('Show Results').prepend('<i class="icon-hand-right"></i>');
            }
        });
    });

    $('#rockon').click(function() {
        $.ajax({
            type: "GET",
            url: "poll/?value=up",
        }).done(function( msg ) {
        if (msg != undefined) {
            if (msg['result'] == 'up') {
                if ($('#progress-lmuy p').html().search('No votes here so far') >= 0) {
                    $('#no_votes').slideUp().hide();
                    $('#pgbar').slideDown();
                }       
                curr_val = parseInt($('.badge_up').html()) + 1; 
                $('.badge_up').html(curr_val);
                var $bar = $('.bar')
                var ups = parseInt($('.badge_up').html())
                var downs = parseInt($('.badge_down').html())
                var perc = ups/(ups + downs)*100
                var perc_d = downs/(ups + downs)*100
                $bar.width(perc+"%");
                $('#ups').html("UpGrades: "+parseInt(perc)+"%");
                $('#downs').html("DownGrades: "+parseInt(perc_d)+"%"); 
            }
            else {
                $('.alert-info').remove();
                $('#branding').after('<div class="alert alert-info front_alert" data-alert="alert" style="display:none;"> <a class="close" href="#" onclick="$(this).parent().fadeOut(\'fast\'); return false;">×</a>'+msg['result']+' </div>');
                $('.alert-info').fadeIn();
            }
        }
        });
    });
    $('#rockoff').click(function() {
        $.ajax({
            type: "GET",
            url: "poll/?value=down",
        }).done(function( msg ) {
        if (msg != undefined) {
            if (msg['result'] == 'down') {
                if ($('#progress-lmuy p').html().search('No votes here so far') >= 0) {
                    $('#no_votes').slideUp().hide();
                    $('#pgbar').slideDown();
                } 
                curr_val = parseInt($('.badge_down').html()) + 1; 
                $('.badge_down').html(curr_val);
                var $bar = $('.bar')
                var ups = parseInt($('.badge_up').html())
                var downs = parseInt($('.badge_down').html())
                var perc = ups/(ups + downs)*100
                var perc_d = downs/(ups + downs)*100
                $bar.width(perc+"%");
                $('#downs').html("DownGrades: "+parseInt(perc_d)+"%"); 
                $('#ups').html("UpGrades: "+parseInt(perc)+"%");
                }   
            else {
                $('.alert-info').remove();
                $('#branding').after('<div class="alert alert-info front_alert" data-alert="alert" style="display:none;"> <a class="close" href="#" onclick="$(this).parent().fadeOut(\'fast\'); return false;">×</a>'+msg['result']+' </div>');
                $('.alert-info').fadeIn();
            }
        }
        });   
    });

});

