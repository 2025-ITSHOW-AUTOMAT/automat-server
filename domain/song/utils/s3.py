import boto3
import os

def upload_s3(file_path: str, s3_key: str) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION")
    )
    bucket = os.getenv("AWS_S3_BUCKET_NAME")
    s3.upload_file(file_path, bucket, s3_key)
    return f"https://{bucket}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{s3_key}"
