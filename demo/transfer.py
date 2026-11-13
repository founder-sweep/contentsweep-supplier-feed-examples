#!/usr/bin/env python3
"""Upload only checksum-bound synthetic fixtures; never approve, quote or start work."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-upload', action='store_true', required=True)
    parser.add_argument('--output', type=Path, required=True, help='Private upload identity file')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / 'manifest.json').read_text())
    product = manifest['product']
    if manifest['default_mode'] != 'hosted':
        parser.error('This product uses local files; no upload is needed')
    endpoint = manifest['endpoint'].removesuffix('mcp/') + 'uploads'
    if not endpoint.startswith('https://mcp.contentsweep.ai/v1/'):
        parser.error('Unexpected upload destination')
    key = os.environ.get(manifest['setting'])
    if not key:
        parser.error('Configure ' + manifest['setting'] + ' privately')
    names = {'feeds': ['supplier.csv', 'later.csv', 'drift.csv'],
             'quality': ['continue.csv', 'block.csv', 'warning.csv'],
             'dag_doctor': ['executor-mismatch/bundle.json', 'executor-mismatch-missing-context/bundle.json'],
             'deployment_fixer': ['blocked/bundle.json', 'supported/bundle.json', 'stateful-unsupported/bundle.json']}[product]
    identity = hashlib.sha256(json.dumps({n: manifest['fixtures_sha256'][n] for n in names}, sort_keys=True).encode()).hexdigest()
    record = {'product': product, 'endpoint': endpoint, 'fixture_identity': identity, 'uploads': {}}
    if args.output.exists():
        if args.output.is_symlink():
            parser.error('Refuse a symlink output')
        record = json.loads(args.output.read_text())
        if record['fixture_identity'] != identity or record['endpoint'] != endpoint:
            parser.error('Saved upload identities refer to different input; review before new work')
    args.output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in names:
        raw = (here / 'fixtures' / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['fixtures_sha256'][name]:
            parser.error('Fixture checksum mismatch')
        if name in record['uploads']:
            continue
        csv = product in {'feeds', 'quality'}
        body = raw if csv else json.dumps(json.loads(raw)).encode()
        request = Request(endpoint + ('?format=csv' if csv else ''), data=body,
                          headers={'Content-Type': 'application/octet-stream' if csv else 'application/json', 'X-API-Key': key})
        with urlopen(request, timeout=30) as response:
            value = json.load(response)
        if product in {'feeds', 'quality'}:
            assert value['sha256'] == hashlib.sha256(raw).hexdigest()
        record['uploads'][name] = value
        temporary = args.output.with_suffix('.tmp')
        with temporary.open('w') as stream:
            os.chmod(temporary, 0o600)
            json.dump(record, stream, indent=2)
        temporary.replace(args.output)
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
