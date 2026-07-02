import re
import urllib.request
import base64
import os

os.chdir(r'c:\Users\jhalverstad\Documents Local\website lokaal')

# Map with correct _rw_1920 URLs with proper hash parameters from live website
image_mappings = {
    'nopainnogain.html': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/1ae72fdf-e87e-4b57-ad41-5f6436f36651_rw_1920.jpg?h=910b425e18364a1407097ae5e422e2b7',
    'cyclocross.html': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/3f0f198b-a918-4cad-91a8-38d066d9d515_rw_1920.jpg?h=3547f9f2e76520148925ff1875e25112',
    'editorial.html': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/49a93af8-e18b-4f0d-a31d-c5066033b150_rw_1920.jpg?h=07b7d74491516fc28102db346b7153b1',
    'bandcamp.html': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/687ac6cd-c031-42ed-8099-ff0263694169_rw_1920.jpg?h=1b510bc94269e10ec693c9a2545c27cf'
}

for fname, url in image_mappings.items():
    print(f'Processing {fname}...')
    
    try:
        print(f'  Downloading {url}...')
        urllib.request.urlretrieve(url, 'temp_full_res.jpg')
        
        with open('temp_full_res.jpg', 'rb') as f:
            image_data = f.read()
        
        base64_string = 'data:image/jpeg;base64,' + base64.b64encode(image_data).decode()
        
        print(f'  Size: {len(image_data) / (1024*1024):.2f} MB, Base64: {len(base64_string) / (1024*1024):.2f} MB')
        
        # Read HTML and replace the data-src
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace any data-src with our new full-res base64
        pattern = r'data-src="data:image/jpeg;base64,[^"]*"'
        new_content = re.sub(pattern, f'data-src="{base64_string}"', content)
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        os.remove('temp_full_res.jpg')
        print(f'  [OK] {fname} updated with 1920px full-res base64')
        
    except Exception as e:
        print(f'  [ERROR] {e}')

print('\nAll files upgraded to full-res 1920px images!')
