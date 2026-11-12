# Supplier Feeds: coding-agent setup

Reuse approved supplier mappings, validate complete flat files and stop structural drift.

## Runtime and credentials

Create or reuse a verified organization at https://mcp.contentsweep.ai/imports, activate this product, and supply its private organization key as `CONTENTSWEEP_SUPPLIER_FEEDS_API_KEY`. Initialization and tool listing require the key. Review upload permission, the quote and the evaluation cost before starting a hosted job. Use the original quote and idempotency key after an uncertain response.

## Gemini CLI

Install the extension from this repository:

```sh
gemini extensions install https://github.com/founder-sweep/contentsweep-supplier-feed-examples
```

Provide the requested setting in the native installation prompt. API keys are sensitive settings. The extension supplies the existing skill and default MCP connection; it does not approve tool calls or spending. For a project-managed connection, merge the Gemini example from `client-configs/gemini.json` into the intended profile.

## Kilo

Use the published marketplace entry when available, or merge `client-configs/kilo.json` into the intended project configuration and install the existing skill. The catalog entry includes a companion skill; companion installation requires a client version supporting that feature. Review prerequisites before installation.

## Cline

Ask Cline to follow this README and `llms-install.md`. Merge the entry in `client-configs/cline.json` into its MCP settings and provide the named setting privately. The hosted example selects `streamableHttp` explicitly. Keep tool approvals enabled.

## Cursor

Install the Cursor plugin from the marketplace or load this repository as a local plugin for development. Configure its declared variable in the plugin settings. The root `mcp.json` is the native plugin connection definition; the copy in `client-configs/cursor.json` is for a manually managed connection. For the manual copy, use Cursor's documented environment interpolation in place of the plugin variable. Preserve unrelated entries.

## Skill and first task

Read [supplier-feed-import](skills/contentsweep-supplier-feeds/SKILL.md) and its relative references. Use the repository-owned synthetic example first and inspect the substantive result, not just execution success. Fixture approval never authorizes customer uploads, business meanings, purchases or downstream writes.

## Price and supported scope

Five trials per verified organization; $20/10 evaluations or $99/month/100. Completed rejections consume an evaluation; exact retries do not.

Flat CSV/JSONL, approved mappings, 10 MiB, 50,000 records, 100 fields. No automatic destination writes.

## Recovery and removal

Keep private keys out of source control and command history. Remove only this product's plugin/server/owned companion skill. Keep unrelated tools and settings. Client installation, marketplace acceptance, recommendations and paid adoption are separate outcomes.
