from . import config
from . import authenticate
from . import api

def get_workspaces(token) -> list[dict]:
    return api.invoke_fabric_api_request("workspaces",token)

def get_workspace_by_id(token, workspace_id) -> dict:
    workspaces = get_workspaces(token)
    result = {}
    for workspace in workspaces:
        if workspace["id"] == workspace_id:
            result = workspace
    return result

def get_workspaces_by_name(token, workspace_name) -> list[dict]:
    workspaces = get_workspaces(token)
    result = []
    for workspace in workspaces:
        if workspace["displayName"] == workspace_name:
            result.append(workspace)
    return result

def create_workspace(token, workspace_name):
    test_existing_workspace = get_workspaces_by_name(token, workspace_name)
    if(len(test_existing_workspace) > 0):
        config.print_color(f"Warning : Workspace {workspace_name} already exists.", "yellow")
    else:
        return api.invoke_fabric_api_request("workspaces",token, method="POST", body={"displayName": workspace_name})

def delete_workspace(token, workspace_id):
    return api.invoke_fabric_api_request(f"workspaces/{workspace_id}",token, method="DELETE")

def main():
    token = authenticate.get_access_token(tenant_id=config.TENANT_ID, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    workspaces = get_workspaces(token)
    for workspace in workspaces:
        config.print_color(workspace, "green")

    workspace_by_id = get_workspace_by_id(token=token, workspace_id=config.WORKSPACE_ID)
    config.print_color(workspace_by_id, "green")

    create_wks = create_workspace(token = token, workspace_name="test_python")
    if create_wks != None:
        config.print_color("Workspace created", "green")

    workspaces_by_name = get_workspaces_by_name(token=token, workspace_name = 'test_python')
    for workspace_to_delete in workspaces_by_name:
        delete_workspace(token = token, workspace_id=workspace_to_delete["id"])
        config.print_color("Workspace deleted", "green")

if __name__ == "__main__":
    main()
