from mcp.server.fastmcp import FastMCP
import subprocess
import os
import re
import shutil
import json
import time
from typing import Dict, Tuple, Optional, Union, Any

# Initialize the server
mcp = FastMCP("azure-agent")

# --- DEPLOYMENT ENFORCEMENT ---
# CRITICAL: All Azure resource deployments MUST go through MCP server tools.
# Direct az deployment commands are FORBIDDEN to ensure compliance orchestration.
ENFORCE_MCP_DEPLOYMENT = True

# --- PATH RESOLUTION HELPERS (CRITICAL FOR PIP PACKAGES) ---

def _get_package_file(*path_parts):
    """
    Calculates the absolute path to a file inside the package.
    Works for both local dev (if structure matches) and installed pip packages.
    """
    # Get the directory containing THIS file (server.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Join with the requested parts (e.g., "scripts", "deploy.ps1")
    full_path = os.path.join(base_dir, *path_parts)
    return full_path

def _get_script_path(script_name: str) -> str:
    """Locates the script in the 'scripts' folder using absolute paths."""
    return _get_package_file("scripts", script_name)

def _get_template_path(template_rel: str) -> str:
    """Locates the bicep file relative to package root."""
    # template_rel is expected to be like "templates/storage.bicep"
    # we split it to pass as separate args to _get_package_file
    parts = template_rel.replace("\\", "/").split("/")
    return _get_package_file(*parts)

# --- INSTRUCTIONS LOADING ---

AGENT_INSTRUCTIONS_FILE = _get_package_file("AGENT_INSTRUCTIONS.md")

