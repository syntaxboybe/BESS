// Notifications.js - Handles real-time notification updates

// Function to update notification badge
function updateNotificationBadge(count) {
    const badge = document.querySelector('#notificationDropdown .badge');

    if (count > 0) {
        if (badge) {
            badge.textContent = count;
        } else {
            // If badge doesn't exist, create it
            const bellIcon = document.querySelector('#notificationDropdown i');
            const newBadge = document.createElement('span');
            newBadge.className = 'badge';
            newBadge.style.backgroundColor = '#008000';
            newBadge.style.color = 'white';
            newBadge.textContent = count;
            bellIcon.parentNode.appendChild(newBadge);
        }
    } else {
        // If count is 0, remove the badge
        if (badge) {
            badge.remove();
        }
    }
}

// Function to update notification content
function updateNotificationContent(data) {
    const dropdownMenu = document.querySelector('#notificationDropdown + .dropdown-menu');
    if (!dropdownMenu) return;

    // Create new content
    let content = `
        <li>
            <h6 class="dropdown-header text-white" style="background-color: #355389; position: sticky; top: 0; z-index: 1000;">
                <center><b>NOTIFICATIONS</b></center>
            </h6>
        </li>
    `;

    if (data.total > 0) {
        content += `
            <li>
                <h6 class="dropdown-header text-white" style="background-color: #006400;">New Requests</h6>
            </li>
        `;

        // Add clearance notifications
        if (data.clearanceRequests && data.clearanceRequests.length > 0) {
            data.clearanceRequests.forEach(request => {
                content += `
                    <li>
                        <a class="dropdown-item d-flex justify-content-between align-items-center" href="/BESS/clearance/">
                            <div>
                                <i class="fas fa-file-alt me-2"></i> Barangay Clearance
                                <small class="d-block text-white-50">${request.resident_name}</small>
                                <small class="d-block text-white-50">${request.date_requested}</small>
                            </div>
                            <span class="badge rounded-pill bg-danger">New</span>
                        </a>
                    </li>
                `;
            });
        }

        // Add indigency notifications
        if (data.indigencyRequests && data.indigencyRequests.length > 0) {
            data.indigencyRequests.forEach(request => {
                content += `
                    <li>
                        <a class="dropdown-item d-flex justify-content-between align-items-center" href="/BESS/indigency_request/">
                            <div>
                                <i class="fas fa-feather-alt me-2"></i> Certificate of Indigency
                                <small class="d-block text-white-50">${request.resident_name}</small>
                                <small class="d-block text-white-50">${request.date_requested}</small>
                            </div>
                            <span class="badge rounded-pill bg-danger">New</span>
                        </a>
                    </li>
                `;
            });
        }

        // Add business permit notifications
        if (data.businessRequests && data.businessRequests.length > 0) {
            data.businessRequests.forEach(request => {
                content += `
                    <li>
                        <a class="dropdown-item d-flex justify-content-between align-items-center" href="/BESS/business_permit_request/">
                            <div>
                                <i class="fas fa-file-contract me-2"></i> Business Permit
                                <small class="d-block text-white-50">${request.resident_name}</small>
                                <small class="d-block text-white-50">${request.date_requested}</small>
                            </div>
                            <span class="badge rounded-pill bg-danger">New</span>
                        </a>
                    </li>
                `;
            });
        }

        // Add building permit notifications
        if (data.buildingRequests && data.buildingRequests.length > 0) {
            data.buildingRequests.forEach(request => {
                content += `
                    <li>
                        <a class="dropdown-item d-flex justify-content-between align-items-center" href="/BESS/building_permit_request/">
                            <div>
                                <i class="far fa-building me-2"></i> Building Permit
                                <small class="d-block text-white-50">${request.resident_name}</small>
                                <small class="d-block text-white-50">${request.date_requested}</small>
                            </div>
                            <span class="badge rounded-pill bg-danger">New</span>
                        </a>
                    </li>
                `;
            });
        }

        // Add residency notifications
        if (data.residencyRequests && data.residencyRequests.length > 0) {
            data.residencyRequests.forEach(request => {
                content += `
                    <li>
                        <a class="dropdown-item d-flex justify-content-between align-items-center" href="/BESS/residency_request/">
                            <div>
                                <i class="fas fa-certificate me-2"></i> Certificate of Residency
                                <small class="d-block text-white-50">${request.resident_name}</small>
                                <small class="d-block text-white-50">${request.date_requested}</small>
                            </div>
                            <span class="badge rounded-pill bg-danger">New</span>
                        </a>
                    </li>
                `;
            });
        }

        // Add mark all as read button
        content += `
            <li><hr class="dropdown-divider bg-white opacity-25"></li>
            <li>
                <div class="dropdown-header text-center">
                    <a href="#" class="text-white" style="text-decoration: none;" onclick="markAllAsRead(); return false;">
                        <i class="fas fa-check-double me-1"></i> Mark all as read
                    </a>
                </div>
            </li>
        `;
    } else {
        // No notifications
        content += `
            <li>
                <div class="dropdown-item text-center text-white-50">
                    No new notifications
                </div>
            </li>
        `;
    }

    // Update DOM if content is different
    if (dropdownMenu.innerHTML.trim() !== content.trim()) {
        dropdownMenu.innerHTML = content;
    }
}

