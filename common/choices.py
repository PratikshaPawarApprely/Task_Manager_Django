
from django.db import models


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"

