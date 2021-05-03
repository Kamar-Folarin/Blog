
function readURL(input) {
    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }
}

var reader = new FileReader();
reader.onload = function (e) {
    $('.update-image img').attr('src', e.target.result);
}
   
    
$("#id_image").change(function(){
    readURL(this);
    $(".update-image").fadeIn();
});

$(function() {
	$("#image-clear_id").click(function(){
		if($("#image-clear_id:checkbox:checked").length){
			$(".update-image").fadeOut();
		}

		else{
			$(".update-image").fadeIn();	
		}
	});
});

$(window).scroll(function(){
	if ($(document).scrollTop()>$(window).height()) {
		$('#goToTop').css('opacity','1');
	}

	else{
		$('#goToTop').css('opacity','0');	
	}
});

$(function() {
	$('#goToTop').click(function(){
		 $("HTML, BODY").animate({ scrollTop: 0 }, 1000); 
	});
});


$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(function(){
	if ($(document).scrollTop()>$(window).height()) {
		$('#goToTop').css('opacity','1');
	}
});


/*Interactivity to determine when an animated element in in view. In view elements trigger our animation*/
$(function() {

  //window and animation items
  var animation_elements = $.find('.animation-element');
  var web_window = $(window);

  //check to see if any animation containers are currently in view
  function check_if_in_view() {
    //get current window information
    var window_height = web_window.height();
    var window_top_position = web_window.scrollTop();
    var window_bottom_position = (window_top_position + window_height);

    //iterate through elements to see if its in view
    $.each(animation_elements, function() {

      //get the element sinformation
      var element = $(this);
      var element_height = $(element).outerHeight();
      var element_top_position = $(element).offset().top;
      var element_bottom_position = (element_top_position + element_height);

      //check to see if this current container is visible (its viewable if it exists between the viewable space of the viewport)
      if ((element_bottom_position >= window_top_position) && (element_top_position <= window_bottom_position)) {
        element.addClass('fly-in');
      }
    });

  }

  //on or scroll, detect elements in view
  $(window).on('scroll resize', function() {
      check_if_in_view()
    })
    //trigger our scroll event on initial load
  $(window).trigger('scroll');

});


// Slugify a string
function slugify(str)
{
    str = str.replace(/^\s+|\s+$/g, '');

    // Make the string lowercase
    str = str.toLowerCase();

    // Remove accents, swap ñ for n, etc
    var from = "ÁÄÂÀÃÅČÇĆĎÉĚËÈÊẼĔȆÍÌÎÏŇÑÓÖÒÔÕØŘŔŠŤÚŮÜÙÛÝŸŽáäâàãåčçćďéěëèêẽĕȇíìîïňñóöòôõøðřŕšťúůüùûýÿžþÞĐđßÆa·/_,:;";
    var to   = "AAAAAACCCDEEEEEEEEIIIINNOOOOOORRSTUUUUUYYZaaaaaacccdeeeeeeeeiiiinnooooooorrstuuuuuyyzbBDdBAa------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    // Remove invalid chars
    str = str.replace(/[^a-z0-9 -]/g, '') 
    // Collapse whitespace and replace by -
    .replace(/\s+/g, '-') 
    // Collapse dashes
    .replace(/-+/g, '-'); 

    return str;
}

$(function(){ // slug creater
  $("#id_title").bind('keyup change',function(){
  let slug = slugify($("#id_title").val());
  $("#id_slug").val(slug); 
  });
});


$(function(){ // comment reply
    $(".reply").click(function(){
      id = $(this).parent().siblings(".reply-container").attr('parent-id');
      form = $("#commentForm").html();
      $(".reply-container").text("");
      $(this).parent().siblings(".reply-container").html(form);
      $(".reply-container #id_comment_body").focus();
      $(".reply-container #id_parent").val(id);
    });
});