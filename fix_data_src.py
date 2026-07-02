import re
import os

os.chdir(r'c:\Users\jhalverstad\Documents Local\website lokaal')

files = ['nopainnogain.html', 'cyclocross.html', 'editorial.html', 'bandcamp.html', 'over.html']

for fname in files:
    print(f'Processing {fname}...')
    
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all data-src attributes
    def fix_data_src(match):
        full_match = match.group(0)
        src_value = match.group(1)
        
        # Check if it starts with data:image
        if src_value.startswith('data:image'):
            return full_match  # Already has prefix
        else:
            # Need to add prefix - check if it's jpeg or png
            if src_value.startswith('/9j/'):  # JPEG signature
                return f'data-src="data:image/jpeg;base64,{src_value}"'
            elif src_value.startswith('iVBORw0'):  # PNG signature
                return f'data-src="data:image/png;base64,{src_value}"'
            else:
                return full_match  # Leave as is
    
    # Match data-src="..." patterns
    pattern = r'data-src="([^"]+)"'
    content = re.sub(pattern, fix_data_src, content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  [OK] {fname} fixed')

print('\nAll files repaired!')
