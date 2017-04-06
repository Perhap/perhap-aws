import json
import boto3

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
#
# def my_handler(event, context):
# message = 'Hello {} {}!'.format(event['first_name'],
#                                 event['last_name'])
# return {
#     'message' : 'hello world'
# }
#
# def new-event(event, context):
