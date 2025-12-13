# SmoothGlue Django File Uploader

A Django app providing secure, pluggable uploads to S3, MinIO, or local storage with validation, checksums, and post-processing. Built for regulated and edge environments from the ground up.

## Overview

`smoothglue_file_uploader` simplifies the process of handling file uploads in a Django project. The core problem it solves is abstracting the storage backend, allowing developers to switch between local development, staging, and production environments without changing application code. You can configure it once in `settings.py` and have your file uploads seamlessly route to the correct storage solution.

### Key Features

*   **Multiple Storage Backends:** Natively supports Local Filesystem, Amazon S3, and MinIO.
*   **Easy Configuration:** A single settings dictionary to control all storage options.
*   **On-the-fly Validation:** Allows custom configurations to validate files prior to them being uploaded.
*   **Pluggable Permissions:** Customize access control for document operations (`get`, `patch`, `delete`) by providing your own permission class.
* **Ease of Access:** Easily upload, download, delete or duplicate files in any supported files stores.

## Installation

### Prerequisites

* Python 3.12+
* Django 4.2+
* Django REST Framework 3.14+

### Install App From PyPI Package (Official Use)

1. Before installing the package, make sure that there is a virtual environment set up inside of the Django project you want to install the app into.

2. Use pip and the following command inside the Django project:
   ```python
   pip install smoothglue_file_uploader
   ```

3. Update the `settings.py` file inside that Django project to point to the new app name:

   ```python
   INSTALLED_APPS = [
     "smoothglue_file_uploader",
     ...,
   ]
   ```


4. Update the `urls.py` file inside that Django project to point to the new app name: :

   ```python
   urlpatterns = [
     path("", include("smoothglue_file_uploader.urls")),
     ...,
   ]
   ```

5. Run the development server to confirm the project continues to work.

## Examples

### Usage Examples

#### Download
```python
    storage_provider, _ = get_storage_provider()
    doc = Document.objects.get(id=instance.id)

    data = storage_provider.download_document(doc.path)
```

#### Upload
```python
    storage_provider, _ = get_storage_provider()
    path = "foo/bar"
    storage_provider.upload_document(path, file_obj)
```

#### Delete
```python
    storage_provider, _ = get_storage_provider()
    doc = Document.objects.get(id=instance.id)

    storage_provider.delete_document(doc.path)
```

#### Duplicate
```python
    storage_provider, _ = get_storage_provider()
    old_doc = Document.objects.get(id=instance.id)
    new_uuid = str(uuid.uuid4())
    new_path = f"path/{new_uuid}"

    duplicate_success = storage_provider.duplicate_document(old_doc.path, new_path)
```

### API Examples

| URL Path    | HTTP Method | Description |
| -------- | ------- | ------- |
| `/`  | `GET`    | Lists documents. A `reference_id` (UUID) must be provided as a query parameter to retrieve all files associated with that ID. |
| `/` | `POST`     | Uploads a new file. The request must be a multipart form containing a `file` and a `reference_id`. |
| `/<uuid:file_id>/` | `GET`     | Downloads the content of the specified file. Access is controlled by the `DOCUMENT_PERMISSION_CLASS`. |
| `/<uuid:file_id>/` | `PATCH`     | Updates the metadata of the specified file. Access is controlled by the `DOCUMENT_PERMISSION_CLASS`. |
| `/<uuid:file_id>/` | `DELETE`     | Archives or deletes the specified file. Access is controlled by the `DOCUMENT_PERMISSION_CLASS`. |


### Settings Example

``` python
UPLOAD_STORAGE_PROVIDER_CONFIG = {
    "minio": {
        "PROVIDER_CLASS": "smoothglue.file_uploader.storage_providers.minio.MinioProvider",
        "PROVIDER_CONFIG": {
            "ACCESS_KEY": os.getenv("ACCESS_KEY"),
            "HOST": os.getenv("HOST"),
            "PORT": int(os.getenv("MINIO_PORT")),
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "SECURE": True if os.getenv("MINIO_PROTOCOL") == "https" else False,
            "BUCKET_NAME": os.getenv("BUCKET_NAME"),
            "REGION": os.getenv("REGION"),
        },
    },
    "s3-sts-web-id": {
        "PROVIDER_CLASS": "smoothglue.file_uploader.storage_providers.s3.STSWebIdentityS3Provider",
        "PROVIDER_CONFIG": {
            "ROLE_ARN": os.getenv("ROLE_ARN", None),
            "WEB_IDENTITY_TOKEN_FILE": os.getenv("WEB_IDENTITY_TOKEN_FILE", None),
            "BUCKET_NAME": os.getenv("BUCKET_NAME", None),
        },
    },
    "local": {
        "PROVIDER_CLASS": "smoothglue.file_uploader.storage_providers.local.LocalFileSystemProvider",
        "PROVIDER_CONFIG": {},
    },
}

SELECTED_STORAGE_PROVIDER = os.getenv("DEFAULT_STORAGE_PROVIDER")

UPLOAD_STORAGE_PROVIDER_CONFIG["default"] = UPLOAD_STORAGE_PROVIDER_CONFIG[
    SELECTED_STORAGE_PROVIDER
]
```

