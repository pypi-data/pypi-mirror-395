import tos
import logging
import os

from sympy import false

from .file_management import FileManagement


class TOSFileClient(FileManagement):
    def __init__(self, auth_info, uuid):
        super().__init__(uuid)
        internal_address = auth_info["endpoint"].replace("volces", "ivolces")
        if self.check_connection(internal_address):
            auth_info["endpoint"] = internal_address
        self.auth_info = auth_info
        self.client = tos.TosClientV2(auth_info["accessKeyId"],
                                      auth_info["accessKeySecret"],
                                      auth_info["endpoint"],
                                      auth_info["region"],
                                      security_token=auth_info["securityToken"]
                                      )
        self.bucket = auth_info["bucket"]

    def download_file(self, path, file=None):
        logging.info('download file from %s....', path)
        if file:
            self.client.get_object_to_file(self.bucket, self.uuid + '/' + path, file)
        else:
            return self.client.get_object(self.bucket, self.uuid + '/' + path).read()

    def upload_file(self, path, filename=None, filestream=None):
        logging.info('upload file to %s....', path)
        if filename is None and filestream is None:
            raise ValueError("filename and filestream cannot be both None.")
        if filename is not None:
            self.client.put_object_from_file(self.bucket, self.uuid + '/' + path, filename)
        else:
            self.client.put_object(self.bucket, self.uuid + '/' + path, content=filestream)
        self.uploaded_files.append(path)

    def list_files(self, path):
        return self.client.list_objects_type2(self.bucket, self.uuid + '/' + path).contents

    def upload_folder(self, path, folder):
        for root, dir, files in os.walk(folder):
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = self.uuid + '/' + path + '/' + file
                self.client.put_object_from_file(self.bucket, remote_path, local_path)

    def check_file_exists(self, path):
        try:
            self.client.head_object(self.bucket, self.uuid + '/' + path)
        except tos.exceptions.TosClientError as e:
            print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
            raise e
        except tos.exceptions.TosServerError as e:
            if e.status_code == 404:
                return False
            else:
                print('fail with server error, code:{}, message:{}, request_id:{}, host_id:{}'.format(
                    e.code, e.message, e.request_id, e.host_id))
                raise e
        return True

    def delete_files(self, path):
        for obj in self.client.list_objects_type2(self.bucket, self.uuid + '/' + path).contents:
            self.client.delete_object(self.bucket, obj.key)

    def copy_file(self, src, tgt):
        self.client.copy_object(self.bucket, self.uuid + '/' + tgt, self.bucket, self.uuid + '/' + src)