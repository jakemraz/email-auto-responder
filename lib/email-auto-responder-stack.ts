import * as cdk from '@aws-cdk/core';
import * as path from 'path';
import * as sqs from '@aws-cdk/aws-sqs';
import * as iam from '@aws-cdk/aws-iam';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources'

export class EmailAutoResponderStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const templateBucket = new s3.Bucket(this, 'TemplateBucket');

    const role = new iam.Role(this, `EMailAutoResponderLambdaRole`, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonSESFullAccess' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonSQSFullAccess' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess' },
      ],
      inlinePolicies: {
        'pinpoint-policy': new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: ['mobiletargeting:GetUserEndpoints'],
              resources: ['*']
            })
          ]
        })
      }
    });

    const dlq = new sqs.Queue(this, `DeadLetterQueue`, {
      retentionPeriod: cdk.Duration.days(1),
    });
    const mailQueue = new sqs.Queue(this, `MailQueue`, {
      deadLetterQueue: {
        queue: dlq,
        maxReceiveCount: 3,
      },
    });

    const requestMailToSqsFn = new lambda.Function(this, `RequestMailToSqsFunction`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, './functions')),
      description: `RequestMailToSqsFunction`,
      handler: 'request-mail-to-sqs.handler',
      role,
      timeout: cdk.Duration.seconds(30),
      environment: {
        QUEUE_URL: mailQueue.queueUrl
      }
    });
    
    
    new lambda.Function(this, `CreateTemplateFunction`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, './functions')),
      description: `CreateTemplateFunction`,
      handler: 'create-template.handler',
      role,
      timeout: cdk.Duration.seconds(30),
      environment: {
        TEMPLATE_BUCKET: templateBucket.bucketName,
        QUEUE_URL: mailQueue.queueUrl
      }
    });

    const requestFn = new lambda.Function(this, `PollTemplateMailFunction`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      functionName: 'PollTemplateMailFunction',
      code: lambda.Code.fromAsset(path.resolve(__dirname, './functions')),
      description: `PollTemplateMailFunction`,
      handler: 'poll-template-mail.handler',
      role,
      deadLetterQueueEnabled: true,
      deadLetterQueue: dlq,
      timeout: cdk.Duration.seconds(30),
      environment: {
        QUEUE_URL: mailQueue.queueUrl
      }
    });
    requestFn.addEventSource(new SqsEventSource(mailQueue, {batchSize: 10}));
  }
}
