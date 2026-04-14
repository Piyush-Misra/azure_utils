from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient
import os

ACCOUNT_URL = "https://ntscubicdataprod.blob.core.windows.net"

DOWNLOAD_DIR = "downloaded_csvs"

CONTAINER_NAME = "cubic-augment"
PREFIX = "incoming_SAPBI/Archive/"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

credential = InteractiveBrowserCredential()
service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
container = service.get_container_client(CONTAINER_NAME)

print("Listing blobs...")
for blob in container.list_blobs(name_starts_with=PREFIX):
    if os.path.basename(blob.name).startswith("WA160") and blob.name.lower().endswith(".csv"):
        blob_client = container.get_blob_client(blob.name)
        local_path = os.path.join(DOWNLOAD_DIR, os.path.basename(blob.name))

        print(f"Downloading {blob.size / (1024 * 1024):.0f} MB of {blob.name} → {local_path}")
        with open(local_path, "wb") as f:
            f.write(blob_client.download_blob().readall())

print("Done.")
