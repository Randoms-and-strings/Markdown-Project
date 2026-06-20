import boto3

# Create an S3 client. not working yet
s3 = boto3.client('s3')

# List all buckets
response = s3.list_buckets()

print("Your S3 Buckets:")
for bucket in response['Buckets']:
    print(f"  - {bucket['Name']}")