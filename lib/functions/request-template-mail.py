import os
import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('mail-request')
logger.setLevel(logging.INFO)

ses = boto3.client('ses')

payload_example = {
  "Source": "Jake <jakemraz100@gmail.com>",
  "Template": "test1", # TemplateName at SES
  "TemplateData": "{ \"name\":\"Alejandro\", \"favoriteanimal\": \"alligator\" }",
  "Destination": ["jakemraz100@gmail.com"]
}

def handler(event, context):
  try:
    response = ses.send_templated_email(
      Source= event["Source"],
      Template= event["Template"],
      ConfigurationSetName= "TestConfigSet",
      TemplateData= event["TemplateData"],
      Destination= {
        "ToAddresses": event["Destination"]
      }
    )
  except ClientError as e:
    return {
      'statusCode': 500,
      'body': json.dumps(e.response)
    }
    
  return {
      'statusCode': 200,
      'body': json.dumps(response)
  }
