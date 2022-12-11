import boto3
import os
import psycopg2

# Set the environment variables for your Kinesis stream and Redshift cluster
os.environ['KINESIS_STREAM_NAME'] = 'my-kinesis-stream'
os.environ['REDSHIFT_CLUSTER_ENDPOINT'] = 'my-cluster.abc123.us-east-1.redshift.amazonaws.com'
os.environ['REDSHIFT_CLUSTER_PORT'] = '5439'
os.environ['REDSHIFT_USERNAME'] = 'my-username'
os.environ['REDSHIFT_PASSWORD'] = 'my-password'

# Create a Kinesis client
kinesis_client = boto3.client('kinesis')

# Get the shard iterator
response = kinesis_client.get_shard_iterator(
    StreamName=os.environ['KINESIS_STREAM_NAME'],
    ShardId='shardId-000000000000', # Replace with the actual shard ID
    ShardIteratorType='TRIM_HORIZON'
)
shard_iterator = response['ShardIterator']

# Create a Redshift client
redshift_client = boto3.client('redshift')

# Connect to the Redshift cluster
conn = psycopg2.connect(
    host=os.environ['REDSHIFT_CLUSTER_ENDPOINT'],
    port=os.environ['REDSHIFT_CLUSTER_PORT'],
    user=os.environ['REDSHIFT_USERNAME'],
    password=os.environ['REDSHIFT_PASSWORD'],
    dbname='dev'
)

# Set up the cursor
cur = conn.cursor()

# Create the table
cur.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        field1 VARCHAR(255),
        field2 VARCHAR(255),
        field3 VARCHAR(255)
    )
""")

# Loop to read records from the Kinesis stream
while True:
    # Get the records from the stream
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,
        Limit=10
    )

    # Process the records
    records = response['Records']
    if records:
        for record in records:
            data = record['Data'].decode('utf-8')
            fields = data.split(',')

            # Insert the data into the table
            cur.execute("""
                INSERT INTO my_table (field1, field2, field3)
                VALUES (%s, %s, %s)
            """, (fields[0], fields[1], fields[2]))

        # Commit the changes to the table
        conn.commit()

    # Get the next shard iterator
    shard_iterator = response['NextShardIterator']

# Close the cursor and connection
cur.close()
conn.close()
