import io
from botocore.exceptions import NoCredentialsError, ClientError
import boto3
from fastapi import HTTPException, UploadFile

from helpers.constants import S3_DEFAULT_AVATAR
from config.config import settings
from helpers.http_status import StatusCode

s3_client = boto3.client(
    's3',
    region_name=settings.S3_REGION,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY
)


def upload_file_to_s3(key: str, file: UploadFile) -> str:
    try:
        minetype = file.content_type
        contents = file.file.read()
        temp_file = io.BytesIO()
        temp_file.write(contents)
        temp_file.seek(0)
        response = s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=temp_file,
            ContentType=minetype,
        )
        temp_file.close()
        return response
    except NoCredentialsError:
        raise Exception("S3 credentials not available.")


def generate_presigned_download_url(key: str, expiration: int = 3600) -> str:
    try:
        object_metadata = s3_client.get_object_attributes(Bucket=settings.S3_BUCKET,
                                                          Key=key,
                                                          ObjectAttributes=["ETag"])
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.S3_BUCKET,
                'Key': key,
            },
            ExpiresIn=expiration
        )
    except NoCredentialsError:
        raise Exception("S3 credentials not available.")
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'NoSuchKey' and "/avatar/" in key:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.S3_BUCKET,
                    'Key': S3_DEFAULT_AVATAR,
                },
                ExpiresIn=expiration
            )
        else:
            raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                                detail="Error while finding file")
    return presigned_url


# def delete_s3_object(object_key):
#     try:
#         s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=object_key)
#     except NoCredentialsError:
#         pass  # Handle error or logging here
