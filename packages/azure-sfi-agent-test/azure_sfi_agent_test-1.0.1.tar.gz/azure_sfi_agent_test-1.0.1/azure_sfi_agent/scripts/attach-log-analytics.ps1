param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceId,
    
    [Parameter(Mandatory = $true)]
    [string]$ResourceId
)

Write-Host "Attaching diagnostic settings to resource..."
Write-Host "Resource ID: $ResourceId"
Write-Host "Workspace ID: $WorkspaceId"
Write-Host ""

# Extract resource name from Resource ID
$resourceName = ($ResourceId -split '/')[-1]
$diagnosticSettingName = "diag-$resourceName"

Write-Host "Creating diagnostic setting: $diagnosticSettingName"
Write-Host ""

try {
    # Get all available diagnostic categories for the resource
    $categories = Get-AzDiagnosticSettingCategory -ResourceId $ResourceId -ErrorAction Stop
    
    $metric = @()
    $log = @()
    
    # Build metric and log settings
    $categories | ForEach-Object {
        if ($_.CategoryType -eq "Metrics") {
            $metric += New-AzDiagnosticSettingMetricSettingsObject -Enabled $true -Category $_.Name
            Write-Host "  + Metric category: $($_.Name)"
        } else {
            $log += New-AzDiagnosticSettingLogSettingsObject -Enabled $true -Category $_.Name
            Write-Host "  + Log category: $($_.Name)"
        }
    }
    
    Write-Host ""
    
    # Create the diagnostic setting
    if ($log.Count -gt 0 -or $metric.Count -gt 0) {
        $params = @{
            Name = $diagnosticSettingName
            ResourceId = $ResourceId
            WorkspaceId = $WorkspaceId
        }
        
        if ($log.Count -gt 0) {
            $params['Log'] = $log
        }
        
        if ($metric.Count -gt 0) {
            $params['Metric'] = $metric
        }
        
        $diagnosticSetting = New-AzDiagnosticSetting @params -ErrorAction Stop
        
        Write-Host "✓ Successfully attached diagnostic settings to resource."
        Write-Host "Diagnostic Setting Name: $diagnosticSettingName"
        Write-Host ""
        
        return $diagnosticSetting
    } else {
        Write-Warning "No diagnostic categories available for this resource type."
        Write-Host "Diagnostic settings not created."
        return $null
    }
    
} catch {
    if ($_.Exception.Message -like "*DiagnosticSettingsResource already exists*") {
        Write-Warning "Diagnostic setting '$diagnosticSettingName' already exists for this resource."
        Write-Host "Skipping creation."
        return $null
    } else {
        Write-Error "Failed to attach diagnostic settings: $_"
        throw
    }
}
