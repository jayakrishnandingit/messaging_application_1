import functools
import logging

from pika_client.base import Connector
from pika_client.environment_variables import EnvironmentVariable
from pika_client.publishers import BasePubSubPublisher

LOGGER = logging.getLogger(__name__)


class EmailPublisher(BasePubSubPublisher):
    pass


def publish_message(connector, task):
    recepients = 
    msg = {
        'recepients': [u.email for u in task.users],
        'task': {'title': task.title, 'status': task.status}
    }
    LOGGER.info("Creating EmailPublisher.")
    publisher = EmailPublisher(
        connector,
        app_id='TASK_UPDATE',
        exchange='notifications_x',
        exchange_type='topic',
        routing_key='notifications.email.task')
    publisher.start()
    publisher.publish_message(msg)
    publisher.stop()
    LOGGER.info("Message send. Stopped EmailPublisher.")


def send_task_update_email(task):
    connector = Connector(EnvironmentVariable.AMQP_URL)
    callback = functools.partial(publish_message, connector, task)
    connector.register_callback('on_channel_open', callback)
    connector.run()