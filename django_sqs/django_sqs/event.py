import json
import boto3

def lambda_handler(event, context):
    # Extract SQS message from the Lambda event
    print(json.dumps(event))
    sqs_message_body = event.get('Records', [])
    print(sqs_message_body)
    # Process SQS messages
    for record in event.get('Records', []):
        # Extract SQS message body
        sqs_message = record.get('body', '')
        print(sqs_message)
        # Check if the SQS message body is empty
        if not sqs_message:
            print("Empty SQS message body received.")
            continue

        try:
            # Assuming the SQS message contains JSON data
            data = json.loads(sqs_message)

            # Ensure that data is a dictionary
            if not isinstance(data, dict):
                print("Invalid data format. Expected a dictionary.")
                continue

            # Store data in DynamoDB
            dynamodb_table_name = 'Employee'
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(dynamodb_table_name)

            # Assuming 'data' is a dictionary that you want to store in DynamoDB
            response = table.put_item(Item=data)
            print("Data stored in DynamoDB:", response)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            # Handle the error or log it as needed

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }
