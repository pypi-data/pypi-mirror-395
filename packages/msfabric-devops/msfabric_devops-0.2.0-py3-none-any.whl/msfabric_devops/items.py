import base64
import json
import os
import re
from pathlib import Path
from . import api
from . import config
from . import authenticate


def get_partitions(tmdl_content: str):
    """
    Extract all partition blocks from a TMDL file.
    Returns a list of strings, each containing one partition block.
    """
    # Match 'partition <name> = <mode>' until the next unindented line or end of file
    pattern = re.compile(
        r"^\tpartition[\s\S]*?=(?:[\s\S]*?)(?=\n\n)",
        re.MULTILINE | re.DOTALL
    )
    partitions = pattern.findall(tmdl_content)
    return partitions

def set_partitions(tmdl_content: str, new_partitions: list[str], delimiter: str = "\r\n") -> str:
    """
    Remove all existing partition blocks in TMDL content and insert new partitions once
    at the location of the first partition block (or append at the end if none found).
    """
    # Regex to match all partition blocks
    pattern = r"(\tpartition[\s\S]*?=\s*```[\s\S]*?```(?:\n\t.*)*)"

    matches = list(re.finditer(pattern, tmdl_content, flags=re.MULTILINE))

    if matches:
        # Use the start of the first match and the end of the last match
        start = matches[0].start()
        end = matches[-1].end()

        # Replace all partition blocks with new partitions exactly once
        replaced_content = tmdl_content[:start] + delimiter.join(new_partitions) + tmdl_content[end:]
    else:
        # Do nothing
        replaced_content = tmdl_content

    return replaced_content

def get_items(
    token: str,
    workspace_id: str
):
    result = api.invoke_fabric_api_request(token=token, uri=f"workspaces/{workspace_id}/items")
    return result

def get_item_by_id(
    token: str,
    workspace_id: str,
    item_id: str
):
    result = api.invoke_fabric_api_request(token=token, uri=f"workspaces/{workspace_id}/items/{item_id}")
    return result

def get_items_by_name(token: str, workspace_id: str, item_name: str):
    items = get_items(token, workspace_id)
    result = []
    for item in items:
        if item['displayName'] == item_name:
            result.append(item)
    return result

