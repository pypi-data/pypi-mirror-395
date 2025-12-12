# Deploy Azure Log Analytics Workspace using Bicep template
# Prompts user for required parameters

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$WorkspaceName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [ValidateSet('PerGB2018','CapacityReservation','Free','Standard','Premium')] [string]$SkuName,
  [Parameter(Mandatory=$false)] [int]$RetentionInDays,
  [Parameter(Mandatory=$false)] [ValidateSet('Enabled','Disabled')] [string]$PublicNetworkAccessForIngestion,
  [Parameter(Mandatory=$false)] [ValidateSet('Enabled','Disabled')] [string]$PublicNetworkAccessForQuery
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $WorkspaceName) { $WorkspaceName = Read-Host "Enter Log Analytics Workspace Name (4-63 chars)" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. eastus)" }

$TemplatePath = Join-Path $PSScriptRoot "..\templates\log-analytics.bicep"

Write-Host "`nDeploying Log Analytics Workspace..." -ForegroundColor Green

$deployParams = @(
  "--resource-group", $ResourceGroupName,
  "--template-file", $TemplatePath,
  "--parameters", "workspaceName=$WorkspaceName", "location=$Location"
)

if ($SkuName) { $deployParams += "skuName=$SkuName" }
if ($RetentionInDays) { $deployParams += "retentionInDays=$RetentionInDays" }
if ($PublicNetworkAccessForIngestion) { $deployParams += "publicNetworkAccessForIngestion=$PublicNetworkAccessForIngestion" }
if ($PublicNetworkAccessForQuery) { $deployParams += "publicNetworkAccessForQuery=$PublicNetworkAccessForQuery" }

az deployment group create @deployParams

if ($LASTEXITCODE -eq 0) { 
  Write-Host "`nDeployment succeeded" -ForegroundColor Green 
} else { 
  Write-Host "`nDeployment failed" -ForegroundColor Red
  exit 1 
}
