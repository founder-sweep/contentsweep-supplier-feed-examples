#!/usr/bin/env python3
"""Publish the owned MCP descriptor, with immutable-version and retry checks."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

REGISTRY = 'https://registry.modelcontextprotocol.io'
NAME = 'ai.contentsweep/supplier-feeds'
BASE = 'https://mcp.contentsweep.ai'


def get_json(url):
    result = subprocess.run(
        ['curl', '--silent', '--show-error', '--max-time', '25',
         '--proto', '=https', '--write-out', '\n%{http_code}', url],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError('Public endpoint could not be checked')
    body, status = result.stdout.rsplit('\n', 1)
    if status == '404':
        return None
    if status != '200':
        raise RuntimeError('Public endpoint returned HTTP ' + status)
    return json.loads(body)


def published_url(server):
    return REGISTRY + '/v0.1/servers/' + quote(server['name'], safe='') + '/versions/' + quote(server['version'], safe='')


def verify_record(record, server):
    if record['server'] != server:
        raise RuntimeError('Registry version already exists with different metadata; use a reviewed new version')
    if record.get('_meta', {}).get('io.modelcontextprotocol.registry/official', {}).get('status') != 'active':
        raise RuntimeError('Registry record is not active')


def publish(server, publisher, private_key, *, read=get_json, run=subprocess.run, sleep=time.sleep):
    if server['name'] != NAME or server.get('websiteUrl') != BASE + '/imports':
        raise ValueError('Only the owned ContentSweep descriptor may be published')
    remotes = server.get('remotes', [])
    if len(remotes) != 1 or remotes[0].get('url') != BASE + '/v1/feeds/mcp/' or remotes[0].get('type') != 'streamable-http':
        raise ValueError('Unexpected remote endpoint')
    headers = remotes[0].get('headers', [])
    if not any(h.get('name') == 'X-API-Key' and h.get('isSecret') is True and h.get('isRequired') is True for h in headers):
        raise ValueError('Descriptor must declare the required secret organization key')
    url = published_url(server)
    existing = read(url)
    if existing is not None:
        verify_record(existing, server)
        return {'state': 'already_published', 'url': url, 'version': server['version']}
    ready = read(BASE + '/health/ready')
    capabilities = read(BASE + '/imports/capabilities.json')
    deployed = read(BASE + '/imports/server.json')
    if ready is None or capabilities is None or deployed is None or deployed.get('remotes') != remotes:
        raise RuntimeError('Deployed service metadata or readiness check failed')
    if capabilities.get('limits', {}).get('rows') != 50000 or capabilities.get('limits', {}).get('bytes') != 10485760:
        raise RuntimeError('Deployed bounds do not match the qualified offer')
    # Capture publisher output: login responses and provider errors can contain secrets.
    login = run([publisher, 'login', 'dns', '--domain', 'contentsweep.ai', '--private-key', private_key],
                capture_output=True, text=True, timeout=90, check=False)
    if login.returncode:
        raise RuntimeError('MCP domain login failed; publisher output withheld')
    try:
        result = run([publisher, 'publish', 'server.json'], capture_output=True, text=True, timeout=90, check=False)
        outcome = result.returncode
    except subprocess.TimeoutExpired:
        outcome = None
    # A timeout or concurrent publisher can succeed upstream. Read back before any retry.
    for attempt in range(4):
        existing = read(url)
        if existing is not None:
            verify_record(existing, server)
            return {'state': 'published_and_verified', 'url': url, 'version': server['version']}
        if attempt != 3:
            sleep(5)
    raise RuntimeError('Publication was not verified (publisher exit ' + str(outcome) + '); do not assume success')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', type=Path, default=Path('server.json'))
    parser.add_argument('--publisher', type=Path, default=Path('./mcp-publisher'))
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    server = json.loads(args.server.read_text())
    if args.verify_only:
        record = get_json(published_url(server))
        if record is None:
            raise RuntimeError('Registry version is absent')
        verify_record(record, server)
        print(json.dumps({'state': 'verified', 'url': published_url(server), 'version': server['version']}))
        return 0
    # The publisher uses cwd for credentials and server.json. The release job runs
    # in its ephemeral checkout; local operators should use an ignored private cwd.
    if args.server.resolve() != Path('server.json').resolve():
        raise ValueError('Run publication from a protected directory containing server.json')
    key = os.environ.get('MCP_PRIVATE_KEY', '').strip()
    if len(key) != 64 or any(c not in '0123456789abcdefABCDEF' for c in key):
        raise ValueError('MCP_PRIVATE_KEY must contain a raw 32-byte hex Ed25519 key')
    print(json.dumps(publish(server, str(args.publisher.resolve()), key)))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, KeyError, OSError, subprocess.TimeoutExpired) as error:
        # Do not print provider responses, command arguments, or exception payloads.
        print(json.dumps({'error': type(error).__name__, 'action': 'publication unverified; inspect configuration and retry safely'}))
        raise SystemExit(1) from None
