# Attach a newly created resource to Network Security Perimeter
# Used after deploying a resource to associate it with an NSP

param(
  [Parameter(Mandatory=$false)] [string]$ResourceID,
  [Parameter(Mandatory=$false)] [string]$ResourceGroupName,
  [Parameter(Mandatory=$false)] [string]$NspName
)

if (-not $ResourceID) { $ResourceID = Read-Host "Enter Resource ID to attach" }
if (-not $ResourceGroupName) { $ResourceGroupName = Read-Host "Enter Resource Group Name" }
if (-not $NspName) { $NspName = Read-Host "Enter NSP Name" }

Write-Host "`nAttaching resource to NSP..." -ForegroundColor Cyan
Write-Host "Resource ID: $ResourceID" -ForegroundColor Gray
Write-Host "NSP: $NspName in Resource Group: $ResourceGroupName" -ForegroundColor Gray

try {
  # Get the NSP profile
  $ProfileNSP = Get-AzNetworkSecurityPerimeterProfile -ResourceGroupName $ResourceGroupName -SecurityPerimeterName $NspName

  # Create a unique association name by hashing the ResourceID and adding a timestamp
  $hashedResourceID = $ResourceID.GetHashCode().ToString("X")
  $uniqueAssociationName = "nsp-assoc-" + $hashedResourceID + "-" + (Get-Date -Format "MMddHHmmss")

  # Ensure the name is under 80 characters
  if ($uniqueAssociationName.Length -gt 80) {
    $uniqueAssociationName = $uniqueAssociationName.Substring(0, 80)
  }

  Write-Host "`nCreating association: $uniqueAssociationName" -ForegroundColor Cyan

  # Create an association object with the unique name
  $nspAssociation = @{ 
    AssociationName = $uniqueAssociationName
    ResourceGroupName = $ResourceGroupName
    SecurityPerimeterName = $NspName
    AccessMode = 'Learning'
    ProfileId = $ProfileNSP.Id 
    PrivateLinkResourceId = $ResourceID
  }

  # Create the association
  New-AzNetworkSecurityPerimeterAssociation @nspAssociation | Format-List
  Write-Host "`nSuccessfully attached resource to NSP" -ForegroundColor Green
  Write-Host "Association Name: $uniqueAssociationName" -ForegroundColor Cyan
  
} catch {
  Write-Host "`nFailed to attach resource to NSP. Error: $_" -ForegroundColor Red
  exit 1
}
