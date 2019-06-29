import logging

from logging_setup import setup_logging
from messaging_application_1.tasks import Task, generate_task
from messaging_application_1.notifications.send_mail import send_task_update_email

setup_logging()
LOGGER = logging.getLogger(__name__)


def update_task(task_id):
    task = generate_task(task_id)
    task.status = Task.DONE
    send_task_update_email(task)
    LOGGER.info("Updated task %d." % task_id)


def main():
    update_task(1)


if __name__ == '__main__':
    main()