
import os

from locust import HttpUser, between, task


class TaskManagerUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        token = os.getenv("LOCUST_ACCESS_TOKEN")

        if token:
            self.client.headers.update({
                "Authorization": f"Bearer {token}"
            })

    @task
    def view_tasks(self):
        self.client.get(
            "/api/v1/tasks/",
            name="GET /api/v1/tasks/"
        )
