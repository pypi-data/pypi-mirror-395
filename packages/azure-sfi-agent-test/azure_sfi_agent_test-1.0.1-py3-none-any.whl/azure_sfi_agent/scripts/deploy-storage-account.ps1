# Deploy Azure Storage Account using Bicep template
# Prompts user for required parameters

param(
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$StorageAccountName,
  [Parameter(Mandatory=$false)] [string]$Location,
  [Parameter(Mandatory=$false)] [ValidateSet('Hot','Cool','Cold')] [string]$AccessTier,
  [Parameter(Mandatory=$false)] [bool]$EnableHierarchicalNamespace
)

if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $StorageAccountName) { $StorageAccountName = Read-Host "Enter Storage Account Name (3-24 lower alnum)" }
if (-not $Location) { $Location = Read-Host "Enter Location (e.g. eastus)" }
if (-not $AccessTier) { $AccessTier = Read-Host "Enter Access Tier (Hot/Cool/Cold)" }
if ($EnableHierarchicalNamespace -eq $null) {
  $hnsInput = Read-Host "Enable Hierarchical Namespace? (y/n, default y)"
  $EnableHierarchicalNamespace = if ($hnsInput -and $hnsInput.ToLower() -eq 'n') { $false } else { $true }
}

$TemplatePath = Join-Path $PSScriptRoot "..\templates\storage-account.bicep"

Write-Host "\nDeploying Storage Account..." -ForegroundColor Green
az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $TemplatePath `
  --parameters storageAccountName=$StorageAccountName location=$Location accessTier=$AccessTier enableHierarchicalNamespace=$EnableHierarchicalNamespace

if ($LASTEXITCODE -eq 0) { Write-Host "Deployment succeeded" -ForegroundColor Green } else { Write-Host "Deployment failed" -ForegroundColor Red; exit 1 }
