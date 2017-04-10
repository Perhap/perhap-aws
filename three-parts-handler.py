import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Perhap-Events')

def get_events(event, context):
    if event['pathParameters']['entity'] == 'keys':
        return get_keys(event, context)
    elif version1(event['pathParameters']['entity']):
        return get_event(event, context)
    elif event['queryStringParameters']['following']:
        return get_filtered_entity(event, context)
    else:
        return get_entity(event, context)

def version1(id):
    return id[14] == '1'

def get_keys(event, context):
    print('keys')


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

def get_filtered_entity(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    entity = event['pathParameters']['entity']
    filtered = event['queryStringParameters']['following']

    sort_key= domain + "|" + entity

    result = table.query(
        ExpressionAttributeValues={":sort_key": sort_key, ":realm": realm, ":filtered": filtered},
        KeyConditionExpression='Realm = :realm and begins_with(RangeId, :sort_key)',
        FilterExpression='EventId > :filtered'
    )
