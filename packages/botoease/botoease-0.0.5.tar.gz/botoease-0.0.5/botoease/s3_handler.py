import boto3
from botocore.exceptions import NoCredentialsError
import os



class S3Handler:
    def __init__(self, bucket, region, access_key, secret_key):
        self.bucket = bucket
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def upload(self, filepath, filename=None):
        if filename is None:
            filename = os.path.basename(filepath)
        try:
            self.s3.upload_file(filepath, self.bucket, filename)
            return {
                "storage": "s3",
                "bucket": self.bucket,
                "filename": filename,
                "url": f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{filename}"
            }
        except FileNotFoundError:
            raise Exception("File not found")
        except NoCredentialsError:
            raise Exception("Invalid AWS credentials")
    
    def delete(self, filename):
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=filename)
            return True
        except Exception as e:
            raise Exception("Failed to delete file from S3")

    def generate_url(self, filename, expires=3600):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': filename},
                ExpiresIn=expires
            )
            return url
        except Exception as e:
            raise Exception("Failed to generate URL")        
