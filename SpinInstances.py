import boto3
import json

def SpinClient():
    try:
        ec2_client = boto3.client("ec2")

        # Create EC2 instance
        instance = ec2_client.run_instances(
            ImageId= "ami-0c101f26f147fa7fd",
            InstanceType= "t2.micro",
            MinCount= 1,
            MaxCount= 1,
            KeyName= "vockey"
        )

        print(instance)

    except Exception as e:
        print(f"Error Spinning Client {e}")

def SpinBucket():
    try:
        s3_client = boto3.client("s3")

        bucket = s3_client.create_bucket(Bucket="mybucket-s2219349")

        print(bucket)

    except Exception as e:
        print(f"Error Spinning Bucket {e}")

def SpinCloudStack():
    try:
        cloudformation_client = boto3.client('cloudformation')

        cloudformation_template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "SQSQueue": {
                    "Type": "AWS::SQS::Queue",
                    "Properties": {
                        "QueueName": "sqs-queue-s2219349"
                    }
                },
                "DynamoDBTable": {
                    "Type": "AWS::DynamoDB::Table",
                    "Properties": {
                        "TableName": "dynamodb-table-s2219349",
                        "AttributeDefinitions": [
                            {
                                "AttributeName": "ImageName",
                                "AttributeType": "S"
                            }
                        ],
                        "KeySchema": [
                            {
                                "AttributeName": "ImageName",
                                "KeyType": "HASH"
                            }
                        ],
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5
                        }
                    }
                }
            }
        }

        # Create CloudFormation stack
        cloudformation_response = cloudformation_client.create_stack(
            StackName= "cloudformationstack-s2219349",
            TemplateBody=json.dumps(cloudformation_template),
            Capabilities=["CAPABILITY_NAMED_IAM"]
        )
    except Exception as e:
        print(f"Error Spinning CloudStack {e}")

if __name__ == "__main__":
    SpinClient()
    SpinBucket()
    SpinCloudStack()