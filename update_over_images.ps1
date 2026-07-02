$workDir = 'c:\Users\jhalverstad\Documents Local\website lokaal'

$urls = @(
    @{file='over.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/05b4dd6c-9154-48d8-aca1-c2767aca4fdf.png?h=0aa30af5513c718b9efe8d83c454c5aa'},
    @{file='over.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/895fb263-eba9-4150-8927-2d7c8bfbe3b3.png?h=60fbc2812492262fdeb923b081c7e3f9'}
)

$images = @{}

foreach ($item in $urls) {
    $url = $item.url
    
    Write-Host "Downloading image from CDN..."
    
    try {
        $tempFile = "$workDir\temp_img_over.png"
        Invoke-WebRequest -Uri $url -OutFile $tempFile
        
        $imageData = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($tempFile))
        $base64String = "data:image/png;base64,$imageData"
        
        Write-Host "  Converted to base64 ($($imageData.Length) chars)..."
        
        $images[$url] = $base64String
        
        Remove-Item $tempFile
        
    } catch {
        Write-Host "  [ERROR] $_"
    }
}

if ($images.Count -gt 0) {
    Write-Host ""
    Write-Host "Updating over.html with embedded images..."
    $filePath = "$workDir\over.html"
    $content = Get-Content $filePath -Raw
    
    foreach ($key in $images.Keys) {
        $content = $content -replace [regex]::Escape("data-src=`"$key`""), "data-src=`"$($images[$key])`""
    }
    
    Set-Content $filePath $content
    Write-Host "[OK] over.html updated with 2 embedded PNG images"
}

Write-Host ""
Write-Host "Complete! All large CDN images are now embedded as base64 in your HTML files."
