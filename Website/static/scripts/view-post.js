document.addEventListener('DOMContentLoaded', function() {
    const deleteButton = document.getElementById('deleteButton');
    
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            const materialId = this.getAttribute('data-material-id');
            
            if (confirm('Are you sure you want to delete this material?')) {
                fetch(`/material/${materialId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = "/dashboard";
                    } else {
                        alert('Failed to delete material');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting');
                });
            }
        });
    }
});