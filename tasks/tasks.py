
from tasks.models import Task
from django.utils import timezone
import logging
from celery import shared_task
from django.db import transaction

from tasks.models import NotificationJob


@shared_task
def process_task_notification(idempotency_key):
    try:
        with transaction.atomic():
            job = NotificationJob.objects.select_for_update().get(
                idempotency_key=idempotency_key
            )

            if job.status == NotificationJob.Status.COMPLETED:
                return {
                    "message": "Job already completed",
                    "idempotency_key": idempotency_key,
                }

            job.status = NotificationJob.Status.PROCESSING
            job.attempts += 1
            job.last_error = ""
            job.save(
                update_fields=[
                    "status",
                    "attempts",
                    "last_error",
                    "updated_at",
                ]
            )

    except NotificationJob.DoesNotExist:
        return {
            "message": "Notification job not found",
            "idempotency_key": idempotency_key,
        }

    try:
        # Simulate notification processing for now.
        # Replace this with the actual notification logic later.
        result_message = "Notification processed successfully"

        with transaction.atomic():
            job = NotificationJob.objects.select_for_update().get(
                idempotency_key=idempotency_key
            )
            job.status = NotificationJob.Status.COMPLETED
            job.save(update_fields=["status", "updated_at"])

        return {
            "message": result_message,
            "idempotency_key": idempotency_key,
        }

    except Exception as exc:
        NotificationJob.objects.filter(
            idempotency_key=idempotency_key
        ).update(
            status=NotificationJob.Status.FAILED,
            last_error=str(exc),
        )
        raise


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def retry_demo_task(self):
    try:
        print("Attempting background task...")

        raise ConnectionError("Temporary service failure")

    except ConnectionError as exc:
        print(f"Task failed: {exc}")
        raise self.retry(exc=exc)


logger = logging.getLogger(__name__)


@shared_task(bind=True)
def monitored_notification_task(self, task_id):
    logger.info(
        "Notification task started",
        extra={
            "celery_task_id": self.request.id,
            "task_id": task_id,
        },
    )

    try:
        # Simulate notification processing
        message = f"Notification processed for task {task_id}"

        logger.info(
            "Notification task completed",
            extra={
                "celery_task_id": self.request.id,
                "task_id": task_id,
            },
        )

        return {
            "status": "COMPLETED",
            "task_id": task_id,
            "message": message,
        }

    except Exception:
        logger.exception(
            "Notification task failed",
            extra={
                "celery_task_id": self.request.id,
                "task_id": task_id,
            },
        )
        raise


logger = logging.getLogger(__name__)


@shared_task
def check_overdue_tasks():
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now().date()
    ).exclude(
        status="COMPLETED"
    )

    count = overdue_tasks.count()

    logger.info("Found %s overdue tasks", count)

    for task in overdue_tasks.iterator():
        logger.info(
            "Overdue task found: ID=%s, title=%s",
            task.id,
            task.title,
        )

    return {
        "overdue_tasks_count": count,
    }
