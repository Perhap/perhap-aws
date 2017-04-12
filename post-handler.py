import json
import boto3

dynamodb = boto3.resource('dynamodb')
events = dynamodb.Table('Perhap-Events')
# domains = dynamodb.Table('Perhap-Domains')
# entities = dynamodb.Table('Perhap-Entities')

def time_order_uuid(id):
    time_low,time_mid,time_hi_and_version,clock_seq_hi_and_reserved,clock_seq_low = id.split("-")
    return time_hi_and_version + "-" + time_mid + "-" + time_low + "-" + clock_seq_hi_and_reserved + "-" + clock_seq_low

def new_event(event, context):
    event_data = json.loads(event['body'])
    event_id = event['pathParameters']['event-id']
    domain = event['pathParameters']['domain']
    realm = event['pathParameters']['realm']
    entity = event['pathParameters']['entity']
    event_type = event['pathParameters']['event-type']
    time_order_id= time_order_uuid(event_id)
    range_id = domain + '|' + entity + '|' + time_order_id
    item= {
        'Realm': realm,
        'Domain': domain,
        'Entity': entity,
        'EventType': event_type,
        'EventId': event_id,
        'EventData': event_data,
        'RangeId': range_id,
        'OrderedId': time_order_id
    }

    add_event = events.put_item(Item = item)
    # add_domain = domains.put_item(Item = {'Realm': realm, 'Domain': domain})
    # add_entity = entities.put_item(Item = {'Domain': domain, 'Entity': entity})

    # kinesis.put_record("Perhap-Kinesis", json.dumps(user), "partitionkey")

    response = {
        "statusCode": add_event["ResponseMetadata"]["HTTPStatusCode"]
    }

    return response
