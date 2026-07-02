import re
import urllib.request
import base64
import os

os.chdir(r'c:\Users\jhalverstad\Documents Local\website lokaal')

# PNG full-res URLs from live website
png_mappings = {
    '05b4dd6c-9154-48d8-aca1-c2767aca4fdf': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/05b4dd6c-9154-48d8-aca1-c2767aca4fdf_rw_1920.png?h=bf2438dd512a982dc661b013b110581e',
    '895fb263-eba9-4150-8927-2d7c8bfbe3b3': 'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/895fb263-eba9-4150-8927-2d7c8bfbe3b3_rw_1920.png?h=872a687e51a2c52704190a591643d94c'
}

print('Downloading PNG full-res versions...')

png_base64_map = {}

for uuid, url in png_mappings.items():
    try:
        print(f'  Downloading {uuid}...')
        urllib.request.urlretrieve(url, 'temp_png.png')
        
        with open('temp_png.png', 'rb') as f:
            image_data = f.read()
        
        base64_string = 'data:image/png;base64,' + base64.b64encode(image_data).decode()
        size_mb = len(image_data) / (1024*1024)
        print(f'    Size: {size_mb:.2f} MB')
        
        png_base64_map[uuid] = base64_string
        os.remove('temp_png.png')
        
    except Exception as e:
        print(f'    [ERROR] {e}')

# Now update over.html with the new PNG base64s
print('\nUpdating over.html...')

with open('over.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace each PNG data-src occurrence with full-res versions
# We have 2 PNGs, so replace them in order
base64_list = list(png_base64_map.values())

# Find all data-src attributes with PNG base64
pattern = r'data-src="data:image/png;base64,[^"]*"'
matches = re.findall(pattern, content)

print(f'Found {len(matches)} PNG data-src attributes')

# Replace each match with our full-res version (in order)
for i, match in enumerate(matches):
    if i < len(base64_list):
        new_match = f'data-src="{base64_list[i]}"'
        content = content.replace(match, new_match, 1)
        print(f'  Updated PNG image {i+1}')

with open('over.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nover.html updated with PNG full-res images!')
