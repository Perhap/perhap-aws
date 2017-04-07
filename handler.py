import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Perhap-Events')

def new_event(event, context):
    event_data = event['body']
    event_id = json.loads(event['body'])['event-id']
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    entity = event['pathParameters']['entity']
    event_type = event['pathParameters']['event-type']
    range_id = domain + '|' + entity + '|' + event_id

    add_event = table.put_item(
        Item={
            'Realm': realm,
            'Domain': domain,
            'Entity': entity,
            'EventType': event_type,
            'EventId': event_id,
            'EventData': event_data,
            'RangeId': range_id
        }
    )

    body = {
        "inputBody": add_event,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
