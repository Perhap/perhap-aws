import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Perhap-Events')

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
