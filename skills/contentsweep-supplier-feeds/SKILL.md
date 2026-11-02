---
name: contentsweep-supplier-feeds
description: Map and validate recurring supplier CSV/JSONL with approved profiles, full-file checks and structural drift review. Use for supplier catalog imports, not unrestricted transformations.
---

# Supplier Feeds: first import and approved reuse

Use for hosted recurring supplier catalogs with explicit mappings and complete-file validation. Upload only permitted files. Field names do not establish meaning; the operator resolves mapping, units, currency and decimal locale.

## Connect and fund

The operator verifies email at https://mcp.contentsweep.ai/account/sign-in?product=supplier-feeds&source=agent-skill&channel=skills&asset=contentsweep-supplier-feeds&campaign=agent-growth-v1 and creates an organization API key. Keep CONTENTSWEEP_API_KEY private. Streamable HTTP MCP: https://mcp.contentsweep.ai/v1/feeds/mcp/ with X-API-Key. All requests, including initialization/tools/list, need authentication. Anonymous 401 is expected. No OAuth or machine payments are enabled.

Five trials once per verified organization. $20 buys ten evaluations; the optional $99/month offer includes 100 evaluations. A completed rejection also uses one evaluation. Previews, unsupported inputs and platform failures do not consume evaluations. No automatic overages. Hand the operator https://mcp.contentsweep.ai/imports/app?source=agent-skill for funding; purchases need approval of displayed terms. Do not buy automatically or reuse Quality credits.

## First import

1. Accept actual UTF-8 flat CSV/JSONL, at most 10 MiB, 50,000 records and 100 fields. No XLSX, nested records, arbitrary code or semantic guesses.
2. upload_supplier_feed with actual content; preview_supplier_feed with the explicit target schema. Preview is sampled, not complete-file acceptance.
3. create_supplier_feed_profile with the mapping, contract and explicit decimal rules. Read back the exact profile. Only after operator review call approve_supplier_feed_profile with its expected_profile_hash and approve=true.
4. quote_supplier_import. On review_required, resolve drift and approve a new version. Under existing spending authorization/cap, start_supplier_import with the quote and a stable idempotency_key.
5. Poll get_supplier_import up to 60 times, two seconds apart. Keep the original quote/key across uncertain retries.
6. Read get_supplier_import_report and the receipt. Only a passed, complete evaluation permits output delivery. Fetch authenticated output (or every get_supplier_import_output page) and verify its SHA256 against the receipt's output fingerprint. Never write a partial page set to a destination.

## Next delivery

Read the owned approved profile using get_supplier_feed_profile; upload the new complete file and quote against that profile. Reuse approved decisions while structure is compatible. Changed structure requires a new reviewed version. A rejected file stops downstream writes; corrected bytes are a new evaluation. Timeout, unknown states, missing output and hash mismatch stop delivery. Destination writes have separate authorization.

Uploads last 24 hours; results seven days; receipts 30 days. Profiles remain until deletion. Store job/quote/key identities privately. Do not create another evaluation to resolve an uncertain retry.

## Runnable reference

From the public repository with CONTENTSWEEP_API_KEY privately configured:

```bash
python3 client.py --base-url https://mcp.contentsweep.ai --file supplier.csv --profile-spec profile.json
```

This previews the supplied mapping without approval or spending. After exact mapping review and spending authorization:

```bash
python3 client.py --base-url https://mcp.contentsweep.ai --file supplier.csv --profile-spec profile.json --approve-mapping --approve-evaluation
python3 client.py --base-url https://mcp.contentsweep.ai --file supplier.csv --saved-profile-id APPROVED_PROFILE_ID --approve-evaluation
```

An uncertain retry supplies --quote-id ORIGINAL_QUOTE_ID --key ORIGINAL_RETRY_KEY --approve-evaluation. Independently verify the downloaded output fingerprint before destination writes. Reference: https://mcp.contentsweep.ai/imports/integrate and /imports/capabilities.json.
