"""Give untitled slides in md/ChX-Y.md a heading taken from their first line of text."""
import os, re, sys

d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not re.match(r'Ch\d+-\d+\.md$', f):
        continue
    p = os.path.join(d, f)
    lines = open(p, encoding='utf-8').read().split('\n')
    for i, l in enumerate(lines):
        m = re.match(r'^## Slide (\d+)(（隱藏投影片）)?$', l)
        if not m:
            continue
        for j in range(i + 1, len(lines)):
            t = lines[j].strip()
            if t.startswith('## Slide'):
                break
            if not t or t.startswith(('［圖', '|', '>')) or t == '（無文字）':
                continue
            t = re.sub(r'\s+', ' ', re.sub(r'^-\s+', '', t))
            if len(t) > 90:
                t = t[:88] + '…'
            lines[i] = f'## Slide {m.group(1)} — {t}' + (m.group(2) or '')
            break
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))
