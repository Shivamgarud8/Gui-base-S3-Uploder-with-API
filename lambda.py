import os
import json
import boto3

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET_NAME', 'shivam-lammbda-gui-save')

def lambda_handler(event, context):
    method = event.get("httpMethod", "")
    params = event.get("queryStringParameters") or {}

    # ✅ Handle CORS preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "CORS preflight success"})
        }

    # Check file name parameter
    filename = params.get("name")
    if not filename:
        return _response(400, {"error": "Missing 'name' parameter"})

    try:
        # Generate presigned URL for direct S3 upload
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': filename},
            ExpiresIn=3600
        )
        return _response(200, {"uploadURL": upload_url})

    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body)
    }
