import json
import boto3

dynamodb = boto3.resource('dynamodb')
events = dynamodb.Table('Perhap-Events')
domains = dynamodb.Table('Perhap-Domains')
entities = dynamodb.Table('Perhap-Entities')

def time_order_uuid(id):
    time_low,time_mid,time_hi_and_version,clock_seq_hi_and_reserved,clock_seq_low = id.split("-")
    return time_hi_and_version + "-" + time_mid + "-" + time_low + "-" + clock_seq_hi_and_reserved + "-" + clock_seq_low

def domain(event, context):
    if event['pathParameters']['domain'] == 'keys':
        return get_keys(event, context)
    elif event['queryStringParameters']:
        if event['queryStringParameters'].get('following'):
            return get_filtered_domain(event, context)
        else:
            return get_domain(event, context)
    else:
        return get_domain(event, context)

def get_keys(event, context):
    realm = event['pathParameters']['realm']
    result = domains.query(
        ExpressionAttributeValues={":realm": realm},
        KeyConditionExpression='Realm = :realm',
        ProjectionExpression='PerhapDomain'
    )

    list_of_values = [d['PerhapDomain'] for d in result['Items']]

    response = {
        "statusCode": 200,
        "body": json.dumps({"keys": list_of_values})
    }

    return response

def get_domain(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']

    all_entities = entities.query(
        ExpressionAttributeValues={":domain": domain},
        KeyConditionExpression='PerhapDomain = :domain',
        ProjectionExpression='Entity'
    )

    list_of_entities = [d['Entity'] for d in all_entities['Items']]

    results = []
    for entity in list_of_entities:

        result = events.query(
            ExpressionAttributeValues={":entity": entity},
            KeyConditionExpression='Entity = :entity',
        )

        results.append(result['Items'])

    list_of_events= [item for sublist in results for item in sublist]

    response = {
        "statusCode": 200,
        "body": json.dumps(list_of_events)
    }

    return response

def get_filtered_domain(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    following = event['queryStringParameters']['following']
    filter_after = time_order_uuid(following)

    all_entities = entities.query(
        ExpressionAttributeValues={":domain": domain},
        KeyConditionExpression='PerhapDomain = :domain',
        ProjectionExpression='Entity'
    )

    list_of_entities = [d['Entity'] for d in all_entities['Items']]

    results = []
    for entity in list_of_entities:

        result = events.query(
            ExpressionAttributeValues={":entity": entity, ":filtered": filter_after},
            KeyConditionExpression='Entity = :entity and OrderedId > :filtered'
        )

        results.append(result['Items'])

    list_of_events= [item for sublist in results for item in sublist]

    response = {
        "statusCode": 200,
        "body": json.dumps(list_of_events)
    }

    return response
