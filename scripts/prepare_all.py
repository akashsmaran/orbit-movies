#!/usr/bin/env python3
"""Rebuild all checked-in scene recipes, then validate the catalog."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
for recipe in json.loads((root/'sources/recipes.json').read_text()):
    args = [sys.executable, str(root/'scripts/prepare_scene.py')]
    for key in ('id', 'source', 'mask', 'context', 'light', 'angle'):
        value = root/recipe[key] if key in ('source','mask') else recipe[key]
        args.extend(['--'+key, str(value)])
    subprocess.run(args, check=True)
subprocess.run([sys.executable, str(root/'scripts/validate_catalog.py')], check=True)
