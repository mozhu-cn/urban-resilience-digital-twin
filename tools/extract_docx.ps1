# Extract text from all .docx files into .txt files (UTF-8)
param(
    [string]$SourceDir = ".",
    [string]$OutDir = "docx_text"
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$docxFiles = Get-ChildItem -Path $SourceDir -Filter *.docx -File
$docxFiles += Get-ChildItem -Path (Join-Path $SourceDir "Miyazaki_Simulation") -Filter *.docx -File -ErrorAction SilentlyContinue

foreach ($file in $docxFiles) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($file.FullName)
    try {
        $entry = $zip.GetEntry("word/document.xml")
        if ($null -eq $entry) { Write-Host "SKIP (no document.xml): $($file.Name)"; continue }
        $reader = New-Object System.IO.StreamReader($entry.Open(), [System.Text.Encoding]::UTF8)
        $xml = $reader.ReadToEnd()
        $reader.Close()

        # Extract text: paragraph boundaries become newlines
        $xml = $xml -replace '</w:p>', "`n"
        $xml = $xml -replace '<w:tab[^>]*/>', "`t"
        $xml = $xml -replace '<[^>]+>', ''
        $xml = [System.Net.WebUtility]::HtmlDecode($xml)
        # Collapse multiple blank lines
        $xml = $xml -replace "(\r?\n){3,}", "`n`n"

        $base = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $outFile = Join-Path $OutDir ($base + ".txt")
        [System.IO.File]::WriteAllText($outFile, $xml, [System.Text.UTF8Encoding]::new($false))
        Write-Host "OK: $($file.Name) -> $outFile ($($xml.Length) chars)"
    } finally {
        $zip.Dispose()
    }
}
