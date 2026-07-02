$workDir = 'c:\Users\jhalverstad\Documents Local\website lokaal'

# URLs uit de HTML files
$urls = @(
    @{file='nopainnogain.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/1ae72fdf-e87e-4b57-ad41-5f6436f36651.jpg?h=a53147190ee7fe0a86b8eadc1275f1c6'},
    @{file='cyclocross.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/3f0f198b-a918-4cad-91a8-38d066d9d515.jpg?h=2d4e20e7f50053dc75a80f0722ab3fa8'},
    @{file='editorial.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/49a93af8-e18b-4f0d-a31d-c5066033b150.jpg?h=8211445aa896b6558edbebb62fd6236c'},
    @{file='bandcamp.html'; url='https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/687ac6cd-c031-42ed-8099-ff0263694169.jpg?h=bc5f06c019edb9b354afa24d4fe5c415'}
)

foreach ($item in $urls) {
    $file = $item.file
    $url = $item.url
    Write-Host "Downloading $file from CDN..."
    
    try {
        $tempFile = "$workDir\temp_img.jpg"
        Invoke-WebRequest -Uri $url -OutFile $tempFile
        $imageData = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($tempFile))
        Write-Host "[OK] Downloaded and converted to base64 - $($imageData.Length) chars"
        Remove-Item $tempFile
    } catch {
        Write-Host "[ERROR] Error downloading: $_"
    }
}
