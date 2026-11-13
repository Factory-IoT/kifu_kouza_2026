param(
    [string]$OutputDirectory = (Join-Path $env:TEMP 'kifu-kouza-local')
)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$packageName = "kifu-kouza-local-$stamp"
$packageRoot = Join-Path $OutputDirectory $packageName
New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot 'system/web/public') -Destination $packageRoot -Recurse
foreach ($name in 'serve-local.py', 'start-local.cmd') {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination $packageRoot
}
Copy-Item -LiteralPath (Join-Path $repoRoot 'doc/operations/local-presentation.md') -Destination (Join-Path $packageRoot 'READ-ME.md')
$archive = Join-Path $OutputDirectory "$packageName.zip"
Compress-Archive -LiteralPath $packageRoot -DestinationPath $archive
Get-FileHash -LiteralPath $archive -Algorithm SHA256
Write-Output "Package: $archive"
