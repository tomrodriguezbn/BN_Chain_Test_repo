#!/usr/bin/env python3
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, ".."))

bad = []
link_re = re.compile(r'\[(.*?)\]\((.*?)\)')

def scan(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for m in link_re.finditer(text):
        target = m.group(2)
        if target.startswith("http"):
            continue
        if target.startswith("#") or target.startswith("mailto:"):
            continue
        candidate = os.path.normpath(os.path.join(os.path.dirname(path), target))
        if not os.path.exists(candidate):
            bad.append((path, target))

for base, _, files in os.walk(REPO):
    for fn in files:
        if fn.endswith(".md"):
            scan(os.path.join(base, fn))

if bad:
    print("Broken relative links:")
    for src, tgt in bad:
        print(f" - {src} -> {tgt}")
    sys.exit(1)

print("All relative links look good.")
