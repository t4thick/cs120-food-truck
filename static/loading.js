/**
 * Loading indicator utilities
 * Add loading spinners to forms and buttons
 */

function showLoading(element) {
    if (!element) return;
    
    // Store original content
    if (!element.dataset.originalText) {
        element.dataset.originalText = element.textContent || element.value;
    }
    
    // Disable element
    element.disabled = true;
    
    // Add loading class
    element.classList.add('loading');
    
    // Update text/button
    if (element.tagName === 'BUTTON' || element.tagName === 'INPUT') {
        element.textContent = element.value = 'Processing...';
    }
}

function hideLoading(element) {
    if (!element) return;
    
    // Restore original content
    if (element.dataset.originalText) {
        if (element.tagName === 'BUTTON') {
            element.textContent = element.dataset.originalText;
        } else if (element.tagName === 'INPUT') {
            element.value = element.dataset.originalText;
        }
    }
    
    // Remove loading class
    element.classList.remove('loading');
    
    // Re-enable element
    element.disabled = false;
}

// Auto-attach to forms
document.addEventListener('DOMContentLoaded', function() {
    // Find all forms and attach loading to submit buttons
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                showLoading(submitBtn);
            }
        });
    });
});

