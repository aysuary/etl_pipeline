from datetime import datetime
from src.extract import extract_transactional_data
from src.transform import identify_and_remove_duplicates
from src.load import df_to_s3

start_time = datetime.now()

#this library is beaing used toread from the .env file
import os
from dotenv import load_dotenv
load_dotenv()

#reading the variables from the .env file
dbname = os.getenv("dbname")
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")

# reading the variables that will connect to s3
key="transformations_final/aa_online_trans_transformed.pkl"
s3_bucket="sep-bootcamp"
aws_access_key_id=os.getenv("aws_access_key_id")
aws_secret_access_key=os.getenv("aws_secret_access_key_id")

#step 1 :extract and transform the data
print("\nExtracting the data from redshift...")
ot=extract_transactional_data(dbname, host, port, user, password)

#step2 : identify and remove duplicate
print("\nIdentifying and removing duplicates")
ot_wout_duplicates = identify_and_remove_duplicates(ot)

#step3 : load data to s3
print("\nLoading data to s3 bucket")
df_to_s3(ot_wout_duplicates, key, s3_bucket, aws_access_key_id, aws_secret_access_key)

# if you want to you can calculate
execution_time = datetime.now() - start_time
print(f"Total execution time (hh:mm:ss) {execution_time}")

