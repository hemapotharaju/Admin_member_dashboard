function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function apiFetch(path, options = {}) {
    const csrfToken = getCookie('csrftoken');
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    if (csrfToken) {
        defaultHeaders['X-CSRFToken'] = csrfToken;
    }
    options.headers = {
        ...defaultHeaders,
        ...(options.headers || {}),
    };
    options.credentials = 'same-origin';
    return fetch(path, options).then(async response => {
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw data;
        }
        return data;
    });
}

function showMessage(elementId, text, isError = false) {
    const target = document.getElementById(elementId);
    if (!target) return;
    target.textContent = text;
    target.style.color = isError ? '#f87171' : '#86efac';
}

if (document.body.id === 'login-page') {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(form);
        const payload = {
            username: formData.get('username'),
            password: formData.get('password'),
        };
        apiFetch('/api/login/', { method: 'POST', body: JSON.stringify(payload) })
            .then(() => { window.location.href = '/dashboard/'; })
            .catch(error => showMessage('login-message', error.detail || 'Login failed', true));
    });
}

if (document.body.id === 'signup-page') {
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(form);
        const payload = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            role: formData.get('role'),
        };
        apiFetch('/api/signup/', { method: 'POST', body: JSON.stringify(payload) })
            .then(() => {
                showMessage('signup-message', 'Account created. Redirecting to login...');
                setTimeout(() => window.location.href = '/login/', 1200);
            })
            .catch(error => showMessage('signup-message', error.detail || 'Signup failed', true));
    });
}

if (document.body.id === 'dashboard-page') {
    const logoutButton = document.getElementById('logout-button');
    const projectForm = document.getElementById('project-form');
    const taskForm = document.getElementById('task-form');
    const projectsList = document.getElementById('projects-list');
    const tasksList = document.getElementById('tasks-list');
    const summaryCards = document.getElementById('summary-cards');

    function redirectToLogin() {
        window.location.href = '/login/';
    }

    function handleError(error) {
        if (error.detail && error.detail.toLowerCase().includes('credentials')) {
            redirectToLogin();
        }
        return error;
    }

    function loadSummary() {
        apiFetch('/api/dashboard-summary/')
            .then(data => {
                summaryCards.innerHTML = `
                    <div class="summary-card">
                        <h3>Projects</h3>
                        <p>${data.project_count}</p>
                    </div>
                    <div class="summary-card">
                        <h3>Tasks</h3>
                        <p>${data.task_count}</p>
                    </div>
                    <div class="summary-card">
                        <h3>Overdue</h3>
                        <p>${data.overdue_count}</p>
                    </div>
                    <div class="summary-card">
                        <h3>Status Summary</h3>
                        <p>${data.status_summary.map(item => `${item.status}: ${item.count}`).join(', ')}</p>
                    </div>
                `;
            })
            .catch(handleError);
    }

    function loadProjects() {
        apiFetch('/api/projects/')
            .then(data => {
                if (!data.length) {
                    projectsList.innerHTML = '<p>No projects created yet.</p>';
                    return;
                }
                projectsList.innerHTML = data.map(project => `
                    <div class="item-card">
                        <h3>${project.name}</h3>
                        <p class="label">ID: ${project.id}</p>
                        <p>${project.description || 'No description provided.'}</p>
                        <p class="label">Owner: ${project.owner.username}</p>
                    </div>
                `).join('');
            })
            .catch(handleError);
    }

    function loadTasks() {
        apiFetch('/api/tasks/')
            .then(data => {
                if (!data.length) {
                    tasksList.innerHTML = '<p>No tasks assigned or created yet.</p>';
                    return;
                }
                tasksList.innerHTML = data.map(task => `
                    <div class="item-card">
                        <h3>${task.title}</h3>
                        <p class="label">Project: ${task.project_name}</p>
                        <p>${task.description || 'No description provided.'}</p>
                        <p class="label">Status: ${task.status}</p>
                        <p class="label">Priority: ${task.priority}</p>
                        <p class="label">Assignee: ${task.assignee_name || 'Unassigned'}</p>
                        <div class="task-actions">
                            <button onclick="updateTask(${task.id}, 'pending')">Pending</button>
                            <button onclick="updateTask(${task.id}, 'in_progress')">In Progress</button>
                            <button onclick="updateTask(${task.id}, 'completed')">Completed</button>
                        </div>
                    </div>
                `).join('');
            })
            .catch(handleError);
    }

    window.updateTask = (taskId, status) => {
        apiFetch(`/api/tasks/${taskId}/`, { method: 'PATCH', body: JSON.stringify({ status }) })
            .then(() => {
                loadTasks();
                loadSummary();
            })
            .catch(err => showMessage('task-message', err.detail || 'Unable to update task', true));
    };

    logoutButton.addEventListener('click', () => {
        apiFetch('/api/logout/', { method: 'POST' })
            .then(() => redirectToLogin())
            .catch(() => redirectToLogin());
    });

    projectForm.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(projectForm);
        const payload = {
            name: formData.get('name'),
            description: formData.get('description'),
        };
        apiFetch('/api/projects/', { method: 'POST', body: JSON.stringify(payload) })
            .then(() => {
                showMessage('project-message', 'Project created successfully.');
                projectForm.reset();
                loadProjects();
                loadSummary();
            })
            .catch(error => showMessage('project-message', error.detail || 'Project creation failed', true));
    });

    taskForm.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(taskForm);
        const payload = {
            title: formData.get('title'),
            description: formData.get('description'),
            project: Number(formData.get('project')),
            due_date: formData.get('due_date') || null,
            priority: formData.get('priority'),
        };
        apiFetch('/api/tasks/', { method: 'POST', body: JSON.stringify(payload) })
            .then(() => {
                showMessage('task-message', 'Task created successfully.');
                taskForm.reset();
                loadTasks();
                loadSummary();
            })
            .catch(error => showMessage('task-message', error.detail || 'Task creation failed', true));
    });

    loadSummary();
    loadProjects();
    loadTasks();
}
