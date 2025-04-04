import boto3
import pandas as pd
import io

# Define S3 bucket and file details
bucket_name = "hotel-reservation-unique-bucket"
file_key = "HotelReservations.csv"

# Initialize S3 client
s3 = boto3.client("s3")

# Get the CSV file object from S3
response = s3.get_object(Bucket=bucket_name, Key=file_key)

# Read the content of the file into a Pandas DataFrame
csv_content = response['Body'].read().decode('utf-8')
df = pd.read_csv(io.StringIO(csv_content))

# Print the first few rows of the DataFrame
print(df.head())

# COMMANDS
# python -m venv .venv
# source .venv/bin/activate
# pip install -e .
# sudo apt update
# sudo apt install awscli