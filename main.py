import boto3
import json

# Set up AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

# Set up AWS Kinesis client
kinesis = boto3.client('kinesis')

# Set up AWS Redshift client
redshift = boto3.client('redshift')

# Retrieve the credentials from AWS Secrets Manager
secret = secrets_manager.get_secret_value(SecretId='my-secrets')
secrets = json.loads(secret['SecretString'])

# Use the credentials to connect to AWS Kinesis and AWS Redshift
kinesis.connect(aws_access_key_id=secrets['access_key'], aws_secret_access_key=secrets['secret_key'])
redshift.connect(dbname=secrets['database'], host=secrets['host'], port=secrets['port'], user=secrets['user'], password=secrets['password'])

# Pull data from the AWS Kinesis stream
response = kinesis.get_records(StreamName='my-stream')
data = response['Records']

# Insert the data into the AWS Redshift SQL table
for record in data:
    redshift.execute("INSERT INTO my_table VALUES (%s, %s)", record['field1'], record['field2'])
