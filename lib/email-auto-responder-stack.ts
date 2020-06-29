import * as cdk from '@aws-cdk/core';
import * as path from 'path';
import * as iam from '@aws-cdk/aws-iam';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';

export class EmailAutoResponderStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const templateBucket = new s3.Bucket(this, 'TemplateBucket');

    const role = new iam.Role(this, `EMailAutoResponderLambdaRole`, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonSESFullAccess' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess' },
      ]
    });
    
    new lambda.Function(this, `CreateTemplateFunction`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, './functions')),
      description: `CreateTemplateFunction`,
      handler: 'create-template.handler',
      role,
      timeout: cdk.Duration.seconds(30),
      environment: {
        TEMPLATE_BUCKET: templateBucket.bucketName
      }
    });

    new lambda.Function(this, `RequestTemplateMailFunction`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, './functions')),
      description: `RequestTemplateMailFunction`,
      handler: 'request-template-mail.handler',
      role,
      timeout: cdk.Duration.seconds(30)
    });
  }
}
