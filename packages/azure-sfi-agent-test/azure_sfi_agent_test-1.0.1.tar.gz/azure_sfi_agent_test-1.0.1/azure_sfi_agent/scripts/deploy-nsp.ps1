# Deploy Network Security Perimeter using Bicep template

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$NspName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [bool]$CreateDefaultProfile = $true
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $NspName) { $NspName = Read-Host "Enter Network Security Perimeter Name" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. westcentralus)" }

$TemplatePath = Join-Path $PSScriptRoot "..\templates\nsp.bicep"

Write-Host "`nDeploying Network Security Perimeter..." -ForegroundColor Green
az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $TemplatePath `
  --parameters nspName=$NspName location=$Location createDefaultProfile=$CreateDefaultProfile

if ($LASTEXITCODE -eq 0) { 
  Write-Host "Deployment succeeded" -ForegroundColor Green 
  Write-Host "`nNetwork Security Perimeter '$NspName' created in resource group '$ResourceGroupName'" -ForegroundColor Cyan
} else { 
  Write-Host "Deployment failed" -ForegroundColor Red
  exit 1 
}
