/* Skills management: autocomplete, add, remove (Variant 2 - user skills) */
(function () {
    const skillsList = document.getElementById('skills-list');
    const addBtn = document.getElementById('add-skill-btn');
    const inputWrap = document.getElementById('skill-input-wrap');
    const input = document.getElementById('skill-input');
    const suggestions = document.getElementById('skill-suggestions');

    if (!addBtn) return;

    let debounceTimer;

    addBtn.addEventListener('click', () => {
        inputWrap.style.display = 'block';
        input.focus();
    });

    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const q = input.value.trim();
        if (!q) { suggestions.style.display = 'none'; return; }
        debounceTimer = setTimeout(() => fetchSuggestions(q), 250);
    });

    function fetchSuggestions(q) {
        fetch(autocompleteUrl + encodeURIComponent(q))
            .then(r => r.json())
            .then(data => {
                suggestions.innerHTML = '';
                const items = data.slice(0, 10);
                const exactMatch = items.some(s => s.name.toLowerCase() === q.toLowerCase());
                items.forEach(skill => {
                    const li = document.createElement('li');
                    li.textContent = skill.name;
                    li.addEventListener('click', () => addSkill(skill.id, null));
                    suggestions.appendChild(li);
                });
                if (!exactMatch && q) {
                    const li = document.createElement('li');
                    li.textContent = `Создать «${q}»`;
                    li.style.fontStyle = 'italic';
                    li.addEventListener('click', () => addSkill(null, q));
                    suggestions.appendChild(li);
                }
                suggestions.style.display = items.length || q ? 'block' : 'none';
            });
    }

    function addSkill(skillId, name) {
        const body = new URLSearchParams();
        if (skillId) body.append('skill_id', skillId);
        else body.append('name', name);

        fetch(addUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken, 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body.toString(),
        })
            .then(r => r.json())
            .then(data => {
                if (data.added) {
                    renderSkillTag(data.skill_id, name || input.value.trim());
                }
                input.value = '';
                suggestions.style.display = 'none';
            });
    }

    function renderSkillTag(skillId, skillName) {
        const span = document.createElement('span');
        span.className = 'skill-tag';
        span.dataset.skillId = skillId;
        span.innerHTML = `${skillName} <button class="skill-tag__remove" data-skill-id="${skillId}" title="Удалить навык">&times;</button>`;
        span.querySelector('.skill-tag__remove').addEventListener('click', () => removeSkill(skillId, span));
        skillsList.appendChild(span);
    }

    // Attach remove to existing tags
    skillsList.querySelectorAll('.skill-tag__remove').forEach(btn => {
        btn.addEventListener('click', () => {
            const skillId = btn.dataset.skillId;
            removeSkill(skillId, btn.closest('.skill-tag'));
        });
    });

    function removeSkill(skillId, tagEl) {
        fetch(`${removeUrlBase}${skillId}/remove/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
        })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') tagEl.remove();
            });
    }

    // Close suggestions on outside click
    document.addEventListener('click', e => {
        if (!inputWrap.contains(e.target) && e.target !== addBtn) {
            suggestions.style.display = 'none';
        }
    });
})();
