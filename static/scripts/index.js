$(document).ready(function() {
  const form = $("#register-form");
  form.on("submit", function(e) {
    const password = $("#password").val();
    const passwordConfirm = $("#password_confirm").val();
    if (!check_password_matches(password, passwordConfirm)) {
      e.preventDefault();
      trigger_flash("Password`s do not match please try again", "danger")
    }
  });

  function check_password_matches(password, passwordConfirm) {
    return password === passwordConfirm;
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
    getUserdata()
  });
  function getUserdata(){
    return $.ajax({
        type: "POST",
        url: "get_user_data",
        success: function (response) {
            return response;
        },
        error: function(error){
            console.log(error)
            trigger_flash("Error getting user data", "danger")
        }
    });
  }
  function fillUserData(){
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


  function getUserdata() {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "POST",
        url: "get_user_data",
        dataType: 'json',
        success: function(response) {
          console.log("Raw server response:", response);
          resolve(response);
        },
        error: function(error) {
          console.error("AJAX error:", error);
          trigger_flash("Error getting user data", "danger");
          reject(error);
        }
      });
    });
  }

  if (window.location.pathname == "/account") {
    getUserdata()
      .then(function(userData) {
        console.log("Full userData object:", userData);

        // Handle potential string response
        if (typeof userData === 'string') {
          try {
            userData = JSON.parse(userData);
          } catch (e) {
            console.error("Failed to parse userData:", e);
            return;
          }
        }

        const privId = userData.privilege_id;
        console.log("Extracted privId:", privId);

        if (privId !== undefined) {
          // Convert to number if it's a string
          const privIdNum = Number(privId);

          switch(privIdNum) {
            case 999:
              $("#admin-link").removeClass("d-none");
              $("#vendor-link").removeClass("d-none");
              break;
            case 998:
              $("#moderator-link").removeClass("d-none");
              $("#vendor-link").removeClass("d-none");
              break;
            case 2:
              $("#vendor-link").removeClass("d-none");
              break;
          }
        } else {
          console.error("No user_id found in response:", userData);
          trigger_flash("Error: Could not determine user privileges", "danger");
        }
      })
      .catch(function(error) {
        console.error("Error in user data processing:", error);
        trigger_flash("Error loading user privileges", "danger");
      });
  }


  if (window.location.pathname == "/vendor_dashboard"){
    fill_vendor_data();
  }

  if (window.location.pathname == "/store"){
    fillStoreItems();
  }



  function getStoreItem(){
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "GET",
        url: "get_items",
        dataType: 'json',
        success: function(response) {
          console.log("Raw server response:", response);
          resolve(response);
        },
        error: function(error) {
          console.error("AJAX error:", error);
          trigger_flash("Error getting user data", "danger");
          reject(error);
        }
      });
    });
  }


function fillStoreItems() {
    console.log("Starting fillStoreItems function");

    getStoreItem()
        .then(function(items) {
            console.log("Raw items data:", items);

            const itemKeys = Object.keys(items);
            const numItemsToShow = Math.min(3, itemKeys.length);

            for(let i = 0; i < numItemsToShow; i++) {
                const item = items[itemKeys[i]];
                console.log(`Filling item ${i}:`, item);

                // Format price in GBP
                const formattedPrice = new Intl.NumberFormat('en-GB', {
                    style: 'currency',
                    currency: 'GBP'
                }).format(item.price);

                const name = $(`#featured-item-name-${i}`);
                name.text(item.name).removeClass('shimmer');

                const price = $(`#featured-item-price-${i}`);
                price.text(formattedPrice).removeClass('shimmer');

                const desc = $(`#featured-item-description-${i}`);
                desc.text(item.description).removeClass('shimmer');

                const vendor = $(`#featured-item-vendor-name-${i}`);
                vendor.text(item.vendor_name).removeClass('shimmer');

                // Set up the button and remove its shimmer
                const buttonEl = $(`#featured-item-btn-${i}`);
                buttonEl.attr('href', `/store/item/${itemKeys[i]}`).removeClass('shimmer');
            }
        })
        .catch(function(error) {
            console.error("Error in fillStoreItems:", error);
            trigger_flash("Error loading store items", "danger");
        });
}


  function calculate_rating(item_id){
    get_reviews(item_id).then(function(reviews) {
      var total_rating = 0;
      for (var review in reviews){
        total_rating += review.rating;
      }
      var average_rating = total_rating / reviews.length;
      return average_rating;
    }).catch(function(error) {
        console.log(error);
    });


  }




});


