import boto3
import json
import datetime
import env
import uuid

def format_date(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def lambda_handler(event, context):
    
    topic_arn = env.arn
    sns_client = boto3.client(
        "sns",
        region_name="eu-west-1"
        )
        
    id = uuid.uuid4()
    publish_object = "Message id %s" % str(id)
    response = sns_client.publish(Message=publish_object,
        TopicArn=topic_arn,
        MessageAttributes={
            "transaction_type": {"DataType": "String", 
                "StringValue": "pub_sub"},
            "transaction_id": {"DataType": "String",
                "StringValue": str(id)},
            "sent_time": {"DataType": "String",
                "StringValue": format_date(datetime.datetime.utcnow())}
        },
        Subject='pub_sub')
    
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }