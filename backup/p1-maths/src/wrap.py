"""Wrap a page template into the standalone page that goes on the site.

Usage (from this folder):  python3 wrap.py dates-2-1.template.html ../../../maths/dates-2-1.html

The templates have no <html>/<head>/<body> skeleton. This adds the doctype,
charset and viewport tags, closes <head> after the first </style>, and closes
<body>/<html> at the end, exactly as the published pages in maths/ are built.
"""
import sys
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf8').read()
head = ('<!doctype html>\n<html lang="zh-HK">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
i = t.index('</style>\n') + len('</style>\n')
page = head + t[:i] + '</head>\n<body>\n' + t[i:].rstrip('\n') + '\n</body>\n</html>\n'
open(out, 'w', encoding='utf8').write(page)
print('wrote', out, len(page.encode('utf8')), 'bytes')
