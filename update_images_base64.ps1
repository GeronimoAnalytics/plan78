$workDir = 'c:\Users\jhalverstad\Documents Local\website lokaal'

$urls = @(
    @{file='nopainnogain.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/1ae72fdf-e87e-4b57-ad41-5f6436f36651.jpg?h=a53147190ee7fe0a86b8eadc1275f1c6'},
    @{file='cyclocross.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/3f0f198b-a918-4cad-91a8-38d066d9d515.jpg?h=2d4e20e7f50053dc75a80f0722ab3fa8'},
    @{file='editorial.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/49a93af8-e18b-4f0d-a31d-c5066033b150.jpg?h=8211445aa896b6558edbebb62fd6236c'},
    @{file='bandcamp.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/687ac6cd-c031-42ed-8099-ff0263694169.jpg?h=bc5f06c019edb9b354afa24d4fe5c415'}
)

foreach ($item in $urls) {
    $file = $item.file
    $url = $item.url
    $filePath = "$workDir\$file"
    
    Write-Host "Processing $file..."
    
    try {
        $tempFile = "$workDir\temp_img_large.jpg"
        Write-Host "  [1] Downloading from CDN..."
        Invoke-WebRequest -Uri $url -OutFile $tempFile
        
        $imageData = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($tempFile))
        $base64String = "data:image/jpeg;base64,$imageData"
        
        Write-Host "  [2] Converting to base64 ($($imageData.Length) chars)..."
        
        $content = Get-Content $filePath -Raw
        
        Write-Host "  [3] Updating HTML with new image..."
        $newContent = $content -replace 'data-src="https://cdn\.myportfolio\.com/[^"]*"', "data-src=`"$base64String`""
        
        Set-Content $filePath $newContent
        
        Remove-Item $tempFile
        Write-Host "  [OK] $file updated successfully"
        
    } catch {
        Write-Host "  [ERROR] $_"
    }
}

Write-Host ""
Write-Host "All files updated with large CDN images embedded as base64!"
Remove-Item "$workDir\temp_img_large.jpg" -ErrorAction SilentlyContinue
