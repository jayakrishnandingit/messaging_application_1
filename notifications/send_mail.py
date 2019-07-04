import functools
import logging
import json

from pika_client.base import Connector
from pika_client.environment_variables import EnvironmentVariable
from pika_client.publishers import BasePubSubPublisher

LOGGER = logging.getLogger(__name__)


class EmailPublisher(BasePubSubPublisher):
    def handle_acknowledged_message(self, method_frame):
        """
        Overriding this method to stop the service after a message is acknowledged.
        """
        self.stop()

    def encode_message_and_properties(self, message):
        properties = self.get_message_properties(content_type='application/json')
        message = json.dumps(message, ensure_ascii=False)
        return message, properties


def publish_message(msg, connector, exchange_type='topic', routing_key='notifications.email'):
    LOGGER.info("Creating EmailPublisher.")
    publisher = EmailPublisher(
        connector,
        app_id='TASK_UPDATE',
        exchange='notifications_x',
        exchange_type=exchange_type,
        routing_key=routing_key)
    callback = functools.partial(publisher.publish_message, msg)
    publisher.register_callback('on_exchange_declareok', callback)
    publisher.start()


def get_task_email_content(task):
    return '''Hi,

    Task {0.title} is updated with new status {0.status}.

    Cheers,
    Team
    '''.format(task)


def send_task_update_email(task):
    connector = Connector(EnvironmentVariable.AMQP_URL)
    msg = {
        'recepients': [u.email for u in task.users],
        'text': get_task_email_content(task)
    }
    callback = functools.partial(publish_message, msg, connector)
    connector.register_callback('on_channel_open', callback)
    connector.run()