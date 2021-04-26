
$("#emailAdvis").click(function() {
  $("#myModalEmail").modal();
});

$("#save_drafts").click(function() {
    var form_data = $("#email_form").serializeArray();
    var myJSON = JSON.stringify({draft: [form_data]});
    $.ajax({
          type: 'POST',
          url: 'http://localhost:5000/email',
          // Always include an `X-Requested-With` header in every AJAX request,
          // to protect against CSRF attacks.
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          contentType: 'application/octet-stream; charset=utf-8',
          success: function(result) {
            $("#myModalDrafts").modal();
          },
          processData: false,
          data: myJSON
        });
});

$("#send_email").click(function() {
    var form_data = $("#email_form").serializeArray();
    var myJSON = JSON.stringify({send: [form_data]});
    $.ajax({
          type: 'POST',
          url: 'http://localhost:5000/email',
          // Always include an `X-Requested-With` header in every AJAX request,
          // to protect against CSRF attacks.
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          contentType: 'application/octet-stream; charset=utf-8',
          success: function(result) {
            $("#myModalSent").modal();
          },
          processData: false,
          data: myJSON
        });
});