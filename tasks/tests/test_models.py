from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task
from projects.models import Project


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!"
        )

        self.project = Project.objects.create(
            name="Testing Project",
            description="Project for testing"
        )

    def test_task_creation(self):
        task = Task.objects.create(
            title="Write unit tests",
            priority="HIGH",
            assigned_to=self.user,
            project=self.project
        )

        self.assertEqual(task.title, "Write unit tests")
        self.assertEqual(task.priority, "HIGH")
        self.assertEqual(task.assigned_to, self.user)
        self.assertEqual(task.project, self.project)

        self.assertTrue(
            Task.objects.filter(id=task.id).exists()
        )
