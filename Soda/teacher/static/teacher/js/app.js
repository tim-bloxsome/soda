$(document).foundation()


/* Active Navbar button */
$(function(){
  
    $('.nav-link').each(function(){
      // console.log(window.location.href)
        if ($(this).prop('href') == window.location.href) {
            $(this).addClass('active'); $(this).parents('li').addClass('active');
        } else if ($(this).prop('id').includes("exams") && window.location.href.includes("exams")) {
          $(this).addClass('active'); $(this).parents('li').addClass('active');
        } else if ($(this).prop('id').includes("student") && window.location.href.includes("student")) {
          $(this).addClass('active'); $(this).parents('li').addClass('active');
        }
    });
});

// need this to avoid FOUC - Flash of unstyled content
// $('ul.hide-on-load').removeClass('hide-on-load');