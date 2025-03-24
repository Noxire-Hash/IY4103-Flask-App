// 1. First define all utility functions
function formatCurrency(amount) {
    return `${Number(amount).toFixed(2)} AW`;
}

// 2. Define the updateFeaturedItem function
function updateFeaturedItem(item, index) {
    console.log('Updating featured item:', item);

    // Update item details
    $(`#featured-item-name-${index}`).text(item.name);
    $(`#featured-item-description-${index}`).text(
        item.description.length > 120
            ? item.description.substring(0, 120) + '...'
            : item.description
    );
    $(`#featured-item-vendor-name-${index}`).text(`By ${item.vendor_name}`);
    $(`#featured-item-price-${index}`).text(formatCurrency(item.price));

    // Update button with correct URL and click handler
    const button = $(`#featured-item-btn-${index}`);

    // Add debug log to check item data
    console.log(`Item ${index} data:`, {id: item.id, name: item.name});

    if (item && item.id) {
        const itemUrl = `/store/item/${item.id}`;
        button
            .removeClass('disabled btn-secondary')
            .addClass('btn-primary')
            .css({
                'opacity': '1',
                'cursor': 'pointer',
                'pointer-events': 'auto'
            })
            .attr('href', itemUrl)
            .off('click')
            .on('click', function(e) {
                e.preventDefault();
                window.location.href = itemUrl;
            });
    } else {
        console.warn(`Missing item ID for featured item ${index}`); // Add warning log
        button
            .attr('href', '#')
            .addClass('disabled btn-secondary')
            .removeClass('btn-primary')
            .css({
                'opacity': '0.65',
                'cursor': 'not-allowed',
                'pointer-events': 'none'
            });
    }
}

// 3. Define the loadFeaturedItems function
function loadFeaturedItems() {
    $.ajax({
        url: '/api/featured-items',
        type: 'GET',
        success: function(response) {
            if (response.items && response.items.length > 0) {
                for (let i = 0; i < Math.min(response.items.length, 3); i++) {
                    updateFeaturedItem(response.items[i], i);
                }
            } else {
                for (let i = 0; i < 3; i++) {
                    $(`#featured-item-name-${i}`).text('No featured items available');
                    $(`#featured-item-description-${i}`).text('Check back later for featured items!');
                    $(`#featured-item-vendor-name-${i}`).text('');
                    $(`#featured-item-price-${i}`).text('N/A');
                    $(`#featured-item-btn-${i}`).addClass('disabled').text('Not Available');
                }
            }
        },
        error: function(error) {
            console.error('Error loading featured items:', error);
            for (let i = 0; i < 3; i++) {
                $(`#featured-item-name-${i}`).text('Error loading items');
                $(`#featured-item-description-${i}`).text('Please try again later');
                $(`#featured-item-vendor-name-${i}`).text('');
                $(`#featured-item-price-${i}`).text('N/A');
                $(`#featured-item-btn-${i}`).addClass('disabled').text('Not Available');
            }
        }
    });
}

// Define loadUserAccount as a separate function
  function loadUserAccount() {
    $.ajax({
      url: "/user_account",
      type: "GET",
        success: function(response) {
        console.log("User account loaded:", response);
      },
        error: function(error) {
        console.error("Error loading user account:", error);
      },
    });
  }

// Add this function outside document ready

