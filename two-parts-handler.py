import json
import boto3

dynamodb = boto3.resource('dynamodb')
events = dynamodb.Table('Perhap-Events')

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
            get_domain(event, context)
    else:
        return get_domain(event, context)

def get_keys(event, context):
    print('keys')

def get_domain(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']

    result = events.query(
        ExpressionAttributeValues={":domain": domain, ":realm": realm},
        KeyConditionExpression='Realm = :realm and begins_with(RangeId, :domain)'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response

def get_filtered_domain(event, context):
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    following = event['queryStringParameters']['following']
    filter_after = time_order_uuid(following)

    result = events.query(
        ExpressionAttributeValues={":sort_key": domain, ":realm": realm, ":filtered": filter_after},
        KeyConditionExpression='Realm = :realm and begins_with(RangeId, :sort_key)',
        FilterExpression='OrderedId > :filtered'
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
