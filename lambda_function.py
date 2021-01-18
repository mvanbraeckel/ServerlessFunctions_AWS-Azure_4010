
'''
@author : Mitchell Van Braeckel
@id : 1002297
@date : 11/20/2020
@version : python 3.8-32 / python 3.8.5
@course : CIS*4010 Cloud Computing
@brief : A3 - Serverless Functions: Cloud System 1 - AWS ; lambda_function.py

@note :
    Description: Used the generated template from AWS Lambda service for S3 buckets using python code
        - modified it to make sure it logs and copies the uploaded file(s) to the "backup" S3 bucket
'''

############################################# IMPORTS #############################################

import json
import urllib.parse
import boto3

############################################ CONSTANTS ############################################

SRC_BUCKET_NAME = "a3cis4010-mvanbrae"
DEST_BUCKET_NAME = "copytwomvanbrae"

############################## STATE VARIABLES, INITIALIZATION, MAIN ##############################

def main():
    #globals
    global s3_client
    global s3_resource

    print("Loading function...")

    s3_client = boto3.client("s3")
    s3_resource = boto3.resource("s3")

############################################ FUNCTIONS ############################################

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and log
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        # LOGS: bucket, key, content type, entire response separate
        print(f"BUCKET: {bucket}, KEY: {key}, CONTENT_TYPE: {response['ContentType']}")
        print(f"RESPONSE: {response}")
    except Exception as e:
        print(e)
        print(f"Error getting object '{key}' from bucket '{bucket}'. Make sure they exist and your bucket is in the same region as this function.")
        raise e

    # Copy object to backup bucket
    try:
        s3_client.copy_object(
            CopySource={
                'Bucket': bucket,
                'Key': key
            },
            Bucket=DEST_BUCKET_NAME,
            Key=key
        )
        print(f"...Successfully backed-up '{key}' from '{bucket}' to '{DEST_BUCKET_NAME}'")
        return response['ContentType']
    except Exception as e:
        print(e)
        print(f"Error copying object '{key}' from bucket '{bucket}' to bucket '{DEST_BUCKET_NAME}'. Make sure they exist and your buckets are in the same region as this function.")
        raise e

############################################# HELPERS #############################################

###################################################################################################

main()
