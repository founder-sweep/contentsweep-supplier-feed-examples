#!/usr/bin/env python3
"""Reference client. Files stay local until uploaded; approvals are explicit flags."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://127.0.0.1:8080')
    parser.add_argument('--file', default=str(Path(__file__).with_name('supplier.csv')))
    parser.add_argument('--profile-spec', default=str(Path(__file__).with_name('profile.json')))
    parser.add_argument('--saved-profile-id')
    parser.add_argument('--quote-id')
    parser.add_argument('--key', help='Job retry key: reuse with the original --quote-id')
    parser.add_argument('--approve-mapping', action='store_true')
    parser.add_argument('--approve-evaluation', action='store_true')
    parser.add_argument('--out', default='normalized-feed.jsonl')
    args = parser.parse_args()
    key = os.environ['CONTENTSWEEP_API_KEY']
    base = args.base_url.rstrip('/')
    def api(path, body=None, *, raw=False):
        payload = body if raw else json.dumps(body).encode() if body is not None else None
        headers = {'X-API-Key': key, 'Content-Type': 'application/octet-stream' if raw else 'application/json'}
        with urlopen(Request(base + path, data=payload, headers=headers), timeout=30) as response:
            content = response.read()
        return content if raw else json.loads(content)
    if args.quote_id:
        quote = {'id': args.quote_id, 'status': 'quoted'}
    else:
        data = Path(args.file).read_bytes()
        spec = json.loads(Path(args.profile_spec).read_text())
        upload = api('/v1/feeds/uploads?format=' + ('jsonl' if args.file.endswith('.jsonl') else 'csv'), data, raw=True)
        upload = json.loads(upload)
        if args.saved_profile_id:
            profile_id = args.saved_profile_id
        else:
            proposal = api('/v1/feeds/preview', {'upload_id': upload['id'], 'target_schema': spec['target_schema']})
            print(json.dumps({'preview': proposal, 'mapping_to_review': spec['mapping']}, indent=2))
            if not args.approve_mapping:
                return 0
            profile = api('/v1/feeds/profiles', {'upload_id': upload['id'], **{k: spec[k] for k in ('target_schema', 'mapping', 'contract')}})
            api('/v1/feeds/profiles/' + profile['id'] + '/approve', {'approve': True, 'expected_profile_hash': profile['hash']})
            profile_id = profile['id']
        quote = api('/v1/feeds/quotes', {'upload_id': upload['id'], 'profile_id': profile_id})
        print(json.dumps({'saved_profile_id': profile_id, 'quote': quote}, indent=2))
    if quote['status'] != 'quoted' or not args.approve_evaluation:
        return 0
    retry_key = args.key or 'reference-' + quote['id']
    job = api('/v1/feeds/jobs', {'quote_id': quote['id'], 'idempotency_key': retry_key})
    print(json.dumps({'job_id': job['id'], 'retry_quote': quote['id'], 'retry_key': retry_key}))
    for _ in range(60):
        job = api('/v1/feeds/jobs/' + job['id'])
        if job['status'] in {'completed', 'failed'}:
            break
        time.sleep(2)
    print(json.dumps(job, indent=2))
    if job['status'] != 'completed':
        return 2
    print(json.dumps(api('/v1/feeds/jobs/' + job['id'] + '/report'), indent=2))
    if job['verdict'] == 'passed':
        Path(args.out).write_bytes(api('/v1/feeds/jobs/' + job['id'] + '/output', raw=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
