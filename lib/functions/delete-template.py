import os
import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('delete-template')
logger.setLevel(logging.INFO)

ses = boto3.client('ses')

def handler(event, context):
  print(event)
  try:

    template_name = event['TemplateName']
    response = ses.delete_template(TemplateName = template_name)
  except Exception as e:
    return {
      'statusCode': 500,
      'body': json.dumps(e)
    }
    
  return {
      'statusCode': 200,
      'body': json.dumps(response)
  }

sample_payload = {
  "TemplateName": "test2"
}

#handler(sample_payload, None)
