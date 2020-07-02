import boto3

SUBJECT = "Amazon SES Test (SDK for Python)"

CHARSET = 'UTF-8'
BODY_HTML = '''<html>
<head></head>
<body>
  <h1>For {} {} Test</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
'''

BODY_TEXT = ("For {} {} Test\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )

ses = boto3.client('ses')

def handler(event, context):

  email = event['email']
  sender = event['sender']
  foo = event['foo']
  bar = event['bar']

  response = ses.send_email(
    Destination={
        'ToAddresses': [email],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': CHARSET,
                'Data': BODY_HTML.format(foo, bar),
            },
            'Text': {
                'Charset': CHARSET,
                'Data': BODY_TEXT.format(foo, bar),
            },
        },
        'Subject': {
            'Charset': CHARSET,
            'Data': SUBJECT,
        },
    },
    Source=sender
  )
  print(response)



payload = {
  'sender': "Jakemraz <jakemraz100@gmail.com>",
  'email': 'jakemraz100@gmail.com',
  'foo': 'hi',
  'bar': 'bye'
}
