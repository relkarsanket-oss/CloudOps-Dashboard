/* =========================================
   CloudOps Dashboard - Application JavaScript
   ========================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});


/* =========================================
   Dashboard Initialization
   ========================================= */

function initializeDashboard() {
    setupRefreshButton();
    setupNotificationButton();
    setupTimeSelector();
    setupNavigation();
    updateLastUpdatedTime();
    checkBackendHealth();
}


/* =========================================
   Refresh Dashboard
   ========================================= */

function setupRefreshButton() {
    const refreshButton = document.querySelector(".btn-primary");

    if (!refreshButton) {
        return;
    }

    refreshButton.addEventListener("click", () => {
        refreshDashboard(refreshButton);
    });
}


function refreshDashboard(button) {
    const originalText = button.innerHTML;

    button.disabled = true;
    button.innerHTML = "â†» Refreshing...";

    setTimeout(() => {
        updateResourceValues();
        updateLastUpdatedTime();

        button.disabled = false;
        button.innerHTML = originalText;

        showNotification(
            "Dashboard refreshed successfully.",
            "success"
        );
    }, 800);
}


/* =========================================
   Resource Value Simulation
   ========================================= */

function updateResourceValues() {
    const resourceValues = document.querySelectorAll(".resource-value");

    resourceValues.forEach((element) => {
        const currentValue = parseInt(
            element.textContent.replace(/,/g, ""),
            10
        );

        if (Number.isNaN(currentValue)) {
            return;
        }

        const variation = Math.floor(
            Math.random() * 5
        ) - 2;

        const newValue = Math.max(
            0,
            currentValue + variation
        );

        element.textContent = newValue.toLocaleString();
    });
}


/* =========================================
   Last Updated Time
   ========================================= */

function updateLastUpdatedTime() {
    const elements = document.querySelectorAll(
        ".last-updated"
    );

    if (elements.length === 0) {
        return;
    }

    const now = new Date();

    const formattedTime = now.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        }
    );

    elements.forEach((element) => {
        element.textContent = `Last updated: ${formattedTime}`;
    });
}


/* =========================================
   Notifications
   ========================================= */

function setupNotificationButton() {
    const notificationButton =
        document.querySelector(".notification-btn");

    if (!notificationButton) {
        return;
    }

    notificationButton.addEventListener("click", () => {
        showNotification(
            "You have 3 recent alerts.",
            "info"
        );
    });
}


/* =========================================
   Notification Message
   ========================================= */

function showNotification(message, type = "info") {
    const existingNotification =
        document.querySelector(".toast-notification");

    if (existingNotification) {
        existingNotification.remove();
    }

    const notification =
        document.createElement("div");

    notification.className =
        `toast-notification toast-${type}`;

    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add("show");
    }, 10);

    setTimeout(() => {
        notification.classList.remove("show");

        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}


/* =========================================
   Performance Time Selector
   ========================================= */

function setupTimeSelector() {
    const selector =
        document.querySelector(".time-selector");

    if (!selector) {
        return;
    }

    selector.addEventListener("change", () => {
        const selectedRange =
            selector.value;

        showNotification(
            `Performance range changed to ${selectedRange}.`,
            "info"
        );
    });
}


/* =========================================
   Sidebar Navigation
   ========================================= */

function setupNavigation() {
    const navigationLinks =
        document.querySelectorAll(".nav-menu a");

    navigationLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();

            navigationLinks.forEach((item) => {
                item.classList.remove("active");
            });

            link.classList.add("active");

            const pageName =
                link.textContent.trim();

            showNotification(
                `${pageName} section selected.`,
                "info"
            );
        });
    });
}

/* =========================================
   Backend API Health Check
   ========================================= */

async function checkBackendHealth() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/health"
        );

        if (!response.ok) {
            throw new Error(
                `Backend returned HTTP ${response.status}`
            );
        }

        const data = await response.json();

        console.log(
            "Backend health:",
            data.status
        );
    } catch (error) {
        console.error(
            "Backend health check failed:",
            error
        );
    }
}
