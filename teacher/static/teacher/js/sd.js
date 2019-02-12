$('form[class=sd-form]').on('submit', function(e) {
  e.preventDefault();
  submit_button = $(this).find("input[type=submit]");
  saved = $(this).find('#saved')
  
  $.ajax({
    type: 'POST',
    url: $(this).attr("action"),
    data: {
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), 
      student: $(this).find('#student-id').val(),
      stu_num: $(this).find('#stu_num').val(),
      last_name: $(this).find('#last_name').val(),
      first_name: $(this).find('#first_name').val(),
      // dob: $(this).find('#dob').val(),
      campus: $(this).find('#campus').val(),
      course: $(this).find('#course').val(),
      teacher: $(this).find('#teacher').val(),
      country: $(this).find('#country').val(),
      homework: String($(this).find('#homework').val() * 1),
      attendance: String($(this).find('#attendance').val() * 1),
      attitude: String($(this).find('#attitude').val() * 1),
      comments: $(this).find('#comments').val(),
      previous: $(this).find('#previous').val()

    },
    success: function () {

    // Snackbar
    // var x = document.getElementById("snackbar");
    // x.className = "show";
    // setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

    saved.addClass("show");
    setTimeout(function(){ $('.show').addClass('').removeClass('show'); }, 3000);

    $(submit_button).prop("disabled", true);

    }
  });
});
  
//   Make the save button active after any input
$('form[class=sd-form]').on('input', function() {
  var submit_button = $(this).find("input[type=submit]");
  $(submit_button).prop("disabled", false);

});