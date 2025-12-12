# AIP Model SDK

This SDK provides a simple interface for registering, uploading, downloading, listing, and deleting machine learning models using ClearML and S3 (Ceph) as storage.

---

## Installation

Install from PyPI:

```bash
pip install aipmodel
```

---

## Authentication

You must provide your own **ClearML Access Key** and **Secret Key**, which you can obtain from:

[http://213.233.184.112:30080/](http://213.233.184.112:30080/) → Credentials section

---

## Example Usage

This example shows how to:

- Upload a local model
- Upload a Hugging Face model
- Upload a model from another S3
- Download a model
- List models
- Get model information
- Delete a model

```python
import os
from dotenv import load_dotenv
from aipmodel.model_registry import MLOpsManager

load_dotenv()

# --- STEP 1: Initialize MLOps Manager ---
print("\n--- STEP 1: Initialize MLOps Manager (Token-Based Auth) ---")
# The manager authenticates using the USER_TOKEN read from the environment (.env file).
manager = MLOpsManager(
    user_token=os.getenv("USER_TOKEN"), 
    CLEARML_API_HOST=os.getenv("CLEARML_API_HOST"),
    CEPH_ENDPOINT_URL=os.getenv("CEPH_ENDPOINT_URL"),
    USER_MANAGEMENT_API=os.getenv("USER_MANAGEMENT_API"),
    verbose=True 
)

# --- STEP 2: Upload local model (Initial Version) ---
print("\n--- STEP 2: Upload local model (Version: v1) ---")
local_model_id = manager.add_model(
    source_type="local",
    model_name="local_test_model",
    version="v1", # SIMPLIFIED VERSION NAME
    source_path="path/to/your/local/model/folder",
    code_path="path/to/your/local/model/model.py",
)
print(f"Local Model ID: {local_model_id}\n")

# --- STEP 3: Upload HuggingFace model (Version Update) ---
print("\n--- STEP 3: Upload HuggingFace model (Version: v2 - New Latest) ---")
hf_model_name = "hf_test_model"
hf_model_id = manager.add_model(
    source_type="hf",
    model_name=hf_model_name,
    version="v2", # SIMPLIFIED VERSION NAME (New latest version)
    source_path="facebook/wav2vec2-base-960h"
)
print(f"HuggingFace Model ID: {hf_model_id}\n")


# --- STEP 4: Upload model from your own S3 (Initial Version) ---
print("\n--- STEP 4: Upload model from S3 (Version: v1) ---")
s3_model_name = "s3_test_model"
s3_model_id = manager.add_model(
    source_type="s3",
    model_name=s3_model_name,
    version="v1", # SIMPLIFIED VERSION NAME
    source_path="path/in/your/bucket/",
    code_path="path/to/your/local/model/model.py",
    # Embedded external S3 credentials/endpoints directly
    external_ceph_endpoint_url="http://your-s3-endpoint.com",  
    external_ceph_bucket_name="your-s3-bucket-name",
    external_ceph_access_key="your-s3-access-key",
    external_ceph_secret_key="your-s3-secret-key"
)
print(f"S3 Model ID: {s3_model_id}\n")


# --- STEP 5: Download a SPECIFIC model version (v1) ---
print("\n--- STEP 5: Download a specific v1 version locally ---")
manager.get_model(
    model_name="local_test_model",
    version="v1", # EXPLICIT VERSION PASSED
    local_dest="./downloaded_local_model_v1/"
)
print("Download of v1 successful.")


# --- STEP 6: List all models in your AIP project ---
print("\n--- STEP 6: List all models and versions ---")
manager.list_models()


# --- STEP 7: Get model information (Check Version map) ---
print("\n--- STEP 7: Get model information for HF model ---")
manager.get_model_info(hf_model_name)
print("--- End Model Info ---")


# --- STEP 8: Delete a specific version (v1 of local_test_model) ---
print("\n--- STEP 8: Delete specific version (v1) of local_test_model ---")
manager.delete_model(model_name="local_test_model", version="v1")
print("Deleted version v1 successfully.")


# --- STEP 9: Delete the entire model (HF model still has v2) ---
print("\n--- STEP 9: Delete the remaining HF model completely ---")
manager.delete_model(model_name=hf_model_name)
print(f"Model {hf_model_name} completely deleted.")
```

---

## Functions Overview
## Functions Overview (Detailed)

| Function Name           | Input Type                                           | Example Input                                                                  | Output Type         | Example Output                                           | Terminal Output                                                                 |
|-------------------------|------------------------------------------------------|---------------------------------------------------------------------------------|---------------------|---------------------------------------------------------|---------------------------------------------------------------------------------|
| `create` (ProjectsAPI)   | `name: str, description: str`                        | `name="new_project", description="description of project"`                      | dict                | `{"id": "12345", "name": "new_project"}`                 | `[OK] Project created successfully: id='12345'`                                |
| `get_all` (ProjectsAPI)  | None                                                 | None                                                                            | list                | `[{"id": "12345", "name": "new_project"}]`               | `[OK] Retrieved N projects successfully`                                       |
| `create` (ModelsAPI)     | `name: str, project_id: str, metadata: dict, uri: str` | `name="new_model", project_id="12345", metadata={"key": "value"}, uri="uri"`   | dict                | `{"id": "67890", "name": "new_model"}`                   | `[OK] Model created successfully: id='67890'`                                  |
| `get_all` (ModelsAPI)    | `project_id: str`                                    | `project_id="12345"`                                                           | list                | `[{"id": "67890", "name": "new_model"}]`                 | `[OK] Retrieved N models successfully`                                         |
| `update` (ModelsAPI)     | `model_id: str, uri: str, metadata: dict or list`    | `model_id="67890", uri="new_uri", metadata=[{"key": "value"}]`                 | dict                | `{"id": "67890", "uri": "new_uri"}`                      | `[OK] Model metadata updated successfully for id='67890'`                      |
| `edit_uri` (ModelsAPI)   | `model_id: str, uri: str`                            | `model_id="67890", uri="new_uri"`                                              | dict                | `{"id": "67890", "uri": "new_uri"}`                      | `[OK] Model URI edited successfully for id='67890'`                            |
| `get_by_id` (ModelsAPI)  | `model_id: str`                                      | `model_id="67890"`                                                             | dict                | `{"id": "67890", "name": "new_model", "uri": "uri"}`     | `[OK] Model retrieved successfully: id='67890'`                                |
| `delete` (ModelsAPI)     | `model_id: str`                                      | `model_id="67890"`                                                             | dict                | `{"status": "success"}`                                  | `[OK] Model deleted successfully: id='67890'`                                  |
| `__init__` (MLOpsManager) | `CLEARML_API_SERVER_URL: str, CLEARML_USERNAME: str, CLEARML_ACCESS_KEY: str, CLEARML_SECRET_KEY: str, verbose: bool` | `CLEARML_API_SERVER_URL="url", CLEARML_USERNAME="user", ...` | None                | None                                                    | `[OK] MLOpsManager initialized successfully`                                   |
| `add_model` (MLOpsManager) | `source_type: str, model_name: str, source_path: str, code_path: str, external_ceph_*: str` | `source_type="local", model_name="local_model", source_path="path/to/model"` | str                 | `"model_id"`                                             | `[SUCCESS] Model 'local_model' (ID: model_id) added successfully`              |
| `get_model` (MLOpsManager) | `model_name: str, local_dest: str`                   | `model_name="local_model", local_dest="path/to/destination"`                   | dict                | `{"id": "12345", "name": "local_model"}`                 | `[OK] Download complete for model: 'local_model'`                              |
| `get_model_info` (MLOpsManager) | `identifier: str`                                | `identifier="local_model"`                                                     | dict or list        | `{"id": "12345", "name": "local_model"}`                 | `[OK] Model info retrieved by name`                                           |
| `list_models` (MLOpsManager) | `verbose: bool`                                    | `verbose=True`                                                                 | list                | `[("model_name", "model_id")]`                           | `[OK] Listed N models successfully`                                            |
| `delete_model` (MLOpsManager) | `model_id: str, model_name: str`                   | `model_id="12345"`                                                             | None                | None                                                    | `[SUCCESS] Model '12345' deleted successfully from ClearML and Ceph`           |
| `transfer_from_s3` (MLOpsManager) | `source_endpoint_url: str, source_access_key: str, source_secret_key: str, source_bucket: str, source_path: str, dest_prefix: str, exclude: list, overwrite: bool` | `source_endpoint_url="http://s3.example.com", ...` | bool                | `True`                                                   | `[OK] Transfer from S3 successful`                                             |

| Function            | Description                                         |
|--------------------|---------------------------------------------------|
| `add_model(...)`   | Uploads a model from local, Hugging Face, or external S3 |
| `get_model(...)`   | Downloads a model from S3 to local path             |
| `get_model_info(...)` | Retrieves detailed information about a model     |
| `list_models()`    | Lists all registered models in your ClearML project |
| `delete_model(...)`| Deletes a model from ClearML and S3                 |
| `transfer_from_s3(...)` | Transfers a model from an external S3 bucket to the initialized Ceph bucket |

---

## Notes

- Ceph credentials (`s3.cloud-ai.ir`, access key, secret key) are hardcoded and used for final storage.
- Your own external S3 bucket is supported only during upload (optional).
- No config file is needed. You must pass ClearML keys manually in code or use environment variables.
- The `source_path` parameter for Hugging Face models should be a valid Hugging Face model repository ID (e.g., `facebook/wav2vec2-base-960h`).
- The `code_path` parameter is optional and must point to a valid `.py` file if provided.

---

## Admin Instructions: Auto-Publishing to PyPI

This SDK uses a GitHub Actions workflow (`.github/workflows/publish.yaml`) for automatic versioning and PyPI publishing.

### Trigger Conditions

- Must push to the `main` branch
- Must include `pipy commit -push` in the commit message
- Must have `PUBLISH_TO_PYPI=true` in GitHub project variables

### Commit Message Format

The following patterns control the version bump:

| Description Contains      | Resulting Bump                 |
|--------------------------|-------------------------------|
| `pipy commit -push major`| Increments **major**          |
| `pipy commit -push minor`| Increments **minor**          |
| `pipy commit -push patch`| Increments **patch**          |
| `pipy commit -push`      | Increments **patch** (default)|

### What Happens Automatically

- Version is read from PyPI
- New version is calculated using `bump_version.py`
- Version in `__init__.py` and `setup.py` is updated
- Changes are committed and pushed to `main`
- Package is built and published to PyPI via Twine

No manual work is needed from the admin.