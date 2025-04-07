/**
 * Möhlenhoff Alpha 2 Web UI JavaScript
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the UI
    initializeUI();
});

/**
 * Initialize UI elements and event handlers
 */
function initializeUI() {
    // Set up room form validation
    setupFormValidation();
    
    // Setup room deletion confirmation
    setupRoomDeletion();
    
    // Setup responsive navigation
    setupMobileNavigation();
    
    // Setup automatic status refresh if on dashboard
    if (document.querySelector('.dashboard')) {
        setupStatusRefresh();
    }
}

/**
 * Set up validation for the add room form
 */
function setupFormValidation() {
    const addRoomForm = document.getElementById('add-room-form');
    if (!addRoomForm) return;
    
    addRoomForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form values
        const nameInput = document.getElementById('name');
        const areaIdInput = document.getElementById('area_id');
        const sensorInput = document.getElementById('temperature_entity_id');
        
        // Validate inputs
        let isValid = true;
        
        if (!nameInput.value.trim()) {
            showInputError(nameInput, 'Room name is required');
            isValid = false;
        } else {
            clearInputError(nameInput);
        }
        
        if (!areaIdInput.value || areaIdInput.value < 1 || areaIdInput.value > 255) {
            showInputError(areaIdInput, 'Area ID must be between 1 and 255');
            isValid = false;
        } else {
            clearInputError(areaIdInput);
        }
        
        if (!sensorInput.value) {
            showInputError(sensorInput, 'Temperature sensor is required');
            isValid = false;
        } else {
            clearInputError(sensorInput);
        }
        
        if (!isValid) return;
        
        // Show loading state
        const submitButton = addRoomForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Adding...';
        
        try {
            // Submit form data
            const formData = new FormData(addRoomForm);
            const response = await fetch('/api/rooms/add', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message and reset form
                showNotification('Room added successfully', 'success');
                addRoomForm.reset();
                
                // Reload the page after a short delay
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                // Show error message
                showNotification(`Error: ${result.message}`, 'error');
            }
        } catch (error) {
            showNotification(`Error: ${error.message}`, 'error');
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
}

/**
 * Set up deletion confirmation for rooms
 */
function setupRoomDeletion() {
    const deleteButtons = document.querySelectorAll('.delete-room');
    if (!deleteButtons.length) return;
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const areaId = this.dataset.areaId;
            const roomName = this.closest('.room-item').querySelector('h3').textContent;
            
            if (confirm(`Are you sure you want to delete "${roomName}"?`)) {
                // Show loading state
                const originalText = this.textContent;
                this.disabled = true;
                this.textContent = 'Deleting...';
                
                try {
                    const response = await fetch(`/api/rooms/delete/${areaId}`, {
                        method: 'POST'
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Show success message
                        showNotification('Room deleted successfully', 'success');
                        
                        // Remove the room element with animation
                        const roomElement = this.closest('.room-item');
                        roomElement.style.opacity = '0';
                        roomElement.style.transform = 'translateX(20px)';
                        roomElement.style.transition = 'opacity 0.3s, transform 0.3s';
                        
                        setTimeout(() => {
                            roomElement.remove();
                            
                            // If no rooms left, show "no rooms" message
                            const roomsList = document.querySelector('.rooms-list');
                            if (roomsList && roomsList.children.length === 0) {
                                roomsList.innerHTML = '<p>No virtual rooms configured.</p>';
                            }
                        }, 300);
                    } else {
                        // Show error message
                        showNotification(`Error: ${result.message}`, 'error');
                        
                        // Reset button state
                        this.disabled = false;
                        this.textContent = originalText;
                    }
                } catch (error) {
                    showNotification(`Error: ${error.message}`, 'error');
                    
                    // Reset button state
                    this.disabled = false;
                    this.textContent = originalText;
                }
            }
        });
    });
}

/**
 * Setup mobile navigation toggle
 */
function setupMobileNavigation() {
    const navToggle = document.createElement('button');
    navToggle.className = 'nav-toggle';
    navToggle.textContent = '☰';
    
    const header = document.querySelector('header');
    const nav = document.querySelector('nav');
    
    if (header && nav) {
        header.insertBefore(navToggle, nav);
        
        navToggle.addEventListener('click', function() {
            nav.classList.toggle('show');
        });
    }
}

/**
 * Setup automatic status refresh on dashboard
 */
function setupStatusRefresh() {
    // Refresh room status every 30 seconds
    setInterval(async function() {
        try {
            const response = await fetch('/api/rooms');
            const rooms = await response.json();
            
            // Update room cards if they exist
            const roomsGrid = document.querySelector('.rooms-grid');
            if (roomsGrid && rooms.length > 0) {
                // We could update the UI here with current temperatures
                // This would require adding more data to the API response
            }
        } catch (error) {
            console.error('Error updating status:', error);
        }
    }, 30000);
}

/**
 * Show an error message for an input field
 */
function showInputError(inputElement, message) {
    // Clear any existing error
    clearInputError(inputElement);
    
    // Create and add error message
    const errorElement = document.createElement('div');
    errorElement.className = 'input-error';
    errorElement.textContent = message;
    errorElement.style.color = 'var(--danger-color)';
    errorElement.style.fontSize = '0.8rem';
    errorElement.style.marginTop = '0.25rem';
    
    inputElement.style.borderColor = 'var(--danger-color)';
    inputElement.parentNode.appendChild(errorElement);
}

/**
 * Clear error message for an input field
 */
function clearInputError(inputElement) {
    const errorElement = inputElement.parentNode.querySelector('.input-error');
    if (errorElement) {
        errorElement.remove();
    }
    inputElement.style.borderColor = '';
}

/**
 * Show a notification message
 */
function showNotification(message, type = 'info') {
    // Remove any existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.position = 'fixed';
    notification.style.top = '1rem';
    notification.style.right = '1rem';
    notification.style.padding = '0.75rem 1rem';
    notification.style.borderRadius = '4px';
    notification.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';
    notification.style.zIndex = '1000';
    notification.style.maxWidth = '300px';
    
    // Set color based on type
    if (type === 'success') {
        notification.style.backgroundColor = 'var(--success-color)';
        notification.style.color = 'white';
    } else if (type === 'error') {
        notification.style.backgroundColor = 'var(--danger-color)';
        notification.style.color = 'white';
    } else {
        notification.style.backgroundColor = 'var(--primary-color)';
        notification.style.color = 'white';
    }
    
    // Add close button
    const closeButton = document.createElement('span');
    closeButton.textContent = '×';
    closeButton.style.marginLeft = '0.5rem';
    closeButton.style.cursor = 'pointer';
    closeButton.style.float = 'right';
    closeButton.style.fontSize = '1.2rem';
    closeButton.style.lineHeight = '1';
    
    closeButton.addEventListener('click', function() {
        notification.remove();
    });
    
    notification.appendChild(closeButton);
    
    // Add to the document
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(20px)';
            notification.style.transition = 'opacity 0.3s, transform 0.3s';
            
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}