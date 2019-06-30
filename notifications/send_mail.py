import functools
import logging

from pika_client.base import Connector
from pika_client.environment_variables import EnvironmentVariable
from pika_client.publishers import BasePubSubPublisher

LOGGER = logging.getLogger(__name__)


class EmailPublisher(BasePubSubPublisher):
    pass


def publish_message(msg, connector, exchange_type='topic', routing_key='notifications.task.email'):
    LOGGER.info("Creating EmailPublisher.")
    publisher = EmailPublisher(
        connector,
        app_id='TASK_UPDATE',
        exchange='notifications_x',
        exchange_type=exchange_type,
        routing_key=routing_key)
    publisher.start()
    publisher.publish_message(msg)
    publisher.stop()
    LOGGER.info("Message send. Stopped EmailPublisher.")


def send_task_update_email(task):
    connector = Connector(EnvironmentVariable.AMQP_URL)
    msg = {
        'recepients': [u.email for u in task.users],
        'task': {'title': task.title, 'status': task.status}
    }
    callback = functools.partial(publish_message, msg, connector)
    connector.register_callback('on_channel_open', callback)
    connector.run()