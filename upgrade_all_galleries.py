import urllib.request
import re
import base64
import json
import os

os.chdir(r'c:\Users\jhalverstad\Documents Local\website lokaal')

pages = {
    'cyclocross.html': 'https://plan78.com/cyclocross',
    'editorial.html': 'https://plan78.com/editorial',
    'bandcamp.html': 'https://plan78.com/bandcamp',
    'miscellaneous.html': 'https://plan78.com/miscellaneous'
}

for html_file, live_url in pages.items():
    print(f'\n{"="*50}')
    print(f'Processing {html_file}')
    print("="*50)
    
    try:
        # Fetch live page
        req = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
        
        # Extract all CDN URLs
        uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})_rw_(\d+)\.jpg\?h=([a-f0-9]+)'
        matches = re.findall(uuid_pattern, html)
        
        # Get unique UUIDs preserving order, prefer 1920
        uuid_map = {}
        for uuid, res, hash_val in matches:
            if uuid not in uuid_map:
                uuid_map[uuid] = {'1920': None, 'other': None, 'hash': hash_val}
            if res == '1920':
                uuid_map[uuid]['1920'] = hash_val
            else:
                uuid_map[uuid]['other'] = hash_val
        
        # Download full-res versions
        print(f'Downloading {len(uuid_map)} full-res images...')
        full_res_map = {}
        for i, (uuid, info) in enumerate(uuid_map.items()):
            hash_val = info['1920'] or info['other'] or info['hash']
            url_1920 = f'https://cdn.myportfolio.com/9f1fc68a-9220-4ac1-bf1e-7aad38041008/{uuid}_rw_1920.jpg?h={hash_val}'
            
            try:
                req_img = urllib.request.Request(url_1920, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_img, timeout=10) as resp:
                    img_data = resp.read()
                b64 = base64.b64encode(img_data).decode('ascii')
                full_res_map[uuid] = b64
                size_mb = len(b64) / 4 * 3 / (1024*1024)
                print(f'  {i+1}/{len(uuid_map)}: {size_mb:.2f} MB')
            except Exception as e:
                print(f'  ERROR {uuid}: {e}')
        
        # Read local HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all gallery thumbnails (100KB-200KB)
        pattern = r'src="data:image/jpeg;base64,([A-Za-z0-9+/=]{100000,200000})"'
        thumbnails = re.findall(pattern, content)
        
        print(f'Found {len(thumbnails)} thumbnails to replace')
        
        # Replace with full-res versions
        b64_list = list(full_res_map.values())
        replaced = 0
        
        for i, thumb_b64 in enumerate(thumbnails[:len(b64_list)]):
            old_str = f'src="data:image/jpeg;base64,{thumb_b64}"'
            new_str = f'src="data:image/jpeg;base64,{b64_list[i]}"'
            
            if old_str in content:
                content = content.replace(old_str, new_str, 1)
                replaced += 1
        
        print(f'Replaced {replaced}/{len(thumbnails)} thumbnails')
        
        # Write back
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✓ Updated {html_file}')
        
    except Exception as e:
        print(f'ERROR: {e}')

print('\n' + '='*50)
print('All pages upgraded!')
