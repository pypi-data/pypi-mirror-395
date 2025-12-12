# Azure MCP Agent (Custom)

This repository contains a custom MCP server (`server.py`) exposing tools to:
1. List active Azure role assignments for the signed-in user.
2. List Azure resources (subscription-wide or specific resource group).
3. Deploy resources via Bicep-backed PowerShell scripts (storage account, key vault, Azure OpenAI, AI Search, AI Foundry).

## Prerequisites
- Windows + PowerShell (`pwsh`) recommended.
- Python 3.10+ installed.
- Azure CLI installed: https://learn.microsoft.com/cli/azure/install-azure-cli
- Logged in to Azure: `az login --use-device-code` (or normal `az login`).
- Appropriate RBAC permissions to list and deploy resources.

## Python Setup
```powershell
cd "c:\Users\v-siddjha\OneDrive - MAQ Software\Desktop\agent"
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run MCP Server Directly
```powershell
python server.py
```
This starts the MCP process that tools (e.g., GitHub Copilot Agent) can attach to.

## Configure GitHub Copilot to Use This MCP Server
In VS Code settings (JSON view), add an MCP server entry. Example:
```json
"github.copilot.mcpServers": {
  "azure-agent": {
    "command": "python",
    "args": [
      "c:/Users/v-siddjha/OneDrive - MAQ Software/Desktop/agent/server.py"
    ],
    "env": {
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```
Restart VS Code or Copilot Agent session. Copilot should list available tools (`azure_login`, `list_permissions`, `list_resources`, `get_resource_parameters`, `deploy_resource`).

## Tool Usage (Within Copilot Chat)
- List permissions:
  - Prompt: `Call tool list_permissions` (optionally pass `user_principal_name` or `out_file`).
- List resources (all):
  - Prompt: `Call tool list_resources`.
- List resources for RG:
  - Prompt: `Call tool list_resources {"resource_group_name":"my-rg"}`.
- Discover required params for deployment:
  - Prompt: `Call tool get_resource_parameters {"resource_type":"storage-account"}`.
- Deploy a resource (must supply required params):
  - Prompt: `Call tool deploy_resource {"resource_type":"storage-account","parameters":{"ResourceGroupName":"my-rg","StorageAccountName":"mystorage123","Location":"eastus","AccessTier":"Hot"}}`.

## Local Test Harness (Without Copilot)
Run the included script:
```powershell
python test_agent.py
```
Uncomment the deployment section and fill real parameter values before testing resource creation.

## Adding New Deployment Scripts
1. Place new `deploy-*.ps1` in `scripts/`.
2. Add a Bicep template in `templates/`.
3. Extend `DEPLOYMENT_SCRIPTS` in `server.py` with logical key -> script filename.
4. Use `get_resource_parameters` to see inferred required params.

## Notes on Parameter Validation
`deploy_resource` infers required parameters by detecting `if (-not $Param)` prompts in the script. Ensure each truly required input has that pattern for stricter enforcement.

## Common Issues
- `Azure CLI not found`: Install CLI and restart shell.
- `Not logged in`: Run `az login`.
- Missing permissions: Confirm role assignments (e.g., Reader, Contributor) with `list_permissions` tool output.
- Deployment failures: Check Bicep template, naming constraints, region availability.

## Security Considerations
- Do not hardcode secrets; use Key Vault deployment then store secrets securely.
- Validate user-supplied parameters before passing to scripts if exposing externally.

## Cleanup
To remove test resources, use Azure Portal or `az group delete -n <RGName> --no-wait --yes`.

---
Happy building! Use the Copilot Agent chat to invoke tools interactively.
