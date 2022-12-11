import boto3
import psycopg2

# Get the secrets for the Redshift database from AWS Secrets Manager
secrets_manager = boto3.client("secretsmanager")
secrets = secrets_manager.get_secret_value(SecretId="redshift_secrets")

# Parse the secrets
username = secrets["username"]
password = secrets["password"]
host = secrets["host"]
port = secrets["port"]
dbname = secrets["dbname"]

# Create a connection to the Redshift database
conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=dbname,
    user=username,
    password=password
)

# Create a cursor object to execute queries
cur = conn.cursor()

# Get the Kinesis Streams client
kinesis_client = boto3.client("kinesis")

# Get the data from the Kinesis stream
response = kinesis_client.get_records(StreamName="my_stream")
records = response["Records"]

# Iterate over the records and insert them into the Redshift table
for record in records:
    cur.execute("INSERT INTO my_table VALUES (%s, %s)", (record["column1"], record["column2"]))

# Commit the changes to the Redshift table
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
