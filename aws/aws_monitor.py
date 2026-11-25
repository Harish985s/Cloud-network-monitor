import boto3

def test_aws_connection():
    sts = boto3.client("sts", region_name="ap-south-1")
    identity = sts.get_caller_identity()
    print("AWS CONNECTION SUCCESSFUL")
    print("Account:", identity["Account"])
    print("User ARN:", identity["Arn"])

test_aws_connection()