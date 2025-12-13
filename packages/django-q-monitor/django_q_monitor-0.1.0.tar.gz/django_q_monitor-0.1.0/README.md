# 🛡️ Django Q Monitor

A reusable Django app that provides a complete **REST API** to monitor and manage **Django Q2** tasks, schedules, and failures.

It decouples the monitoring logic from the backend, allowing you to build custom dashboards (React, Vue, Mobile) without exposing the Django Admin.

---

## 🚀 Features

* **Task Monitoring:** View execution history, status, args, and results.
* **Schedules:** View upcoming scheduled tasks (Cron/Repeated).
* **Failures:** Dedicated endpoint for failed tasks.
* **Interactivity:**
    * 🔄 **Retry:** Re-queue failed or finished tasks directly via API.
    * 🧹 **Cleanup:** Delete old tasks to free up database space.
* **Standard JSON:** Built on Django REST Framework.

---

## 📦 Installation

### 1. Install the package

You can install it directly from the source (or PyPI if published):
```bash
pip install django-q-monitor
# OR via git for the latest version
pip install git+https://github.com/YOUR_USERNAME/django-q-monitor.git
```

### 2. Add to Installed Apps

Add `q_monitor` and `rest_framework` to your `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_q',
    'q_monitor',  # <--- Add this
]
```

### 3. Include URLs

Map the API endpoints in your project's `urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    ...
    path('api/monitor/', include('q_monitor.urls')),
]
```

---

## 🔌 API Reference

By default, endpoints are restricted to Admin users (`IsAdminUser`).

### Tasks

| Method   | Endpoint                        | Description                                  |
|----------|---------------------------------|----------------------------------------------|
| `GET`    | `/api/monitor/tasks/`           | List all tasks (ordered by start time).      |
| `GET`    | `/api/monitor/tasks/{id}/`      | Retrieve task details.                       |
| `POST`   | `/api/monitor/tasks/{id}/retry/`| Action: Re-queue the task with original args.|
| `DELETE` | `/api/monitor/tasks/cleanup/`   | Action: Delete all finished/failed tasks.    |

### Schedules

| Method | Endpoint                      | Description                  |
|--------|-------------------------------|------------------------------|
| `GET`  | `/api/monitor/schedules/`     | List all scheduled jobs.     |
| `GET`  | `/api/monitor/schedules/{id}/`| Retrieve schedule details.   |

### Failures

| Method | Endpoint                   | Description               |
|--------|----------------------------|---------------------------|
| `GET`  | `/api/monitor/failures/`   | List only failed tasks.   |

---

## ⚙️ Configuration

No extra configuration is needed if Django Q is already set up. The API respects your existing `Q_CLUSTER` settings.

---

## 🛠️ Development

To run this package locally within another project:

1. Clone the repo.
2. Install in editable mode:
```bash
pip install -e /path/to/django-q-monitor
```

---

## 📄 License

MIT License - feel free to use and modify as needed.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.