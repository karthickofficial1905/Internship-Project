// Attendance Admin Panel JavaScript

// Initialize date display
function initializeDateDisplay() {
    const now = new Date();
    
    // Month and Year
    const monthYear = now.toLocaleDateString('en-US', { 
        month: 'long', 
        year: 'numeric' 
    });
    document.getElementById('adh-my').textContent = monthYear;
    
    // Day
    const day = now.getDate();
    document.getElementById('adh-d').textContent = day;
    
    // Weekday
    const weekday = now.toLocaleDateString('en-US', { 
        weekday: 'long' 
    });
    document.getElementById('adh-wd').textContent = weekday;
}

// Tab switching functionality
function switchAdmTab(tabName, element) {
    // Remove active class from all tabs
    document.querySelectorAll('.adm-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Add active class to clicked tab
    element.classList.add('active');
    
    // Hide all sections
    document.querySelectorAll('.adm-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`adm-${tabName}`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// Filter attendance by status
function filterAtt(status, element) {
    // Remove active class from all filter pills
    document.querySelectorAll('.filter-pills .fpil').forEach(pill => {
        pill.classList.remove('active');
    });
    
    // Add active class to clicked pill
    element.classList.add('active');
    
    // Get all attendance cards
    const cards = document.querySelectorAll('.att-card');
    
    cards.forEach(card => {
        const cardStatus = card.getAttribute('data-status');
        
        if (status === 'all' || cardStatus === status) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Search attendance by employee name
function searchAtt(searchTerm) {
    const cards = document.querySelectorAll('.att-card');
    const searchLower = searchTerm.toLowerCase();
    
    cards.forEach(card => {
        const employeeName = card.getAttribute('data-name');
        
        if (employeeName.includes(searchLower)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Filter leave requests by status
function filterLeave(status, element) {
    // Remove active class from all filter pills
    document.querySelectorAll('.filter-pills .fpil').forEach(pill => {
        pill.classList.remove('active');
    });
    
    // Add active class to clicked pill
    element.classList.add('active');
    
    // Get all leave table rows
    const rows = document.querySelectorAll('#leave-tbody tr');
    
    rows.forEach(row => {
        const rowStatus = row.getAttribute('data-status');
        
        if (status === 'all' || rowStatus === status) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}

// Search leave requests by employee name
function searchLeave(searchTerm) {
    const rows = document.querySelectorAll('#leave-tbody tr');
    const searchLower = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const employeeName = row.getAttribute('data-name');
        
        if (employeeName.includes(searchLower)) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}

// Demo action for leave approval/rejection
function demoAction(button, action) {
    const row = button.closest('tr');
    const employeeName = row.querySelector('.lt-name').textContent;
    const statusBadge = row.querySelector('.badge');
    const actionCell = row.querySelector('td:last-child');
    
    if (action === 'approve') {
        statusBadge.className = 'badge b-present';
        statusBadge.innerHTML = '<span class="bdot"></span>Approved';
        row.setAttribute('data-status', 'approved');
        actionCell.innerHTML = '<span style="font-size:12px;color:var(--slate)">—</span>';
        
        // Show success message
        showToast(`Leave approved for ${employeeName}`, 'success');
    } else if (action === 'reject') {
        statusBadge.className = 'badge b-absent';
        statusBadge.innerHTML = '<span class="bdot"></span>Rejected';
        row.setAttribute('data-status', 'rejected');
        actionCell.innerHTML = '<span style="font-size:12px;color:var(--slate)">—</span>';
        
        // Show success message
        showToast(`Leave rejected for ${employeeName}`, 'error');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;
    
    // Add toast styles if not already present
    if (!document.getElementById('toast-styles')) {
        const styles = document.createElement('style');
        styles.id = 'toast-styles';
        styles.textContent = `
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 16px;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
                max-width: 300px;
            }
            .toast-success { background: #059669; }
            .toast-error { background: #dc2626; }
            .toast-info { background: #0284c7; }
            .toast-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
            }
            .toast-close {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Add toast to page
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 3000);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializeDateDisplay();
    
    // Set up real-time clock update
    setInterval(initializeDateDisplay, 60000); // Update every minute
});