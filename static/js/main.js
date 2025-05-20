document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const demoForm = document.querySelector('#demo-form');
    if (demoForm) {
        demoForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            try {
                submitButton.textContent = 'Sending...';
                submitButton.disabled = true;
                
                const response = await fetch('/request-demo', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification('Demo request received! We\'ll contact you soon.', 'success');
                    this.reset();
                } else {
                    showNotification('Something went wrong. Please try again.', 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again.', 'error');
            } finally {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Notification system
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg ${
            type === 'success' ? 'bg-green-500' : 'bg-red-500'
        } text-white z-50`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    // Add floating animation to specific elements
    document.querySelectorAll('.floating').forEach(element => {
        element.classList.add('floating');
    });
}); 