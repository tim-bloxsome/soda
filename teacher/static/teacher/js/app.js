$(document).foundation()


/* Active Navbar button */
$(function(){
  
    $('.nav-link').each(function(){
        if ($(this).prop('href') == window.location.href) {
            $(this).addClass('active'); $(this).parents('li').addClass('active');
        } else if ($(this).prop('id').includes("exams") && window.location.href.includes("exams")) {
          $(this).addClass('active'); $(this).parents('li').addClass('active');
        } else if ($(this).prop('id').includes("student") && window.location.href.includes("student")) {
          $(this).addClass('active'); $(this).parents('li').addClass('active');
        }
    });
});
