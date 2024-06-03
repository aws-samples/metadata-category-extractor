import json
import boto3
import os
from urllib.parse import unquote_plus

METADATA_SUFFIX = '.metadata.json'

s3 = boto3.client('s3')

def lambda_handler(event, context):
    metadata_template = {
        "metadataAttributes": {
            "${catalog}": None
        }
    }

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Object {object_key} uploaded. ")

    # Avoid recursive calls due to events triggered from putting metadata file into same bucket
    # Assumes files are stored in folders named after categories
    if object_key.endswith(METADATA_SUFFIX) or not "/" in object_key:
        return
    metadata_key = unquote_plus(object_key + METADATA_SUFFIX)
    category = unquote_plus(object_key.split('/')[-2])  
    print(f"Object {object_key} analyzed. Category {category} was identified")
    metadata_template["metadataAttributes"]["${catalog}"] = category
    print(f"Metadata {metadata_key} is created.")

    try:
        s3.put_object(
            Body=json.dumps(metadata_template),
            Bucket=bucket_name,
            Key=metadata_key
        )
    except Exception as e:
        print(f"Error creating metadata: {e}")
        raise e
