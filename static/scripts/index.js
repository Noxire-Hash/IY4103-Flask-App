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
function handleUserAccountPage() {
    console.log("Loading user account page");

    // Follow/Unfollow functionality
    const followBtn = document.getElementById('followBtn');
    const unfollowBtn = document.getElementById('unfollowBtn');

    if (followBtn) {
        followBtn.addEventListener('click', function() {
            // Show loading state
            followBtn.disabled = true;
            followBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Following...';

            const userId = followBtn.getAttribute('data-user-id');
            // Ajax call to follow user
            fetch(`/api/follow/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    // Reset button
                    followBtn.disabled = false;
                    followBtn.innerHTML = '<i class="fas fa-user-plus me-2"></i> Follow User';
                    alert('Error following user: ' + (data.message || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Reset button
                followBtn.disabled = false;
                followBtn.innerHTML = '<i class="fas fa-user-plus me-2"></i> Follow User';
                alert('Error following user');
            });
        });
    }

    if (unfollowBtn) {
        unfollowBtn.addEventListener('click', function() {
            // Handle unfollow action
            unfollowBtn.disabled = true;
            unfollowBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Unfollowing...';

            const userId = unfollowBtn.getAttribute('data-user-id');
            fetch(`/api/unfollow/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    // Reset button
                    unfollowBtn.disabled = false;
                    unfollowBtn.innerHTML = '<i class="fas fa-user-minus me-2"></i> Unfollow';
                    alert('Error unfollowing user: ' + (data.message || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Reset button
                unfollowBtn.disabled = false;
                unfollowBtn.innerHTML = '<i class="fas fa-user-minus me-2"></i> Unfollow';
                alert('Error unfollowing user');
            });
        });
    }
}

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
            case PATHS.USER_ACCOUNT:
                handleUserAccountPage();
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

    // Load featured items
    loadFeaturedItems();

    // Load all items
    loadAllItems();

    // Initialize admin dashboard if on admin page
    if ($('#admin-dashboard').length) {
        initAdminDashboard();
    }

    // Initialize features based on which page we're on

    // Check if we're on store page
    if ($('#featured-items-container').length) {
        loadFeaturedItems();
        loadAllItems();
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
