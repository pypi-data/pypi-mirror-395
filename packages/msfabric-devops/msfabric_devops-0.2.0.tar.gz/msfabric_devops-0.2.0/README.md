# msfabric-devops

A Python package to interact with Microsoft Fabric objects, providing functionality to manage workspaces, semantic models, and items through the Fabric REST API.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Authentication](#authentication)
  - [get_access_token](#get_access_tokentenant_idnone-client_idnone-client_secretnone---str)
- [Workspaces](#workspaces)
  - [get_workspaces](#get_workspacestoken---listdict)
  - [get_workspace_by_id](#get_workspace_by_idtoken-workspace_id---dict)
  - [get_workspaces_by_name](#get_workspaces_by_nametoken-workspace_name---listdict)
  - [create_workspace](#create_workspacetoken-workspace_name---dict)
  - [delete_workspace](#delete_workspacetoken-workspace_id---none)
- [Items](#items)
  - [get_items](#get_itemstoken-workspace_id---listdict)
  - [get_item_by_id](#get_item_by_idtoken-workspace_id-item_id---dict)
  - [get_items_by_name](#get_items_by_nametoken-workspace_id-item_name---listdict)
  - [get_item_definition_by_id](#get_item_definition_by_idtoken-workspace_id-item_id-output_dirnone-formatnone---dict)
  - [import_item](#import_itemtoken-workspace_id-path-item_propertiesnone-skip_if_existsfalse-retain_rolesfalse-retain_all_partitionsfalse-retain_partitions_tablesnone---dict)
  - [delete_item_by_id](#delete_item_by_idtoken-workspace_id-item_id---none)
- [Internal API Functions](#internal-api-functions)
  - [invoke_fabric_api_request](#invoke_fabric_api_requesturi-tokennone-methodget-bodynone-content_typeapplicationjson-charsetutf-8-timeout_sec240-retry_count0-api_urlnone---dict--list--none)
- [Complete Example](#complete-example)
- [License](#license)
- [Author](#author)

## Installation

```bash
pip install msfabric-devops
```

## Requirements

- Python >= 3.9
- Azure AD service principal credentials (tenant ID, client ID, client secret)
- `azure-identity` package

## Authentication

### `get_access_token(tenant_id=None, client_id=None, client_secret=None) -> str`

Authenticates using a service principal and returns an access token for the Fabric REST API.

**Parameters:**
- `tenant_id` (str): Azure AD Tenant ID.
- `client_id` (str): Azure AD Application (client) ID.
- `client_secret` (str): Azure AD Client Secret.

**Returns:**
- `str`: A valid access token string for authenticating Fabric API requests.

**Example:**
```python
from msfabric_devops import get_access_token

token = get_access_token(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
```

## Workspaces

### `get_workspaces(token) -> list[dict]`

Retrieves all Fabric workspaces accessible to the authenticated user.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.

**Returns:**
- `list[dict]`: List of workspace dictionaries containing workspace details (id, displayName, type, etc.).

**Example:**
```python
from msfabric_devops import get_access_token, get_workspaces

token = get_access_token()
workspaces = get_workspaces(token)
for workspace in workspaces:
    print(workspace["displayName"])
```

### `get_workspace_by_id(token, workspace_id) -> dict`

Retrieves a specific workspace by its ID.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.

**Returns:**
- `dict`: Workspace dictionary containing workspace details. Returns empty dict if not found.

**Example:**
```python
from msfabric_devops import get_access_token, get_workspace_by_id

token = get_access_token()
workspace = get_workspace_by_id(token, "workspace-id-here")
print(workspace["displayName"])
```

### `get_workspaces_by_name(token, workspace_name) -> list[dict]`

Retrieves all workspaces matching a specific display name.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_name` (str): The display name to search for (exact match).

**Returns:**
- `list[dict]`: List of workspace dictionaries matching the name.

**Example:**
```python
from msfabric_devops import get_access_token, get_workspaces_by_name

token = get_access_token()
workspaces = get_workspaces_by_name(token, "My Workspace")
```

### `create_workspace(token, workspace_name) -> dict`

Creates a new Fabric workspace with the specified name.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_name` (str): Display name for the new workspace.

**Returns:**
- `dict`: Created workspace dictionary containing workspace details. Returns None if workspace already exists (with a warning message).

**Example:**
```python
from msfabric_devops import get_access_token, create_workspace

token = get_access_token()
workspace = create_workspace(token, "New Workspace")
```

### `delete_workspace(token, workspace_id) -> None`

Deletes a Fabric workspace by its ID.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace to delete.

**Returns:**
- `None`: No return value on success. Raises exception on error.

**Example:**
```python
from msfabric_devops import get_access_token, delete_workspace

token = get_access_token()
delete_workspace(token, "workspace-id-here")
```

## Items

### `get_items(token, workspace_id) -> list[dict]`

Retrieves all items in a specified Fabric workspace.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.

**Returns:**
- `list[dict]`: List of item dictionaries containing item details (id, displayName, type, etc.).

**Example:**
```python
from msfabric_devops import get_access_token, get_items

token = get_access_token()
items = get_items(token, "workspace-id-here")
for item in items:
    print(f"{item['displayName']} ({item['type']})")
```

### `get_item_by_id(token, workspace_id, item_id) -> dict`

Retrieves a specific item by its ID within a workspace.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.
- `item_id` (str): The unique identifier of the item.

**Returns:**
- `dict`: Item dictionary containing item details.

**Example:**
```python
from msfabric_devops import get_access_token, get_item_by_id

token = get_access_token()
item = get_item_by_id(token, "workspace-id", "item-id")
print(item["displayName"])
```

### `get_items_by_name(token, workspace_id, item_name) -> list[dict]`

Retrieves all items matching a specific display name within a workspace.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.
- `item_name` (str): The display name to search for (exact match).

**Returns:**
- `list[dict]`: List of item dictionaries matching the name.

**Example:**
```python
from msfabric_devops import get_access_token, get_items_by_name

token = get_access_token()
items = get_items_by_name(token, "workspace-id", "My Item")
```

### `get_item_definition_by_id(token, workspace_id, item_id, output_dir=None, format=None) -> dict`

Exports an item definition from a Fabric workspace. Optionally saves the definition files to a local directory.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.
- `item_id` (str): The unique identifier of the item.
- `output_dir` (str, optional): Local directory path where definition files should be saved. If provided, files are decoded from Base64 and written to disk. Defaults to None (no files saved).
- `format` (str, optional): Export format (e.g., 'PBIP'). Defaults to None.

**Returns:**
- `dict`: Response dictionary containing the definition with parts array. Each part includes path, payload (Base64 encoded), and payloadType.

**Example:**
```python
from msfabric_devops import get_access_token, get_item_definition_by_id

token = get_access_token()
definition = get_item_definition_by_id(
    token,
    "workspace-id",
    "item-id",
    output_dir="./output"
)
```

### `import_item(token, workspace_id, path, item_properties=None, skip_if_exists=False, retain_roles=False, retain_all_partitions=False, retain_partitions_tables=None) -> dict`

Imports a Fabric item (semantic model or report) from a local PBIP folder into a Fabric workspace. Supports both `.pbism` (semantic models) and `.pbir` (reports) files.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the target workspace.
- `path` (str): Local folder path containing the PBIP export. Must contain either a `.pbism` or `.pbir` file.
- `item_properties` (dict, optional): Dictionary to override item properties:
  - `displayName` (str): Override the display name
  - `semanticModelId` (str): **Required** when importing reports that use byPath connections to semantic models
  - `type` (str): Override the item type (usually auto-detected)
- `skip_if_exists` (bool, optional): If True, does not update the definition if an item with the same name and type already exists. Defaults to False.
- `retain_roles` (bool, optional): If True, preserves existing RLS (Row-Level Security) roles from the published model when updating. This option:
  - Fetches the current model definition
  - Extracts role definitions from `definition/roles/*.tmdl` files
  - Merges them with the new definition
  - Updates `definition/model.tmdl` to include role references
  Defaults to False.
- `retain_all_partitions` (bool, optional): If True, preserves partition definitions for all tables in the published model when updating. The function will copy partition blocks from the currently published `definition/tables/*.tmdl` parts into the matching table parts in the new definition. Defaults to False.
- `retain_partitions_tables` (list[str] | None, optional): List of table names for which to preserve partitions. When provided, only partitions for tables whose names are in this list will be retained. If `retain_all_partitions` is True this parameter is ignored. Defaults to None.

**Returns:**
- `dict`: Dictionary containing the imported/updated item details with keys: `id`, `displayName`, `type`.

**Behavior:**
- **Item Detection**: Automatically detects item type based on `.pbism` (SemanticModel) or `.pbir` (Report) files
- **File Processing**: Processes all files in the folder except:
  - Files starting with `item.`
  - Files with `.abf` extension
  - Files in `.pbi` directory
- **Report Connections**: For reports using byPath connections, you must provide `item_properties.semanticModelId` to convert to byConnection format
- **Preserve Partitions**: When `retain_all_partitions=True` the importer will read the published model definition and copy partition blocks found in `definition/tables/*.tmdl` into the corresponding table parts of the new definition. Alternatively, pass `retain_partitions_tables=["Table A","Table B"]` to keep partitions only for specific tables.
- **Create vs Update**: Creates a new item if none exists with the same name and type, otherwise updates the existing item

**Examples:**
```python
from msfabric_devops import get_access_token, import_item

token = get_access_token()

# Import a semantic model and preserve all partitions and roles from the published model
result = import_item(
    token,
    "workspace-id",
    r"C:\path\to\semantic-model-pbip",
    item_properties={"displayName": "My Semantic Model"},
    retain_roles=True,
    retain_all_partitions=True
)

# Import a semantic model and preserve partitions only for specific tables
result = import_item(
    token,
    "workspace-id",
    r"C:\path\to\semantic-model-pbip",
    item_properties={"displayName": "My Semantic Model"},
    retain_partitions_tables=["Sales","Items"]
)

# Import a report connected to a semantic model (requires semanticModelId for byPath reports)
result = import_item(
    token,
    "workspace-id",
    r"C:\path\to\report-pbip",
    item_properties={
        "displayName": "My Report",
        "semanticModelId": "existing-semantic-model-id"
    }
)
```

### `delete_item_by_id(token, workspace_id, item_id) -> None`

Deletes a Fabric item by its ID.

**Parameters:**
- `token` (str): Access token from `get_access_token()`.
- `workspace_id` (str): The unique identifier of the workspace.
- `item_id` (str): The unique identifier of the item to delete.

**Returns:**
- `None`: No return value on success. Raises exception on error.

**Example:**
```python
from msfabric_devops.authenticate import get_access_token
from msfabric_devops import delete_item_by_id

token = get_access_token()
delete_item_by_id(token, "workspace-id", "item-id")
```

## Internal API Functions

### `invoke_fabric_api_request(uri, token=None, method="GET", body=None, content_type="application/json; charset=utf-8", timeout_sec=240, retry_count=0, api_url=None) -> dict | list | None`

Low-level function to make requests to the Fabric REST API. Handles authentication, error handling, throttling, and long-running operations.

**Parameters:**
- `uri` (str): API endpoint URI (relative to base API URL).
- `token` (str, optional): Bearer token for authentication.
- `method` (str, optional): HTTP method ("GET", "POST", "DELETE", etc.). Defaults to "GET".
- `body` (dict | list | str, optional): Request body. If dict/list, sent as JSON; if str, sent as raw data.
- `content_type` (str, optional): Content-Type header. Defaults to "application/json; charset=utf-8".
- `timeout_sec` (int, optional): Request timeout in seconds. Defaults to 240.
- `retry_count` (int, optional): Internal retry counter for throttling. Defaults to 0.
- `api_url` (str, optional): Base API URL. Defaults to "https://api.fabric.microsoft.com/v1".

**Returns:**
- `dict | list | None`: Parsed JSON response. Returns None for successful LRO operations with no result.

**Features:**
- **Long-Running Operations (LRO)**: Automatically polls Location header for 202 responses
- **Throttling**: Retries up to 3 times on 429 (Too Many Requests) with exponential backoff
- **Error Handling**: Raises exceptions for API errors and network issues
- **JSON Parsing**: Automatically extracts `value` field from responses if present

## Complete Example

```python
from msfabric_devops import (
    get_access_token,
    get_workspaces,
    create_workspace,
    get_items,
    import_item
)

# Authenticate
token = get_access_token()

# List all workspaces
workspaces = get_workspaces(token)
print(f"Found {len(workspaces)} workspaces")

# Create a new workspace
workspace = create_workspace(token, "My New Workspace")
workspace_id = workspace["id"]

# List items in the workspace
items = get_items(token, workspace_id)
print(f"Found {len(items)} items")

# Import a semantic model
result = import_item(
    token,
    workspace_id,
    r"C:\path\to\pbip\export",
    item_properties={"displayName": "Published Model"},
    retain_roles=True
)
print(f"Imported: {result['displayName']} (ID: {result['id']})")
```

## License

MIT

## Author

Hugo Salaun (hcrsalaun@gmail.com)
