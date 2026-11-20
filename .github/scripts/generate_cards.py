import base64
import re

medallions = {
    'pull_shark': ('images/pull-shark-silver-x3.png', 'images/badge_label_pull_shark.svg', 'Pull Shark (Silver x3)'),
    'pair_extraordinaire': ('images/medallion_pair_extraordinaire.png', 'images/badge_label_pair_extraordinaire.svg', 'Pair Extraordinaire'),
    'starstruck': ('images/medallion_starstruck.png', 'images/badge_label_starstruck.svg', 'Starstruck'),
    'yolo': ('images/medallion_yolo.png', 'images/badge_label_yolo.svg', 'YOLO'),
    'quickdraw': ('images/medallion_quickdraw.png', 'images/badge_label_quickdraw.svg', 'Quickdraw')
}

for name, (img_path, label_path, title) in medallions.items():
    with open(img_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    with open(label_path, 'r', encoding='utf-8') as f:
        label_svg = f.read()

    # Extract defs from label_svg
    defs_match = re.search(r'<defs>([\s\S]*?)</defs>', label_svg)
    defs_content = defs_match.group(1) if defs_match else ''
    
    # Extract inner elements (strip svg tag and defs)
    inner = re.sub(r'<\?xml[^>]*\?>', '', label_svg)
    inner = re.sub(r'<svg[^>]*>', '', inner)
    inner = re.sub(r'</svg>', '', inner)
    inner = re.sub(r'<defs>[\s\S]*?</defs>', '', inner).strip()
    
    combined_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="105" height="137" viewBox="0 0 105 137">
  <defs>
{defs_content}
  </defs>

  <!-- Achievement Medallion -->
  <image href="data:image/png;base64,{img_b64}" x="0" y="0" width="105" height="105" />

  <!-- Achievement Label -->
  <g transform="translate(0, 113)">
    {inner}
  </g>
</svg>'''

    out_file = f'images/card_achievement_{name}.svg'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(combined_svg)
    print(f'Generated {out_file}')

print('All 5 cards generated successfully!')
