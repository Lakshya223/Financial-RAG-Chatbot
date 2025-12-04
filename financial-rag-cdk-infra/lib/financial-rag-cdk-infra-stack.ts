import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as dotenv from "dotenv";
dotenv.config();
import {
  DockerImageFunction,
  DockerImageCode,
  FunctionUrlAuthType,
  Architecture,
} from 'aws-cdk-lib/aws-lambda';

import { ManagedPolicy } from 'aws-cdk-lib/aws-iam';  
import { open } from 'fs';




export class FinancialRagCdkInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Function to handle the API requests. Uses same base image, but different handler.
    const apiImageCode = DockerImageCode.fromImageAsset("../image", {
      cmd: [ "app.main.handler" ],// need to change this.. 
      buildArgs: {
        platform: "linux/amd64",
      },
    });

    const apiFunction = new DockerImageFunction(this, "ApiFunc", {
      code: apiImageCode,
      memorySize: 256,
      timeout: cdk.Duration.seconds(60),
      architecture: Architecture.X86_64,
      environment: {
        OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
        OPENAI_BASE_URL: process.env.OPENAI_BASE_URL || "",
        OPENAI_CHAT_MODEL: process.env.OPENAI_CHAT_MODEL || "gpt-4.1-mini",
        OPENAI_EMBEDDING_MODEL: process.env.OPENAI_EMBEDDING_MODEL || "text-embedding-3-large",
        OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY || "",
        OPENROUTER_BASE_URL: process.env.OPENROUTER_BASE_URL || "",
        TABLE_NAME: process.env.TABLE_NAME || "",
        IS_USING_IMAGE_RUNTIME: "true",
      },
    });

        // Public URL for the API function.
    const functionUrl = apiFunction.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE,
    });

        // Output the URL for the API function.
    new cdk.CfnOutput(this, "FunctionUrl", {
      value: functionUrl.url,
    });

  }
}
