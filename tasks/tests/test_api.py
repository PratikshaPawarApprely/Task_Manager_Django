
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Group
from projects.models import Project
from tasks.models import Task

class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer_test",
            password="TestPass123!"
        )

        self.viewer_group, _ = Group.objects.get_or_create(
            name="Contributor"
        )
        self.user.groups.add(self.viewer_group)

        self.project = Project.objects.create(
            name="Test Project",
            description="Project for API testing"
        )

        self.client.force_authenticate(user=self.user)

    def test_task_list_api(self):
        url = reverse("task-list")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data
        )


    def test_create_task_api(self):
        url = reverse("task-list")

        data = {
            "title": "Test API task",
            "description": "Testing task creation",
            "priority": "high",
            "assigned_to": self.user.id,
            "project": self.project.id
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data
        )

    
    def test_update_task_api(self):
        task = Task.objects.create(
            title="Original task",
            description="Original description",
            priority="high",
            assigned_to=self.user,
            created_by=self.user,
            project=self.project
        )

        url = reverse("task-detail", kwargs={"pk": task.id})

        data = {
            "title": "Updated task"
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data
        )

        task.refresh_from_db()
        self.assertEqual(task.title, "Updated task")

    
    def test_contributor_cannot_update_another_users_task(self):
        another_user = User.objects.create_user(
            username="another_contributor",
            password="TestPass123!"
        )

        task = Task.objects.create(
            title="Another user's task",
            description="Must not be modified by this contributor",
            priority="high",
            assigned_to=another_user,
            created_by=another_user,
            project=self.project
        )

        url = reverse("task-detail", kwargs={"pk": task.id})

        response = self.client.patch(
            url,
            {"title": "Unauthorized update"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.data
        )

        task.refresh_from_db()
        self.assertEqual(task.title, "Another user's task")



    def test_delete_own_task_api(self):
        task = Task.objects.create(
            title="Task to delete",
            description="Testing task deletion",
            priority="high",
            assigned_to=self.user,
            created_by=self.user,
            project=self.project
        )

        url = reverse("task-detail", kwargs={"pk": task.id})

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            response.data
        )

        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )