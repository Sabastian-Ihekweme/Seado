function confirmDelete(materialId) {
    if (confirm('Are you sure you want to permanently delete this material?')) {
        // Show loading state
        const preview = document.querySelector('.material-preview');
        preview.classList.add('loading');
        
        fetch(`/materials/${materialId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'  // Add CSRF protection
            }
        })
        .then(response => {
            if (response.ok) {
                // Show success message before redirect
                alert('Material deleted successfully');
                window.location.href = "{{ url_for('views.tutor_dashboard') }}";
            } else {
                preview.classList.remove('loading');
                throw new Error('Delete failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete material. Please try again.');
            preview.classList.remove('loading');
        });
    }
}

// Add media player event listeners
document.addEventListener('DOMContentLoaded', function() {
    const videoPlayers = document.querySelectorAll('video');
    videoPlayers.forEach(player => {
        player.addEventListener('error', function() {
            alert('Error loading video. Please check the file.');
        });
    });
});