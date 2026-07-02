import re
import json
import os

os.chdir(r'c:\Users\jhalverstad\Documents Local\website lokaal')

# Load the full-res base64 images
with open('temp_full_res_map.json', 'r') as f:
    full_res_map = json.load(f)

# Read nopainnogain.html
with open('nopainnogain.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all gallery image src attributes that are thumbnails (100KB-200KB base64)
# Pattern: src="data:image/jpeg;base64,XXXXX" where base64 is roughly 100KB-200KB
pattern = r'src="data:image/jpeg;base64,([A-Za-z0-9+/=]{100000,200000})"'
thumbnails = re.findall(pattern, content)

print(f'Found {len(thumbnails)} gallery image thumbnails to replace')

# Get full-res versions
b64_list = list(full_res_map.values())
print(f'Have {len(b64_list)} full-res images to use')

replacements_made = 0
for i, thumb_b64 in enumerate(thumbnails[:26]):
    if i < len(b64_list):
        old_str = f'src="data:image/jpeg;base64,{thumb_b64}"'
        new_str = f'src="data:image/jpeg;base64,{b64_list[i]}"'
        
        if old_str in content:
            content = content.replace(old_str, new_str, 1)
            replacements_made += 1
            size_old = len(thumb_b64) / 4 * 3 / (1024*1024)
            size_new = len(b64_list[i]) / 4 * 3 / (1024*1024)
            print(f'  {i+1}. Replaced {size_old:.2f}MB -> {size_new:.2f}MB')

print(f'\nSuccessfully replaced {replacements_made}/{len(thumbnails)} thumbnails')

# Write back
with open('nopainnogain.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated nopainnogain.html ✓')

# Clean up
import os
os.remove('temp_full_res_map.json')
