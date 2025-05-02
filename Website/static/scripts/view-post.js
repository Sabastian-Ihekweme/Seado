function confirmDelete(materialId) {
    if (confirm('Are you sure you want to delete this material?')) {
        fetch(`/materials/${materialId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = "{{ url_for('views.tutor_dashboard') }}";
            } else {
                alert('Failed to delete material');
            }
        });
    }
}
