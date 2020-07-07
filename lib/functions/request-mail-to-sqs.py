import os
import boto3
import logging
import json
from botocore.exceptions import ClientError

logger = logging.getLogger('request-mail-to-sqs')
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']




def handler(event, context):

  print(QUEUE_URL)
  try:
    response = sqs.send_message(
      QueueUrl=QUEUE_URL,
      MessageBody='AUTO_RESPONDER',
      MessageAttributes={
        'Source': {
          'StringValue': event['Source'],
          'DataType': 'String'
        },
        'Template': {
          'StringValue': event['Template'],
          'DataType': 'String'
        },
        'TemplateData' : {
          'StringValue': event['TemplateData'],
          'DataType': 'String'
        },
        'TargetUserId' : {
          'StringValue': event['TargetUserId'],
          'DataType': 'String'
        },
        'PinpointApplicationId' : {
          'StringValue': event['PinpointApplicationId'],
          'DataType': 'String'
        }
      }
    )
  except ClientError as e:
    logger.error(e.response['Error']['Message'])

  return {
      'statusCode': 200,
      'body': json.dumps(response)
  }


sample_payload = {
  "Source": "Jake <jakemraz100@gmail.com>",
  "Template": "test1", # TemplateName at SES
  "TemplateData": "{\"name\":\"Alejandro\",\"favoriteanimal\":\"alligator\"}",
  #"Destination": "jakemraz100@gmail.com",
  "TargetUserId": '25667',
  "PinpointApplicationId": "blahblah"
}

# handler(sample_payload, None)