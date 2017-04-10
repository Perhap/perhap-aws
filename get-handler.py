import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Perhap-Events')

def version1(id):
    return id[14] == '1'

def get_events(event, context):
    if version1(event['pathParameters']['id']):
        get_event(event, context)
    else:
        get_entity(event, context)

def get_event(event, context):
    print(event)
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    event_id = event['pathParameters']['entity']

    result = table.query(
        IndexName= 'event-id',
        ExpressionAttributeValues={":event_id": event_id, ":realm": realm},
        KeyConditionExpression='EventId = :event_id and Realm = :realm'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
#
# def get-domain(event, context):
#
#     result = table.query(
#         Key={
#             'Realm': event['pathParameters']['realm'],
#             'Domain': event['pathParameters']['realm']
#         }
#     )
#
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(result[Items])
#     }
#
#     return response
