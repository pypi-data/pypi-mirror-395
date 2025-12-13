from .client_oss import OSSFileClient
from .client_s3 import S3FileClient
from .client_tos import TOSFileClient


def get_file_client(auth_info, uuid):
    if auth_info["type"] == "oss":
        return OSSFileClient(auth_info, uuid)
    elif auth_info["type"] == "tos":
        return TOSFileClient(auth_info, uuid)
    elif auth_info["type"] == "s3":
        return S3FileClient(auth_info, uuid)
    else:
        raise ValueError("Unknown file client type.")