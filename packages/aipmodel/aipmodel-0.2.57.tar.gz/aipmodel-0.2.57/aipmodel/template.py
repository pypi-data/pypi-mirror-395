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
    version="v1", 
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
    version="v2", 
    source_path="facebook/wav2vec2-base-960h"
)
print(f"HuggingFace Model ID: {hf_model_id}\n")


# --- STEP 4: Upload model from your own S3 (Initial Version) ---
print("\n--- STEP 4: Upload model from S3 (Version: v1) ---")
s3_model_name = "s3_test_model"
s3_model_id = manager.add_model(
    source_type="s3",
    model_name=s3_model_name,
    version="v1", 
    source_path="path/in/your/bucket/",
    code_path="path/to/your/local/model/model.py",
    external_ceph_endpoint_url="http://your-s3-endpoint.com",  
    external_ceph_bucket_name="your-s3-bucket-name",
    external_ceph_access_key="your-s3-access-key",
    external_ceph_secret_key="your-s3-secret-key"
)
print(f"S3 Model ID (Explicit): {s3_model_id}\n")

print("\n--- STEP 4b: Upload model from S3 (Auto-Fetch Credentials) ---")
s3_model_auto_id = manager.add_model(
    source_type="s3",
    model_name="s3_auto_auth_model",
    version="v1",
    source_path="path/in/your/user/bucket/",
    # No external keys provided here
)
print(f"S3 Model ID (Auto): {s3_model_auto_id}\n")

# --- STEP 5: Download a SPECIFIC model version (v1) ---
print("\n--- STEP 5: Download a specific v1 version locally ---")
manager.get_model(
    model_name="local_test_model",
    version="v1", 
    local_dest="./downloaded_local_model_v1/"
)
print("Download of v1 successful.")

print("\n--- STEP 6: Set specific version as Latest manually ---")
manager.set_latest_version(model_name="local_test_model", version="v1")

# --- STEP 6: List all models in your AIP project ---
print("\n--- STEP 7: List all models and versions ---")
manager.list_models()

print("\n--- STEP 8: Get model information ---")
manager.get_model_info(hf_model_name)
print("--- End Model Info ---")

# --- STEP 8: Delete a specific version (v1 of local_test_model) ---
print("\n--- STEP 9: Delete specific version (v1) of local_test_model ---")
manager.delete_model(model_name="local_test_model", version="v1")
print("Deleted version v1 successfully.")

# --- STEP 9: Delete the entire model (HF model still has v2) ---
print("\n--- STEP 10: Delete the remaining HF model completely ---")
manager.delete_model(model_name=hf_model_name)
print(f"Model {hf_model_name} completely deleted.")