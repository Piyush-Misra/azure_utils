import sys
from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URLS = {
    "dev":  "https://ntscubicdatadev.blob.core.windows.net",
    "prod": "https://ntscubicdataprod.blob.core.windows.net"
}

if len(sys.argv) != 2 or sys.argv[1] not in ACCOUNT_URLS:
    print("Usage: python test_access.py [dev|prod]")
    sys.exit(1)

env = sys.argv[1]
ACCOUNT_URL = ACCOUNT_URLS[env]

credential = InteractiveBrowserCredential()
service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)

container = service.get_container_client("cubic-augment")

print(f"Testing access to {env}...")
print(container.get_container_properties())
