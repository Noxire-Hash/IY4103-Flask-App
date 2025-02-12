$(document).ready(function() {
  const form = $("#register-form");
  form.on("submit", function(e) {
    const password = $("#password").val();
    const password_confirm = $("#password_confirm").val();
    if (!check_password_matches(password, password_confirm)) {
      e.preventDefault();
      trigger_flash("Password`s do not match please try again", "danger")
    }
  });

  function check_password_matches(password, password_confirm) {
    return password === password_confirm;
  }
  function trigger_flash(message, category) {
    const flashMessage = `
    <div class="alert alert-${category} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`;
    $(".alert-container").append(flashMessage);
  }
  $("#get_userdata").click(function(){
    get_userdata()
  });
  function get_userdata(){
    return $.ajax({
        type: "POST",
        url: "get_user_data",
        success: function (response) {
            console.log(response)
            return response;
        },
        error: function(error){
            console.log(error)
            trigger_flash("Error getting user data", "danger")
        }
    });
  }
  function fill_user_data(){
    get_userdata().then(function(user_data) {
        $("#username").text(user_data.username);
        $("#email").text(user_data.email);
        $("#privilege").text(user_data.privilege_id);
    }).catch(function(error) {
        console.log(error);
    });
  }
function fill_vendor_data(){

}

  if (window.location.pathname == "/account"){
    fill_user_data();
  }

  if (window.location.pathname == "/vendor_dashboard"){
    fill_vendor_data();
  }




});


