import os
import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('create-template')
logger.setLevel(logging.INFO)

ses = boto3.client('ses')
s3 = boto3.client('s3')


def handler(event, context):
  print(event)
  try:

    template_name = event['TemplateName']
    subject = event['Subject']
    filename = event['Filename']

    bucket = os.environ['TEMPLATE_BUCKET']
    response = s3.get_object(Bucket=bucket, Key=filename)
    obj = response['Body']
    html = str(obj.read().decode('utf-8'))

    template = {
      'TemplateName': template_name,
      'SubjectPart': subject,
      'HtmlPart': html
    }

    response = ses.create_template(Template = template)
  except ClientError as e:
    return {
      'statusCode': 500,
      'body': json.dumps(e.response)
    }
    
  return {
      'statusCode': 200,
      'body': json.dumps(response)
  }

sample_payload = {
  "TemplateName": "test2",
  "Subject": "주문접수안내2",
  "Filename": "m-011.html"
}

#handler(payload, None)
