import os
import boto3
from botocore.exceptions import ClientError
from .base_storage import BaseStorage

class S3Storage(BaseStorage):
    def __init__(self, bucket, region, access_key, secret_key):
        self.bucket = bucket
        self.region = region

        self.s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def upload(self, filepath, filename=None):
        if not filename:
            filename = os.path.basename(filepath)

        try:
            self.s3.upload_file(filepath, self.bucket, filename)

            return {
                "storage": "s3",
                "bucket": self.bucket,
                "filename": filename,
                "url": f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{filename}"
            }

        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    def delete(self, filename):
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=filename)
            return True
        except ClientError as e:
            raise Exception(f"S3 delete failed: {str(e)}")

    def generate_url(self, filename, expires=3600):
        try:
            return self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": filename},
                ExpiresIn=expires
            )
        except ClientError as e:
            raise Exception(f"S3 URL generation failed: {str(e)}")
