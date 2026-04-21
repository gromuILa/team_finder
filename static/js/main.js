/* Favorite button toggle (not used in variant 2 but kept for UI) */
document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const projectId = btn.dataset.projectId;
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrf) return;
        fetch(`/projects/${projectId}/toggle-favorite/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf.value },
        })
            .then(r => r.json())
            .then(data => {
                if (data.favorited) btn.classList.add('favorited');
                else btn.classList.remove('favorited');
            })
            .catch(() => {});
    });
});
