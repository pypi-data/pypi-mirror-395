# Deploy Azure AI Foundry (AIServices + optional Project) using Bicep template

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$AiFoundryName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [string]$AiProjectName = '',
  [Parameter(Mandatory=$false)] [bool]$DisableLocalAuth = $true,
  [Parameter(Mandatory=$false)] [bool]$DisablePublicNetworkAccess = $true,
  [Parameter(Mandatory=$false)] [bool]$RestrictOutboundNetworkAccess = $true,
  [Parameter(Mandatory=$false)] [bool]$AllowProjectManagement = $true,
  [Parameter(Mandatory=$false)] [string]$CustomSubDomainName = '',
  [Parameter(Mandatory=$false)] [bool]$ApplyNetworkAcls = $false
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $AiFoundryName) { $AiFoundryName = Read-Host "Enter AI Foundry Name" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. eastus)" }

$TemplatePath = Join-Path $PSScriptRoot "..\templates\ai-foundry.bicep"

Write-Host "\nDeploying AI Foundry (AIServices)..." -ForegroundColor Green
az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $TemplatePath `
  --parameters aiFoundryName=$AiFoundryName location=$Location aiProjectName=$AiProjectName disableLocalAuth=$DisableLocalAuth disablePublicNetworkAccess=$DisablePublicNetworkAccess restrictOutboundNetworkAccess=$RestrictOutboundNetworkAccess allowProjectManagement=$AllowProjectManagement customSubDomainName=$CustomSubDomainName applyNetworkAcls=$ApplyNetworkAcls

if ($LASTEXITCODE -eq 0) { Write-Host "Deployment succeeded" -ForegroundColor Green } else { Write-Host "Deployment failed" -ForegroundColor Red; exit 1 }
