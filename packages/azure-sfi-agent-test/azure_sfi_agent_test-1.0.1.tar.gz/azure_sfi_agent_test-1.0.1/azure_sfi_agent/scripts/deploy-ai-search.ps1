# Deploy Azure AI Search using Bicep template

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$ServiceName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [ValidateSet('free','basic','standard','standard2','standard3','standard3_high_density','storage_optimized_l1','storage_optimized_l2')] [string]$SkuName = 'standard'
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $ServiceName) { $ServiceName = Read-Host "Enter AI Search Service Name (2-60 chars)" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. eastus)" }

$TemplatePath = Join-Path $PSScriptRoot "..\templates\ai-search.bicep"

Write-Host "\nDeploying AI Search service..." -ForegroundColor Green
az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $TemplatePath `
  --parameters name=$ServiceName location=$Location skuName=$SkuName

if ($LASTEXITCODE -eq 0) { Write-Host "Deployment succeeded" -ForegroundColor Green } else { Write-Host "Deployment failed" -ForegroundColor Red; exit 1 }
