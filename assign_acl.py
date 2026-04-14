from azure.identity import InteractiveBrowserCredential
from azure.storage.filedatalake import DataLakeServiceClient

ACCOUNT_URL = "https://ntscubicdataprod.dfs.core.windows.net"
FILESYSTEM = "cubic-augment"
DIRECTORY = "incoming_SAPBI/Archive"

# Your Azure AD Object ID
USER_OID = "bb1f8b84-b4c0-4a3f-85b6-188c6b8ae50e"

credential = InteractiveBrowserCredential()
service = DataLakeServiceClient(account_url=ACCOUNT_URL, credential=credential)

filesystem = service.get_file_system_client(FILESYSTEM)
directory = filesystem.get_directory_client(DIRECTORY)

print("Fixing ACLs on existing files...\n")

paths = filesystem.get_paths(path=DIRECTORY, recursive=True)

for path in paths:
    if path.is_directory:
        continue

    file_client = filesystem.get_file_client(path.name)

    # Get existing ACL
    acl_props = file_client.get_access_control()
    acl = acl_props['acl'].split(',')

    new_entry = f"user:{USER_OID}:r-x"

    if new_entry not in acl:
        acl.append(new_entry)
        new_acl = ",".join(acl)

        print(f"Applying ACL to {path.name}")
        file_client.set_access_control(acl=new_acl)
    else:
        print(f"Already has ACL: {path.name}")

print("\nDone. All existing files now have your read permissions.")
