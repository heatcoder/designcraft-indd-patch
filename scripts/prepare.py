#!/usr/bin/env python3
"""Fetch the exact upstream release and apply the portable source patch."""
from pathlib import Path
import json, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
meta = json.loads((ROOT / 'upstream.json').read_text())
dest = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'build/designcraft'
if dest.exists():
    raise SystemExit(f'Refusing to overwrite existing source: {dest}')
dest.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['git','clone','--no-checkout','--filter=blob:none',meta['repository'],str(dest)],check=True)
subprocess.run(['git','checkout','--detach',meta['revision']],cwd=dest,check=True)
patch = ROOT/'patches/designcraft-0.8.0-indd.patch'
subprocess.run(['git','apply','--check',str(patch)],cwd=dest,check=True)
subprocess.run(['git','apply',str(patch)],cwd=dest,check=True)
print(f'Prepared {dest}')
