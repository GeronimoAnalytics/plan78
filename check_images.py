import re

files = ['nopainnogain.html', 'cyclocross.html', 'editorial.html', 'bandcamp.html', 'over.html']

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find data-src
    ds_match = re.search(r'data-src="([^"]{80})"', content)
    if ds_match:
        print(f'{fname} - data-src starts: {ds_match.group(1)[:80]}')
    
    # Find img src
    img_match = re.search(r'<img[^>]*src="([^"]{80})"', content)
    if img_match:
        print(f'{fname} - img src starts: {img_match.group(1)[:80]}')
    print()
