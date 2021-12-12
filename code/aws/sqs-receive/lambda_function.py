import datetime
import boto3
import time
import json
import env

def lambda_handler(event, context):
    
    for record in event['Records']:
        message_json = json.dumps(record)
        message = json.loads(message_json)
        # get relevant data from response message
        # id - uuid generated by send function
        id = message["messageAttributes"]["transaction_id"]["stringValue"]
        # function_send_time
        function_send_time = message["messageAttributes"]["sent_time"]["stringValue"]
        # queue_receive_time
        dt_format = "%Y-%m-%d %H:%M:%S.%f"
        queue_receive_time = datetime.datetime.utcfromtimestamp((int(message["attributes"]["SentTimestamp"]))/1000).strftime(dt_format)
        # function_receive_time
        function_receive_time = datetime.datetime.utcnow().isoformat()
        # message
        message = message["body"]
        
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