$(document).ready(function() {
  console.log("index.js is running on this page:", window.location.pathname);

  // Constants
  const PATHS = {
    ACCOUNT: "/account",
    STORE: "/store",
    VENDOR_DASHBOARD: "/vendor_dashboard",
    ITEM_PREVIEW: "/store/item",
    CHECKOUT_DEPOSIT: "/checkout/deposit",
    ADMIN_DASHBOARD: "/admin",
    USER_ACCOUNT: "/user",
        COMMUNITY: "/community",
        COMMUNITY_POST_CRAFTER: "/community/create_post"
  };

  // Event Listeners
  setupEventListeners();
  handlePageSpecificCode();

  // Functions
  function setupEventListeners() {
    // Register form validation
    const form = $("#register-form");
        if (form.length) {
    form.on("submit", handleRegisterSubmit);
        }

    // User data button
        const userDataBtn = $("#get_userdata");
        if (userDataBtn.length) {
            userDataBtn.click(getUserData);
        }
  }

  function handlePageSpecificCode() {
    const path = window.location.pathname;
        console.log("Path detected:", path);

        // Path-specific initializations
        if (path === PATHS.ACCOUNT) {
            handleMyAccountPage();
        }
        else if (path === PATHS.STORE) {
            console.log("Loading store page specific code");
            // Only load featured items on the store page
            loadFeaturedItems();
            loadAllItems();
        }
        else if (path === PATHS.VENDOR_DASHBOARD) {
        fillVendorData();
        }
        else if (path === PATHS.CHECKOUT_DEPOSIT) {
        handleCheckoutDeposit();
        }
        else if (path === PATHS.ADMIN_DASHBOARD) {
        handleAdminDashboard();
        }
        else if (path === PATHS.USER_ACCOUNT) {
            handleUserAccountPage();
        }
        else if (path === PATHS.COMMUNITY) {
            console.log("Loading community forums page");

            // Initialize forums page functionality with enhanced UI
            enhanceCommunityForumsPage();

        }
        else if (path === PATHS.COMMUNITY_POST_CRAFTER) {
            console.log("Loading community post crafter page from index.js");

            // Initialize post crafter with enhanced functionality
            handleCommunityPostCrafter();

            // Add transitions and animations to the post crafter page
            $('#postTitle, #postContent').on('focus', function() {
                $(this).parent().addClass('input-focused');
            }).on('blur', function() {
                $(this).parent().removeClass('input-focused');
            });

            // Smoother preview toggle
            $('#previewToggle').on('click', function() {
                const $editor = $('#editorSection');
                const $preview = $('#previewSection');

                if ($editor.is(':visible')) {
                    $editor.fadeOut(200, function() {
                        $preview.fadeIn(200);
                    });
                } else {
                    $preview.fadeOut(200, function() {
                        $editor.fadeIn(200);
                    });
                }
            });
        }

        // Check for specific elements on the page regardless of path
        if ($('#admin-dashboard').length) {
        handleAdminDashboard();
        }

        if ($('#featured-items-container').length) {
            console.log("Found featured items container, loading items");
            loadFeaturedItems();
            loadAllItems();
        }

        // Check if postCrafterForm exists on any page
        if ($('#postCrafterForm').length) {
            console.log("Found post crafter form, initializing");
            handleCommunityPostCrafter();
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
    function handleMyAccountPage() {
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
                $("#bio").text(userData.bio);
                $("#update-bio").click(function() {
                    console.log("Update bio clicked");
                    $.ajax({
                        url: "/api/account/update_bio",
                        type: "POST",
                        data: { bio: $("#bio").val() },
                        success: function(response) {
                            console.log("Bio updated successfully");
                            triggerFlash("Bio updated successfully", "success");
                        },
                        error: function(error) {
                            console.error("Error updating bio:", error);
                            triggerFlash("Error updating bio", "danger");
                        }
                    });
                });
            })

      .catch(function (error) {
        console.error("Error processing user data:", error);
        triggerFlash("Error loading user privileges", "danger");
      });
  }

  function fillStoreItems() {
    getStoreItems()
        .then(function(response) {
            console.log('Raw items response:', response); // Debug log

            if (response.items && response.items.length > 0) {
                const numItemsToShow = Math.min(3, response.items.length);
                for (let i = 0; i < numItemsToShow; i++) {
                    updateFeaturedItem(response.items[i], i);
                }
            } else {
                console.warn('No items returned from getStoreItems');
                // Handle empty state
                for (let i = 0; i < 3; i++) {
                    $(`#featured-item-name-${i}`).text('No items available');
                    $(`#featured-item-description-${i}`).text('Check back later!');
                    $(`#featured-item-vendor-name-${i}`).text('');
                    $(`#featured-item-price-${i}`).text('N/A');
                    $(`#featured-item-btn-${i}`)
                        .addClass('disabled')
                        .attr('href', '#')
                        .text('Not Available');
                }
            }
        })
        .catch(function(error) {
            console.error("Error filling store items:", error);
            triggerFlash("Error loading store items", "danger");
        });
  }

  function handleItemPreview(itemId) {
    $.ajax({
        type: "GET",
        url: `/get_item_data_from_id/${itemId}`,
      success: function (response) {
        console.log("Item data received:", response);
            updateItemPreview(response);
        },
      error: function (error) {
        console.error("Error loading item data:", error);
            triggerFlash("Error loading item details", "danger");
      },
    });
  }

  function createItemCard(item, itemId) {
    return `
      <div class="featured-card">
        <div class="featured-content">
          <h5 class="card-title">${item.name}</h5>
          <p class="card-text">${item.description.substring(0, 100)}${item.description.length > 100 ? '...' : ''}</p>
          <p class="card-text">By ${item.vendor_name}</p>
          <div class="d-flex justify-content-between align-items-center mt-3">
            <h6 class="fw-bold mb-0">${formatCurrency(item.price)}</h6>
            <a href="/store/item/${itemId}" class="btn btn-primary">View Details</a>
          </div>
        </div>
      </div>
    `;
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
        systemDiv.hide();
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

  function loadAllItems() {
    const itemsContainer = $('#itemsContainer');
    itemsContainer.empty();

    // Add loading placeholders
    for (let i = 0; i < 6; i++) {
      itemsContainer.append(`
        <div class="featured-card">
          <div class="featured-content">
            <div class="loading-placeholder title"></div>
            <div class="loading-placeholder description"></div>
            <div class="loading-placeholder price"></div>
          </div>
        </div>
      `);
    }

    $.ajax({
      url: '/api/items',
      type: 'GET',
      success: function(response) {
        itemsContainer.empty();

        if (!response.items || response.items.length === 0) {
          itemsContainer.html('<div class="col-12 text-center"><p>No items available at this time. Check back later!</p></div>');
          return;
        }

        response.items.forEach((item) => {
          const itemCard = createItemCard(item, item.id);
          itemsContainer.append(itemCard);
        });
      },
      error: function(error) {
        console.error('Error loading items:', error);
        itemsContainer.html('<div class="col-12 text-center"><p class="text-danger">Failed to load items. Please try again later.</p></div>');
      }
    });
  }

    // User Account Page handler
    function handleUserAccountPage() {
        console.log("Loading User Account Page specific code");

        // Simple code for the user account page
        const messageBtn = document.querySelector('.btn-outline-primary i.fa-envelope');
        if (messageBtn && messageBtn.parentElement) {
            messageBtn.parentElement.addEventListener('click', function(e) {
                e.preventDefault();
                alert('Message functionality would be implemented here');
            });
        }

        // Get admin action buttons if they exist
        if (document.getElementById('adminActionModal')) {
            const adminButtons = document.querySelectorAll('#adminActionModal .list-group-item');

            adminButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    const action = this.textContent.trim();
                    console.log('Admin action selected:', action);
                    alert(`Admin action: ${action} would be executed here`);
                });
            });
        }
    }

    function handleCommunityPostCrafter() {
        // Check if already initialized to prevent duplicate execution
        if (window.postCrafterInitialized) {
            console.log("Post crafter already initialized, skipping");
            return;
        }

        console.log("Initializing post crafter functionality");

        // Character counters
        const $titleInput = $('#postTitle');
        const $titleCounter = $('#titleCounter');
        const $contentInput = $('#postContent');
        const $contentCounter = $('#contentCounter');

        $titleInput.on('input', function() {
            $titleCounter.text($(this).val().length);
        });

        $contentInput.on('input', function() {
            $contentCounter.text($(this).val().length);
        });

        // Tag previewer
        const $tagsInput = $('#postTags');
        const $tagPreview = $('#tagPreview');

        $tagsInput.on('input', function() {
            const tags = $(this).val().split(',').filter(tag => tag.trim() !== '');
            $tagPreview.empty();

            tags.slice(0, 5).forEach(tag => {
                $('<span>')
                    .addClass('badge bg-primary me-2 mb-2')
                    .text(tag.trim())
                    .appendTo($tagPreview);
            });
        });

        // Preview toggle
        const $previewToggle = $('#previewToggle');
        const $previewArea = $('#previewArea');
        const $previewTitle = $('#previewTitle');
        const $previewTags = $('#previewTags');
        const $previewContent = $('#previewContent');

        // Remove any existing click handlers to prevent duplicates
        $previewToggle.off('click');

        $previewToggle.on('click', function(e) {
            // Prevent default behavior and stop propagation
            e.preventDefault();
            e.stopPropagation();

            console.log("Preview toggle clicked");

            // Toggle preview visibility
            if ($previewArea.hasClass('d-none')) {
                // Show preview
                $previewArea.removeClass('d-none');
                $(this).html('<i class="fas fa-edit me-2"></i>Continue Editing');

                try {
                    // Update preview content
                    $previewTitle.text($titleInput.val() || 'Post Title');

                    // Update tags
                    $previewTags.empty();
                    const tags = $tagsInput.val().split(',').filter(tag => tag.trim() !== '');
                    tags.forEach(tag => {
                        $('<span>')
                            .addClass('badge bg-secondary me-2')
                            .text(tag.trim())
                            .appendTo($previewTags);
                    });

                    // Format content with improved handling
                    let formattedContent = $contentInput.val() || 'Post content will appear here...';

                    // Apply formatting
                    formattedContent = formatPostContent(formattedContent);

                    // Set the formatted content
                    $previewContent.html(formattedContent);

                    console.log("Preview content updated successfully");
                } catch (error) {
                    console.error("Error updating preview:", error);
                    $previewContent.html('<div class="alert alert-danger">Error generating preview. Please check your content.</div>');
                }
            } else {
                // Hide preview
                $previewArea.addClass('d-none');
                $(this).html('<i class="fas fa-eye me-2"></i>Preview Post');
            }
        });

        // Helper function to format post content with better regex handling
        function formatPostContent(content) {
            if (!content) return '<p>No content to preview</p>';

            // Save original content for debugging
            const originalContent = content;
            console.log("Formatting content, length:", content.length);

            try {
                // First handle paragraphs
                content = content.replace(/\n\n+/g, '</p><p>');
                content = '<p>' + content + '</p>';

                // Then handle single line breaks within paragraphs
                content = content.replace(/\n/g, '<br>');

                // Basic text formatting
                content = content
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.*?)\*/g, '<em>$1</em>');

                // Headers (match at beginning of line or after a break)
                content = content
                    .replace(/(^|<br>|<\/p><p>)# (.*?)($|<br>|<\/p>)/g, '$1<h1>$2</h1>$3')
                    .replace(/(^|<br>|<\/p><p>)## (.*?)($|<br>|<\/p>)/g, '$1<h2>$2</h2>$3')
                    .replace(/(^|<br>|<\/p><p>)### (.*?)($|<br>|<\/p>)/g, '$1<h3>$2</h3>$3');

                // Lists
                let listItems = [];
                content = content.replace(/(^|<br>|<\/p><p>)- (.*?)($|<br>|<\/p>)/g, function(match, p1, p2, p3) {
                    listItems.push(p2);
                    if (p3.startsWith('<br>') || p3.startsWith('</p>')) {
                        const list = '<ul><li>' + listItems.join('</li><li>') + '</li></ul>';
                        listItems = [];
                        return p1 + list + p3;
                    }
                    return ''; // Temporarily remove the item so we can collect them
                });

                // Add any remaining list items
                if (listItems.length > 0) {
                    content += '<ul><li>' + listItems.join('</li><li>') + '</li></ul>';
                }

                // Links and images
                content = content
                    .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="img-fluid rounded my-2">')
                    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

                // Code blocks
                content = content.replace(/```([\s\S]*?)```/g, '<pre class="bg-dark p-3 rounded"><code>$1</code></pre>');

                // Clean up any empty paragraphs
                content = content.replace(/<p><\/p>/g, '');

                console.log("Formatting completed successfully");
                return content;
            } catch (error) {
                console.error("Error during content formatting:", error);
                return '<p>' + originalContent + '</p>'; // Return plain content on error
            }
        }

        // Format buttons
        $('.format-btn').off('click'); // Remove any existing handlers

        $('.format-btn').on('click', function() {
            const format = $(this).data('format');
            const $textarea = $('#postContent');
            const textarea = $textarea[0];
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const selectedText = $textarea.val().substring(start, end);

            let formattedText = '';

            switch (format) {
                case 'bold':
                    formattedText = `**${selectedText}**`;
                    break;
                case 'italic':
                    formattedText = `*${selectedText}*`;
                    break;
                case 'heading':
                    formattedText = `## ${selectedText}`;
                    break;
                case 'list':
                    formattedText = selectedText.split('\n').map(line => `- ${line}`).join('\n');
                    break;
                case 'link':
                    const url = prompt('Enter URL:', 'https://');
                    if (url) {
                        formattedText = `[${selectedText || 'Link text'}](${url})`;
                    } else {
                        return;
                    }
                    break;
                case 'image':
                    const imageUrl = prompt('Enter image URL:', 'https://');
                    if (imageUrl) {
                        formattedText = `![${selectedText || 'Image description'}](${imageUrl})`;
                    } else {
                        return;
                    }
                    break;
                case 'code':
                    formattedText = '```\n' + selectedText + '\n```';
                    break;
            }

            // Insert the formatted text
            $textarea.focus();
            const currentValue = $textarea.val();
            const newValue = currentValue.substring(0, start) + formattedText + currentValue.substring(end);
            $textarea.val(newValue);

            // Update character count
            $contentCounter.text($textarea.val().length);

            // Set cursor position after the inserted text
            const newPosition = start + formattedText.length;
            textarea.setSelectionRange(newPosition, newPosition);
        });

        // Mark as initialized to prevent duplicate initialization
        window.postCrafterInitialized = true;
        console.log("Post crafter initialization complete");
    }

    // Add a new function to handle the community forum page
    function handleCommunityPage() {
        // Make tavern cards clickable
        $('.tavern-card').on('click', function() {
            console.log("Tavern card clicked");
            // Add navigation logic here
        });

        // Setup tooltips if they exist
        if ($('[data-bs-toggle="tooltip"]').length) {
            $('[data-bs-toggle="tooltip"]').tooltip();
        }
  }

  // Initialize other features as needed
});


