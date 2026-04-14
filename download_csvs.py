from azure.storage.blob import BlobServiceClient
import os

ACCOUNT_URL = "https://ntscubicdataprod.blob.core.windows.net"
CONTAINER_NAME = "cubic-augment"
PREFIX = "incoming_SAPBI/Archive/"
DOWNLOAD_DIR = "downloaded_csvs"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

SAS_TOKEN = "sv=2025-11-05&ss=bfqt&srt=co&sp=rwdlacupyx&se=2026-04-16T10:36:47Z&st=2026-04-10T02:21:47Z&spr=https&sig=hPJqRoNAZ%2BbgZhGqVveGnrJxzvxQx0jGdRtDDN8ME4g%3D"

service = BlobServiceClient(account_url=ACCOUNT_URL, credential=SAS_TOKEN)
container = service.get_container_client(CONTAINER_NAME)

print("Listing blobs...")
for blob in container.list_blobs(name_starts_with=PREFIX):
    if os.path.basename(blob.name).startswith("WA160") and blob.name.lower().endswith(".csv"):
        blob_client = container.get_blob_client(blob.name)
        local_path = os.path.join(DOWNLOAD_DIR, os.path.basename(blob.name))

        print(f"Downloading {blob.size / (1024 * 1024):.2f} MB → {local_path}")
        with open(local_path, "wb") as f:
            f.write(blob_client.download_blob().readall())

print("Done.")
