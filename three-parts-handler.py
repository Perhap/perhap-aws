import json
import boto3

dynamodb = boto3.resource('dynamodb')
events = dynamodb.Table('Perhap-Events')
entities = dynamodb.Table('Perhap-Entities')

def time_order_uuid(id):
    time_low,time_mid,time_hi_and_version,clock_seq_hi_and_reserved,clock_seq_low = id.split("-")
    return time_hi_and_version + "-" + time_mid + "-" + time_low + "-" + clock_seq_hi_and_reserved + "-" + clock_seq_low

def get_events(event, context):
    if event['pathParameters']['entity'] == 'keys':
        return get_keys(event, context)
    elif version1(event['pathParameters']['entity']):
        return get_event(event, context)
    elif event['queryStringParameters']:
        if event['queryStringParameters'].get('following'):
            return get_filtered_entity(event, context)
        else: return get_entity(event, context)
    else:
        return get_entity(event, context)

def version1(id):
    return id[14] == '1'

def get_keys(event, context):
    domain = event['pathParameters']['domain']
    result = entities.query(
        ExpressionAttributeValues={":domain": domain},
        KeyConditionExpression='PerhapDomain = :domain',
        ProjectionExpression='Entity'
    )

    list_of_values = [d['Entity'] for d in result['Items']]

    response = {
        "statusCode": result["ResponseMetadata"]["HTTPStatusCode"],
        "body": json.dumps({"keys": list_of_values})
    }

    return response


def get_event(event, context):
    entity = event['pathParameters']['domain']
    event_id = event['pathParameters']['entity']
    ordered_id = time_order_uuid(event_id)

    result = events.query(
        ExpressionAttributeValues={":ordered_id": ordered_id, ":entity": entity},
        KeyConditionExpression='OrderedId = :ordered_id and Entity = :entity'
    )

    response = {
        "statusCode": result["ResponseMetadata"]["HTTPStatusCode"],
        "body": json.dumps(result['Items'])
    }

    return response

def get_entity(event, context):
    entity = event['pathParameters']['entity']

    result = events.query(
        ExpressionAttributeValues={":entity": entity},
        KeyConditionExpression='Entity = :entity',
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response

def get_filtered_entity(event, context):
    entity = event['pathParameters']['entity']
    following = event['queryStringParameters']['following']
    filter_after = time_order_uuid(following)

    result = events.query(
        ExpressionAttributeValues={":entity": entity, ":filtered": filter_after},
        KeyConditionExpression='Entity = :entity and OrderedId > :filtered'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
