import json
import mimetypes
import os
import random
import shutil
import string
import subprocess
import sys

import boto3
import requests
from botocore.exceptions import ClientError, EndpointConnectionError
from tqdm import tqdm


class CephS3Manager:
    def __init__(self, CEPH_ENDPOINT_URL, CEPH_ADMIN_ACCESS_KEY, CEPH_ADMIN_SECRET_KEY, CEPH_USER_BUCKET, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print("[SDK_INFO] Initializing CephS3Manager...")
        if not all([CEPH_ENDPOINT_URL, CEPH_ADMIN_ACCESS_KEY, CEPH_ADMIN_SECRET_KEY, CEPH_USER_BUCKET]):
            error_msg = "Missing required Ceph configuration parameters"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

        self.bucket_name = CEPH_USER_BUCKET
        if self.verbose:
            print(f"[SDK_INFO] Setting bucket name to {self.bucket_name}")

        if self.verbose:
            print("[SDK_INFO] Creating boto3 S3 client...")
        self.s3 = boto3.client(
            "s3",
            endpoint_url=CEPH_ENDPOINT_URL,
            aws_access_key_id=CEPH_ADMIN_ACCESS_KEY,
            aws_secret_access_key=CEPH_ADMIN_SECRET_KEY,
        )
        if self.verbose:
            print("[SDK_OK] S3 client created successfully")

        if self.verbose:
            print("[SDK_INFO] Checking connection...")
        if not self.check_connection():
            error_msg = "Ceph connection not established."
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

        if self.verbose:
            print("[SDK_INFO] Checking authentication...")
        if not self.check_auth():
            error_msg = "Ceph Authentication not correct."
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

        if self.verbose:
            print("[SDK_INFO] Ensuring bucket exists...")
        self.ensure_bucket_exists()
        print("[SDK_OK] CephS3Manager initialized successfully")

    def generate_random_string(self, length=12):
        if self.verbose:
            print(f"[SDK_DEBUG] Generating random string of length {length}...")
        try:
            characters = string.ascii_letters + string.digits
            result = "".join(random.choices(characters) for _ in range(length))
            if self.verbose:
                print(f"[SDK_DEBUG] Random string generated successfully: {result}")
            return result
        except Exception as e:
            error_msg = f"Unexpected error generating random string: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def generate_key(self, length=12, characters=None):
        if self.verbose:
            print(f"[SDK_DEBUG] Generating key of length {length}...")
        try:
            if characters is None:
                characters = string.ascii_letters + string.digits
            result = "".join(random.choices(characters) for _ in range(length))
            if self.verbose:
                print(f"[SDK_DEBUG] Key generated successfully: {result}")
            return result
        except Exception as e:
            error_msg = f"Unexpected error generating key: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def generate_access_key(self):
        if self.verbose:
            print("[SDK_DEBUG] Generating access key...")
        try:
            characters = string.ascii_uppercase + string.digits
            result = "".join(random.choices(characters) for _ in range(20))
            if self.verbose:
                print(f"[SDK_DEBUG] Access key generated successfully: {result}")
            return result
        except Exception as e:
            error_msg = f"Unexpected error generating access key: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def generate_secret_key(self):
        if self.verbose:
            print("[SDK_DEBUG] Generating secret key...")
        try:
            characters = string.ascii_letters + string.digits
            result = "".join(random.choices(characters) for _ in range(40))
            if self.verbose:
                print(f"[SDK_DEBUG] Secret key generated successfully: {result}")
            return result
        except Exception as e:
            error_msg = f"Unexpected error generating secret key: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def create_user(self, username):
        if self.verbose:
            print(f"[SDK_INFO] Starting user creation for {username} using Admin Ops API...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Generating access and secret keys...")
            access_key = self.generate_access_key()
            secret_key = self.generate_secret_key()
            if self.verbose:
                print("[SDK_DEBUG] Keys generated successfully")

            if self.verbose:
                print("[SDK_DEBUG] Extracting admin credentials and endpoint...")
            endpoint_url = self.s3.meta.endpoint_url
            admin_access_key = self.s3.meta.client._request_signer._credentials.access_key
            admin_secret_key = self.s3.meta.client._request_signer._credentials.secret_key
            if self.verbose:
                print("[SDK_DEBUG] Credentials extracted successfully")

            if self.verbose:
                print("[SDK_DEBUG] Preparing API parameters...")
            params = {
                "uid": username,
                "display-name": username,
                "access-key": access_key,
                "secret-key": secret_key,
                "format": "json"
            }
            if self.verbose:
                print("[SDK_DEBUG] Parameters prepared")

            admin_path = "/admin/user"
            if self.verbose:
                print(f"[SDK_DEBUG] Sending PUT request to {endpoint_url}{admin_path}...")
            response = requests.put(
                f"{endpoint_url}{admin_path}",
                params=params,
                auth=(admin_access_key, admin_secret_key)
            )
            if self.verbose:
                print(f"[SDK_DEBUG] Response received with status code {response.status_code}")

            if response.status_code != 200:
                error_msg = f"API error: {response.status_code} - {response.text}"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)

            if self.verbose:
                print("[SDK_DEBUG] Parsing JSON response...")
            try:
                output = response.json()
                if self.verbose:
                    print(f"[SDK_INFO] API response: {json.dumps(output, indent=2)}")
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON output from API: {e!s}"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)

            print(f"[SDK_OK] User {username} created successfully")
            return access_key, secret_key

        except ClientError as e:
            error_msg = f"Boto3 client error: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error connecting to Ceph RGW: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error creating user {username}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def set_user_quota(self, username, quota_gb):
        if self.verbose:
            print(f"[SDK_INFO] Starting to set quota for user {username} to {quota_gb} GB using Admin Ops API...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Extracting admin credentials and endpoint...")
            endpoint_url = self.s3.meta.endpoint_url
            admin_access_key = self.s3.meta.client._request_signer._credentials.access_key
            admin_secret_key = self.s3.meta.client._request_signer._credentials.secret_key
            if self.verbose:
                print("[SDK_DEBUG] Credentials extracted successfully")

            if self.verbose:
                print("[SDK_DEBUG] Converting quota to bytes...")
            max_size_bytes = int(quota_gb * 1024 * 1024 * 1024)
            if self.verbose:
                print(f"[SDK_DEBUG] Quota converted to {max_size_bytes} bytes")

            if self.verbose:
                print("[SDK_DEBUG] Preparing API parameters...")
            params = {
                "uid": username,
                "quota-type": "user",
                "max-size": str(max_size_bytes),
                "enabled": "true",
                "format": "json"
            }
            if self.verbose:
                print("[SDK_DEBUG] Parameters prepared")

            admin_path = "/admin/user?quota"
            if self.verbose:
                print(f"[SDK_DEBUG] Sending PUT request to {endpoint_url}{admin_path}...")
            response = requests.put(
                f"{endpoint_url}{admin_path}",
                params=params,
                auth=(admin_access_key, admin_secret_key)
            )
            if self.verbose:
                print(f"[SDK_DEBUG] Response received with status code {response.status_code}")

            if response.status_code != 200:
                error_msg = f"API error: {response.status_code} - {response.text}"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)

            print(f"[SDK_OK] Quota set successfully for user {username}")

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error setting quota for user {username}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def enforce_storage_limit(self, bucket_name, storage_limit):
        if self.verbose:
            print(f"[SDK_INFO] Starting to enforce storage limit for bucket {bucket_name} with limit {storage_limit} GB...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Getting bucket size...")
            size_mb = self.get_uri_size(f"s3://{bucket_name}/")
            size_gb = size_mb / 1024
            if self.verbose:
                print(f"[SDK_DEBUG] Bucket size calculated: {size_gb:.2f} GB")

            if size_gb > storage_limit:
                warning_msg = f"Bucket {bucket_name} size ({size_gb:.2f} GB) exceeds limit ({storage_limit} GB)"
                print(f"[SDK_WARN] {warning_msg}")
                return False

            print(f"[SDK_OK] Bucket {bucket_name} size ({size_gb:.2f} GB) within limit ({storage_limit} GB)")
            print("[SDK_OK] Storage limit enforced successfully")
            return True

        except ValueError as e:
            error_msg = f"Bucket {bucket_name} does not exist: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error enforcing storage limit for {bucket_name}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def run_cmd(self, cmd, shell=False):
        if self.verbose:
            print(f"[SDK_INFO] Starting to run command: {cmd if isinstance(cmd, str) else ' '.join(cmd)} with shell={shell}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=shell, check=True)
            if self.verbose:
                print(f"[SDK_OK] Command executed successfully: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
            return result
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {e.stderr}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error executing command: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def check_s5cmd(self):
        if self.verbose:
            print("[SDK_DEBUG] Checking if s5cmd is installed...")
        try:
            cmd = ["s5cmd", "--version"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if self.verbose:
                print(f"[SDK_OK] s5cmd is installed: {result.stdout.strip()}")
                print("[SDK_OK] s5cmd check completed successfully")
            return True
        except subprocess.CalledProcessError:
            error_msg = "s5cmd is not installed"
            print(f"[SDK_FAIL] {error_msg}")
            return False
        except Exception as e:
            error_msg = f"Unexpected error checking s5cmd: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            return False

    def check_command_exists(self, cmd_name, path=None):
        if self.verbose:
            print(f"[SDK_DEBUG] Checking if command {cmd_name} exists...")
        try:
            if path:
                result = os.path.isfile(path) and os.access(path, os.X_OK)
                if result:
                    if self.verbose:
                        print(f"[SDK_OK] Command {cmd_name} exists at path {path}")
                elif self.verbose:
                    print(f"[SDK_FAIL] Command {cmd_name} does not exist at path {path}")
                if self.verbose:
                    print("[SDK_DEBUG] Command existence check completed")
                return result
            result = shutil.which(cmd_name)
            if result:
                if self.verbose:
                    print(f"[SDK_OK] Command {cmd_name} found at: {result}")
                    print("[SDK_OK] Command existence check completed successfully")
                return True
            if self.verbose:
                print(f"[SDK_FAIL] Command {cmd_name} not found")
                print("[SDK_DEBUG] Command existence check completed")
            return False
        except Exception as e:
            error_msg = f"Unexpected error checking command {cmd_name}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def check_aws_credentials_folder(self):
        if self.verbose:
            print("[SDK_DEBUG] Checking AWS credentials folder...")
        try:
            aws_dir = os.path.expanduser("~/.aws")
            os.makedirs(aws_dir, exist_ok=True)
            if self.verbose:
                print(f"[SDK_OK] AWS credentials folder exists: {aws_dir}")
                print("[SDK_OK] AWS credentials folder check completed successfully")
            return True
        except Exception as e:
            error_msg = f"Failed to create AWS credentials folder: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def _list_all_files(self):
        if self.verbose:
            print("[SDK_DEBUG] Listing all files in bucket...")
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name)
            result = []
            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        result.append(obj["Key"])

            if self.verbose:
                print(f"[SDK_OK] Listed {len(result)} files")
                print("[SDK_DEBUG] File listing completed successfully")
            return result
        except Exception as e:
            error_msg = f"Unexpected error listing files: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def _find_closest_match(self, target_name, file_list):
        if self.verbose:
            print(f"[SDK_DEBUG] Finding closest match for {target_name}...")
        try:
            import difflib
            matches = difflib.get_close_matches(target_name, file_list, n=1, cutoff=0.5)
            result = matches[0] if matches else None
            if result:
                if self.verbose:
                    print(f"[SDK_OK] Closest match found: {result}")
            elif self.verbose:
                print("[SDK_WARN] No close match found")
            if self.verbose:
                print("[SDK_DEBUG] Closest match search completed successfully")
            return result
        except Exception as e:
            error_msg = f"Unexpected error finding closest match: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def get_local_path(self, key):
        if self.verbose:
            print(f"[SDK_DEBUG] Generating local path for key {key}...")
        try:
            result = os.path.join("./downloads", self.bucket_name, key)
            if self.verbose:
                print(f"[SDK_OK] Local path generated: {result}")
                print("[SDK_DEBUG] Local path generation completed successfully")
            return result
        except Exception as e:
            error_msg = f"Unexpected error generating local path: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def print_file_info(self, file_key, response):
        if self.verbose:
            print(f"[SDK_DEBUG] Printing file info for {file_key}...")
        try:
            metadata = response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
            file_size = metadata.get("content-length", "Unknown Size")
            file_type = metadata.get("content-type", "Unknown Type")
            last_modified = response.get("LastModified", "Unknown Date")
            print("\nSDK_INFO: Downloaded File Information:")
            print(f"SDK_INFO: File Name: {file_key}")
            print(f"SDK_INFO: File Size: {file_size} bytes")
            print(f"SDK_INFO: File Type: {file_type}")
            print(f"SDK_INFO: Last Modified: {last_modified}")
            print("[SDK_OK] File info printed successfully")
        except Exception as e:
            error_msg = f"Unexpected error printing file info: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def read_file_from_s3(self, key):
        if self.verbose:
            print(f"[SDK_INFO] Starting to read file from S3: {key}...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Checking if file exists...")
            if not self.check_if_exists(key):
                file_list = self._list_all_files()
                closest_match = self._find_closest_match(key, file_list)
                if closest_match:
                    error_msg = f"File '{key}' not found. Similar file found: '{closest_match}'"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)
                error_msg = f"File '{key}' does not exist in bucket '{self.bucket_name}'."
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)
            if self.verbose:
                print("[SDK_DEBUG] File exists")

            if self.verbose:
                print("[SDK_DEBUG] Detecting file type...")
            file_type, _ = mimetypes.guess_type(key)
            file_type = file_type if file_type else "Unknown file type"
            if self.verbose:
                print(f"[SDK_DEBUG] File type detected: {file_type}")

            if self.verbose:
                print("[SDK_DEBUG] Getting object from S3...")
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            body = response["Body"].read()
            if self.verbose:
                print("[SDK_DEBUG] Object retrieved successfully")

            if self.verbose:
                print("[SDK_DEBUG] Processing file based on type...")
            if file_type and ("text" in file_type or file_type in ["application/json", "application/xml"]):
                content = body.decode("utf-8")
                if file_type == "application/json":
                    content = json.dumps(json.loads(content), indent=4)
                if self.verbose:
                    print(f"\nSDK_DEBUG: File Content:\n{content}")
                print("[SDK_OK] Text file processed successfully")
                return content
            if file_type and "image" in file_type:
                local_path = "downloaded_image.jpg"
                with open(local_path, "wb") as f:
                    f.write(body)
                print(f"[SDK_OK] Image saved as '{local_path}'")
                if self.verbose:
                    print("[SDK_DEBUG] Image file processed successfully")
                return local_path
            if file_type and "audio" in file_type:
                local_path = "downloaded_audio.mp3"
                with open(local_path, "wb") as f:
                    f.write(body)
                print(f"[SDK_OK] Audio file saved as '{local_path}'")
                if self.verbose:
                    print("[SDK_DEBUG] Audio file processed successfully")
                return local_path
            if file_type and "pdf" in file_type:
                local_path = "downloaded_file.pdf"
                with open(local_path, "wb") as f:
                    f.write(body)
                print(f"[SDK_OK] PDF file saved as '{local_path}'")
                if self.verbose:
                    print("[SDK_DEBUG] PDF file processed successfully")
                return local_path
            local_path = "downloaded_file.bin"
            with open(local_path, "wb") as f:
                f.write(body)
            print(f"[SDK_OK] Binary file saved as '{local_path}'")
            if self.verbose:
                print("[SDK_DEBUG] Binary file processed successfully")
            return local_path

        except ClientError as e:
            error_msg = f"Failed to read file '{key}': {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error reading file '{key}': {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def get_identity(self):
        if self.verbose:
            print("[SDK_INFO] Starting to get caller identity using STS...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Creating STS client...")
            sts_client = boto3.client(
                "sts",
                endpoint_url=self.s3.meta.endpoint_url,
                aws_access_key_id=self.s3.meta.client._request_signer._credentials.access_key,
                aws_secret_access_key=self.s3.meta.client._request_signer._credentials.secret_key,
            )
            if self.verbose:
                print("[SDK_DEBUG] STS client created")

            if self.verbose:
                print("[SDK_DEBUG] Getting caller identity...")
            identity = sts_client.get_caller_identity()
            if self.verbose:
                print(f"[SDK_OK] Caller Identity: {identity}")
            print("[SDK_OK] Caller identity retrieved successfully")
            return identity
        except ClientError as e:
            error_msg = f"Failed to get caller identity: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error getting caller identity: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def get_user_info(self):
        if self.verbose:
            print("[SDK_INFO] Starting to get user info using IAM...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Creating IAM client...")
            iam_client = boto3.client(
                "iam",
                endpoint_url=self.s3.meta.endpoint_url,
                aws_access_key_id=self.s3.meta.client._request_signer._credentials.access_key,
                aws_secret_access_key=self.s3.meta.client._request_signer._credentials.secret_key,
            )
            if self.verbose:
                print("[SDK_DEBUG] IAM client created")

            if self.verbose:
                print("[SDK_DEBUG] Getting user info...")
            user_info = iam_client.get_user()
            if self.verbose:
                print(f"[SDK_OK] User Info: {user_info['User']}")
            print("[SDK_OK] User info retrieved successfully")
            return user_info["User"]
        except ClientError as e:
            error_msg = f"Failed to get user info: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error getting user info: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def ensure_bucket_exists(self):
        if self.verbose:
            print(f"[SDK_DEBUG] Ensuring bucket {self.bucket_name} exists...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Listing buckets...")
            buckets = self.s3.list_buckets()
            names = [b["Name"] for b in buckets.get("Buckets", [])]
            if self.verbose:
                print(f"[SDK_DEBUG] Existing buckets: {names}")

            if self.bucket_name not in names:
                if self.verbose:
                    print(f"[SDK_INFO] Creating bucket {self.bucket_name}...")
                self.s3.create_bucket(Bucket=self.bucket_name)
                print(f"[SDK_OK] Ceph S3 Bucket Created: {self.bucket_name}")
            else:
                print(f"[SDK_OK] Ceph S3 Bucket Exists: {self.bucket_name}")
            print("[SDK_OK] Bucket ensured successfully")
        except ClientError as e:
            error_msg = f"Failed to ensure bucket exists: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error ensuring bucket exists: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def check_connection(self):
        if self.verbose:
            print("[SDK_DEBUG] Checking Ceph S3 connection...")
        try:
            self.s3.list_buckets()
            print("[SDK_OK] Ceph S3 Connection")
            if self.verbose:
                print("[SDK_DEBUG] Connection check completed successfully")
            return True
        except EndpointConnectionError as e:
            error_msg = "Ceph S3 Connection failed"
            print(f"[SDK_FAIL] {error_msg}: {e!s}")
            raise ValueError(error_msg)
        except ClientError as e:
            error_msg = f"Ceph S3 ClientError: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Ceph S3 Unknown error: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("Ceph S3 Connection failed")

    def check_auth(self):
        if self.verbose:
            print("[SDK_DEBUG] Checking Ceph S3 authentication...")
        try:
            self.s3.list_buckets()
            print("[SDK_OK] Ceph S3 Auth")
            if self.verbose:
                print("[SDK_DEBUG] Authentication check completed successfully")
            return True
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ["InvalidAccessKeyId", "SignatureDoesNotMatch"]:
                error_msg = "Ceph S3 Auth Invalid"
            else:
                error_msg = f"Ceph S3 Auth: {code}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(f"Ceph S3 Authentication failed: {code}")
        except Exception as e:
            error_msg = f"Ceph S3 Auth Unknown: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("Ceph S3 Authentication failed")

    def check_if_exists(self, key):
        if self.verbose:
            print(f"[SDK_DEBUG] Checking if key '{key}' exists in bucket {self.bucket_name}...")
        try:
            # Check for 1 key, it's faster than listing all
            resp = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=key, MaxKeys=1)
            result = "Contents" in resp and len(resp["Contents"]) > 0

            if result:
                if self.verbose:
                    print(f"[SDK_OK] Key '{key}' exists")
            elif self.verbose:
                print(f"[SDK_WARN] Key '{key}' does not exist")
            if self.verbose:
                print("[SDK_DEBUG] Existence check completed successfully")
            return result
        except ClientError as e:
            error_msg = f"Failed to check if key '{key}' exists: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error checking if key '{key}' exists: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def get_uri_size(self, uri):
        if self.verbose:
            print(f"[SDK_INFO] Starting to get size for URI {uri}...")
        try:
            import re
            if self.verbose:
                print("[SDK_DEBUG] Parsing URI...")
            pattern = r"^s3://([^/]+)/(.+)$"
            match = re.match(pattern, uri)
            if not match:
                # If standard uri parsing fails, assume it's a key in current bucket if not s3://
                if uri.startswith("s3://"):
                    error_msg = f"Invalid S3 URI: {uri}"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)
                else:
                     key = uri
            else:
                bucket, key = match.groups()
                if bucket != self.bucket_name:
                    error_msg = f"URI bucket '{bucket}' does not match initialized bucket '{self.bucket_name}'"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)
            if self.verbose:
                print("[SDK_DEBUG] URI parsed successfully")

            if self.verbose:
                print("[SDK_DEBUG] Attempting to get file size...")
            try:
                response = self.s3.head_object(Bucket=self.bucket_name, Key=key)
                size = response["ContentLength"] / (1024**2)
                print(f"[SDK_OK] Found file: {key} ({size:.2f} MB)")
                if self.verbose:
                    print("[SDK_DEBUG] URI size retrieved successfully")
                return size
            except self.s3.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    if self.verbose:
                        print("[SDK_WARN] Object not found, checking as folder...")
                    if not key.endswith("/"):
                        key += "/"
                else:
                    error_msg = f"Failed to get size for {uri}: {e.response['Error']['Code']}"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)

            if self.verbose:
                print("[SDK_DEBUG] Scanning folder for size...")
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=key)
            total_size = 0
            found = False
            for page in tqdm(pages, desc=f"Scanning {uri}"):
                contents = page.get("Contents", [])
                if contents:
                    found = True
                    for obj in contents:
                        total_size += obj["Size"]
            if not found:
                print(f"[SDK_WARN] No objects found at URI '{uri}'.")
                return 0.0
            size_mb = total_size / (1024**2)
            print(f"[SDK_OK] Folder total size: {size_mb:.2f} MB")
            if self.verbose:
                print("[SDK_DEBUG] Folder size calculation completed successfully")
            return size_mb
        except Exception as e:
            error_msg = f"Unexpected error getting URI size: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_buckets(self):
        if self.verbose:
            print("[SDK_INFO] Starting to list buckets...")
        try:
            response = self.s3.list_buckets()
            buckets = response.get("Buckets", [])
            bucket_data = [{"Name": b["Name"], "CreationDate": str(b["CreationDate"])} for b in buckets]
            if not buckets:
                print("SDK_INFO: No buckets found.")
            else:
                print("SDK_INFO: Available S3 buckets:")
                for bucket in buckets:
                    print(f"SDK_INFO: - {bucket['Name']} (Created: {bucket['CreationDate']})")
            print("[SDK_OK] Buckets listed successfully")
            return bucket_data
        except ClientError as e:
            error_msg = f"Failed to list buckets: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing buckets: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_folder_contents(self, folder_prefix):
        if self.verbose:
            print(f"[SDK_INFO] Starting to list folder contents for {folder_prefix}...")
        try:
            if not folder_prefix.endswith("/"):
                folder_prefix += "/"
                if self.verbose:
                    print(f"[SDK_DEBUG] Adjusted prefix: {folder_prefix}")

            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=folder_prefix)

            all_contents = []
            for page in pages:
                if "Contents" in page:
                    all_contents.extend(page["Contents"])

            if not all_contents:
                all_files = self._list_all_files()
                closest_match = self._find_closest_match(folder_prefix, all_files)
                if closest_match:
                    print(f"[SDK_FAIL] Folder '{folder_prefix}' was not found.")
                    print(f"[SDK_WARN] However, a similar folder was found: '{closest_match}'")
                    folder_prefix = closest_match
                    # Retry with closest match
                    pages = paginator.paginate(Bucket=self.bucket_name, Prefix=folder_prefix)
                    for page in pages:
                        if "Contents" in page:
                            all_contents.extend(page["Contents"])
                else:
                    error_msg = f"Folder '{folder_prefix}' does not exist in bucket '{self.bucket_name}'."
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)

            print(f"SDK_INFO: \nFiles in folder: {folder_prefix}\n")
            for obj in all_contents:
                print(f"SDK_INFO: - {obj['Key']} (Last Modified: {obj['LastModified']})")
            print("[SDK_OK] Folder contents listed successfully")
        except ClientError as e:
            error_msg = f"Failed to list folder contents: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing folder contents: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_available_buckets(self):
        if self.verbose:
            print("[SDK_INFO] Starting to list available buckets...")
        try:
            response = self.s3.list_buckets()
            buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
            if not buckets:
                print("SDK_INFO: No buckets found in Ceph S3.")
            print("[SDK_OK] Available buckets listed successfully")
            return buckets
        except ClientError as e:
            error_msg = f"Failed to list buckets: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing buckets: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def print_bucket_full_detail(self):
        if self.verbose:
            print("[SDK_INFO] Starting to print full bucket details...")
        try:
            import json
            response = self.s3.list_buckets()
            print(json.dumps(response, indent=4, default=str))
            print("[SDK_OK] Full bucket details printed successfully")
            return response
        except ClientError as e:
            error_msg = f"Failed to retrieve bucket details: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while retrieving bucket details: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def print_bucket_short_detail(self):
        if self.verbose:
            print("[SDK_INFO] Starting to print short bucket details...")
        try:
            from tabulate import tabulate
            response = self.s3.list_buckets()
            buckets = response.get("Buckets", [])
            bucket_data = [[b["Name"], b["CreationDate"]] for b in buckets]
            if bucket_data:
                print("SDK_INFO: \nAvailable S3 Buckets:")
                print(tabulate(bucket_data, headers=["Bucket Name", "Creation Date"], tablefmt="fancy_grid"))
            else:
                print("SDK_INFO: No buckets found.")
            print("[SDK_OK] Short bucket details printed successfully")
        except ImportError:
            error_msg = "Tabulate library is not installed. Please install it using 'pip install tabulate'."
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except ClientError as e:
            error_msg = f"Failed to retrieve bucket details: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while printing bucket details: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def find_file(self, file_or_folder_name):
        if self.verbose:
            print(f"[SDK_INFO] Starting to find file or folder {file_or_folder_name}...")
        try:
            import mimetypes

            def list_all_files():
                if self.verbose:
                    print("[SDK_DEBUG] Listing all files for finding...")
                return self._list_all_files() # Use the paginated version

            def find_closest_match(target, file_list):
                return self._find_closest_match(target, file_list)

            def check_if_exists(key):
                return self.check_if_exists(key)

            def list_folder_contents(prefix):
                if not prefix.endswith("/"):
                    prefix += "/"
                if self.verbose:
                    print(f"[SDK_DEBUG] Listing folder contents for {prefix}...")
                paginator = self.s3.get_paginator("list_objects_v2")
                pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
                results = []
                for page in pages:
                    if "Contents" in page:
                        for obj in page["Contents"]:
                            results.append((obj["Key"], obj["LastModified"]))

                if not results:
                    closest_match = find_closest_match(prefix, list_all_files())
                    if closest_match:
                        error_msg = f"Folder '{prefix}' not found. Similar folder found: '{closest_match}'"
                        print(f"[SDK_FAIL] {error_msg}")
                        raise ValueError(error_msg)
                    error_msg = f"Folder '{prefix}' does not exist in bucket '{self.bucket_name}'."
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)

                if self.verbose:
                    print(f"[SDK_DEBUG] Found {len(results)} items in folder")
                return results

            def read_file(key):
                if self.verbose:
                    print(f"[SDK_DEBUG] Reading file {key}...")
                file_list = list_all_files()
                if not check_if_exists(key):
                    closest_match = find_closest_match(key, file_list)
                    if closest_match:
                        error_msg = f"File '{key}' not found. Similar file found: '{closest_match}'"
                        print(f"[SDK_FAIL] {error_msg}")
                        raise ValueError(error_msg)
                    error_msg = f"File '{key}' does not exist in bucket '{self.bucket_name}'."
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)
                file_type, _ = mimetypes.guess_type(key)
                result = [(key, file_type or "Unknown file type")]
                if self.verbose:
                    print("[SDK_DEBUG] File read successfully")
                return result

            if file_or_folder_name.endswith("/") or "." not in file_or_folder_name:
                results = list_folder_contents(file_or_folder_name)
                print(f"SDK_INFO: \nFiles in folder: {file_or_folder_name}\n")
                for key, last_modified in results:
                    print(f"SDK_INFO: - {key} (Last Modified: {last_modified})")
                print("[SDK_OK] Folder finding completed successfully")
                return results
            results = read_file(file_or_folder_name)
            print(f"SDK_INFO: \nFile Type Detected: {results[0][1]}\n")
            print("[SDK_OK] File finding completed successfully")
            return results
        except ClientError as e:
            error_msg = f"Failed to find file/folder: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while finding file/folder: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_model_classes(self):
        if self.verbose:
            print("[SDK_INFO] Starting to list model classes...")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix="_models/", Delimiter="/")
            if "CommonPrefixes" not in response:
                print(f"[SDK_INFO] No models found in bucket '{self.bucket_name}'.")
                if self.verbose:
                    print("[SDK_DEBUG] Model classes list completed (empty)")
                return []
            model_classes = [prefix["Prefix"].split("/")[1] for prefix in response["CommonPrefixes"]]
            if self.verbose:
                print(f"[SDK_DEBUG] Found model classes: {model_classes}")
            print("[SDK_OK] Model classes listed successfully")
            return model_classes
        except ClientError as e:
            error_msg = f"Failed to list model classes: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            if e.response["Error"]["Code"] == "NoSuchBucket":
                raise ValueError(f"Bucket '{self.bucket_name}' does not exist.")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing model classes: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_buckets_and_model_classes(self):
        if self.verbose:
            print("[SDK_INFO] Starting to list buckets and model classes...")
        try:
            result = {}
            if self.verbose:
                print("[SDK_DEBUG] Listing buckets...")
            buckets = self.s3.list_buckets()
            bucket_names = [bucket["Name"] for bucket in buckets.get("Buckets", [])]
            if self.verbose:
                print(f"[SDK_DEBUG] Found buckets: {bucket_names}")

            for bucket in bucket_names:
                try:
                    if self.verbose:
                        print(f"[SDK_DEBUG] Processing bucket {bucket}...")
                    response = self.s3.list_objects_v2(Bucket=bucket, Prefix="_models/", Delimiter="/")
                    if "CommonPrefixes" in response:
                        model_classes = [prefix["Prefix"].split("/")[1] for prefix in response["CommonPrefixes"]]
                    else:
                        model_classes = []
                    result[bucket] = model_classes
                    print(f"SDK_INFO: Bucket: {bucket}")
                    if model_classes:
                        print(f"SDK_INFO:   Model Classes: {model_classes}")
                    else:
                        print("SDK_INFO:   No model classes found")
                    if self.verbose:
                        print("[SDK_DEBUG] " + "-" * 40)
                except ClientError as e:
                    code = e.response["Error"]["Code"]
                    if code == "NoSuchBucket":
                        print(f"[SDK_WARN] Bucket '{bucket}' does not exist.")
                        continue
                    error_msg = f"Failed to list model classes for bucket '{bucket}': {code}"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)
            print("[SDK_OK] Buckets and model classes listed successfully")
            return result
        except ClientError as e:
            error_msg = f"Failed to list buckets: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing buckets and model classes: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def list_models_and_versions(self):
        if self.verbose:
            print("[SDK_INFO] Starting to list models and versions...")
        try:
            all_models = {}
            if self.verbose:
                print("[SDK_DEBUG] Listing model classes...")
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix="_models/", Delimiter="/")
            if "CommonPrefixes" not in response:
                print(f"[SDK_INFO] No models found in bucket '{self.bucket_name}'.")
                if self.verbose:
                    print("[SDK_DEBUG] Models and versions list completed (empty)")
                return all_models
            model_classes = [prefix["Prefix"].split("/")[1] for prefix in response["CommonPrefixes"]]
            if self.verbose:
                print(f"[SDK_DEBUG] Model classes: {model_classes}")

            for model_class in model_classes:
                all_models[model_class] = {}
                if self.verbose:
                    print(f"[SDK_DEBUG] Processing model class {model_class}...")
                response = self.s3.list_objects_v2(
                    Bucket=self.bucket_name, Prefix=f"_models/{model_class}/", Delimiter="/"
                )
                if "CommonPrefixes" not in response:
                    continue
                models = [prefix["Prefix"].split("/")[2] for prefix in response["CommonPrefixes"]]
                if self.verbose:
                    print(f"[SDK_DEBUG] Models in {model_class}: {models}")

                for model in models:
                    if self.verbose:
                        print(f"[SDK_DEBUG] Processing model {model} in {model_class}...")
                    version_response = self.s3.list_objects_v2(
                        Bucket=self.bucket_name, Prefix=f"_models/{model_class}/{model}/", Delimiter="/"
                    )
                    if "CommonPrefixes" in version_response:
                        versions = [prefix["Prefix"].split("/")[-2] for prefix in version_response["CommonPrefixes"]]
                        numeric_versions = sorted(
                            [v for v in versions if v.startswith("model_v") and v[7:].isdigit()],
                            key=lambda v: int(v[7:]),
                        )
                        non_numeric_versions = [v for v in versions if v not in numeric_versions]
                        all_models[model_class][model] = numeric_versions + non_numeric_versions
                    else:
                        all_models[model_class][model] = []
                    print(f"SDK_INFO: \nCategory: {model_class}")
                    print(f"SDK_INFO:   Model: {model}")
                    print(
                        f"SDK_INFO:     Versions: {', '.join(all_models[model_class][model]) if all_models[model_class][model] else 'No versions found'}"
                    )
                    if self.verbose:
                        print("[SDK_DEBUG] " + "-" * 50)
            print("[SDK_OK] Models and versions listed successfully")
            return all_models
        except ClientError as e:
            error_msg = f"Failed to list models and versions: {e.response['Error']['Code']}"
            print(f"[SDK_FAIL] {error_msg}")
            if e.response["Error"]["Code"] == "NoSuchBucket":
                raise ValueError(f"Bucket '{self.bucket_name}' does not exist.")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while listing models and versions: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def is_folder(self, key):
        if self.verbose:
            print(f"[SDK_DEBUG] Checking if {key} is a folder...")
        try:
            # A key is a folder if it ends with / OR if objects exist *under* it.
            if key.endswith("/"):
                if self.verbose:
                    print(f"[SDK_OK] {key} is a folder (ends with /)")
                return True

            # Check if any object exists with this prefix + "/"
            prefix = key + "/"
            resp = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=1)
            is_folder = "Contents" in resp and len(resp["Contents"]) > 0

            if is_folder:
                if self.verbose:
                    print(f"[SDK_OK] {key} is a folder (contains objects)")
            elif self.verbose:
                print(f"[SDK_OK] {key} is not a folder")
            if self.verbose:
                print("[SDK_DEBUG] Folder check completed successfully")
            return is_folder
        except Exception as e:
            error_msg = f"Unexpected error checking if {key} is folder: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def _download_file_with_progress_bar(self, remote_path, local_path):
        if self.verbose:
            print(f"[SDK_DEBUG] Downloading file {remote_path} with progress bar to {local_path}...")
        try:
            if self.verbose:
                print("[SDK_DEBUG] Fetching metadata...")
            meta_data = self.s3.head_object(Bucket=self.bucket_name, Key=remote_path)
            total_length = int(meta_data.get("ContentLength", 0))
            if self.verbose:
                print(f"[SDK_DEBUG] Metadata fetched, total length: {total_length}")

        except Exception as e:
            error_msg = f"Failed to fetch metadata for '{remote_path}': {e!s}"
            print(f"[SDK_ERROR] {error_msg}")
            total_length = None

        try:
            with tqdm(
                total=total_length,
                desc=os.path.basename(remote_path),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                leave=False,
                dynamic_ncols=True,
                ncols=100,
                file=sys.stdout,
                ascii=True,
            ) as pbar, open(local_path, "wb") as f:
                self.s3.download_fileobj(self.bucket_name, remote_path, f, Callback=pbar.update)
            print(f"[SDK_OK] File downloaded successfully to {local_path}")
        except Exception as e:
            error_msg = f"Error downloading file with progress: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def download_file(self, remote_path, local_path):
        if self.verbose:
            print(f"[SDK_INFO] Starting to download file {remote_path} to {local_path}...")
        try:
            if os.path.isdir(local_path):
                local_path = os.path.join(local_path, os.path.basename(remote_path))
                if self.verbose:
                    print(f"[SDK_DEBUG] Adjusted local path to {local_path}")

            if self.verbose:
                print("[SDK_DEBUG] Creating directories if needed...")
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            if self.verbose:
                print("[SDK_DEBUG] Directories ready")

            self._download_file_with_progress_bar(remote_path, local_path)
            print(f"[SDK_OK] File {remote_path} downloaded successfully to {local_path}")
        except Exception as e:
            error_msg = f"Error downloading file '{remote_path}': {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def download_folder(self, remote_folder, local_folder, keep_folder=False, exclude=[], overwrite=False):
        if self.verbose:
            print(f"[SDK_INFO] Starting to download folder {remote_folder} to {local_folder} (keep_folder={keep_folder}, overwrite={overwrite})...")
        try:
            if not remote_folder.endswith("/"):
                remote_folder += "/"
                if self.verbose:
                    print(f"[SDK_DEBUG] Adjusted remote folder to {remote_folder}")

            if self.verbose:
                print("[SDK_DEBUG] Listing objects in folder...")
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=remote_folder)

            all_objects = []
            for page in pages:
                if "Contents" in page:
                    all_objects.extend(page["Contents"])

            if not all_objects:
                error_msg = f"Folder {remote_folder} not found or is empty"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)

            if self.verbose:
                print(f"[SDK_DEBUG] Found {len(all_objects)} objects")

            if self.verbose:
                print("[SDK_DEBUG] Preparing local folder...")
            if keep_folder:
                local_folder = os.path.join(local_folder, remote_folder.split("/")[-2])
                if self.verbose:
                    print(f"[SDK_DEBUG] Adjusted local folder to {local_folder}")
            os.makedirs(local_folder, exist_ok=True)
            if self.verbose:
                print("[SDK_DEBUG] Local folder ready")

            with tqdm(total=len(all_objects), desc="Downloading") as pbar:
                for obj in all_objects:
                    file_key = obj["Key"]
                    relative_path = file_key[len(remote_folder):]

                    # Skip if it's just the folder itself (empty key)
                    if not relative_path:
                        pbar.update(1)
                        continue

                    if any(x in relative_path for x in exclude):
                        if self.verbose:
                            print(f"[SDK_DEBUG] Skipped file {file_key}. File matches excluded pattern.")
                        pbar.update(1)
                        continue

                    local_file_path = os.path.join(local_folder, relative_path)

                    # Create subdirectories if they don't exist
                    local_file_dir = os.path.dirname(local_file_path)
                    os.makedirs(local_file_dir, exist_ok=True)

                    if not overwrite and os.path.exists(local_file_path):
                        if self.verbose:
                            print(f"[SDK_DEBUG] Skipped file {file_key}. File already exists.")
                        pbar.update(1)
                        continue

                    self.download_file(file_key, local_file_path)
                    pbar.update(1)
            print(f"[SDK_OK] Folder {remote_folder} downloaded successfully")
        except Exception as e:
            error_msg = f"Error downloading folder {remote_folder}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def download(self, remote_path, local_path, keep_folder=False, exclude=[], overwrite=False):
        if self.verbose:
            print(f"[SDK_INFO] Starting download from {remote_path} to {local_path}...")
        try:
            if os.path.isfile(local_path) and self.is_folder(remote_path):
                error_msg = "Cannot download folder to file path"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)
            if os.path.isdir(local_path) and not self.is_folder(remote_path):
                local_path = os.path.join(local_path, os.path.basename(remote_path))
                if self.verbose:
                    print(f"[SDK_DEBUG] Adjusted local path to {local_path}")

            if self.is_folder(remote_path):
                self.download_folder(remote_path, local_path, keep_folder=keep_folder, exclude=exclude, overwrite=overwrite)
            else:
                self.download_file(remote_path, local_path)
            print("[SDK_OK] Download completed successfully")
        except Exception as e:
            error_msg = f"Error in download: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def upload_file(self, local_file_path, remote_path):
        if self.verbose:
            print(f"[SDK_DEBUG] Starting to upload file {local_file_path} to {remote_path}...")
        try:
            self.s3.upload_file(local_file_path, self.bucket_name, remote_path)
            print(f"[SDK_OK] Uploaded {local_file_path} -> s3://{self.bucket_name}/{remote_path}")
            if self.verbose:
                print("[SDK_DEBUG] File upload completed successfully")
        except Exception as e:
            error_msg = f"Failed to upload file {local_file_path} to {remote_path}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def upload(self, local_path, remote_path):
        if self.verbose:
            print(f"[SDK_INFO] Starting upload from {local_path} to {remote_path}...")
        try:
            if os.path.isfile(local_path) and self.is_folder(remote_path):
                error_msg = "Cannot upload file to folder path"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)
            if os.path.isdir(local_path):
                if self.check_if_exists(remote_path) and not self.is_folder(remote_path):
                    error_msg = "Cannot upload folder to file path"
                    print(f"[SDK_FAIL] {error_msg}")
                    raise ValueError(error_msg)

            uploaded_files = []
            if self.check_s5cmd() and os.path.isdir(local_path):
                if self.verbose:
                    print("[SDK_INFO] Using s5cmd for upload...")
                
                # Ensure remote path has trailing slash for folder structure consistency
                if not remote_path.endswith('/'): remote_path += '/'
                
                cmd = ["s5cmd", "--endpoint-url", self.s3.meta.endpoint_url, "cp", f"{local_path}/*", f"s3://{self.bucket_name}/{remote_path}"]
                
                # Set environment variables for s5cmd authentication
                env = os.environ.copy()
                env["AWS_ACCESS_KEY_ID"] = self.s3.meta.client._request_signer._credentials.access_key
                env["AWS_SECRET_ACCESS_KEY"] = self.s3.meta.client._request_signer._credentials.secret_key
                
                subprocess.run(cmd, check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if self.verbose:
                    print("[SDK_OK] s5cmd upload completed")
            elif os.path.isdir(local_path):
                if self.verbose:
                    print("[SDK_INFO] Uploading folder files one by one...")
                for root, _, files in os.walk(local_path):
                    for file in files:
                        local_file = os.path.join(root, file)
                        s3_key = os.path.join(remote_path, os.path.relpath(local_file, local_path)).replace("\\", "/")
                        self.upload_file(local_file, s3_key)
                        uploaded_files.append(s3_key)
            else:
                self.upload_file(local_path, remote_path)
                uploaded_files.append(remote_path)

            uri = f"s3://{self.bucket_name}/{remote_path}"
            try:
                if self.verbose:
                    print("[SDK_DEBUG] Calculating uploaded size...")
                size_mb = self.get_uri_size(uri)
                print(f"[SDK_OK] Uploaded {local_path} to {uri}, size: {size_mb:.2f} MB")
                if self.verbose:
                    print("[SDK_OK] Upload completed successfully")
                return size_mb
            except Exception as e:
                warning_msg = f"Failed to calculate size for {uri}: {e!s}"
                print(f"[SDK_WARN] {warning_msg}")
                return 0.0
        except Exception as e:
            error_msg = f"Upload failed: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            # Cleanup partial uploads if recursive python method was used
            for s3_key in uploaded_files:
                try:
                    if self.verbose:
                        print(f"[SDK_DEBUG] Cleaning up {s3_key}...")
                    self.s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
                    print(f"[SDK_OK] Cleaned up {s3_key}")
                except Exception as cleanup_error:
                    print(f"[SDK_ERROR] Failed to clean up {s3_key}: {cleanup_error!s}")
            raise ValueError(error_msg)

    def delete_folder(self, prefix):
        if self.verbose:
            print(f"[SDK_INFO] Starting to delete folder {prefix}...")
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)

            objects_to_delete = []
            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        objects_to_delete.append({"Key": obj["Key"]})

            if not objects_to_delete:
                print(f"[SDK_WARN] No objects found to delete for prefix: {prefix}")
                print("[SDK_OK] Folder delete (no-op) completed successfully")
                return

            print(f"[SDK_INFO] Found {len(objects_to_delete)} objects to delete. Deleting in chunks of 1000...")

            # Boto3 delete_objects can handle 1000 keys at a time
            for i in range(0, len(objects_to_delete), 1000):
                chunk = objects_to_delete[i:i+1000]
                self.s3.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={"Objects": chunk}
                )
                if self.verbose:
                    print(f"[SDK_DEBUG] Deleted chunk {i//1000 + 1}")

            print(f"[SDK_OK] Deleted s3://{self.bucket_name}/{prefix}")
            print("[SDK_OK] Folder deleted successfully")
        except Exception as e:
            error_msg = f"Failed to delete folder {prefix}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)

    def move_folder(self, src_prefix, dest_prefix):
        if self.verbose:
            print(f"[SDK_INFO] Starting to move folder from {src_prefix} to {dest_prefix}...")
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=src_prefix)

            keys_to_copy = []
            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        keys_to_copy.append(obj["Key"])

            if not keys_to_copy:
                error_msg = f"Source folder {src_prefix} does not exist or is empty"
                print(f"[SDK_FAIL] {error_msg}")
                raise ValueError(error_msg)

            print(f"[SDK_INFO] Found {len(keys_to_copy)} objects to move. Copying...")

            for src_key in keys_to_copy:
                dest_key = src_key.replace(src_prefix, dest_prefix, 1)
                if self.verbose:
                    print(f"[SDK_DEBUG] Copying {src_key} to {dest_key}...")
                self.s3.copy_object(Bucket=self.bucket_name, CopySource={"Bucket": self.bucket_name, "Key": src_key}, Key=dest_key)

            print("[SDK_INFO] Copy complete. Deleting source folder...")
            # Now delete the old folder efficiently
            self.delete_folder(src_prefix)

            print(f"[SDK_OK] Moved s3://{self.bucket_name}/{src_prefix} -> s3://{self.bucket_name}/{dest_prefix}")
            print("[SDK_OK] Folder moved successfully")
        except Exception as e:
            error_msg = f"Failed to move folder from {src_prefix} to {dest_prefix}: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)