@mcp.prompt()
def agent_instructions():
    """Returns the agent persona and menu from the MD file."""
    if os.path.exists(AGENT_INSTRUCTIONS_FILE):
        with open(AGENT_INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Error: AGENT_INSTRUCTIONS.md not found in package."

def load_agent_instructions() -> str:
    """Load the AGENT_INSTRUCTIONS.md file content if present."""
    if os.path.exists(AGENT_INSTRUCTIONS_FILE):
        try:
            with open(AGENT_INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Failed to read instructions: {e}"
    return "Instructions file not found."

# --- CONFIGURATION ---

# Resources that MUST be attached to NSP after creation
NSP_MANDATORY_RESOURCES = [
    "storage-account", # ADLS is usually a storage account with HNS enabled
    "key-vault",
    "cosmos-db",
    "sql-db"
]

# Resources that MUST have diagnostic settings (Log Analytics) attached after creation
LOG_ANALYTICS_MANDATORY_RESOURCES = [
    "logic-app",
    "function-app",
    "app-service",
    "key-vault",
    "synapse",
    "data-factory",
    "ai-hub",
    "ai-project",
    "ai-foundry",
    "ai-services",
    "ai-search",
    "front-door",
    "virtual-machine",
    "redis-cache",
    "redis-enterprise"
]

# 1. PowerShell Scripts for Deployment
# Maps resource_type -> script filename in 'scripts/' folder
DEPLOYMENT_SCRIPTS = {
    "storage-account": "deploy-storage-account.ps1",
    "key-vault": "deploy-keyvault.ps1",
    "openai": "deploy-openai.ps1",
    "ai-search": "deploy-ai-search.ps1",
    "ai-foundry": "deploy-ai-foundry.ps1",
    "log-analytics": "deploy-log-analytics.ps1",
    # Add cosmos/sql here if you create scripts for them:
    # "cosmos-db": "deploy-cosmos-db.ps1",
    # "sql-db": "deploy-sql-db.ps1",
}

# 2. Bicep Templates (Modern/Template approach)
TEMPLATE_MAP = {
    "storage-account": "templates/storage-account.bicep",
    "key-vault": "templates/azure-key-vaults.bicep",
    "openai": "templates/azure-openai.bicep",
    "ai-search": "templates/ai-search.bicep",
    "ai-foundry": "templates/ai-foundry.bicep",
    "cosmos-db": "templates/cosmos-db.bicep",
    "sql-db": "templates/sql-db.bicep",
    "log-analytics": "templates/log-analytics.bicep"
}

# 3. Operational Scripts (Permissions/Listings)
OP_SCRIPTS = {
    "permissions": "list-permissions.ps1",
    "resources": "list-resources.ps1",
    "create-rg": "create-resourcegroup.ps1"
}

# --- HELPERS ---

def run_command(command: list[str]) -> str:
    """Generic command runner."""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running command {' '.join(command)}: {e.stderr}"

def _run_powershell_script(script_path: str, parameters: dict) -> str:
    """Executes a PowerShell script with named parameters."""
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    
    # Use -ExecutionPolicy Bypass to avoid permission issues
    cmd = [ps_executable, "-ExecutionPolicy", "Bypass", "-File", script_path]
    
    for k, v in parameters.items():
        if v is not None and v != "":
            cmd.append(f"-{k}")
            cmd.append(str(v))
            
    return run_command(cmd)

# --- NSP ORCHESTRATION HELPERS ---

def _get_rg_location(resource_group: str) -> str:
    """Fetches location of the resource group."""
    try:
        res = run_command(["az", "group", "show", "-n", resource_group, "--query", "location", "-o", "tsv"])
        return res.strip()
    except:
        return "eastus" # Fallback

def _get_resource_id(resource_group: str, resource_type: str, parameters: Dict[str, str]) -> Optional[str]:
    """
    Attempts to find the Resource ID based on parameters provided during creation.
    We look for common naming parameter keys.
    """
    # Common parameter names for resource names in Bicep templates
    name_keys = [
        "name", "accountName", "keyVaultName", "serverName", "databaseName", "storageAccountName",
        "workspaceName", "searchServiceName", "serviceName", "vmName", "virtualMachineName",
        "siteName", "functionAppName", "appServiceName", "logicAppName", "workflowName",
        "factoryName", "cacheName", "frontDoorName", "clusterName"
    ]
    
    resource_name = None
    for key in name_keys:
        if key in parameters:
            resource_name = parameters[key]
            break
            
    # If we couldn't find a specific name, we might check the deployment output, 
    # but for now, we fail gracefully if we can't identify the resource name.
    if not resource_name:
        return None

    # Map internal types to Azure Resource Provider types for CLI lookup
    provider_map = {
        "storage-account": "Microsoft.Storage/storageAccounts",
        "key-vault": "Microsoft.KeyVault/vaults",
        "cosmos-db": "Microsoft.DocumentDB/databaseAccounts",
        "sql-db": "Microsoft.Sql/servers",
        "logic-app": "Microsoft.Logic/workflows",
        "function-app": "Microsoft.Web/sites",
        "app-service": "Microsoft.Web/sites",
        "synapse": "Microsoft.Synapse/workspaces",
        "data-factory": "Microsoft.DataFactory/factories",
        "ai-hub": "Microsoft.MachineLearningServices/workspaces",
        "ai-project": "Microsoft.MachineLearningServices/workspaces",
        "ai-foundry": "Microsoft.CognitiveServices/accounts",
        "ai-services": "Microsoft.CognitiveServices/accounts",
        "ai-search": "Microsoft.Search/searchServices",
        "front-door": "Microsoft.Network/frontDoors",
        "virtual-machine": "Microsoft.Compute/virtualMachines",
        "redis-cache": "Microsoft.Cache/redis",
        "redis-enterprise": "Microsoft.Cache/redisEnterprise"
    }
    
    provider = provider_map.get(resource_type)
    if not provider:
        return None

    try:
        cmd = [
            "az", "resource", "show", 
            "-g", resource_group, 
            "-n", resource_name, 
            "--resource-type", provider, 
            "--query", "id", "-o", "tsv"
        ]
        return run_command(cmd).strip()
    except:
        return None

def _orchestrate_nsp_attachment(resource_group: str, resource_type: str, parameters: Dict[str, str]) -> str:
    """
    Checks requirements and performs NSP creation/attachment using check-nsp.ps1.
    """
    if resource_type not in NSP_MANDATORY_RESOURCES:
        return "" # No action needed

    log = ["\n[NSP Orchestration Triggered]"]
    
    # 1. Run check-nsp.ps1 to ensure NSP exists (creates if needed)
    check_nsp_script = _get_script_path("check-nsp.ps1")
    if not os.path.exists(check_nsp_script):
        log.append("[WARNING] check-nsp.ps1 not found. Skipping NSP orchestration.")
        return "\n".join(log)
    
    log.append(f"Checking/Creating NSP in '{resource_group}'...")
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    nsp_check_result = run_command([
        ps_executable, "-File", check_nsp_script,
        "-ResourceGroupName", resource_group
    ])
    log.append(nsp_check_result)
    nsp_name = f"{resource_group}-nsp"

    # 2. Get Resource ID
    resource_id = _get_resource_id(resource_group, resource_type, parameters)
    if not resource_id:
        return "\n".join(log) + "\n[WARNING] Could not determine Resource ID. Skipping NSP attachment. Please attach manually."

    # 3. Attach Resource using attach-nsp.ps1
    attach_nsp_script = _get_script_path("attach-nsp.ps1")
    if not os.path.exists(attach_nsp_script):
        log.append("[WARNING] attach-nsp.ps1 not found. Please attach resource manually.")
        return "\n".join(log)
    
    log.append(f"Attaching resource to NSP '{nsp_name}'...")
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    attach_result = run_command([
        ps_executable, "-File", attach_nsp_script,
        "-ResourceGroupName", resource_group,
        "-NSPName", nsp_name,
        "-ResourceId", resource_id
    ])
    
    if "Error" in attach_result or "FAILED" in attach_result:
        log.append(f"FAILED to attach resource: {attach_result}")
    else:
        log.append("Resource successfully attached to NSP.")
        log.append(attach_result)

    return "\n".join(log)

def _orchestrate_log_analytics_attachment(resource_group: str, resource_type: str, parameters: Dict[str, str]) -> str:
    """
    Checks requirements and performs Log Analytics Workspace creation/diagnostic settings attachment.
    If multiple workspaces exist, requires user to specify which one to use.
    """
    if resource_type not in LOG_ANALYTICS_MANDATORY_RESOURCES:
        return "" # No action needed

    log = ["\n[Log Analytics Orchestration Triggered]"]
    
    # 1. Run check-log-analytics.ps1 to ensure Log Analytics Workspace exists (creates if needed)
    check_law_script = _get_script_path("check-log-analytics.ps1")
    if not os.path.exists(check_law_script):
        log.append("[WARNING] check-log-analytics.ps1 not found. Skipping Log Analytics orchestration.")
        return "\n".join(log)
    
    log.append(f"Checking/Creating Log Analytics Workspace in '{resource_group}'...")
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    law_check_result = run_command([
        ps_executable, "-File", check_law_script,
        "-ResourceGroupName", resource_group
    ])
    log.append(law_check_result)
    
    # Check if multiple workspaces exist and require user selection
    if "MULTIPLE LOG ANALYTICS WORKSPACES FOUND" in law_check_result or "RequiresSelection" in law_check_result:
        log.append("\n[ACTION REQUIRED]")
        log.append("Multiple Log Analytics Workspaces detected in this resource group.")
        log.append("Please specify which workspace to use for diagnostic settings by providing the workspace name or ID.")
        log.append("Diagnostic settings attachment SKIPPED - awaiting user selection.")
        return "\n".join(log)
    
    # Extract workspace ID from output or construct it
    workspace_name = f"{resource_group}-law"
    workspace_id = f"/subscriptions/{_get_subscription_id()}/resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}"

    # 2. Get Resource ID
    resource_id = _get_resource_id(resource_group, resource_type, parameters)
    if not resource_id:
        return "\n".join(log) + "\n[WARNING] Could not determine Resource ID. Skipping diagnostic settings attachment. Please attach manually."

    # 3. Attach Diagnostic Settings using attach-log-analytics.ps1
    attach_law_script = _get_script_path("attach-log-analytics.ps1")
    if not os.path.exists(attach_law_script):
        log.append("[WARNING] attach-log-analytics.ps1 not found. Please attach diagnostic settings manually.")
        return "\n".join(log)
    
    log.append(f"Attaching diagnostic settings to resource...")
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    attach_result = run_command([
        ps_executable, "-File", attach_law_script,
        "-ResourceGroupName", resource_group,
        "-WorkspaceId", workspace_id,
        "-ResourceId", resource_id
    ])
    
    if "Error" in attach_result or "FAILED" in attach_result:
        log.append(f"FAILED to attach diagnostic settings: {attach_result}")
    else:
        log.append("Diagnostic settings successfully attached.")
        log.append(attach_result)

    return "\n".join(log)

def _get_subscription_id() -> str:
    """Fetches the current subscription ID."""
    try:
        res = run_command(["az", "account", "show", "--query", "id", "-o", "tsv"])
        return res.strip()
    except:
        return ""

# --- PARSERS ---

def _get_script_parameters(script_path: str) -> dict:
    """Parses a PowerShell script Param() block."""
    required = []
    optional = []
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        param_block_match = re.search(r'Param\s*\((.*?)\)', content, re.IGNORECASE | re.DOTALL)
        if param_block_match:
            lines = param_block_match.group(1).split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue
                var_match = re.search(r'\$([a-zA-Z0-9_]+)', line)
                if var_match:
                    param_name = var_match.group(1)
                    if '=' in line: optional.append(param_name)
                    else: required.append(param_name)
    except Exception as e:
        return {"error": str(e)}
    return {"required": sorted(list(set(required))), "optional": sorted(list(set(optional)))}

def _parse_bicep_parameters(template_path: str) -> Dict[str, Tuple[bool, Optional[str]]]:
    params: Dict[str, Tuple[bool, Optional[str]]] = {}
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_strip = line.strip()
                if line_strip.startswith('param '):
                    m = re.match(r"param\s+(\w+)\s+[^=\n]+(?:=\s*(.+))?", line_strip)
                    if m:
                        name = m.group(1)
                        default_raw = m.group(2).strip() if m.group(2) else None
                        required = default_raw is None
                        params[name] = (required, default_raw)
    except Exception:
        pass
    return params

def _validate_bicep_parameters(resource_type: str, provided: Dict[str, str]) -> Tuple[bool, str, Dict[str, Tuple[bool, Optional[str]]]]:
    if resource_type not in TEMPLATE_MAP:
        return False, f"Unknown resource_type '{resource_type}'.", {}
    template_path = _get_template_path(TEMPLATE_MAP[resource_type])
    if not os.path.exists(template_path):
        return False, f"Template not found at {template_path}", {}
    params = _parse_bicep_parameters(template_path)
    missing = [p for p, (req, _) in params.items() if req and (p not in provided or provided[p] in (None, ""))]
    if missing:
        return False, f"Missing required parameters: {', '.join(missing)}", params
    return True, "OK", params

def _deploy_bicep(resource_group: str, resource_type: str, parameters: Dict[str,str]) -> str:
    if resource_type not in TEMPLATE_MAP:
        return f"Unknown resource_type '{resource_type}'."
    template_path = _get_template_path(TEMPLATE_MAP[resource_type])
    if not os.path.exists(template_path):
        return f"Template not found: {template_path}"
    
    # Ensure RG exists check
    rg_check = run_command(["az", "group", "show", "-n", resource_group, "-o", "none"])
    if "Error" in rg_check or "not found" in rg_check.lower():
        return f"Resource group '{resource_group}' not found. Please create it first."
    
    cmd = ["az", "deployment", "group", "create", "-g", resource_group, "-f", template_path]
    if parameters:
        cmd.append("--parameters")
        for k, v in parameters.items():
            # Convert Python boolean strings to proper values for Azure CLI
            if isinstance(v, str):
                v_lower = v.lower()
                if v_lower in ('true', 'false'):
                    v = v_lower  # Azure CLI accepts lowercase 'true'/'false'
            cmd.append(f"{k}={v}")
            
    deploy_result = run_command(cmd)
    
    # --- NSP ORCHESTRATION INJECTION ---
    if "Error" not in deploy_result:
        nsp_logs = _orchestrate_nsp_attachment(resource_group, resource_type, parameters)
        law_logs = _orchestrate_log_analytics_attachment(resource_group, resource_type, parameters)
        return f"{deploy_result}\n{nsp_logs}\n{law_logs}"
    
    return deploy_result

# --- INTENT PARSING ---

def parse_intent(text: str) -> str:
    t = normalize(text)
    if is_greeting(t): return "greeting"
    if any(k in t for k in ["menu", "help", "options"]): return "menu"
    if any(k in t for k in ["list permissions", "show permissions", "check permissions"]): return "permissions"
    if "list resources" in t or "show resources" in t or re.search(r"resources in", t): return "resources"
    if any(k in t for k in ["create rg", "create resource group", "new rg", "new resource group"]): return "create-rg"
    if any(k in t for k in ["create", "deploy", "provision"]): return "create"
    return "unknown"

def extract_resource_group(text: str) -> Optional[str]:
    m = re.search(r"resources in ([A-Za-z0-9-_\.]+)", text, re.IGNORECASE)
    return m.group(1) if m else None

def get_action_menu() -> str:
    return (
        "Available actions:\n"
        "1. List all active permissions (Live Fetch)\n"
        "2. List all accessible resources (optional resource group)\n"
        "3. Create resource group (requires: name, region, project name)\n"
        "4. Create SFI compliant resources (REQUIRES USER INPUT FOR ALL PARAMETERS)\n"
        "   Workflow: \n"
        "   a) Call get_bicep_requirements(resource_type) to see what's needed\n"
        "   b) Ask user for ALL required values\n"
        "   c) Deploy with deploy_bicep_resource()\n"
        "   Supported types: storage-account | key-vault | openai | ai-search | ai-foundry | cosmos-db | sql-db | log-analytics\n"
        "   - NSP auto-attached for: storage-account, key-vault, cosmos-db, sql-db\n"
        "   - Diagnostic settings auto-configured for resources requiring monitoring"
    )

def get_azure_sfi_greeting() -> str:
    """Returns a welcoming message when user greets the Azure SFI agent."""
    return (
        "👋 Hello! I'm your Azure SFI (Secure Foundation Infrastructure) Deployment Agent.\n\n"
        "I help you deploy Azure resources with built-in compliance and security best practices:\n\n"
        "✅ **What I Can Do:**\n"
        "  • Deploy SFI-compliant Azure resources (Storage, Key Vault, OpenAI, AI Search, etc.)\n"
        "  • Automatically configure Network Security Perimeters (NSP)\n"
        "  • Set up diagnostic settings with Log Analytics\n"
        "  • List your Azure permissions and resources\n"
        "  • Create resource groups with proper tagging\n\n"
        "🔒 **Security Features:**\n"
        "  • NSP auto-attachment for Storage, Key Vault, Cosmos DB, SQL DB\n"
        "  • Log Analytics integration for monitoring\n"
        "  • Bicep-based infrastructure as code\n"
        "  • Compliance-first deployment approach\n\n"
        "💡 **Quick Start Commands:**\n"
        "  • 'List my Azure permissions' - See your role assignments\n"
        "  • 'Show all resources' - View your Azure resources\n"
        "  • 'Deploy a storage account' - Create SFI-compliant storage\n"
        "  • 'Create a Key Vault' - Deploy secure key vault\n\n"
        "📋 **Current Context:**\n"
        "  • Using your Azure CLI credentials (az login)\n"
        "  • Deploying to your Azure subscription\n"
        "  • All resources created with your permissions\n\n"
        "Ready to help! What would you like to deploy today? 🚀"
    )

GREETING_PATTERN = re.compile(r"\b(hi|hello|hey|greetings|good (morning|afternoon|evening))\b", re.IGNORECASE)
AZURE_SFI_GREETING = re.compile(r"\b(hello|hi|hey)\s+(azure\s+)?sfi\s+agent\b", re.IGNORECASE)

def is_greeting(text: str) -> bool:
    return bool(GREETING_PATTERN.search(text))

def is_azure_sfi_greeting(text: str) -> bool:
    """Check if user is specifically greeting the Azure SFI agent."""
    return bool(AZURE_SFI_GREETING.search(text))

def normalize(text: str) -> str:
    return text.lower().strip()

# --- TOOLS ---

@mcp.tool()
def azure_login() -> str:
    """Initiates Azure login."""
    return run_command(["az", "login", "--use-device-code"])

@mcp.tool()
def list_permissions(user_principal_name: str = None, force_refresh: bool = True) -> str:
    """
    Lists active role assignments. 
    Uses force_refresh=True by default to ensure recent role activations are captured.
    """
    script_name = OP_SCRIPTS["permissions"]
    script_path = _get_script_path(script_name)
    
    if not os.path.exists(script_path):
        return f"Error: Script '{script_name}' not found at {script_path}"

    params = {}
    if user_principal_name:
        params["UserPrincipalName"] = user_principal_name
    
    return _run_powershell_script(script_path, params)

@mcp.tool()
def list_resources(resource_group_name: str = None) -> str:
    """Lists Azure resources (all or by group)."""
    script_name = OP_SCRIPTS["resources"]
    script_path = _get_script_path(script_name)
    if not os.path.exists(script_path): return f"Error: Script '{script_name}' not found."
    params = {}
    if resource_group_name: params["ResourceGroupName"] = resource_group_name
    return _run_powershell_script(script_path, params)

@mcp.tool()
def create_resource_group(resource_group_name: str, region: str, project_name: str) -> str:
    """Creates an Azure resource group with project tagging."""
    if not resource_group_name or not region or not project_name:
        return "Error: All parameters (resource_group_name, region, project_name) are required."
    
    script_name = OP_SCRIPTS["create-rg"]
    script_path = _get_script_path(script_name)
    if not os.path.exists(script_path): 
        return f"Error: Script '{script_name}' not found."
    
    params = {
        "ResourceGroupName": resource_group_name,
        "Region": region,
        "ProjectName": project_name
    }
    return _run_powershell_script(script_path, params)

@mcp.tool()
def attach_diagnostic_settings(resource_group: str, workspace_id: str, resource_id: str) -> str:
    """
    Manually attaches diagnostic settings to a resource with a specified Log Analytics Workspace.
    Use this when multiple workspaces exist and user needs to select one.
    """
    if not resource_group or not workspace_id or not resource_id:
        return "STOP: All parameters (resource_group, workspace_id, resource_id) are required."
    
    attach_law_script = _get_script_path("attach-log-analytics.ps1")
    if not os.path.exists(attach_law_script):
        return "Error: attach-log-analytics.ps1 not found."
    
    ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
    result = run_command([
        ps_executable, "-File", attach_law_script,
        "-ResourceGroupName", resource_group,
        "-WorkspaceId", workspace_id,
        "-ResourceId", resource_id
    ])
    
    return result

@mcp.tool()
def get_deployment_requirements(resource_type: str) -> str:
    """(PowerShell Path) Inspects the PS deployment script for parameters."""
    if resource_type not in DEPLOYMENT_SCRIPTS:
        return f"Unknown resource type. Valid: {', '.join(DEPLOYMENT_SCRIPTS.keys())}"
    script_path = _get_script_path(DEPLOYMENT_SCRIPTS[resource_type])
    if not os.path.exists(script_path): return f"Error: Script not found."
    return json.dumps(_get_script_parameters(script_path), indent=2)

@mcp.tool()
def deploy_resource(resource_type: str, parameters: dict[str, str]) -> str:
    """
    (PowerShell Path) Deploys a resource using a PS script.
    REQUIRES ALL PARAMETERS - call get_deployment_requirements() first to see what's needed.
    """
    if resource_type not in DEPLOYMENT_SCRIPTS:
        return f"Unknown resource type. Options: {', '.join(DEPLOYMENT_SCRIPTS.keys())}"
    script_path = _get_script_path(DEPLOYMENT_SCRIPTS[resource_type])
    if not os.path.exists(script_path): return f"Error: Script not found."
    
    script_params = _get_script_parameters(script_path)
    missing = [p for p in script_params.get("required", []) if p not in parameters or not parameters[p]]
    if missing:
        return f"STOP: Missing mandatory parameters: {', '.join(missing)}\n\nPlease call get_deployment_requirements('{resource_type}') to see all required parameters."

    return _run_powershell_script(script_path, parameters)

@mcp.tool()
def get_bicep_requirements(resource_type: str) -> str:
    """(Bicep Path) Returns required/optional params for a Bicep template."""
    if resource_type not in TEMPLATE_MAP:
        return f"Unknown resource_type. Valid: {', '.join(TEMPLATE_MAP.keys())}"
    template_path = _get_template_path(TEMPLATE_MAP[resource_type])
    params = _parse_bicep_parameters(template_path)
    structured = {
        "required": [p for p, (req, _) in params.items() if req],
        "optional": [p for p, (req, _) in params.items() if not req],
        "defaults": {p: default for p, (req, default) in params.items() if default is not None}
    }
    return json.dumps(structured, indent=2)

@mcp.tool()
def deploy_bicep_resource(resource_group: str, resource_type: str, parameters: dict[str, str]) -> str:
    """
    (Bicep Path) Validates and deploys a resource using its specific PowerShell script.
    
    1. Validates parameters against the Bicep template.
    2. Selects the correct script (e.g., deploy-storage-account.ps1).
    3. Deploys the resource.
    4. Automatically Orchestrates NSP and Log Analytics attachment.
    """
    # 1. Strict Validation
    if not resource_group or not resource_group.strip():
        return "STOP: Resource group name is required."
    
    if not resource_type or not resource_type.strip():
        return f"STOP: Resource type is required. Valid types: {', '.join(TEMPLATE_MAP.keys())}"

    # 2. Check if we have a script for this resource type
    if resource_type not in DEPLOYMENT_SCRIPTS:
        return f"STOP: No deployment script defined for '{resource_type}'. Available scripts: {', '.join(DEPLOYMENT_SCRIPTS.keys())}"

    # 3. Validate parameters against Bicep template requirements
    # (We keep this check to ensure the user provides what the Bicep file needs, even if we run via PS)
    ok, msg, parsed_params = _validate_bicep_parameters(resource_type, parameters)
    if not ok:
        req_params = [p for p, (req, _) in parsed_params.items() if req]
        return f"STOP: {msg}\n\nPlease call get_bicep_requirements('{resource_type}') to see requirements.\nRequired: {', '.join(req_params)}"

    # 4. Locate the Specific Script
    script_name = DEPLOYMENT_SCRIPTS[resource_type]
    script_path = _get_package_file("scripts", script_name)
    
    if not os.path.exists(script_path):
        return f"CRITICAL ERROR: Script '{script_name}' not found at {script_path}. Check package structure."

    # 5. Execute Deployment
    # We add ResourceGroupName to the parameters for the script
    deployment_params = parameters.copy()
    deployment_params["ResourceGroupName"] = resource_group
    
    # We use _run_powershell_script because it unpacks the dict into individual flags 
    # (e.g. -sku Standard_LRS) which is usually what specific scripts expect.
    deploy_result = _run_powershell_script(script_path, deployment_params)

    # 6. SFI Orchestration (NSP & Logs)
    # Only proceed if deployment didn't look like a total failure
    if "Error" not in deploy_result and "FAILED" not in deploy_result:
        nsp_logs = _orchestrate_nsp_attachment(resource_group, resource_type, parameters)
        law_logs = _orchestrate_log_analytics_attachment(resource_group, resource_type, parameters)
        return f"{deploy_result}\n{nsp_logs}\n{law_logs}"

    return deploy_result

@mcp.tool()
def agent_dispatch(user_input: str) -> str:
    """High-level dispatcher."""
    # Check for specific Azure SFI agent greeting first
    if is_azure_sfi_greeting(user_input):
        return get_azure_sfi_greeting()
    
    intent = parse_intent(user_input)
    if intent in ("greeting", "menu"): return get_action_menu()
    if intent == "permissions": return list_permissions(force_refresh=True)
    if intent == "resources":
        rg = extract_resource_group(user_input)
        return list_resources(rg) if rg else list_resources()
    if intent == "create-rg":
        return (
            "Resource Group creation flow:\n\n"
            "Please provide:\n"
            "1. Resource Group Name\n"
            "2. Region (e.g., eastus, westus2, westeurope)\n"
            "3. Project Name (for tagging)\n\n"
            "This will use the create-resourcegroup.ps1 script with proper project tagging."
        )
    if intent == "create":
        return (
            "Creation flow initiated:\n\n"
            "STEP 1: First, call get_bicep_requirements(resource_type) to see what parameters are needed.\n"
            "STEP 2: Gather all required values from the user.\n"
            "STEP 3: Then call deploy_bicep_resource() with ALL required parameters.\n\n"
            "Supported types: storage-account | key-vault | openai | ai-search | ai-foundry | cosmos-db | sql-db | log-analytics\n\n"
            "Note: SFI Compliance will be automatically applied:\n"
            "  - NSP attachment for Storage, KeyVault, Cosmos, and SQL\n"
            "  - Diagnostic settings (Log Analytics) for applicable resources\n\n"
            "NEVER proceed without getting all required parameters from the user first."
        )
    return "Unrecognized command. " + get_action_menu()

@mcp.tool()
def show_agent_instructions() -> str:
    return load_agent_instructions()

def main():
    """Entry point for the azure-mcp-agent command."""
    mcp.run()

if __name__ == "__main__":
    main()