## Settings Overview
 
**`UPLOAD_STORAGE_PROVIDER_CONFIG`**

This setting defines the configurations for the storage providers. `smoothglue.file_uploader` uses `smoothglue.file_uploader.storage_providers.base.StorageProvider` as an interface for interacting with different storage backends. Each provider may have its own required settings in `PROVIDER_CONFIG`.

The `"default"` key specifies the storage provider to use for all file uploads unless a different key is specified.

**Required Keys for `smoothglue.file_uploader.storage_providers.s3.BaseS3StorageProvider`:**
-   `"BUCKET_NAME"`: The S3 bucket to store uploaded files in.

**Required Keys for `smoothglue.file_uploader.storage_providers.s3.STSS3Provider`:**
-   `"ROLE_ARN"`: The IAM role for the credentials used to access S3.
-   `"BUCKET_NAME"`: The S3 bucket to store uploaded files in.

**Required Keys for `smoothglue.file_uploader.storage_providers.s3.STSWebIdentityS3Provider`:**
-   `"ROLE_ARN"`: The IAM role for the credentials used to access S3.
-   `"WEB_IDENTITY_TOKEN_FILE"`: The path to the identity token file.
-   `"BUCKET_NAME"`: The S3 bucket to store uploaded files in.

**Required Keys for `smoothglue.file_uploader.storage_providers.minio.MinioProvider`:**
-   `"ACCESS_KEY"`: The access key for the MinIO user.
-   `"HOST"`: The hostname or IP address of the MinIO server.
-   `"PORT"`: (Optional) The port the MinIO service listens on if different from the default.
-   `"SECRET_KEY"`: The secret key for the MinIO user.
-   `"SECURE"`: `True` if MinIO uses SSL, `False` otherwise.
-   `"BUCKET_NAME"`: The MinIO bucket to store uploaded files in.

**`UPLOAD_POST_PROCESSORS`**

A dictionary mapping file extensions to post-processor classes. These classes are executed after a file has been successfully uploaded to the configured storage provider.
-   `"*"`: Applies to all uploaded files.
-   `"txt"`: Applies only to files with a `.txt` extension.

**`UPLOAD_VALIDATORS`**

A dictionary mapping file extensions to file validator classes. These classes are executed before a file is uploaded and can raise a `ValidationError` (resulting in a 400 response) to prevent the upload.
-   `"*"`: Applies to all uploaded files.
-   `"txt"`: Applies only to files with a `.txt` extension.

**`DEFAULT_TO_SOFT_DELETE`**

A boolean that determines whether to perform a soft delete (archive) or a hard delete when a `DELETE` request is made. When set to `True`, the file's `is_archived` flag is set to `True`, and the file remains in the storage backend. When `False`, the file is permanently deleted from both the database and the storage backend. The default value is `True`.

**`DOCUMENT_PERMISSION_CLASS`**

A string representing the import path to a custom permission class that controls access to individual documents. This class is used in the `DocumentView` for `get`, `patch`, and `delete` operations. The default is `'smoothglue.file_uploader.permissions.DefaultDocumentPermission'`, which allows all access.

To implement custom logic, create a class that inherits from `smoothglue.file_uploader.permissions.BaseDocumentPermission` and implement the `has_permission` method.

*Example Custom Permission Class:*
```python
# myapp/permissions.py
from smoothglue.file_uploader.permissions import BaseDocumentPermission

class StaffOnlyPermission(BaseDocumentPermission):
    def has_permission(self, request, view, document) -> bool:
        # Only allow staff users to access documents
        return request.user.is_staff
```

*In your `settings.py`:*
`DOCUMENT_PERMISSION_CLASS = "myapp.permissions.StaffOnlyPermission"`

**Local File System Storage Provider**

Used for running a simple upload to the file system. Defaults go to the Django MEDIA_ROOT configuration, otherwise you can specify the location using `UPLOAD_PATH` in the config.

```
UPLOAD_STORAGE_PROVIDER_CONFIG = {
   "default": {
   "PROVIDER_CLASS": "smoothglue.file_uploader.storage_providers.local.LocalFileSystemProvider",
   "PROVIDER_CONFIG": {"UPLOAD_PATH": "/tmp/uploaded_files"}
},
...
}
```

**Optional File Checksum validation**

```
# calculate sha256 file checksum and inserts it to the db. May cause performance issue for large file uploads
CALCULATE_CHECKSUM: bool = True

# Enforce checksum validation if an existing file with the same checksum exist in the document table.

UPLOAD_VALIDATORS={
    "*": "smoothglue.file_uploader.validators.DuplicateFileValidator"
}
```

## License

This project is licensed under a Proprietary License. See the [LICENSE](./LICENSE) file for more details.
