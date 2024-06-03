# S3 Category Extractor 
This lambda is intended to integrate within an AWS Knowledgebase (RAG) flow.  
For more information refer to: [Set up a data source for your knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html)

The function is triggered by S3 objecet creation event. It extracts category from the object key (last "folder" in the key).   
The extracted category is added to a metadata file which is placed in the same bucket.

Metadata path: <object_key>.metadata.json
Metadata file structure:  
{  
  "metadataAttributes": {  
    "${category}": "[extracted category]"    
  }  
}  

## Example:
S3 object created: files/pdf/my_document.pdf

That triggers an event that causes the creation of the following metadata:  
metadata object key: files/pdf/my_document.pdf.metadata.json  
  
To attach the lambda function to a specific S3 bucket:  
1. In the lambda console select "Add Trigger"  
2. Source: "S3"  
3. Select Bucket  
4. Event Type: s3:ObjectCreated:Put, s3:ObjectCreated:CompleteMultipartUpload  
5. Prefix: object key prefix (e.g. documents)  
  
Permissions:  
Besides AWSLambdaBasicExecutionRole add (e.g. inline profile):  
{  
"Version": "2012-10-17",  
"Statement": [  
  {  
    "Sid": "VisualEditor0",  
    "Effect": "Allow",  
    "Action": [  
        "s3:PutObject",  
        "s3:GetObject"  
    ],  
    "Resource": "arn:aws:s3:::<bucket name>/*"  
    }  
  ]  
}  
 


