$(document).ready(function() {
  console.log("✅ index.js is running on this page:", window.location.pathname);

  // Constants
  const PATHS = {
    ACCOUNT: "/account",
    STORE: "/store",
    VENDOR_DASHBOARD: "/vendor_dashboard",
    ITEM_PREVIEW: "/store/item",
    CHECKOUT_DEPOSIT: "/checkout/deposit"
  };

  // Event Listeners
  setupEventListeners();
  handlePageSpecificCode();

  // Functions
  function setupEventListeners() {
    // Register form validation
    const form = $("#register-form");
    form.on("submit", handleRegisterSubmit);

    // User data button
    $("#get_userdata").click(getUserData);
  }

  function handlePageSpecificCode() {
    const path = window.location.pathname;

    switch(path) {
      case PATHS.ACCOUNT:
        handleAccountPage();
        break;
      case PATHS.STORE:
        fillStoreItems();
        break;
      case PATHS.VENDOR_DASHBOARD:
        fillVendorData();
        break;
      case PATHS.CHECKOUT_DEPOSIT:
        handleCheckoutDeposit();
        break;
    }

    // Handle item preview pages
    if (path.includes(PATHS.ITEM_PREVIEW)) {
      const itemId = path.split('/').pop();
      handleItemPreview(itemId);
    }
  }

  // Form Handling
  function handleRegisterSubmit(e) {
    const password = $("#password").val();
    const passwordConfirm = $("#password_confirm").val();

    if (!checkPasswordMatches(password, passwordConfirm)) {
      e.preventDefault();
      triggerFlash("Passwords do not match, please try again", "danger");
    }
  }

  function checkPasswordMatches(password, passwordConfirm) {
    return password === passwordConfirm;
  }

  // UI Helpers
  function triggerFlash(message, category) {
    const flashMessage = `
      <div class="alert alert-${category} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
    $(".alert-container").append(flashMessage);
  }

  // API Calls
  function getUserData() {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "POST",
        url: "get_user_data",
        dataType: 'json',
        success: function(response) {
          console.log("User data received:", response);
          resolve(response);
        },
        error: function(error) {
          console.error("AJAX error:", error);
          triggerFlash("Error getting user data", "danger");
          reject(error);
        }
      });
    });
  }

  function getStoreItems() {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "GET",
        url: "get_items",
        dataType: 'json',
        success: function(response) {
          resolve(response);
        },
        error: function(error) {
          console.error("AJAX error:", error);
          triggerFlash("Error getting store items", "danger");
          reject(error);
        }
      });
    });
  }

  // Page Specific Functions
  function handleAccountPage() {
    getUserData()
      .then(function(userData) {
        if (typeof userData === 'string') {
          userData = JSON.parse(userData);
        }

        const privId = Number(userData.privilege_id);

        // Show/hide privilege-specific links
        switch(privId) {
          case 999: // Admin
            $("#admin-link, #vendor-link").removeClass("d-none");can 
            break;
          case 998: // Moderator
            $("#moderator-link, #vendor-link").removeClass("d-none");
            break;
          case 2: // Vendor
            $("#vendor-link").removeClass("d-none");
            break;
        }
       // Update user fields
        $("#username").text(userData.username);
        $("#email").text(userData.email);
        $("#privilege").text(userData.privilege_id);
        $("#sub-tier").text("Exclusive");
        $("#balance").text("1000");
        $("#pending-balance").text("0");

      })
      .catch(function(error) {
        console.error("Error processing user data:", error);
        triggerFlash("Error loading user privileges", "danger");
      });
  }

  function fillStoreItems() {
    getStoreItems()
      .then(function(items) {
        const itemKeys = Object.keys(items);
        const numItemsToShow = Math.min(3, itemKeys.length);

        for(let i = 0; i < numItemsToShow; i++) {
          const item = items[itemKeys[i]];
          updateFeaturedItem(i, item, itemKeys[i]);
        }
      })
      .catch(function(error) {
        console.error("Error filling store items:", error);
        triggerFlash("Error loading store items", "danger");
      });
  }

  function updateFeaturedItem(index, item, itemId) {
    // Update featured items with new currency format
    $(`#featured-item-name-${index}`).text(item.name).removeClass('shimmer');
    $(`#featured-item-price-${index}`).html(formatCurrency(item.price)).removeClass('shimmer');
    $(`#featured-item-description-${index}`).text(item.description).removeClass('shimmer');
    $(`#featured-item-vendor-name-${index}`).text(item.vendor_name).removeClass('shimmer');
    $(`#featured-item-btn-${index}`)
        .attr('href', `/store/item/${itemId}`)
        .removeClass('shimmer');
  }

  function handleItemPreview(itemId) {
    $.ajax({
        type: "GET",
        url: `/get_item_data_from_id/${itemId}`,
        success: function(response) {
            console.log("🎯 Item data received:", response);
            updateItemPreview(response);
        },
        error: function(error) {
            console.error("❌ Error loading item data:", error);
            triggerFlash("Error loading item details", "danger");
        }
    });
  }

  function formatCurrency(amount) {
    // Format with 2 decimal places and add AW with glow effect
    return `<span class="price-amount">${Number(amount).toFixed(2)}</span> <span class="currency-aw">AW</span>`;
  }

  function updateItemPreview(itemData) {
    try {
        $('.item-title').text(itemData.name).removeClass('shimmer');
        $('.vendor-name').text(itemData.vendor_name).removeClass('shimmer');
        $('.item-price').html(formatCurrency(itemData.price)).removeClass('shimmer');
        $('.sales-count').text(`${itemData.sales} sales`).removeClass('shimmer');
        $('.item-description').text(itemData.description).removeClass('shimmer');

        // Update tags if they exist
        if (itemData.tags) {
            const tags = itemData.tags.split(',');
            const tagsHtml = tags.map(tag =>
                `<span class="badge bg-secondary me-1">${tag.trim()}</span>`
            ).join('');
            $('.item-tags').html(tagsHtml).removeClass('shimmer');
        }

        $('.purchase-btn').removeClass('shimmer');
    } catch (error) {
        triggerFlash("Error updating item details", "danger");
    }
  }

  function fillVendorData() {
    // Add vendor dashboard specific code here
    console.log("Vendor dashboard loaded");
  }

  function handleCheckoutDeposit() {
    const awInput = $("#aw-amount");
    const poundsInput = $("#pounds-amount");
    const summaryAmount = $("#summary-amount");
    const summaryPrice = $("#summary-price");

    function updatePounds() {
      const awValue = parseInt(awInput.val()) || 0;
      const poundsValue = awValue / 10;
      poundsInput.val(poundsValue.toFixed(2));
      summaryAmount.text(awValue + " AW");
      summaryPrice.text("£" + poundsValue.toFixed(2));
      if(awValue <= 10){
        awInput.val(10);
        updatePounds();
      }
    }
    updatePounds();
    awInput.on("input", updatePounds);
    console.log("Checkout deposit loaded");
  }
});


