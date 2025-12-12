import os
import shutil
from base64 import b64encode
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from huggingface_hub import snapshot_download
from fastapi import HTTPException
from typing import Optional, List, Dict, Any
import json
import logging
import time
import uuid

from .CephS3Manager import CephS3Manager

load_dotenv()

logger = logging.getLogger(__name__)

class ProjectsAPI:
    def __init__(self, post, verbose):
        self.verbose = verbose
        if self.verbose:
            print("[SDK_DEBUG] Initializing ProjectsAPI...")
        self._post = post
        print("[SDK_OK] ProjectsAPI initialized successfully")

    def create(self, name, description=""):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to create project: name={name}, description={description}")
        print(f"[SDK_INFO] Starting to create project: name={name}, description={description}")
        response = self._post("/projects.create", {"name": name, "description": description})
        if not response or "id" not in response:
            error_msg = "Failed to create project in ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Project creation completed: id={response['id']}")
        print(f"[SDK_OK] Project created successfully: id={response['id']}")
        return response

    def get_all(self):
        if self.verbose:
            print("[SDK_DEBUG] Preparing to retrieve all projects...")
        print("[SDK_INFO] Starting to get all projects...")
        response = self._post("/projects.get_all")
        if not response or "projects" not in response:
            error_msg = "Failed to retrieve projects from ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Projects retrieval completed: found {len(response['projects'])} projects")
        print(f"[SDK_OK] Retrieved {len(response['projects'])} projects successfully")
        return response["projects"]

class ModelsAPI:
    def __init__(self, post, verbose):
        self.verbose = verbose
        if self.verbose:
            print("[SDK_DEBUG] Initializing ModelsAPI...")
        self._post = post
        print("[SDK_OK] ModelsAPI initialized successfully")

    def get_all(self, project_id=None):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to retrieve models for project_id={project_id}")
        print(f"[SDK_INFO] Starting to get all models for project_id={project_id}")
        payload = {"project": project_id} if project_id else {}
        response = self._post("/models.get_all", payload)

        if isinstance(response, dict):
            if "models" in response and isinstance(response["models"], list):
                if self.verbose:
                    print(f"[SDK_DEBUG] Models retrieval completed: found {len(response['models'])} models")
                print(f"[SDK_OK] Retrieved {len(response['models'])} models successfully")
                return response["models"]
            if "data" in response and isinstance(response["data"], dict) and "models" in response["data"]:
                if self.verbose:
                    print(f"[SDK_DEBUG] Models retrieval completed: found {len(response['data']['models'])} models")
                print(f"[SDK_OK] Retrieved {len(response['data']['models'])} models successfully")
                return response["data"]["models"]

        error_msg = f"'models' not found in response: {response}"
        print(f"[SDK_ERROR] {error_msg}")
        raise ValueError("Failed to retrieve models from ClearML")

    def create(self, name, project_id, metadata=None, uri=""):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to create model: name={name}, project_id={project_id}, uri={uri}")
        print(f"[SDK_INFO] Starting to create model: name={name}, project_id={project_id}, uri={uri}")
        payload = {
            "name": name,
            "project": project_id,
            "uri": uri
        }

        if isinstance(metadata, (dict, list)):
            payload["metadata"] = metadata

        response = self._post("/models.create", payload)
        if not response or "id" not in response:
            error_msg = "Failed to create model in ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Model creation completed: id={response['id']}")
        print(f"[SDK_OK] Model created successfully: id={response['id']}")
        return response

    def update(self, model_id, uri=None, metadata=None):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to update model: model_id={model_id}, uri={uri}")
        print(f"[SDK_INFO] Starting to update model: model_id={model_id}, uri={uri}")
        payload = {"model": model_id}
        if uri:
            payload["uri"] = uri
        if isinstance(metadata, (dict, list)):
            payload["metadata"] = metadata

        response = self._post("/models.add_or_update_metadata", payload)
        if not response:
            error_msg = "Failed to update model metadata in ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Model metadata update completed for id={model_id}")
        print(f"[SDK_OK] Model metadata updated successfully for id={model_id}")
        return response

    def edit_uri(self, model_id, uri):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to edit URI for model_id={model_id}, uri={uri}")
        print(f"[SDK_INFO] Starting to edit URI for model_id={model_id}, uri={uri}")
        payload = {"model": model_id, "uri": uri}
        response = self._post("/models.edit", payload)
        if not response:
            error_msg = "Failed to edit model URI in ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Model URI edit completed for id={model_id}")
        print(f"[SDK_OK] Model URI edited successfully for id={model_id}")
        return response

    def get_by_id(self, model_id):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to retrieve model by id: {model_id}")
        print(f"[SDK_INFO] Starting to get model by id: {model_id}")
        response = self._post("/models.get_by_id", {"model": model_id})
        
        model_object = response.get("model") or response.get("data", {}).get("model")
        
        if not model_object:
            error_msg = f"Failed to retrieve model with ID {model_id} from ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        
        if self.verbose:
            print(f"[SDK_DEBUG] Model retrieval completed: id={model_object.get('id')}")
        print(f"[SDK_OK] Model retrieved successfully: id={model_object.get('id')}")
        
        return model_object 

    def delete(self, model_id):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to delete model: id={model_id}")
        print(f"[SDK_INFO] Starting to delete model: id={model_id}")
        response = self._post("/models.delete", {"model": model_id})
        if not response:
            error_msg = f"Failed to delete model with ID {model_id} from ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print(f"[SDK_DEBUG] Model deletion completed: id={model_id}")
        print(f"[SDK_OK] Model deleted successfully: id={model_id}")
        return response

