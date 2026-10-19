
from locust import HttpUser, task, between


class TaskManagerUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.headers.update({
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkyMDgzMDIyLCJpYXQiOjE3OTE5OTY2MjIsImp0aSI6IjA0NzkwODliOWU2ODRiY2JhZDY5MzE3ZjZkNjNiMWM2IiwidXNlcl9pZCI6IjEifQ.BOM1DmQM2pQpRbXzkY3DE11WeNN1e3bE8mvZ9bn0M4A"
        })

    @task
    def view_tasks(self):
        self.client.get(
            "/api/v1/tasks/",
            name="GET /api/v1/tasks/"
        )
