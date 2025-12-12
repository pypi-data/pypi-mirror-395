param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName
)

Write-Host "Using current subscription context..."
$context = Get-AzContext
$subscriptionId = $context.Subscription.Id
Write-Host "Subscription ID: $subscriptionId"

# Fetch resource group details
Write-Host "Fetching resource group details for '$ResourceGroupName'..."
$resourceGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (-not $resourceGroup) {
    Write-Error "Resource Group '$ResourceGroupName' not found."
    exit 1
}

Write-Host "Resource Group: $($resourceGroup.ResourceGroupName)"
Write-Host "Location: $($resourceGroup.Location)"
Write-Host ""

Write-Host "Checking for existing Log Analytics Workspaces in resource group '$ResourceGroupName'..."
$existingWorkspaces = Get-AzOperationalInsightsWorkspace -ResourceGroupName $ResourceGroupName -ErrorAction SilentlyContinue

if ($existingWorkspaces) {
    $workspaceCount = ($existingWorkspaces | Measure-Object).Count
    
    if ($workspaceCount -eq 1) {
        $workspace = $existingWorkspaces
        Write-Host "LOG ANALYTICS WORKSPACE FOUND: '$($workspace.Name)'"
        Write-Host ""
        Write-Host "One Log Analytics Workspace exists in this resource group."
        Write-Host "Use attach-log-analytics.ps1 to attach diagnostic settings to resources."
        Write-Host ""
        
        return @{
            ResourceGroup = $ResourceGroupName
            Exists = $true
            WorkspaceName = $workspace.Name
            WorkspaceId = $workspace.ResourceId
            Location = $workspace.Location
            Count = 1
        }
    } else {
        Write-Host "MULTIPLE LOG ANALYTICS WORKSPACES FOUND: $workspaceCount workspaces"
        Write-Host ""
        Write-Host "Available workspaces:"
        for ($i = 0; $i -lt $workspaceCount; $i++) {
            Write-Host "  [$($i+1)] $($existingWorkspaces[$i].Name) - Location: $($existingWorkspaces[$i].Location)"
        }
        Write-Host ""
        Write-Host "Multiple Log Analytics Workspaces exist."
        Write-Host "Please specify which workspace to use for diagnostic settings."
        Write-Host ""
        
        # Return all workspace details for user to choose
        $workspaceList = @()
        foreach ($ws in $existingWorkspaces) {
            $workspaceList += @{
                Name = $ws.Name
                ResourceId = $ws.ResourceId
                Location = $ws.Location
            }
        }
        
        return @{
            ResourceGroup = $ResourceGroupName
            Exists = $true
            Count = $workspaceCount
            Workspaces = $workspaceList
            RequiresSelection = $true
        }
    }
} else {
    Write-Host "LOG ANALYTICS WORKSPACE NOT FOUND."
    Write-Host "Creating Log Analytics Workspace in resource group '$ResourceGroupName'..."
    Write-Host ""
    
    # Define expected Log Analytics Workspace name
    $workspaceName = "$ResourceGroupName-law"
    
    # Deploy using Bicep template with Azure CLI
    $templatePath = Join-Path $PSScriptRoot "..\templates\log-analytics.bicep"
    
    if (-not (Test-Path $templatePath)) {
        Write-Error "Bicep template not found at: $templatePath"
        exit 1
    }
    
    $deploymentName = "log-analytics-deployment-$(Get-Date -Format 'yyyyMMddHHmmss')"
    
    try {
        # Use Azure CLI for deployment
        Write-Host "Deploying workspace '$workspaceName'..."
        $output = az deployment group create `
            --name $deploymentName `
            --resource-group $ResourceGroupName `
            --template-file $templatePath `
            --parameters workspaceName=$workspaceName location=$($resourceGroup.Location) `
            --output json 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Deployment failed: $output"
            exit 1
        }
        
        Write-Host "✓ Log Analytics Workspace '$workspaceName' created successfully."
        Write-Host ""
        
        # Fetch the newly created workspace
        $newWorkspace = Get-AzOperationalInsightsWorkspace -ResourceGroupName $ResourceGroupName -Name $workspaceName
        
        return @{
            ResourceGroup = $ResourceGroupName
            Exists = $true
            WorkspaceName = $workspaceName
            WorkspaceId = $newWorkspace.ResourceId
            Location = $newWorkspace.Location
            Created = $true
            Count = 1
        }
    } catch {
        Write-Error "Failed to create Log Analytics Workspace: $_"
        exit 1
    }
}