def get_user_info_with_bearer(bearer_token: str, user_management_url):
    try:
        url = urljoin(user_management_url.rstrip("/") + "/", "metadata")
        
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {bearer_token}"},
            timeout=100,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to authenticate with bearer token: {response.text}",
            )
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error calling user management API with bearer token: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with user management service: {str(e)}",
        )

def get_user_metadata(bearer_token: Optional[str] = None, user_management_url: str = None):
    if bearer_token:
        logger.info("Authenticating with bearer token")
        user_data = get_user_info_with_bearer(bearer_token , user_management_url)
        user_metadata = user_data.get("metadata")
        authenticated_username = user_data.get("username")
        
        if not user_metadata or not authenticated_username:
             raise KeyError(f"User API returned data without 'metadata' or 'username' keys. Received keys: {list(user_data.keys())}")
             
        return user_metadata, authenticated_username
    
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required: Provide Bearer token in Authorization header"
        )

class MLOpsManager:
    def _parse_versions_map(self, metadata_container):
        versions_map_raw = "{}"
        
        if isinstance(metadata_container, dict):
            if "versions_map" in metadata_container:
                val = metadata_container["versions_map"]
                if isinstance(val, dict) and "value" in val:
                    versions_map_raw = val["value"]
                elif isinstance(val, str):
                     versions_map_raw = val
        
        elif isinstance(metadata_container, list):
            for item in metadata_container:
                if isinstance(item, dict) and item.get("key") == "versions_map":
                    versions_map_raw = item.get("value", "{}")
                    break
        
        if isinstance(versions_map_raw, dict):
             return versions_map_raw
             
        try:
            return json.loads(versions_map_raw)
        except:
            return {}

    def _extract_metadata_value(self, metadata_container, key, default=None):
        if isinstance(metadata_container, dict):
            if key in metadata_container:
                val = metadata_container[key]
                if isinstance(val, dict) and "value" in val:
                    return str(val["value"])
                return str(val)
            return default
            
        elif isinstance(metadata_container, list):
            for item in metadata_container:
                if isinstance(item, dict) and item.get("key") == key:
                    value = item.get("value", default)
                    return str(value) if value is not None else default
        return default

    def set_latest_version(self, model_name, version):
        print(f"[SDK_INFO] Setting latest version for '{model_name}' to '{version}'...")
        model_id = self.get_model_id_by_name(model_name)
        if not model_id:
            raise ValueError(f"Model {model_name} not found")

        model_data = self.models.get_by_id(model_id)
        metadata = model_data.get("metadata", {}) 
        
        versions_map = self._parse_versions_map(metadata)
        
        if version not in versions_map:
            raise ValueError(f"Version '{version}' does not exist for model '{model_name}'")

        latest_path = versions_map[version]["path"]
        uri = f"s3://{self.ceph.bucket_name}/{latest_path}"

        self.models.edit_uri(model_id, uri=uri)
        
        new_metadata = [
            {"key": "latest_version", "type": "str", "value": version},
            {"key": "haveModelPy", "type": "str", "value": versions_map[version].get("haveModelPy", "false")}
        ]
        self.models.update(model_id, metadata=new_metadata)
        print(f"[SDK_SUCCESS] Latest version for '{model_name}' is now '{version}'")

    def __init__(
        self,
        user_token,
        CLEARML_API_HOST=None,
        CEPH_ENDPOINT_URL=None,
        USER_MANAGEMENT_API=None,
        verbose=False
    ):
        self.verbose = verbose
        if self.verbose:
            print("[SDK_INFO] Initializing MLOpsManager...")
        print("[SDK_INFO] Starting MLOpsManager initialization...")

        self.USER_TOKEN = user_token
        self.CLEARML_API_HOST = CLEARML_API_HOST or os.environ.get("CLEARML_API_HOST")
        self.USER_MANAGEMENT_API = USER_MANAGEMENT_API or os.environ.get("USER_MANAGEMENT_API")
        self.CEPH_ENDPOINT_URL = CEPH_ENDPOINT_URL or os.environ.get("CEPH_ENDPOINT_URL")

        user_info, self.CLEARML_USERNAME = get_user_metadata(bearer_token=user_token, user_management_url=self.USER_MANAGEMENT_API)

        if self.verbose:
            print("[SDK_INFO] Validating ClearML credentials...")
        if not all([self.CLEARML_API_HOST, self.USER_MANAGEMENT_API, self.CEPH_ENDPOINT_URL]):
            error_msg = "Missing required ClearML configuration parameters"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print("[SDK_OK] ClearML credentials validated successfully")

        self.CEPH_ADMIN_ACCESS_KEY = user_info["s3_access_key"]
        self.CEPH_ADMIN_SECRET_KEY = user_info["s3_secret_key"]
        self.CEPH_USER_BUCKET = user_info["s3_bucket"]
        self.CLEARML_ACCESS_KEY = user_info["clearml_access_key"]
        self.CLEARML_SECRET_KEY = user_info["clearml_secret_key"]
        if self.verbose:
            print(f"[SDK_DEBUG] {self.CLEARML_ACCESS_KEY}, {self.CLEARML_SECRET_KEY}, {self.CLEARML_USERNAME}")

        if self.verbose:
            print("[SDK_INFO] Performing ClearML service health checks...")
        if not self.check_clearml_service():
            error_msg = "ClearML Server down."
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if not self.check_clearml_auth():
            error_msg = "ClearML Authentication not correct."
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        if self.verbose:
            print("[SDK_OK] ClearML service health checks completed")

        if self.verbose:
            print("[SDK_INFO] Initializing CephS3Manager...")
        self.ceph = CephS3Manager(
            self.CEPH_ENDPOINT_URL,
            self.CEPH_ADMIN_ACCESS_KEY,
            self.CEPH_ADMIN_SECRET_KEY,
            self.CEPH_USER_BUCKET,
            verbose=self.verbose
        )
        if self.verbose:
            print("[SDK_OK] CephS3Manager initialized successfully")

        if self.verbose:
            print("[SDK_INFO] Preparing to login to ClearML...")
        print("[SDK_INFO] Logging in to ClearML...")
        creds = f"{self.CLEARML_ACCESS_KEY}:{self.CLEARML_SECRET_KEY}"
        auth_header = b64encode(creds.encode("utf-8")).decode("utf-8")
        res = requests.post(
            f"{self.CLEARML_API_HOST}/auth.login",
            headers={"Authorization": f"Basic {auth_header}"}
        )
        if res.status_code != 200:
            error_msg = "Failed to authenticate with ClearML"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg)
        self.token = res.json()["data"]["token"]
        if self.verbose:
            print("[SDK_OK] ClearML login completed successfully")
        print("[SDK_OK] Logged in to ClearML successfully")

        self.projects = ProjectsAPI(self._post, verbose=self.verbose)
        self.models = ModelsAPI(self._post, verbose=self.verbose)

        if self.verbose:
            print("[SDK_INFO] Checking for user-specific project...")
        print("[SDK_INFO] Getting or creating user-specific project...")
        projects = self.projects.get_all()
        self.project_name = f"project_{self.CLEARML_USERNAME}"
        exists = [p for p in projects if p["name"] == self.project_name]
        self.project_id = exists[0]["id"] if exists else self.projects.create(self.project_name)["id"]
        if self.verbose:
            print(f"[SDK_DEBUG] User-specific project processing completed: project_id={self.project_id}")
        print(f"[SDK_OK] Project ID: {self.project_id}")
        print("[SDK_OK] MLOpsManager initialized successfully")

    def _post(self, path, params=None):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing POST request to {path}...")
        print(f"[SDK_INFO] Starting POST request to {path}...")
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            res = requests.post(f"{self.CLEARML_API_HOST}{path}", headers=headers, json=params)
            res.raise_for_status()

            data = res.json()
            if "data" not in data:
                error_msg = f"No 'data' key in response: {data}"
                print(f"[SDK_ERROR] {error_msg}")
                raise ValueError(f"Request to {path} failed: No data in response")
            if self.verbose:
                print(f"[SDK_DEBUG] POST request to {path} completed successfully")
            print(f"[SDK_OK] POST request to {path} successful")
            return data["data"]

        except requests.exceptions.RequestException as e:
            error_msg = f"Request to {path} failed: {e}"
            print(f"[SDK_ERROR] {error_msg}")
            print(f"[SDK_ERROR] Status Code: {res.status_code}, Response: {res.text}")
            raise ValueError(f"Request to {path} failed: {e!s}")

        except ValueError as e:
            error_msg = f"Failed to parse JSON from {path}: {e}"
            print(f"[SDK_ERROR] {error_msg}")
            print(f"[SDK_ERROR] Raw response: {res.text}")
            raise ValueError(f"Request to {path} failed: {e!s}")

    def check_clearml_service(self):
        if self.verbose:
            print("[SDK_DEBUG] Preparing to check ClearML service...")
        print("[SDK_INFO] Checking ClearML service...")
        try:
            r = requests.get(self.CLEARML_API_HOST + "/auth.login", timeout=5)
            if r.status_code in [200, 401]:
                if self.verbose:
                    print("[SDK_DEBUG] ClearML service check completed")
                print("[SDK_OK] ClearML Service")
                return True
            error_msg = f"ClearML Service {r.status_code}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("ClearML Service is not reachable")
        except Exception as e:
            error_msg = f"ClearML Service: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("ClearML Service is not reachable")

    def check_clearml_auth(self):
        if self.verbose:
            print("[SDK_DEBUG] Preparing to check ClearML authentication...")
        print("[SDK_INFO] Checking ClearML authentication...")
        try:
            creds = f"{self.CLEARML_ACCESS_KEY}:{self.CLEARML_SECRET_KEY}"
            auth_header = b64encode(creds.encode("utf-8")).decode("utf-8")
            r = requests.post(
                self.CLEARML_API_HOST + "/auth.login",
                headers={"Authorization": f"Basic {auth_header}"},
                timeout=5
            )
            if r.status_code == 200:
                if self.verbose:
                    print("[SDK_DEBUG] ClearML authentication check completed")
                print("[SDK_OK] ClearML Auth")
                return True
            error_msg = f"ClearML Auth {r.status_code}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("ClearML Authentication failed")
        except Exception as e:
            error_msg = f"ClearML Auth: {e!s}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError("ClearML Authentication failed")

    def get_model_id_by_name(self, name):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to get model ID for name: {name}")
        print(f"[SDK_INFO] Starting to get model ID by name: {name}")
        models = self.models.get_all(self.project_id)
        if self.verbose:
            print(f"[SDK_DEBUG] Retrieved {len(models)} models for ID lookup")
        for m in models:
            if m["name"] == name:
                if self.verbose:
                    print(f"[SDK_DEBUG] Model ID lookup completed: id={m['id']}")
                print(f"[SDK_OK] Model ID found: {m['id']}")
                return m["id"]
        if self.verbose:
            print("[SDK_DEBUG] Model ID lookup completed: no model found")
        print("[SDK_OK] No model found with given name")
        return None

    def get_model_name_by_id(self, model_id):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to get model name for ID: {model_id}")
        print(f"[SDK_INFO] Starting to get model name by ID: {model_id}")
        model = self.models.get_by_id(model_id)
        result = model.get("name") if model else None
        if result:
            if self.verbose:
                print(f"[SDK_DEBUG] Model name lookup completed: name={result}")
            print(f"[SDK_OK] Model name found: {result}")
        else:
            if self.verbose:
                print("[SDK_DEBUG] Model name lookup completed: no model found")
            print("[SDK_OK] No model found with given ID")
        return result

    def generate_random_string(self):
        if self.verbose:
            print("[SDK_DEBUG] Preparing to generate random string...")
        print("[SDK_INFO] Generating random string...")
        import random
        import string
        result = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        if self.verbose:
            print(f"[SDK_DEBUG] Random string generation completed: {result}")
        print(f"[SDK_OK] Random string generated: {result}")
        return result

    def transfer_from_s3(self, source_endpoint_url, source_access_key, source_secret_key, source_bucket, source_path, dest_prefix):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing transfer from S3: source_path={source_path}, dest_prefix={dest_prefix}")
        print(f"[SDK_INFO] Starting transfer from S3: source_path={source_path}, dest_prefix={dest_prefix}")
        tmp_dir = None
        try:
            tmp_dir = f"./tmp_{self.generate_random_string()}"
            if self.verbose:
                print(f"[SDK_DEBUG] Creating temporary directory: {tmp_dir}")
            print(f"[SDK_INFO] Creating temporary directory: {tmp_dir}")
            os.makedirs(tmp_dir, exist_ok=True)

            if self.verbose:
                print("[SDK_DEBUG] Initializing source CephS3Manager...")
            print("[SDK_INFO] Initializing source CephS3Manager...")
            src_ceph = CephS3Manager(source_endpoint_url, source_access_key, source_secret_key, source_bucket)
            if self.verbose:
                print("[SDK_OK] Source CephS3Manager initialized")
            print("[SDK_INFO] Downloading from source...")
            src_ceph.download(source_path, tmp_dir, keep_folder=True, exclude=[".git", ".DS_Store"], overwrite=True)

            if self.verbose:
                print("[SDK_DEBUG] Preparing to delete destination folder if exists...")
            print("[SDK_INFO] Deleting destination folder if exists...")
            self.ceph.delete_folder(dest_prefix)
            if self.verbose:
                print("[SDK_DEBUG] Destination folder deletion completed")
            print("[SDK_INFO] Uploading to destination...")
            self.ceph.upload(tmp_dir, dest_prefix)

            if self.verbose:
                print("[SDK_OK] S3 transfer completed successfully")
            print("[SDK_OK] Transfer from S3 successful")
            return True
        except Exception as e:
            error_msg = f"Failed to transfer model from S3: {e}"
            print(f"[SDK_FAIL] {error_msg}")
            try:
                self.ceph.delete_folder(dest_prefix)
            except Exception as cleanup_error:
                print(f"[SDK_ERROR] Failed to clean up destination folder {dest_prefix}: {cleanup_error}")
            raise ValueError(f"Failed to transfer model from S3: {e!s}")
        finally:
            if tmp_dir and os.path.exists(tmp_dir):
                try:
                    shutil.rmtree(tmp_dir)
                    if self.verbose:
                        print(f"[SDK_DEBUG] Temporary directory cleanup completed: {tmp_dir}")
                    print(f"[SDK_OK] Cleaned up temporary directory {tmp_dir}")
                except Exception as cleanup_error:
                    print(f"[SDK_ERROR] Failed to clean up temporary directory {tmp_dir}: {cleanup_error}")

    def add_model(self, source_type, model_name=None, version=None, source_path=None, code_path=None,
                  external_ceph_endpoint_url=None, external_ceph_bucket_name=None, external_ceph_access_key=None, external_ceph_secret_key=None):

        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to add model: source_type={source_type}, model_name={model_name}, version={version}")
        print(f"[SDK_INFO] Starting to add model: source_type={source_type}, model_name={model_name}, version={version}")

        if not model_name or not isinstance(model_name, str):
            error_msg = "Model name is required"
            logger.error(error_msg)
            print("[SDK_ERROR] model_name must be a non-empty string")
            return None
        
        if not version or not isinstance(version, str):
            error_msg = "Version is required"
            logger.error(error_msg)
            print("[SDK_ERROR] version must be a non-empty string")
            return None

        if source_type not in ["local", "hf", "s3"]:
            error_msg = f"Unknown source_type: {source_type}"
            logger.error(error_msg)
            print(f"[SDK_ERROR] {error_msg}")
            return None
        
        if source_type == "local":
            if not source_path or not os.path.exists(source_path):
                error_msg = f"Local path {source_path} does not exist"
                print(f"[SDK_FAIL] {error_msg}")
                return None
        
        if source_type == "s3":
            provided_creds = all([external_ceph_access_key, external_ceph_secret_key, external_ceph_bucket_name, external_ceph_endpoint_url])
            
            if not provided_creds:
                print("[SDK_INFO] S3 Credentials not provided. Fetching from User Management API...")
                try:
                    user_meta, _ = get_user_metadata(bearer_token=self.USER_TOKEN, user_management_url=self.USER_MANAGEMENT_API)
                    external_ceph_access_key = user_meta["s3_access_key"]
                    external_ceph_secret_key = user_meta["s3_secret_key"]
                    external_ceph_bucket_name = user_meta["s3_bucket"]
                    external_ceph_endpoint_url = self.CEPH_ENDPOINT_URL
                    print("[SDK_OK] Auto-fetched S3 credentials successfully")
                except Exception as e:
                    error_msg = f"Failed to auto-fetch S3 credentials: {e}"
                    print(f"[SDK_FAIL] {error_msg}")
                    return None

            if not all([source_path, external_ceph_access_key, external_ceph_secret_key, external_ceph_endpoint_url, external_ceph_bucket_name]):
                error_msg = "Missing required S3 parameters (even after auto-fetch attempt)"
                print(f"[SDK_FAIL] {error_msg}")
                return None

        if self.verbose:
            print("[SDK_DEBUG] Checking for existing model...")
        
        is_new_model = False
        existing_model_id = self.get_model_id_by_name(model_name)
        if existing_model_id:
            model_id = existing_model_id
            print(f"[SDK_INFO] Adding version to existing model ID: {model_id}")
        else:
            print("[SDK_INFO] Creating new model in ClearML...")
            created_model = self.models.create(name=model_name, project_id=self.project_id, uri="s3://placeholder")
            model_id = created_model["id"]
            is_new_model = True
            print(f"[SDK_OK] Model created with ID: {model_id}")

        if source_type == "hf":
            model_folder_name = f"hf_{model_name}"
        elif source_type == "local" or source_type == "s3":
            model_folder_name = os.path.basename(source_path.rstrip('/'))
        else:
            model_folder_name = "unknown"

        dest_version_path = f"_models/{model_id}/{version}/"
        temp_suffix = self.generate_random_string()
        dest_temp_path = f"_models/{model_id}/{version}_tmp_{temp_suffix}/"

        local_path = None
        temp_local_path = None
        have_model_py = False
        size_mb = 0.0

        try:
            print(f"[SDK_INFO] Uploading to temporary path: {dest_temp_path}")

            if source_type == "local":
                temp_local_path = f"./tmp_{temp_suffix}"
                shutil.copytree(source_path, temp_local_path, dirs_exist_ok=True)
                size_mb = self.ceph.upload(temp_local_path, dest_temp_path)
            elif source_type == "hf":
                local_path = snapshot_download(repo_id=source_path)
                size_mb = self.ceph.upload(local_path, os.path.join(dest_temp_path, model_folder_name))
            elif source_type == "s3":
                success = self.transfer_from_s3(
                    external_ceph_endpoint_url, external_ceph_access_key, external_ceph_secret_key,
                    external_ceph_bucket_name, source_path, dest_temp_path
                )
                if not success: raise ValueError("S3 Transfer failed")
                size_mb = self.ceph.get_uri_size(f"s3://{self.ceph.bucket_name}/{dest_temp_path}")

            if code_path and os.path.isfile(code_path):
                self.ceph.upload(code_path, dest_temp_path + "model.py")
                have_model_py = True

            if self.ceph.check_if_exists(dest_version_path):
                print(f"[SDK_INFO] Version {version} exists. Overwriting...")
                self.ceph.delete_folder(dest_version_path)
            
            self.ceph.move_folder(dest_temp_path, dest_version_path)
            print("[SDK_OK] Upload committed successfully.")

            model_data = self.models.get_by_id(model_id)
            metadata = model_data.get("metadata", {})
            
            versions_map = self._parse_versions_map(metadata)

            version_info = {
                "path": dest_version_path,
                "size": size_mb,
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "haveModelPy": str(have_model_py).lower(),
                "folderName": model_folder_name
            }
            versions_map[version] = version_info
            
            # Clean up potential garbage keys before saving back
            keys_to_clean = [k for k in versions_map.keys() if k in ["key", "value", "type"]]
            for k in keys_to_clean:
                del versions_map[k]
            
            total_size = sum(float(v["size"]) for v in versions_map.values() if isinstance(v, dict) and "size" in v)

            new_metadata = [
                {"key": "versions_map", "type": "str", "value": json.dumps(versions_map)},
                {"key": "latest_version", "type": "str", "value": version},
                {"key": "modelSize", "type": "float", "value": f"{total_size:.2f}"},
                {"key": "modelFolderName", "type": "str", "value": model_folder_name},
                {"key": "haveModelPy", "type": "str", "value": str(have_model_py).lower()}
            ]

            uri = f"s3://{self.ceph.bucket_name}/{dest_version_path}"
            self.models.edit_uri(model_id, uri=uri)
            self.models.update(model_id, metadata=new_metadata)

            print(f"[SDK_SUCCESS] Model '{model_name}' version '{version}' added successfully.")
            return model_id

        except (Exception, KeyboardInterrupt) as e:
            error_msg = f"Upload or registration failed: {e}"
            logger.error(error_msg, exc_info=True)
            print(f"[SDK_ERROR] {error_msg}")
            print("[SDK_INFO] Cleaning up partially uploaded model...")
            if "model_id" in locals():
                try:
                    if is_new_model:
                        self.models.delete(model_id)
                        if self.verbose:
                            print("[SDK_DEBUG] ClearML model cleanup completed (newly created model)")
                        print("[SDK_OK] Cleaned up ClearML model (rolled back creation)")
                    else:
                        print(f"[SDK_INFO] Model ID {model_id} existed before this operation. Skipping ClearML deletion to preserve other versions.")
                except Exception as cleanup_error:
                    error_cleanup = f"Failed to clean up ClearML model {model_id}: {cleanup_error}"
                    logger.error(error_cleanup)
                    print(f"[SDK_ERROR] {cleanup_error}")
            if dest_temp_path:
                try:
                    self.ceph.delete_folder(dest_temp_path)
                    if self.verbose:
                        print("[SDK_DEBUG] Ceph folder cleanup completed")
                    print("[SDK_OK] Cleaned up temp folder")
                except Exception as cleanup_error:
                    error_cleanup = f"Failed to clean up Ceph folder {dest_temp_path}: {cleanup_error}"
                    logger.error(error_cleanup)
                    print(f"[SDK_ERROR] {cleanup_error}")
            return None
        finally:
            for path in [local_path, temp_local_path]:
                if path and os.path.exists(path):
                    try:
                        shutil.rmtree(path)
                        if self.verbose:
                            print(f"[SDK_DEBUG] Local directory cleanup completed: {path}")
                        print(f"[SDK_OK] Cleaned up local directory {path}")
                    except Exception as cleanup_error:
                        error_cleanup = f"Failed to clean up local directory {path}: {cleanup_error}"
                        logger.error(error_cleanup)
                        print(f"[SDK_ERROR] {cleanup_error}")

    def get_model(self, model_name, local_dest, version=None):
        logger.info("Starting get_model for name=%r, dest=%r, version=%r", model_name, local_dest, version)
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to get model: model_name={model_name}, local_dest={local_dest}, version={version}")
        print(f"[SDK_INFO] Starting get_model: model_name={model_name}, local_dest={local_dest}, version={version or 'latest'}")

        try:
            model_id = self.get_model_id_by_name(model_name)
            if not model_id: raise ValueError(f"Model {model_name} not found")
            
            model_data = self.models.get_by_id(model_id)
            metadata = model_data.get("metadata", {})
            
            versions_map = self._parse_versions_map(metadata)
            target_path = None

            if version:
                if version not in versions_map: raise ValueError(f"Version {version} not found")
                target_path = versions_map[version]["path"]
            else:
                uri = model_data.get("uri")
                if uri and uri.startswith("s3://"):
                    latest_version = self._extract_metadata_value(metadata, "latest_version")
                    if latest_version and latest_version in versions_map:
                         target_path = versions_map[latest_version]["path"]
                    else:
                         _, target_path = uri.replace("s3://", "").split("/", 1)
                else: raise ValueError("No valid URI for latest version")

            print(f"[SDK_INFO] Downloading from: {target_path}")
            self.ceph.download(
                target_path,
                local_dest,
                keep_folder=True,
                exclude=[".git", ".DS_Store"],
                overwrite=True,
            )
            print(f"[SDK_OK] Download complete for model: {model_name}")

        except Exception as exc:
            error_msg = f"Failed to download model: {exc}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(error_msg) from exc

    def get_model_info(self, identifier):
        if self.verbose:
            print(f"[SDK_DEBUG] Preparing to get model info for identifier: {identifier}")
        print(f"[SDK_INFO] Starting to get model info for identifier: {identifier}")
        
        model_id = self.get_model_id_by_name(identifier)
        if not model_id: model_id = identifier

        try:
            data = self.models.get_by_id(model_id)
        except:
             raise ValueError(f"No model found with identifier: '{identifier}'")

        m = data
        metadata = m.get("metadata", {})
        
        total_size = self._extract_metadata_value(metadata, "modelSize", "0")
        latest_version = self._extract_metadata_value(metadata, "latest_version", "N/A")
        
        versions_map = self._parse_versions_map(metadata)
        
        print("=" * 50)
        print(f"SDK_INFO: ID: {m.get('id')}")
        print(f"SDK_INFO: Name: {m.get('name')}")
        print(f"SDK_INFO: Total Size: {total_size} MB")
        print(f"SDK_INFO: Latest Version: {latest_version}")
        
        print("\nSDK_INFO: [Versions]")
        if versions_map:
            def sort_key(item):
                v, _ = item
                if v.startswith('v') and v[1:].isdigit():
                    return (0, int(v[1:]))
                return (1, v)
                
            sorted_versions = sorted(versions_map.items(), key=sort_key)

            for v, info in sorted_versions:
                if not isinstance(info, dict):
                    continue 
                size_mb = info.get('size', 0)
                print(f"SDK_INFO:   - {v:<10} | Size: {size_mb:.2f} MB | Created: {info.get('created')}")
        else:
             print("SDK_INFO:   No versions recorded in metadata.")
        print("=" * 50)

    def list_models(self, verbose=True):
        if self.verbose:
            print("[SDK_INFO] Preparing to list models...")
        print("[SDK_INFO] Starting to list models...")
        try:
            models = self.models.get_all(self.project_id)
            results = []
            
            print(f"{'Model Name':<25} | {'ID':<25} | {'Latest':<10} | {'Size (MB)':<15} | {'Versions'}")
            print("-" * 120)

            for m in models:
                name = m["name"]
                mid = m["id"]
                metadata = m.get("metadata", {})
                
                versions_map = self._parse_versions_map(metadata)
                latest = self._extract_metadata_value(metadata, "latest_version", "N/A")
                total_size = self._extract_metadata_value(metadata, "modelSize", "0.00")
                
                valid_versions = [v for v in versions_map.keys() if v.startswith('v') and isinstance(versions_map[v], dict)]

                def sort_key(v):
                    if v.startswith('v') and v[1:].isdigit():
                        return (0, int(v[1:]))
                    return (1, v)

                sorted_keys = sorted(valid_versions, key=sort_key)
                
                formatted_versions = []
                for v in sorted_keys:
                    if v == latest:
                        formatted_versions.append(f"{v} (latest)")
                    else:
                        formatted_versions.append(v)
                
                display_versions = ", ".join(formatted_versions)
                
                print(f"{name:<25} | {mid:<25} | {latest:<10} | {str(total_size):<15} | {display_versions}")
                results.append({"name": name, "id": mid, "versions": sorted_keys, "latest": latest})
            
            print("[SDK_OK] Models listed successfully")
            return results
        except Exception as e:
            error_msg = f"Failed to list models: {e}"
            print(f"[SDK_FAIL] {error_msg}")
            raise ValueError(f"Failed to list models: {e!s}")

    def delete_model(self, model_id=None, model_name=None, version=None):
        print(f"[SDK_INFO] Starting to delete model: model_id={model_id}, model_name={model_name}, version={version}")
        if model_name and not model_id:
            model_id = self.get_model_id_by_name(model_name)
        if not model_id: raise ValueError(f"No model found")

        model_data = self.models.get_by_id(model_id)
        metadata = model_data.get("metadata", {})
        
        versions_map = self._parse_versions_map(metadata)

        # Force clean up garbage keys from versions_map in memory
        keys_to_clean = [k for k in versions_map.keys() if k in ["key", "value", "type"]]
        for k in keys_to_clean:
            del versions_map[k]

        if version:
            if version not in versions_map: raise ValueError(f"Version {version} not found")
            
            path_to_delete = versions_map[version]["path"]
            self.ceph.delete_folder(path_to_delete)
            del versions_map[version]
            
            if not versions_map:
                print("[SDK_INFO] No versions left. Deleting entire model...")
                self.ceph.delete_folder(f"_models/{model_id}/") 
                self.models.delete(model_id)
            else:
                total_size = sum(float(v["size"]) for v in versions_map.values() if isinstance(v, dict) and "size" in v)
                latest_ver = self._extract_metadata_value(metadata, "latest_version", None)
                new_latest = latest_ver

                if latest_ver == version:
                    def sort_key(v):
                        if v.startswith('v') and v[1:].isdigit():
                            return (0, int(v[1:]))
                        return (1, v)

                    # Only sort keys that are left (which are valid now)
                    sorted_versions_keys = sorted(versions_map.keys(), key=sort_key)
                    if sorted_versions_keys:
                        new_latest = sorted_versions_keys[-1]
                        new_uri = f"s3://{self.ceph.bucket_name}/{versions_map[new_latest]['path']}"
                        self.models.edit_uri(model_id, new_uri)
                        print(f"[SDK_WARN] Deleted latest version. New latest is {new_latest}")
                    else:
                         # Should not happen if versions_map is not empty
                         new_latest = "N/A"

                new_metadata = [
                    {"key": "versions_map", "type": "str", "value": json.dumps(versions_map)},
                    {"key": "modelSize", "type": "float", "value": f"{total_size:.2f}"},
                    {"key": "latest_version", "type": "str", "value": new_latest},
                    {"key": "haveModelPy", "type": "str", "value": versions_map[new_latest].get("haveModelPy", "false") if new_latest in versions_map else "false"}
                ]
                self.models.update(model_id, metadata=new_metadata)
            print(f"[SDK_SUCCESS] Deleted version {version}")

        else:
            self.ceph.delete_folder(f"_models/{model_id}/")
            self.models.delete(model_id)
            print(f"[SDK_SUCCESS] Model '{model_id}' deleted completely")

if __name__ == "__main__":
    model_registry = MLOpsManager(user_token=os.getenv("USER_TOKEN"), verbose=True)