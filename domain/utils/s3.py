import boto3
import os
import random
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()


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

def random_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION")
    )
    bucket = os.getenv("AWS_S3_BUCKET_NAME")
    prefix = 'song/'  # S3 내 노래 파일들이 있는 폴더 경로

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    contents = response.get('Contents', [])
    if not contents:
        raise HTTPException(status_code=400, detail="S3에 노래 파일이 없습니다.")

    # .wav 파일만 필터링
    song_files = [obj['Key'] for obj in contents if obj['Key'].endswith('.wav')]
    if not song_files:
        raise HTTPException(status_code=400, detail="S3에 .wav 파일이 없습니다.")

    chosen_song = random.choice(song_files)
    song_url = f"https://{bucket}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{chosen_song}"
    return song_url, chosen_song