// Function to fetch notification counts from server
function fetchNotificationCounts() {
    // Using Fetch API to get counts
    fetch('/api/notifications/count/')
        .then(response => response.json())
        .then(data => {
            // Update total badge
            updateNotificationBadge(data.total);

            // If we're using dynamic content updates
            if (data.clearanceRequests || data.indigencyRequests || data.businessRequests ||
                data.buildingRequests || data.residencyRequests) {
                updateNotificationContent(data);
            } else {
                // Otherwise just update the individual badges
                updateDocumentBadge('clearance', data.clearance);
                updateDocumentBadge('indigency', data.indigency);
                updateDocumentBadge('business', data.business);
                updateDocumentBadge('building', data.building);
                updateDocumentBadge('residency', data.residency);
            }
        })
        .catch(error => console.error('Error fetching notification counts:', error));
}

// Function to mark all notifications as read
function markAllAsRead() {
    fetch('/api/notifications/mark-all-read/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update UI to show no notifications
            updateNotificationBadge(0);

            const dropdownMenu = document.querySelector('#notificationDropdown + .dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.innerHTML = `
                    <li>
                        <h6 class="dropdown-header text-white" style="background-color: #355389; position: sticky; top: 0; z-index: 1000;">
                            <center><b>NOTIFICATIONS</b></center>
                        </h6>
                    </li>
                    <li>
                        <div class="dropdown-item text-center text-white-50">
                            No new notifications
                        </div>
                    </li>
                `;
            }

            // Show success feedback
            showNotification('All notifications marked as read');
        }
    })
    .catch(error => console.error('Error marking notifications as read:', error));
}

// Helper function to get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Function to show notification feedback
function showNotification(message) {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('notification-toast');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification-toast';
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            z-index: 9999;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s, transform 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        `;
        document.body.appendChild(notification);
    }

    // Update message and show
    notification.textContent = message;
    notification.style.opacity = '1';
    notification.style.transform = 'translateY(0)';

    // Hide after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(20px)';
    }, 3000);
}

// Auto-refresh notifications every 30 seconds
let refreshInterval;

function startNotificationRefresh() {
    // Initial fetch
    fetchNotificationCounts();

    // Set up interval for refreshing
    refreshInterval = setInterval(fetchNotificationCounts, 30000); // 30 seconds
}

function stopNotificationRefresh() {
    clearInterval(refreshInterval);
}

// Function to update individual document type count badges (used for non-dynamic updates)
function updateDocumentBadge(type, count) {
    const selector = `.dropdown-item[href*="${type}"] .badge`;
    const badge = document.querySelector(selector);

    if (count > 0) {
        if (badge) {
            badge.textContent = count;
        } else {
            // If badge doesn't exist, create it
            const menuItem = document.querySelector(`.dropdown-item[href*="${type}"]`);
            if (menuItem) {
                const newBadge = document.createElement('span');
                newBadge.className = 'badge rounded-pill bg-danger';
                newBadge.textContent = count;
                menuItem.appendChild(newBadge);
            }
        }
    } else {
        // If count is 0, remove the badge
        if (badge) {
            badge.remove();
        }
    }
}

// Initialize notifications when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize for authenticated users who have the notification dropdown
    const notificationDropdown = document.getElementById('notificationDropdown');
    if (notificationDropdown) {
        startNotificationRefresh();
    }

    // Add bell animation when new notifications arrive
    const bellIcon = document.querySelector('#notificationDropdown i');
    if (bellIcon) {
        // Add animation class when count changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' ||
                    (mutation.type === 'characterData' && mutation.target.parentNode.classList.contains('badge'))) {
                    bellIcon.classList.add('notification-bell-animation');
                    setTimeout(() => {
                        bellIcon.classList.remove('notification-bell-animation');
                    }, 1000);
                }
            });
        });

        observer.observe(notificationDropdown, {
            childList: true,
            characterData: true,
            subtree: true
        });
    }
});
