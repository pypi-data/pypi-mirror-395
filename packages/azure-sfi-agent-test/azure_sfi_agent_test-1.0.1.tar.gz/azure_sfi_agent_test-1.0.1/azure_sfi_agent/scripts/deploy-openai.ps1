# Deploy Azure OpenAI using Bicep template
# Prompts user for required parameters and deploys the resource

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$AccountName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location,
    
    [Parameter(Mandatory=$false)]
    [bool]$DisableLocalAuth = $true,
    [Parameter(Mandatory=$false)]
    [bool]$DisablePublicNetworkAccess = $true,
    [Parameter(Mandatory=$false)]
    [bool]$RestrictOutboundNetworkAccess = $true
)

# Prompt for Resource Group if not provided
if (-not $ResourceGroupName) {
    $ResourceGroupName = Read-Host "Enter Resource Group Name"
}

# Prompt for Account Name if not provided
if (-not $AccountName) {
    $AccountName = Read-Host "Enter Azure OpenAI Account Name (2-64 chars, globally unique)"
}

# Prompt for Location if not provided
if (-not $Location) {
    $Location = Read-Host "Enter Location (e.g., eastus, westus)"
}

# (Template includes additional booleans; parameters defaulted. No extra prompts unless user overrides.)

# Build the template file path (assumes template is in ../templates/)
$TemplatePath = Join-Path $PSScriptRoot "..\templates\azure-openai.bicep"

# Build deployment command parameters
Write-Host "`nDeploying Azure OpenAI resource..." -ForegroundColor Green
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Cyan
Write-Host "Account Name: $AccountName" -ForegroundColor Cyan
Write-Host "Location: $Location" -ForegroundColor Cyan

# Execute deployment
az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file $TemplatePath `
    --parameters accountName=$AccountName location=$Location disableLocalAuth=$DisableLocalAuth disablePublicNetworkAccess=$DisablePublicNetworkAccess restrictOutboundNetworkAccess=$RestrictOutboundNetworkAccess

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDeployment completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nDeployment failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