def get_item_definition_by_id(token: str, workspace_id: str, item_id: str, output_dir: str = None, format: str | None = None):
    """
    Exports a Fabric item from a Fabric workspace, optionnaly to a specified local path.

    Args:
        workspace_id (str): The Fabric workspace ID.
        item_id (str): The Fabric item ID (e.g. semantic model).
        path (str, optional): Output directory. Defaults to './pbipOutput'.
        format (str, optional): Optional export format (e.g., 'PBIP').

    Returns:
        dict: Response from the Fabric API request.
    """

    uri = f"workspaces/{workspace_id}/items/{item_id}/getDefinition"

    if format:
        uri += f"?format={format}"

    # POST request to the Fabric API
    response = api.invoke_fabric_api_request(uri=uri, token=token,  method="POST")
    if output_dir:
        parts = response.get("definition", {}).get("parts", [])
        for part in parts:
            path = part["path"]
            payload = part["payload"]
            payload_type = part.get("payloadType")

            # Compute full file path
            if(output_dir):
                full_path = os.path.join(output_dir, path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                # Decode Base64 payload (only for InlineBase64 types)
                if payload_type == "InlineBase64":
                    content = base64.b64decode(payload)
                    with open(full_path, "wb") as f:
                        f.write(content)
                    print(f"✅ Saved: {full_path}")
                else:
                    print(f"⚠️ Skipped {path} (unsupported payloadType: {payload_type})")
    return response

def import_item(
    token: str,
    workspace_id: str,
    path: str,
    item_properties: dict | None = None,
    skip_if_exists: bool = False,
    retain_roles:bool = False,
    retain_all_partitions:bool = False,
    retain_partitions_tables: list[str] = []
):
    """
    Imports .pbir or .pbism items from PBIP folder into a Fabric workspace.

    :param path: Folder containing PBIP output.
    :param workspace_id: Fabric workspace ID.
    :param item_properties: Optional override for displayName, type, semanticModelId, ...
    :param skip_if_exists: Do not update definition if item already exists.
    """

    path = Path(path).resolve()

    # ----------------------------------------------------------------------
    # 1. Detect item definition files (.pbir or .pbism)
    # ----------------------------------------------------------------------

    items_in_folder = [
        p for p in path.iterdir()
        if p.suffix.lower() in [".pbir", ".pbism"]
    ]

    if not items_in_folder:
        raise Exception(f"No .pbir or .pbism files found in: {path}")

    # Determine item type
    if any(p.suffix.lower() == ".pbir" for p in items_in_folder):
        item_type = "Report"
    elif any(p.suffix.lower() == ".pbism" for p in items_in_folder):
        item_type = "SemanticModel"
    else:
        raise Exception("Cannot determine item type.")

    # ----------------------------------------------------------------------
    # 2. Read workspace existing items
    # ----------------------------------------------------------------------

    items = api.invoke_fabric_api_request(
        token=token,
        uri=f"workspaces/{workspace_id}/items",
        method="GET"
    )

    # ----------------------------------------------------------------------
    # 3. Enumerate files to upload
    # ----------------------------------------------------------------------

    all_files = [
        f for f in path.rglob("*")
        if f.is_file()
        and not f.name.startswith("item.")
        and not f.suffix.lower() == ".abf"
        and f.parent.name != ".pbi"
    ]

    # ----------------------------------------------------------------------
    # 4. Determine displayName and type
    # ----------------------------------------------------------------------

    display_name = None

    if item_properties:
        display_name = item_properties.get("displayName")

    platform_file = path / ".platform"
    if platform_file.exists() and (not display_name or not item_type):
        with open(platform_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        item_type = metadata["metadata"].get("type", item_type)
        display_name = metadata["metadata"].get("displayName", display_name)

    if not item_type or not display_name:
        raise Exception("Missing required fields: itemType or displayName")

    # ----------------------------------------------------------------------
    # 5. Build the Parts payload
    # ----------------------------------------------------------------------

    parts = []
    item_id = item_properties.get("semanticModelId") if item_properties else None

    for file in all_files:
        relative_path = file.relative_to(path).as_posix()

        if file.suffix.lower() == ".pbir":
            text = file.read_text(encoding="utf-8")
            pbir_json = json.loads(text)

            # Resolve semantic model connection
            if item_id or (
                pbir_json.get("datasetReference")
                and pbir_json["datasetReference"].get("byPath", {}).get("path")
            ):
                if not item_id:
                    raise Exception(
                        "Report uses byPath connection. You MUST pass itemProperties.semanticModelId"
                    )

                # Remove byPath
                if "byPath" in pbir_json["datasetReference"]:
                    pbir_json["datasetReference"]["byPath"] = None

                # Ensure $schema exists
                if "$schema" not in pbir_json:
                    pbir_json["$schema"] = (
                        "https://developer.microsoft.com/json-schemas/"
                        "fabric/item/report/definitionProperties/2.0.0/schema.json"
                    )

                schema = pbir_json["$schema"]

                # Old vs new schema connection
                if "1.0.0" in schema:
                    by_connection = {
                        "connectionString": None,
                        "pbiServiceModelId": None,
                        "pbiModelVirtualServerName": "sobe_wowvirtualserver",
                        "pbiModelDatabaseName": item_id,
                        "name": "EntityDataSource",
                        "connectionType": "pbiServiceXmlaStyleLive",
                    }
                else:
                    by_connection = {
                        "connectionString": f"semanticmodelid={item_id}"
                    }

                pbir_json["datasetReference"]["byConnection"] = by_connection
                file_bytes = json.dumps(pbir_json, indent=2).encode("utf-8")
            else:
                file_bytes = text.encode("utf-8")
        else:
            file_bytes = file.read_bytes()

        parts.append({
            "Path": relative_path,
            "Payload": base64.b64encode(file_bytes).decode("utf-8"),
            "PayloadType": "InlineBase64",
        })


    # ----------------------------------------------------------------------
    # 6. Check if item exists
    # ----------------------------------------------------------------------

    existing = [
        x for x in items
        if x["type"].lower() == item_type.lower()
        and x["displayName"].lower() == display_name.lower()
    ]

    item_id = existing[0]["id"] if existing else None
    published_item_definition = get_item_definition_by_id(token, workspace_id, item_id) if existing else None

    # ----------------------------------------------------------------------
    # 7. Keep existing partitions and update part payloads
    # ----------------------------------------------------------------------

    if (retain_all_partitions or retain_partitions_tables) and existing:
        partition_definitions = []

        for file in published_item_definition.get("definition", {}).get("parts", []):
            if re.match(r"definition/tables/.*\.tmdl", file['path']):
                content = base64.b64decode(file['payload']).decode('utf-8')
                file_bytes = content.encode("utf-8")
                target_partitions = get_partitions(content)
                for part in parts:
                    if part["Path"] == file["path"]:
                        original_content = base64.b64decode(part['Payload']).decode('utf-8')
                        table_name = re.findall(r'table (.*)', original_content)[0]
                        if retain_all_partitions or table_name in retain_partitions_tables:
                            modified_content = set_partitions(original_content, target_partitions)
                            part["Payload"] = base64.b64encode(modified_content.encode("utf-8")).decode("utf-8")

    # ----------------------------------------------------------------------
    # 8. Keep existing roles and update part payloads
    # ----------------------------------------------------------------------

    if retain_roles and existing:
        role_definitions = []
        role_names: list[str] = []

        # remove roles from original path
        parts[:] = [
            part for part in parts
            if not part["Path"].startswith('definition/roles/')
        ]

        for file in published_item_definition.get("definition", {}).get("parts", []):
            if re.match(r"definition/roles/.*\.tmdl", file['path']):
                role_definitions.append(file)
                content = base64.b64decode(file['payload']).decode('utf-8')
                file_bytes = content.encode("utf-8")

                role_name = re.findall(r'role (.*)', content)[0]
                role_names.append(f'ref role {role_name}')
                parts.append({
                    "Path": f"{file['path']}",
                    "Payload": base64.b64encode(file_bytes).decode("utf-8"),
                    "PayloadType": "InlineBase64",
                })

        # edit model.tmdl to keep existing roles
        for file in published_item_definition.get("definition", {}).get("parts", []):
            if file['path'].endswith("definition/model.tmdl"):
                content = base64.b64decode(file['payload']).decode('utf-8')
                parts[:] = [
                    part for part in parts
                    if not part["Path"].endswith('definition/model.tmdl')
                ]

                # Split the content into lines
                lines = content.splitlines()

                # Filter out lines starting with 'ref role'
                filtered_lines = [line for line in lines if not line.strip().startswith('ref role')]

                # Join the lines back into a single string
                modified_content = '\n'.join(filtered_lines)
                modified_content += '\n' + '\n'.join(role_names)

                # Re-encode the modified content to base64
                modified_bytes = modified_content.encode('utf-8')
                parts.append({
                    "Path": f"definition/model.tmdl",
                    "Payload": base64.b64encode(modified_bytes).decode('utf-8'),
                    "PayloadType": "InlineBase64",
                })

    # ----------------------------------------------------------------------
    # 9. Create or update
    # ----------------------------------------------------------------------

    if item_id is None:
        # --- CREATE ---
        payload = {
            "displayName": display_name,
            "type": item_type,
            "definition": {"Parts": parts}
        }

        result = api.invoke_fabric_api_request(
            token = token,
            uri=f"workspaces/{workspace_id}/items",
            method="POST",
            body=json.dumps(payload)
        )

        return {
            "id": result["id"],
            "displayName": display_name,
            "type": item_type
        }

    else:
        # --- UPDATE ---
        if skip_if_exists:
            return {
                "id": item_id,
                "displayName": display_name,
                "type": item_type
            }

        update_payload = {
            "definition": {"Parts": parts}
        }

        api.invoke_fabric_api_request(
            token = token,
            uri=f"workspaces/{workspace_id}/items/{item_id}/updateDefinition",
            method="POST",
            body=json.dumps(update_payload)
        )

        return {
            "id": item_id,
            "displayName": display_name,
            "type": item_type
        }


def delete_item_by_id(
    token: str,
    workspace_id: str,
    item_id: str
):
    result = api.invoke_fabric_api_request(token=token, uri=f"workspaces/{workspace_id}/items/{item_id}", method="DELETE")
    config.print_color(f"Deleted item: {item_id}", "green")
    return result


def main():
    token = authenticate.get_access_token()

    #config.print_color(get_items(                   token=token, workspace_id=config.WORKSPACE_ID)                                      ,"green")
    #config.print_color(get_item_by_id(              token=token, workspace_id=config.WORKSPACE_ID, item_id = config.SEMANTIC_MODEL_ID)  ,"green")
    #config.print_color(get_items_by_name(           token=token, workspace_id=config.WORKSPACE_ID, item_name="test")                    ,"green")
    #config.print_color(get_item_definition_by_id(   token=token, workspace_id=config.WORKSPACE_ID, item_id = "c90bc409-0d20-4c49-a898-c3b0038e0c78").get("definition", {}).get("parts", [])  ,"green")
    print(import_item(         token=token, workspace_id=config.WORKSPACE_ID, path="../output", item_properties={"displayName":"test2"}, retain_roles = False, retain_partitions_tables={"Sales"}))
    #config.print_color(delete_item_by_id( token=token, workspace_id=config.WORKSPACE_ID, item_id = ""))
if __name__ == "__main__":
    main()
