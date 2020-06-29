#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { EmailAutoResponderStack } from '../lib/email-auto-responder-stack';

const app = new cdk.App();

new EmailAutoResponderStack(app, 'EmailAutoResponderStack');
