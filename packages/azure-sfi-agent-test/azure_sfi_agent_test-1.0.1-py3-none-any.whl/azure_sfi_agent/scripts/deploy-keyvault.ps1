# Deploy Azure Key Vault using Bicep template

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$KeyVaultName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [ValidateSet('standard','premium')] [string]$SkuName = 'standard',
  [Parameter(Mandatory=$false)] [int]$SoftDeleteRetentionInDays = 90
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $KeyVaultName) { $KeyVaultName = Read-Host "Enter Key Vault Name (3-24 chars)" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. eastus)" }

$TemplatePath = Join-Path $PSScriptRoot "..\templates\azure-key-vaults.bicep"

Write-Host "\nDeploying Key Vault..." -ForegroundColor Green
az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $TemplatePath `
  --parameters keyVaultName=$KeyVaultName location=$Location skuName=$SkuName softDeleteRetentionInDays=$SoftDeleteRetentionInDays

if ($LASTEXITCODE -eq 0) { Write-Host "Deployment succeeded" -ForegroundColor Green } else { Write-Host "Deployment failed" -ForegroundColor Red; exit 1 }
