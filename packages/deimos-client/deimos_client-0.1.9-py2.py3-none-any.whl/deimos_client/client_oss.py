import oss2 as oss
import logging
import os
from .file_management import FileManagement


class OSSFileClient(FileManagement):
    def __init__(self, auth_info, uuid):
        super().__init__(uuid)
        internal_address = auth_info["endpoint"].replace(".aliyuncs", "-internal.aliyuncs")
        if self.check_connection(internal_address):
            auth_info["endpoint"] = internal_address
        self.auth_info = auth_info
        auth = oss.StsAuth(auth_info["accessKeyId"], auth_info["accessKeySecret"], auth_info["securityToken"])
        self.bucket = oss.Bucket(auth, auth_info["endpoint"], auth_info["bucket"])

    def download_file(self, path, file=None):
        logging.info('download file from %s....', path)
        if file:
            self.bucket.get_object_to_file(self.uuid + '/' + path, file)
        else:
            return self.bucket.get_object(self.uuid + '/' + path).read()

    def upload_file(self, path, filename=None, filestream=None):
        logging.info('upload file to %s....', path)
        if filename is None and filestream is None:
            raise ValueError("filename and filestream cannot be both None.")
        if filename is not None:
            self.bucket.put_object_from_file(self.uuid + '/' + path, filename)
        else:
            self.bucket.put_object(self.uuid + '/' + path, filestream)
        self.uploaded_files.append(path)

    def list_files(self, path):
        return self.bucket.list_objects(self.uuid + '/' + path).object_list

    def upload_folder(self, path, folder):
        for root, dir, files in os.walk(folder):
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = self.uuid + '/' + path + '/' + file
                self.bucket.put_object_from_file(remote_path, local_path)

    def check_file_exists(self, path):
        return self.bucket.object_exists(self.uuid + '/' + path)

    def delete_files(self, path):
        for obj in oss.ObjectIterator(self.bucket, prefix=self.uuid + '/' + path):
            self.bucket.delete_object(obj.key)

    def copy_file(self, src, tgt):
        self.bucket.copy_object(self.auth_info["bucket"], self.uuid + '/' + src, self.uuid + '/' + tgt)
