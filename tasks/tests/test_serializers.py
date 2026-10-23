from django.test import TestCase
from tasks.task_serializer import TaskSerializer


class TaskSerializerTest(TestCase):

    def test_valid_task_data(self):
        data = {
            "title": "Write unit tests",
            "description": "Testing serializer validation",
            "priority": "high"
        }

        serializer = TaskSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_short_title_is_invalid(self):
        data = {
            "title": "AB",
            "description": "Testing short title",
            "priority": "high"
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_invalid_priority(self):
        data = {
            "title": "Write unit tests",
            "description": "Testing invalid priority",
            "priority": "URGENT"
        }

        serializer = TaskSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("priority", serializer.errors)
