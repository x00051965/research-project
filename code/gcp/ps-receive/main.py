from google.cloud import firestore
import base64
import datetime
import json

def receive(event, context):

    attributes = event['attributes']
    data = {
        u'id': attributes['transaction_id'],
        u'function_send_time': attributes['sent_time'],
        u'queue_receive-time': context.timestamp,
        u'function_receive_time': datetime.datetime.utcnow().isoformat(),
        u'message': base64.b64decode(event['data']).decode('utf-8')
    }
    # Add a new doc in collection 'message_details' with ID 'transactionId'
    db = firestore.Client()
    doc_ref = db.collection(u'message_details').document()
    doc_ref.set(data)
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }