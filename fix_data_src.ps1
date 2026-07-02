$workDir = 'c:\Users\jhalverstad\Documents Local\website lokaal'

$files = @(
    'nopainnogain.html',
    'cyclocross.html', 
    'editorial.html',
    'bandcamp.html',
    'over.html'
)

foreach ($file in $files) {
    $filePath = "$workDir\$file"
    Write-Host "Fixing $file..."
    
    $content = Get-Content $filePath -Raw
    
    # Find all data-src attributes that contain raw base64 without the prefix
    $pattern = 'data-src="([^"]*)jpeg[^"]*"'
    $matches = [regex]::Matches($content, $pattern)
    
    foreach ($match in $matches) {
        $oldValue = $match.Value
        $base64Content = $match.Groups[1].Value
        
        # Check if it already has the prefix
        if ($base64Content -notlike 'data:image/*') {
            # Need to add the prefix
            if ($base64Content -like '*jpeg*') {
                $newValue = 'data-src="data:image/jpeg;base64,' + $base64Content + '"'
            } elseif ($base64Content -like '*png*') {
                $newValue = 'data-src="data:image/png;base64,' + $base64Content.Replace('data:image/png;base64,', '') + '"'
            }
            
            $content = $content.Replace($oldValue, $newValue)
            Write-Host "  Fixed one data-src"
        }
    }
    
    Set-Content $filePath $content
    Write-Host "  [OK] $file saved"
}

Write-Host ""
Write-Host "All files fixed!"
