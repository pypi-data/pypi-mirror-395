# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_provider_type_enum.yaml

from enum import Enum


class StorageProviderType(Enum):
    """Supported storage backends for storing and accessing 3D model files"""
    GOOGLE_DRIVE = 'google_drive'
    DROPBOX = 'dropbox'
    ONEDRIVE = 'onedrive'
    WEBDAV = 'webdav'
    SYNOLOGY_NAS = 'synology_nas'
    QNAP_NAS = 'qnap_nas'
    AWS_S3 = 'aws_s3'
    AZURE_BLOB = 'azure_blob'
    LOCAL_FILESYSTEM = 'local_filesystem'
    OTHER_CLOUD = 'other_cloud'
    OTHER_NAS = 'other_nas'
    SELF_HOSTED = 'self_hosted'
    MINIO = 'minio'
    SFTP = 'sftp'
    THINGIVERSE = 'thingiverse'
    MYMINIFACTORY = 'myminifactory'
