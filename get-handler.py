import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Perhap-Events')

def version1(id):
    return id[14] == '1'

def get_events(event, context):
    v1 = version1(event['pathParameters']['entity'])
    if v1:
        return get_event(event, context)
    else:
        return get_entity(event, context)

def get_event(event, context):
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

def get_entity(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    entity = event['pathParameters']['entity']

    sort_key= domain + "|" + entity

    result = table.query(
        ExpressionAttributeValues={":sort_key": sort_key, ":realm": realm},
        KeyConditionExpression='Realm = :realm and begins_with(RangeId, :sort_key)'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response

def domain(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']

    result = table.query(
        ExpressionAttributeValues={":domain": domain, ":realm": realm},
        KeyConditionExpression='Realm = :realm and begins_with(RangeId, :domain)'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
