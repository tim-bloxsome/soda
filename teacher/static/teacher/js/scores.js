/* Exam total score triggered on page ready and input */
$('form[name=scores]').each(calculateTotal) 
$('form[name=scores]').on('input', calculateTotal);

function calculateTotal() {

  reading = parseFloat($(this).find('#score-re').val() / 36);
  if (isNaN(reading)) {
    reading = 0;
  } 
  uofe = parseFloat($(this).find('#score-us').val() / 36);
  if (isNaN(uofe)) {
    uofe = 0;
  } 
  writing = parseFloat($(this).find('#score-wr').val() / 5);
  if (isNaN(writing)) {
    writing = 0;
  } 
  listening = parseFloat($(this).find('#score-li').val() / 30);
  if (isNaN(listening)) {
    listening = 0;
  } 
  speaking = parseFloat($(this).find('#score-sp').val() / 5);
  if (isNaN(speaking)) {
    speaking = 0;
  } 

  var testScoreSum = reading + uofe + writing + listening + speaking;

  examTotal = ((testScoreSum / 5) * 100  ).toFixed(0)  + "%";

  $(this).find('#exam-total').html(examTotal);
}


/* Ajax for exam scores*/
$('form[name=scores]').on('submit', function(e) {
  e.preventDefault();
  saved = $(this).find('#saved')
  submit_button = $(this).find("input[type=submit]");
  console.log($(this).attr("action"))
  $.ajax({
    type: 'POST',
    url: $(this).attr("action"),
    data: {
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), 
      exam_name: $(this).find('#exam_name').val(),
      reading: String($(this).find('#score-re').val() * 1),
      uofe: String($(this).find('#score-us').val() * 1),
      writing: String($(this).find('#score-wr').val( ) * 1),
      listening: String($(this).find('#score-li').val() * 1),
      speaking: String($(this).find('#score-sp').val() * 1),
      student: String($(this).find('#student-id').val() * 1)
    },
    success: function () {

      // Snackbar
      // var x = document.getElementById("snackbar");
      // x.className = "show";
      // setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

      // var x = document.getElementById("saved");
      saved.addClass("show");
      setTimeout(function(){ $('.show').addClass('').removeClass('show'); }, 3000);
      // setTimeout(function(){ saved.className = saved.className.replace("show", ""); }, 3000);

      $(submit_button).prop("disabled", true);

      // Use the variable created above to use $(this) outside scope
      // $(this_form).addClass("show");
    }
  });
});

$('form[name=scores]').on('input', function() {
  var submit_button = $(this).find("input[type=submit]");
  $(submit_button).prop("disabled", false);
});


/* Calculate percentage of each test score */
$("input[class='score']").each(calculatePerc);
$("input[class='score']").on("input", calculatePerc);

function calculatePerc() {

  var total    = "";
  if ($(this).attr('id') == "score-re" || $(this).attr('id') == "score-us") {
    total = 36;
  } else if ($(this).attr('id') == "score-wr") {
    total = 5;
  } else if ($(this).attr('id') == "score-li") {
    total = 30;
  } else if ($(this).attr('id') == "score-sp") {
    total = 5;
  }

  var score    = parseFloat($(this).val());
  var calcPerc = "";
  if (isNaN(score)) {
    calcPerc=" ";
  } else {
  calcPerc = ((score / total) * 100).toFixed(0)  + "%";
  }
  $(this).closest('div').find('#percentage').html( calcPerc );

}