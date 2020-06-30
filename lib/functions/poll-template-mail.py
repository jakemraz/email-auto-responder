import os
import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('mail-request')
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')
ses = boto3.client('ses')
pinpoint = boto3.client('pinpoint')

QUEUE_URL = os.environ['QUEUE_URL']

# payload_example = {
#   "Source": "Jake <jakemraz100@gmail.com>",
#   "Template": "test1", # TemplateName at SES
#   "TemplateData": "{\"name\":\"Alejandro\",\"favoriteanimal\":\"alligator\"}",
#   "Destination": ["jakemraz100@gmail.com"]
# }

# event called by sqs

def handler(event, context):
  try:

    for record in event['Records']:
      logger.info(record)
      msg_attr = record['messageAttributes']
      source = msg_attr['Source']['stringValue']
      template = msg_attr['Template']['stringValue']
      template_data = msg_attr['TemplateData']['stringValue']
      target_user_id = msg_attr['TargetUserId']['stringValue']
      pinpoint_application_id = msg_attr['PinpointApplicationId']['stringValue']

      response = pinpoint.get_user_endpoints(
        ApplicationId= pinpoint_application_id,
        UserId= target_user_id
      )

      print(response)

      email = ""
      for item in response['EndpointsResponse']['Item']:
        if item['ChannelType'] == 'EMAIL' and item['Address'] is not None:
          email = item['Address']
          break

      print(email)

      response = ses.send_templated_email(
        Source= source,
        Template= template,
        ConfigurationSetName= "TestConfigSet",
        TemplateData= template_data,
        Destination= {
          "ToAddresses": [email]
        }
      )
      print(response)
  except ClientError as e:
    return {
      'statusCode': 500,
      'body': json.dumps(e.response)
    }
  else:
    logger.info("Email sent! Message ID:"),
    logger.info(response['MessageId'])
    sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=record['receiptHandle'],
    )
    
  return {
      'statusCode': 200,
      'body': json.dumps(response)
  }
