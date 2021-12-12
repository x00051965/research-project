import datetime
import boto3
import time
import json
import env

def delete_message(receipt_handle):
    sqs_client = boto3.client("sqs", region_name="eu-west-1")
    response = sqs_client.delete_message(
        QueueUrl=env.url,
        ReceiptHandle=receipt_handle,
    )
    print(response)

def lambda_handler(event, context):
    
    sqs_client = boto3.client("sqs", region_name="eu-west-1")
    response = sqs_client.receive_message(
        QueueUrl=env.url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=0,
        # MessageAttributeNames=["sent_time","transaction_id"]
        MessageAttributeNames=["All"],
        AttributeNames=["All"]
    )
    
    
    for record in response.get("Messages", []):
        message_json = json.dumps(record)
        message = json.loads(message_json)
        
        # get relevant data from response message
        # id - uuid generated by send function
        id = message['MessageAttributes']['transaction_id']['StringValue']
        # function_send_time
        function_send_time = message['MessageAttributes']['sent_time']['StringValue']
        # queue_receive_time
        dt_format = "%Y-%m-%d %H:%M:%S.%f"
        queue_receive_time = datetime.datetime.utcfromtimestamp((int(message['Attributes']['SentTimestamp']))/1000).strftime(dt_format)
        # function_receive_time
        function_receive_time = datetime.datetime.utcnow().isoformat()
        # message
        message = message['Body']
        
        # delete message from queue
        delete_message(record['ReceiptHandle'])
        
        # print("id: %s" % str(id))
        # print("function_send_time: %s" % str(function_send_time))
        # print("queue_receive_time: %s" % str(queue_receive_time))
        # print("function_receive_time: %s" % str(function_receive_time))
        # print("message: %s" % str(message))
        
        db = boto3.resource("dynamodb")
        table = db.Table(env.table_name)
    
        try:
            response = table.put_item(
                Item={
                    "id": str(id),
                    "function_send_time": str(function_send_time),
                    "queue_receive_time": str(queue_receive_time),
                    "function_receive_time": str(function_receive_time),
                    "message": str(message)
                })
        except:
            time.sleep(1)
            response = table.put_item(
                Item={
                    "id": str(id),
                    "function_send_time": str(function_send_time),
                    "queue_receive_time": str(queue_receive_time),
                    "function_receive_time": str(function_receive_time),
                    "message": str(message)
                })
        
                
    return {
        "statusCode": 200,
        "body": json.dumps("done")
    }