// Search and filter functionality
function handleSearch() {
  const searchInput = document.getElementById('searchInput');
  const categorySelect = document.getElementById('categorySelect');
  const sortSelect = document.getElementById('sortSelect');
  const itemsContainer = document.getElementById('itemsContainer');

  // Clear existing items
  itemsContainer.innerHTML = '';

  // Add loading placeholders
  for (let i = 0; i < 6; i++) {
    const placeholder = document.createElement('div');
    placeholder.className = 'col-md-4 mb-4';
    placeholder.innerHTML = `
      <div class="item-card loading">
        <div class="loading-placeholder title"></div>
        <div class="loading-placeholder description"></div>
        <div class="loading-placeholder price"></div>
      </div>
    `;
    itemsContainer.appendChild(placeholder);
  }

  // Get filter values
  const searchQuery = searchInput.value.toLowerCase();
  const selectedCategory = categorySelect.value;
  const sortBy = sortSelect.value;

  // Make API request with filters
  $.ajax({
    url: '/api/items',
    method: 'GET',
    data: {
      search: searchQuery,
      category: selectedCategory,
      sort: sortBy
    },
    success: function(response) {
      // Clear loading placeholders
      itemsContainer.innerHTML = '';

      if (response.items && response.items.length > 0) {
        response.items.forEach(item => {
          const itemCard = createItemCard(item);
          itemsContainer.appendChild(itemCard);
        });
      } else {
        itemsContainer.innerHTML = `
          <div class="col-12 text-center">
            <p class="text-muted">No items found matching your criteria.</p>
          </div>
        `;
      }
    },
    error: function(xhr, status, error) {
      console.error('Error loading items:', error);
      itemsContainer.innerHTML = `
        <div class="col-12 text-center">
          <p class="text-danger">Error loading items. Please try again later.</p>
        </div>
      `;
    }
  });
}

// Event listeners for search and filters
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('searchInput');
  const categorySelect = document.getElementById('categorySelect');
  const sortSelect = document.getElementById('sortSelect');
  const searchButton = document.getElementById('searchButton');

  // Only add event listeners if elements exist
  if (searchInput && categorySelect && sortSelect && searchButton) {
    // Debounce function to limit API calls
    function debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }

    // Debounced search handler
    const debouncedSearch = debounce(handleSearch, 500);

    // Event listeners
    searchInput.addEventListener('input', debouncedSearch);
    categorySelect.addEventListener('change', handleSearch);
    sortSelect.addEventListener('change', handleSearch);
    searchButton.addEventListener('click', function(e) {
      e.preventDefault();
      handleSearch();
    });

    // Initial load
    handleSearch();
  }
});

// Enhance community forums page function
function enhanceCommunityForumsPage() {
    console.log("Enhancing community forums page");

    // Format all dates on the page
    $('.post-date').each(function() {
        const dateString = $(this).data('date');
        if (dateString) {
            $(this).text(formatDate(dateString));
        }
    });

    // Make user links clickable - now using user IDs
    $(document).on('click', '.post-author', function(e) {
        e.preventDefault();
        const userId = $(this).data('user-id');
        if (userId) {
            window.location.href = `/user/${userId}`;
        }
    });

    // Fetch usernames for displayed posts if needed
    fetchCreatorUsernames();

    // Hover effects for post cards
    $('.post-card').each(function() {
        $(this).hover(
            function() {
                $(this).find('.post-content h5 a').css('color', 'var(--accent-color)');
            },
            function() {
                $(this).find('.post-content h5 a').css('color', '');
            }
        );
    });

    // Enhance voting experience
    $('.vote-btn').on('mousedown', function() {
        $(this).addClass('scale-95');
    }).on('mouseup mouseleave', function() {
        $(this).removeClass('scale-95');
    });

    // Add staggered loading animation for posts
    $('.post-card').each(function(index) {
        const $card = $(this);
        $card.css('opacity', '0');
        $card.css('transform', 'translateY(20px)');

        setTimeout(function() {
            $card.css('transition', 'opacity 0.5s ease, transform 0.5s ease');
            $card.css('opacity', '1');
            $card.css('transform', 'translateY(0)');
        }, 100 + (index * 100));
    });

    // Add ripple effect to buttons
    $('.btn').on('mousedown', function(e) {
        const $this = $(this);

        // Remove any existing ripple
        $this.find('.ripple').remove();

        // Create ripple element
        const $ripple = $('<span class="ripple"></span>');
        $this.append($ripple);

        // Get button position and dimensions
        const offset = $this.offset();
        const width = $this.outerWidth();
        const height = $this.outerHeight();

        // Calculate ripple position
        const posX = e.pageX - offset.left;
        const posY = e.pageY - offset.top;

        // Set ripple size and position
        $ripple.css({
            width: Math.max(width, height) * 2,
            height: Math.max(width, height) * 2,
            top: posY - $ripple.height() / 2,
            left: posX - $ripple.width() / 2
        });

        // Trigger animation
        setTimeout(function() {
            $ripple.addClass('active');
        }, 10);

        // Remove ripple after animation
        setTimeout(function() {
            $ripple.remove();
        }, 650);
    });

    // Add smooth scrolling for navigation
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();

        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });
}

// New function to fetch usernames for creator IDs
function fetchCreatorUsernames() {
    // Collect all user IDs that need usernames
    const creatorIds = [];
    $('.post-author').each(function() {
        const userId = $(this).data('user-id');
        // Only add if this element has no text or default "User" text
        if (userId && ($(this).text() === 'User' || $(this).text().trim() === '')) {
            creatorIds.push(userId);
        }
    });

    // If we have IDs that need usernames, fetch them
    if (creatorIds.length > 0) {
        // Remove duplicates
        const uniqueCreatorIds = [...new Set(creatorIds)];

        console.log("Fetching usernames for creator IDs:", uniqueCreatorIds);

        // Make an API request to get the usernames
        $.ajax({
            url: '/api/get_usernames',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_ids: uniqueCreatorIds }),
            success: function(response) {
                if (response.users) {
                    // Update the username display for each post author
                    $('.post-author').each(function() {
                        const creatorId = $(this).data('user-id');
                        const user = response.users.find(u => u.id == creatorId);
                        if (user && user.username) {
                            $(this).text(user.username);
                        }
                    });
                }
            },
            error: function(error) {
                console.error("Error fetching usernames:", error);
            }
        });
    }
}

// Initialize with enhanced animations
$(document).ready(function() {
    console.log("Document ready with enhanced animations");

    // Add CSS for new animation effects
    $('<style>')
        .html(`
            .scale-95 {
                transform: scale(0.95) !important;
            }

            .input-focused {
                border-color: var(--accent-color) !important;
                box-shadow: 0 0 0 0.25rem rgba(177, 152, 237, 0.25) !important;
            }

            .ripple {
                position: absolute;
                border-radius: 50%;
                background-color: rgba(255, 255, 255, 0.4);
                transform: scale(0);
                opacity: 1;
                pointer-events: none;
                z-index: 1;
            }

            .ripple.active {
                animation: ripple 0.6s linear;
            }

            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `)
        .appendTo('head');

    // Initialize user context - will call the function we defined above
    if (typeof initializeUserContext === 'function') {
        initializeUserContext();
    } else {
        console.log("User context initialization skipped");
    }

    // Initialize tooltips and popovers with smoother animations
    if (typeof bootstrap !== 'undefined') {
        if (bootstrap.Tooltip) {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipOptions = {
                animation: true,
                delay: { show: 100, hide: 100 }
            };
            var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl, tooltipOptions);
            });
        }

        if (bootstrap.Popover) {
            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
            var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        }
    }

    // Call page-specific initialization
    if (typeof handlePageSpecificCode === 'function') {
        handlePageSpecificCode();
    } else {
        console.log("Page-specific code initialization skipped");
    }
});

// Add this function to format dates in a friendly way
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (isNaN(date.getTime())) {
        return "Unknown date";
    }

    if (diffDays === 0) {
        // Today, show hours
        const hours = Math.floor(diffTime / (1000 * 60 * 60));
        if (hours === 0) {
            const minutes = Math.floor(diffTime / (1000 * 60));
            return minutes === 0 ? "Just now" : `${minutes}m ago`;
        }
        return `${hours}h ago`;
    } else if (diffDays === 1) {
        return "Yesterday";
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else {
        // Format as MM/DD/YYYY for older posts
        return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
    }
}

// First, add this missing function at the bottom of your index.js file
function initializeUserContext() {
    // Just a stub function to prevent errors
    console.log("User context initialized");
    // You can add actual user context initialization here if needed later
}
