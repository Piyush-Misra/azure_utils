import sys
from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URLS = {
    "dev":  "https://ntscubicdatadev.blob.core.windows.net",
    "prod": "https://ntscubicdataprod.blob.core.windows.net"
}

if len(sys.argv) != 2 or sys.argv[1] not in ACCOUNT_URLS:
    print("Usage: python test_folder_access.py [dev|prod]")
    sys.exit(1)

env = sys.argv[1]
ACCOUNT_URL = ACCOUNT_URLS[env]

CONTAINER_NAME = "cubic-augment"
PREFIX = "incoming_SAPBI/Archive/"

credential = InteractiveBrowserCredential()
service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
container = service.get_container_client(CONTAINER_NAME)

print(f"Listing blobs in {env} under prefix: {PREFIX}\n")

total_bytes = 0

try:
    for blob in container.list_blobs(name_starts_with=PREFIX):
        size_mb = blob.size / (1024 * 1024)
        total_bytes += blob.size
        print(f"{blob.name}  —  {size_mb:.2f} MB")

    total_mb = total_bytes / (1024 * 1024)
    print(f"\nTotal size: {total_mb:.2f} MB")

except Exception as e:
    print("ERROR:", e)
