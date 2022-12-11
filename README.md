# aws_kinesis_example

The file `main.py` is an example Python program using AWS Secrets Manager to hold credentials for all AWS services and pull data from an AWS Kinesis stream, then write it to an AWS Redshift SQL table.

This code assumes that you have already stored the necessary credentials and connection information for your AWS services in AWS Secrets Manager. It uses the `boto3` library to interact with AWS services and the `json` library to parse the secret values from AWS Secrets Manager.

To use this code, you will need to replace the placeholders (e.g. `my-secrets`, `my-stream`, `my_table`) with the actual names and values for your AWS resources. You may also need to modify the code to handle any additional features or requirements of your specific use case.