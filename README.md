# aws_kinesis_example

Here is an example of a python program that pulls data from an AWS Kinesis stream and writes it to an AWS Redshift SQL table using AWS Secrets Manager to store the credentials:

This program assumes that the secrets for the Redshift database are stored in AWS Secrets Manager in the following format:

`
{
    "username": "username",
    "password": "password",
    "host": "host",
    "port": "port",
    "dbname": "dbname"
}
`

You will need to replace my_stream and my_table with the appropriate names for your Kinesis stream and Redshift table. You will also need to specify the structure of the data in the Redshift table (i.e. the names and data types of the columns) in the INSERT INTO statement.
