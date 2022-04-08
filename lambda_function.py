# Import modules for API
import boto3
import json
from custom_encoder import CustomEncoder
import logging
import urllib3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create the client outside of the handler
dynamodbTableName = 'product-inventory' # Corresponding to DDB table created in AWS
dynamodb = boto3.resource('dynamodb') # Dynamo client, from boto3
table = dynamodb.Table(dynamodbTableName)

# Methods
getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
# Paths
healthPath = '/health'
productPath = '/product'
productsPath = '/products'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        get_API_data()
        response = buildResponse(200)
    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event['queryStringParameters']['productId'])
    elif httpMethod == getMethod and path == productsPath:
        response = getProducts()
    elif httpMethod == postMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = saveProduct(requestBody)
    elif httpMethod == patchMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = modifyProduct(requestBody['productId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = deleteProduct(requestBody['productId'])
    else:
        response = buildResponse(404, 'Not Found')

    return response
    
def get_API_data(post_id=5, get_path="http://jsonplaceholder.typicode.com/posts"):
    http = urllib3.PoolManager()
    data = [{"userId": None, "id": None, "title": None, "body": None}]
    try:
        r = http.request(
            "GET",
            get_path,
            retries=urllib3.util.Retry(2),
            fields={'id': post_id}
        )
        data = json.loads(r.data.decode("utf8").replace("'", '"'))
    except:
        print("API GET data error")
        
    # Save to DDB
    post_title = data[0]['title']
    post_body = data[0]['body']
    table.put_item(Item={
        'productId': '999999',
        'postTitle': post_title,
        'postBody': post_body
    })
    
    return data

def getProduct(productId):
    try:
        response = table.get_item(
            Key = {
                'productId': productId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        # Added lines of code

        # Replace productId with symbol/ticker
        stock_price = get_stock(productId)
        if stock_price:
          saveProduct(productId)
          return buildResponse(200, stock_price)

        else:
            return buildResponse(404, {'Message': 'ProductId %s not found' % productId})
    except:
        logger.exception('Error: unable to get product')

def getProducts():
    try:
        response = table.scan()
        result = response['Items']

        # If DDB is too large, 'LastEvalutedKey' will be returned in response
        # While loop to parse through responses
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'products': result
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error: unable to get products')

def saveProduct(requestBody):
    try:
        table.put_item(Item = requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': ' SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error: unable to save product')

def modifyProduct(productId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key = {
                'productId': productId
            },
            UpdateExpression = 'set %s = :value' % updateKey,
            ExpressionAttributeValues = {
                ':value': updateValue
            },
            ReturnValues = 'UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error: unable to modify product')

def deleteProduct(productId):
    try:
        response = table.delete_item(
            Key = {
                'productId': productId
            },
            ReturnValues = 'ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error: unable to delete product')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' # To allow cross region access
        }
    }

    if body: # User pass in a custom object
        # Object we get from DDB is decimals, not supported by default JSON encoder
        # Define CustomEncoder for float conversion
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response
