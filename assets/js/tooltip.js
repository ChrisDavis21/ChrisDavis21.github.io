$(document).ready(function(){

    // set the image-map width and height to match the img size
    $('#image-map').css({'width':$('#image-map img').width(),
                      'height':$('#image-map img').height()
    })
    
    //tooltip direction
    var tooltipDirection;
                 
    for (i=0; i<$(".pin").length; i++)
    {               
        // set tooltip direction type - up or down             
        if ($(".pin").eq(i).hasClass('pin-down')) {
            tooltipDirection = 'tooltip-down';
        }else if ($(".pin").eq(i).hasClass('pin-right')) {
            tooltipDirection = 'tooltip-right';
		}else if ($(".pin").eq(i).hasClass('pin-bright')) {
            tooltipDirection = 'tooltip-bright';
		}else if ($(".pin").eq(i).hasClass('pin-bdown')) {
            tooltipDirection = 'tooltip-bdown';
		}else if ($(".pin").eq(i).hasClass('pin-bup')) {
            tooltipDirection = 'tooltip-bup';
        }else {
            tooltipDirection = 'tooltip-up';
            }
    
        // append the tooltip
        $("#image-map").append("<div style='left:"+$(".pin").eq(i).data('xpos')+"px;top:"+$(".pin").eq(i).data('ypos')+"px' class='" + tooltipDirection +"'>\
                                            <div class='tooltip'>" + $(".pin").eq(i).html() + "</div>\
                                    </div>");
    }    
    
    // show/hide the tooltip
    $('.tooltip-up, .tooltip-down, .tooltip-right, .tooltip-bup, .tooltip-bdown, .tooltip-bright').mouseenter(function(){
                $(this).children('.tooltip').fadeIn(100);
            }).mouseleave(function(){
                $(this).children('.tooltip').fadeOut(100);
            })
});