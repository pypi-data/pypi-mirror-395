from datetime import datetime
import pytz
import uuid
import json
from typing import Optional, Dict

from .log import adscale_log
from .services import ServiceEnum
from arcane.datastore import Client as DatastoreClient
from arcane.pubsub import Client as PubSubClient

PUBSUB_ACTIVITY_TRACKING_TOPIC = 'activity-tracker'


def send_tracking_information(
    email: str,
    service: str,
    function_name: str,
    origin: str,
    project: str,
    execution_time: float,
    additionnal_info: Optional[Dict],
    status_code: int,
    pubsub_client: PubSubClient,
    datastore_client: DatastoreClient) -> None:
    """ Send pubsub message to the tracking cloud function"""

    users_query = datastore_client.query(kind='users')
    users_query.add_filter('email', '=', email)
    if users_query is None:
        adscale_log(ServiceEnum.TRACKING, f'User {email} is not an Adscale User. Tracking info will not be saved.')
    else:
        timestamp = datetime.now(tz=pytz.timezone('Europe/Paris')).strftime("%Y-%m-%dT%H:%M:%SZ")
        insert_id = str(uuid.uuid4())

        pubsub_client.push_to_topic(
            project=project,
            topic_name=PUBSUB_ACTIVITY_TRACKING_TOPIC,
            parameters={'user_email': email,
                        'service': service,
                        'execution_time': execution_time,
                        'additionnal_info': json.dumps(additionnal_info) if additionnal_info is not None else None,
                        'status_code': status_code,
                        'timestamp': timestamp,
                        'function_name': function_name,
                        'insert_id': insert_id,
                        'origin': origin
                        }
        )
