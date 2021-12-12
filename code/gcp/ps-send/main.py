import datetime
import uuid
import json
from google.cloud import pubsub_v1

def publish_messages_with_custom_attributes(project_id: str, topic_id: str):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    id = uuid.uuid4()
    data = f"Message id %s" % str(id)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, 
        data, 
        transaction_type="pub_sub", 
        transaction_id=str(id),
        sent_time=str(datetime.datetime.utcnow())
    )

def send(request):
    x = publish_messages_with_custom_attributes("arch-itqa", "pstopic")
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }
