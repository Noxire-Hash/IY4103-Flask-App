$(document).ready(function () {
  console.log("✅ index.js is running on this page:", window.location.pathname);

  // Constants
  const PATHS = {
    ACCOUNT: "/account",
    STORE: "/store",
    VENDOR_DASHBOARD: "/vendor_dashboard",
    ITEM_PREVIEW: "/store/item",
    CHECKOUT_DEPOSIT: "/checkout/deposit",
    ADMIN_DASHBOARD: "/admin",
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

    switch (path) {
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
      case PATHS.ADMIN_DASHBOARD:
        handleAdminDashboard();
        break;
    }

    // Handle item preview pages
    if (path.includes(PATHS.ITEM_PREVIEW)) {
      const itemId = path.split("/").pop();
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
        dataType: "json",
        success: function (response) {
          console.log("User data received:", response);
          resolve(response);
        },
        error: function (error) {
          console.error("AJAX error:", error);
          triggerFlash("Error getting user data", "danger");
          reject(error);
        },
      });
    });
  }

  function getStoreItems() {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "GET",
        url: "get_items",
        dataType: "json",
        success: function (response) {
          resolve(response);
        },
        error: function (error) {
          console.error("AJAX error:", error);
          triggerFlash("Error getting store items", "danger");
          reject(error);
        },
      });
    });
  }

  // Page Specific Functions
  function handleAccountPage() {
    getUserData()
      .then(function (userData) {
        if (typeof userData === "string") {
          userData = JSON.parse(userData);
        }

        const privId = Number(userData.privilege_id);

        // Show/hide privilege-specific links
        switch (privId) {
          case 999: // Admin
            $("#admin-link, #vendor-link").removeClass("d-none");
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
        $("#balance").text(userData.balance);
        $("#pending-balance").text(userData.pending_balance);
      })
      .catch(function (error) {
        console.error("Error processing user data:", error);
        triggerFlash("Error loading user privileges", "danger");
      });
  }

  function fillStoreItems() {
    getStoreItems()
      .then(function (items) {
        const itemKeys = Object.keys(items);
        const numItemsToShow = Math.min(3, itemKeys.length);

        for (let i = 0; i < numItemsToShow; i++) {
          const item = items[itemKeys[i]];
          updateFeaturedItem(i, item, itemKeys[i]);
        }
      })
      .catch(function (error) {
        console.error("Error filling store items:", error);
        triggerFlash("Error loading store items", "danger");
      });
  }

  function updateFeaturedItem(index, item, itemId) {
    // Update featured items with new currency format
    $(`#featured-item-name-${index}`).text(item.name).removeClass("shimmer");
    $(`#featured-item-price-${index}`)
      .html(formatCurrency(item.price))
      .removeClass("shimmer");
    $(`#featured-item-description-${index}`)
      .text(item.description)
      .removeClass("shimmer");
    $(`#featured-item-vendor-name-${index}`)
      .text(item.vendor_name)
      .removeClass("shimmer");
    $(`#featured-item-btn-${index}`)
      .attr("href", `/store/item/${itemId}`)
      .removeClass("shimmer");
  }

  function handleItemPreview(itemId) {
    $.ajax({
      type: "GET",
      url: `/get_item_data_from_id/${itemId}`,
      success: function (response) {
        console.log("🎯 Item data received:", response);
        updateItemPreview(response);
      },
      error: function (error) {
        console.error("❌ Error loading item data:", error);
        triggerFlash("Error loading item details", "danger");
      },
    });
  }

  function formatCurrency(amount) {
    // Format with 2 decimal places and add AW with glow effect
    return `<span class="price-amount">${Number(amount).toFixed(2)}</span> <span class="currency-aw">AW</span>`;
  }

  function updateItemPreview(itemData) {
    try {
      $(".item-title").text(itemData.name).removeClass("shimmer");
      $(".vendor-name").text(itemData.vendor_name).removeClass("shimmer");
      $(".item-price")
        .html(formatCurrency(itemData.price))
        .removeClass("shimmer");
      $(".sales-count").text(`${itemData.sales} sales`).removeClass("shimmer");
      $(".item-description").text(itemData.description).removeClass("shimmer");

      // Update tags if they exist
      if (itemData.tags) {
        const tags = itemData.tags.split(",");
        const tagsHtml = tags
          .map(
            (tag) =>
              `<span class="badge bg-secondary me-1">${tag.trim()}</span>`,
          )
          .join("");
        $(".item-tags").html(tagsHtml).removeClass("shimmer");
      }

      $(".purchase-btn").removeClass("shimmer");
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
    const lessThan10 = $("#less-than-10");
    const btnPayment = $("#btn-payment");

    function updatePounds() {
      const awValue = parseInt(awInput.val()) || 0;
      const poundsValue = awValue / 10;
      poundsInput.val(poundsValue.toFixed(2));
      summaryAmount.text(awValue + " AW");
      summaryPrice.text("£" + poundsValue.toFixed(2));
      if (awValue < 10) {
        lessThan10.removeClass("d-none");
      } else {
        lessThan10.addClass("d-none");
      }
    }
    btnPayment.on("click", function () {
      const paymentRequest = {
        provider_id: this.id,
        user_id: userObj.id,
        amountPound: summaryPrice,
      };
      console.log(paymentRequest);
    });

    updatePounds();
    awInput.on("input", updatePounds);
    console.log("Checkout deposit loaded");
  }

  // Admin Dashboard Functions
  function handleAdminDashboard() {
    // Handle sender type changes in transaction form
    $("#sender_type").on("change", function () {
      const senderUserDiv = $("#senderUserDiv");
      const paymentProviderDiv = $("#paymentProviderDiv");
      const systemDiv = $("#systemDiv");
      if ($(this).val() === "payment_provider") {
        senderUserDiv.hide();
        systemDiv.hide();
        paymentProviderDiv.show();
      } else if ($(this).val() === "system") {
        senderUserDiv.hide();
        paymentProviderDiv.hide();
        systemDiv.show();
      } else {
        systremDiv.hide();
        paymentProviderDiv.hide();
        senderUserDiv.show();
      }
    });

    // Handle privilege changes
    $(".privilege-select").on("change", function () {
      const userId = $(this).data("userId");
      const privilegeId = $(this).val();
      const select = $(this);

      $.ajax({
        url: "/admin/update_user/" + userId,
        method: "POST",
        data: { privilege_id: privilegeId },
        success: function (data) {
          if (data.success) {
            triggerFlash("Privilege updated successfully", "success");
          } else {
            triggerFlash("Error updating privilege", "danger");
            select.val(select.data("originalValue"));
          }
        },
        error: function (error) {
          console.error("Error updating privilege:", error);
          triggerFlash("Error updating privilege", "danger");
          select.val(select.data("originalValue"));
        },
      });
    });

    // Handle edit user button clicks
    $(".edit-user").on("click", function () {
      const userId = $(this).data("userId");
      let otp = "";
      $(".resetPassword").on("click", function () {
        console.log("Reset password clicked");
        otp = Math.random().toString(36).substr(2, 8);
      });

      $.ajax({
        url: "/admin/get_user/" + userId,
        method: "GET",
        success: function (data) {
          $("#edit_user_id").val(data.id);
          $("#edit_username").val(data.username);
          $("#edit_email").val(data.email);
          $("#edit_balance").val(data.balance);
          $("#edit_password").val(otp);
        },
        error: function (error) {
          console.error("Error fetching user data:", error);
          triggerFlash("Error loading user data", "danger");
        },
      });
    });

    // Initialize tooltips if they exist
    $('[data-bs-toggle="tooltip"]').tooltip();

    console.log("Admin dashboard initialized");
  }
});
