$target = "C:\Users\lenovo\OneDrive - Plaksha University\Plaksha\Work\Research\2025\Projects\AI_Projects\AI_chatbot_Sugarcane"
$archive = "$target\_archive_$(Get-Date -Format 'yyyyMMdd_HHmm')"

# Create archive directory
New-Item -ItemType Directory -Force -Path $archive | Out-Null
Write-Host "Created archive folder at: $archive"

# List of known active files to KEEP
# Anything NOT in this list will be moved to archive
$keep_files = @(
    "app.py",
    "ai_services.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",
    "cleanup.ps1"
)

$keep_folders = @(
    "static",
    "templates",
    "knowledge_base",
    ".git",
    "venv",
    "_archive*" # Don't move archives into archives
)

# Get all items in the folder
$items = Get-ChildItem -Path $target

foreach ($item in $items) {
    # Check if folder is the archive folder itself
    if ($item.FullName -eq $archive) { continue }
    
    $should_keep = $false
    
    if ($item.PSIsContainer) {
        # Check folders
        if ($keep_folders -contains $item.Name -or $item.Name -like "_archive*") {
            $should_keep = $true
        }
    } else {
        # Check files
        if ($keep_files -contains $item.Name) {
            $should_keep = $true
        }
    }
    
    if (-not $should_keep) {
        Write-Host "Archiving: $($item.Name)"
        Move-Item -Path $item.FullName -Destination $archive -Force
    }
}

Write-Host "Cleanup complete. Clean application files remain."
Write-Host "Verify the folder and then run: git add . && git commit -m 'Cleanup and update'"
