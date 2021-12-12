import boto3
import json
import datetime
import env
import uuid

def format_date(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
        
def lambda_handler(event, context):
    
    sqs_url = env.url
    sqs_client = boto3.client(
        "sqs",
        region_name="eu-west-1"
        )
    
    id = uuid.uuid4()
    publish_object = "Message id %s" % str(id)
    response = sqs_client.send_message(MessageBody=publish_object,
        QueueUrl=sqs_url,
        MessageAttributes={
            "transaction_type": {"DataType": "String", 
                "StringValue": "pub_sub"},
            "transaction_id": {"DataType": "String",
                "StringValue": str(id)},
            "sent_time": {"DataType": "String",
                "StringValue": format_date(datetime.datetime.utcnow())}
        })
    
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }