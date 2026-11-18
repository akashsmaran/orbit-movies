#!/usr/bin/env python3
"""Validate the version 1 catalog and local artwork using only Python's stdlib."""
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def validate(value, schema, where='$'):
    kind = schema.get('type')
    types = {'object':dict, 'array':list, 'string':str, 'integer':int}
    if kind and (not isinstance(value, types[kind]) or kind == 'integer' and isinstance(value, bool)):
        raise ValueError(f'{where}: expected {kind}')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{where}: expected {schema["const"]}')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value: raise ValueError(f'{where}: missing {key}')
        properties = schema.get('properties', {})
        for key, child in value.items():
            if schema.get('additionalProperties') is False and key not in properties:
                raise ValueError(f'{where}: unknown field {key}')
            if key in properties: validate(child, properties[key], f'{where}.{key}')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', float('inf')):
            raise ValueError(f'{where}: invalid item count')
        for index, child in enumerate(value): validate(child, schema['items'], f'{where}[{index}]')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', float('inf')):
            raise ValueError(f'{where}: invalid string length')
        if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
            raise ValueError(f'{where}: invalid format')
    if isinstance(value, int):
        if value < schema.get('minimum', -float('inf')) or value > schema.get('maximum', float('inf')):
            raise ValueError(f'{where}: number outside permitted range')

def main():
    catalog = json.loads((ROOT/'movies.json').read_text())
    schema = json.loads((ROOT/'movies.schema.json').read_text())
    validate(catalog, schema)
    identifiers = set()
    for movie in catalog['movies']:
        if movie['id'] in identifiers: raise ValueError(f'Duplicate movie id: {movie["id"]}')
        identifiers.add(movie['id'])
        if not movie['title'].strip(): raise ValueError('Movie title cannot be blank')
        art = urlparse(movie['artwork'])
        if art.scheme:
            if art.scheme != 'https' or not art.hostname or art.username:
                raise ValueError('Remote artwork must use HTTPS')
        else:
            local = (ROOT/movie['artwork']).resolve()
            if movie['artwork'].startswith('/') or '..' in movie['artwork'] or not local.is_relative_to(ROOT):
                raise ValueError('Artwork path must stay inside the repository')
            if not local.is_file(): raise ValueError(f'Missing artwork: {movie["artwork"]}')
            if local.suffix.lower() not in ('.png', '.webp'): raise ValueError('Use PNG or WebP cutouts')
            if local.stat().st_size > 4*1024*1024: raise ValueError('Artwork exceeds 4 MiB')
        for link in movie['links']:
            if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)+', link['packageName']):
                raise ValueError('Invalid Android package name')
            if 'url' in link:
                uri = urlparse(link['url'])
                if not uri.scheme or uri.scheme.lower() in ('http','file','content','javascript','data','intent') or uri.username:
                    raise ValueError('Use HTTPS or a verified streaming-app URI')
    if (ROOT/'movies.json').stat().st_size > 1024*1024: raise ValueError('Catalog exceeds 1 MiB')
    print(f'Valid catalog: {len(identifiers)} movies')

if __name__ == '__main__':
    main()
