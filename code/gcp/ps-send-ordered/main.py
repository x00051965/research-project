import datetime
import uuid
import json
from google.cloud import pubsub_v1

def publish_messages_with_custom_attributes(project_id: str, topic_id: str):
    #enable message ordering
    publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
    publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)

    topic_path = publisher.topic_path(project_id, topic_id)
    id = uuid.uuid4()
    data = f"Message id %s" % str(id)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, 
        data=data, 
        ordering_key="key1",
        transaction_type="pub_sub", 
        transaction_id=str(id),
        sent_time=str(datetime.datetime.utcnow())
    )

def send_ordered(request):
    x = publish_messages_with_custom_attributes("arch-itqa", "ps-topic-ordered")
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }