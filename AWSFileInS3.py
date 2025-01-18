  

# 2. Code an AWS Lambda function to store a document or PDF file in an S3 bucket.

import json
import base64
import boto3
from botocore.exceptions import ClientError
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda function to upload a document/PDF to S3
    
    Expected event structure:
    {
        "filename": "example.pdf",
        "fileContent": "<base64-encoded-file-content>",
        "contentType": "application/pdf"
    }
    """
    try:
        # Extract file information from event
        filename = event['filename']
        file_content = event['fileContent']
        content_type = event.get('contentType', 'application/pdf')
        
        # Configure S3 bucket
        bucket_name = 'YOUR_BUCKET_NAME'  # Replace with your bucket name
        
        # Decode base64 content
        decoded_content = base64.b64decode(file_content)
        
        # Generate S3 key (file path)
        s3_key = f'documents/{filename}'
        
        # Upload file to S3
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=decoded_content,
            ContentType=content_type,
            Metadata={
                'uploaded-by': context.function_name,
                'timestamp': context.aws_request_id
            }
        )
        
        logger.info(f"File uploaded successfully: {s3_key}")
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded successfully',
                'location': f's3://{bucket_name}/{s3_key}',
                'versionId': response.get('VersionId')
            })
        }
        
    except KeyError as e:
        logger.error(f"Missing required parameter: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Missing required parameters. Please provide filename and fileContent.'
            })
        }
        
    except ClientError as e:
        logger.error(f"S3 operation failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to upload file to S3',
                'details': str(e)
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }