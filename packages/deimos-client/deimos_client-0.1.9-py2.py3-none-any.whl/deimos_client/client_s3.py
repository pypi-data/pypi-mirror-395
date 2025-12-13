import boto3
import os
import logging
from .file_management import FileManagement

class FileListObjects:
    key: str
    def __init__(self, key):
        self.key = key

class S3FileClient(FileManagement):
    def __init__(self, auth_info, uuid):
        super().__init__(uuid)
        self.auth_info = auth_info
        self.client = boto3.client(
            's3',
            aws_access_key_id=auth_info["accessKeyId"],
            aws_secret_access_key=auth_info["accessKeySecret"],
            aws_session_token=auth_info["securityToken"],
            region_name=auth_info["region"],
            endpoint_url=auth_info["endpoint"],
        )
        self.bucket_name = auth_info["bucket"]

    def download_file(self, path, file=None):
        logging.info('download file from %s....', path)
        if file:
            self.client.download_file(self.bucket_name, self.uuid + '/' + path, file)
        else:
            return self.client.get_object(Bucket=self.bucket_name, Key=self.uuid + '/' + path)["Body"].read()

    def upload_file(self, path, filename=None, filestream=None):
        logging.info('upload file to %s....', path)
        if filename is None and filestream is None:
            raise ValueError("filename and filestream cannot be both None.")
        if filename is not None:
            self.client.upload_file(filename, self.bucket_name, self.uuid + '/' + path)
        else:
            self.client.put_object(Bucket=self.bucket_name, Key=self.uuid + '/' + path, Body=filestream)
        self.uploaded_files.append(path)

    def list_files(self, path):
        aws_response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.uuid + '/' + path)
        file_list = aws_response.get('Contents', [])
        return [FileListObjects(key=obj['Key']) for obj in file_list]

    def upload_folder(self, path, folder):
        for root, dir, files in os.walk(folder):
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = self.uuid + '/' + path + '/' + file
                self.client.upload_file(local_path, self.bucket_name, remote_path)

    def check_file_exists(self, path):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=self.uuid + '/' + path)
        except self.client.exceptions.ClientError:
            return False
        return True

    def delete_files(self, path):
        for obj in self.list_files(path):
            self.client.delete_object(Bucket=self.bucket_name, Key=obj.key)

    def copy_file(self, src, tgt):
        self.client.copy_object(
            Bucket=self.bucket_name,
            CopySource={'Bucket': self.bucket_name, 'Key': self.uuid + '/' + src},
            Key=self.uuid + '/' + tgt,
        )
