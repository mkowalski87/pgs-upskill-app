import boto3
from botocore.client import Config
from Exceptions import NotSupportedContentType
class FileStorageManager():
    bucket_name = 'mkowalski-upskill'

    def __init__(self):
        self.s3_res = boto3.resource('s3')
        self.s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))

    def upload_file(self, filename, data):
        self.s3_res.Bucket(FileStorageManager.bucket_name).put_object(Key=filename, Body=data)

    def get_preassigned_url(self, filename):
        response = self.s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': FileStorageManager.bucket_name,
                                                                'Key': filename},
                                                        ExpiresIn=60*60)
        return response

    @staticmethod
    def validate_content_type(type):
        types = ['application/pdf']
        if type not in types:
            raise NotSupportedContentType(type)
