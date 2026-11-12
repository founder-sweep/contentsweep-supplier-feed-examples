# Supplier Feeds: coding-agent setup

Reuse approved supplier mappings, validate complete flat files and stop structural drift.

## Runtime and credentials

Create or reuse a verified organization at https://mcp.contentsweep.ai/imports, activate this product, and supply its private organization key as `CONTENTSWEEP_SUPPLIER_FEEDS_API_KEY`. Initialization and tool listing require the key. Review upload permission, the quote and the evaluation cost before starting a hosted job. Use the original quote and idempotency key after an uncertain response.

## Gemini CLI

Install the extension from this repository:

```sh
gemini extensions install https://github.com/founder-sweep/contentsweep-supplier-feed-examples --ref main
```

The explicit branch selects the integration source rather than an older Python runtime release archive. Provide the requested setting in the native installation prompt. API keys are sensitive settings. The extension supplies the existing skill and default MCP connection; it does not approve tool calls or spending. For a project-managed connection, merge the Gemini example from `client-configs/gemini.json` into the intended profile.

## Kilo

Use the published marketplace entry when available, or merge `client-configs/kilo.json` into your private user-level Kilo CLI configuration and install the existing skill. Alternatively set `KILO_CONFIG` to the absolute path of an explicitly trusted private configuration file. Kilo CLI rejects environment substitutions in untrusted project configuration and drops MCP entries with variable-bearing project headers; keep the supplied environment-based credentials in user-level configuration. The editor marketplace installs its prompted values into private MCP settings. The catalog entry includes a companion skill; companion installation requires a client version supporting that feature. Review prerequisites before installation.

## Cline

Ask Cline to follow this README and `llms-install.md`. Merge the entry in `client-configs/cline.json` into the editor extension's MCP settings and provide the named setting privately. Cline editor 4.1.26 supports `${env:NAME}` interpolation. Make those variables available in the client launch environment, or fill the actual values directly in the client's private MCP settings. Restart the client after changing its launch environment. The hosted editor example selects `streamableHttp` explicitly. Keep tool approvals enabled.

Cline CLI 3.0.74 stores its connection under a `transport` object. Use its native command to write that schema instead of copying the editor JSON into a CLI profile. With the required private setting(s) available in the launch environment:

```bash
cline mcp add contentsweep-supplier-feeds --yes --transport streamable-http --header "X-API-Key: ${CONTENTSWEEP_SUPPLIER_FEEDS_API_KEY}" "https://mcp.contentsweep.ai/v1/feeds/mcp/"
```

For an isolated CLI profile, retain its `--config`, `--data-dir` and `--hooks-dir` options on configuration commands. Start a fresh Cline CLI task after adding the server so the model discovers its new tools. Copy the existing skill directory with every relative resource into the project's `.cline/skills/` directory; manual file copying does not require a second skill-install command. Verify an actual MCP result after setup.

## Cursor

Install the Cursor plugin from the marketplace or load this repository as a local plugin for development. Configure its declared variable in the plugin settings. The root `mcp.json` is the native plugin connection definition; the copy in `client-configs/cursor.json` is for a manually managed connection. For the manual copy, use Cursor's documented environment interpolation in place of the plugin variable. Preserve unrelated entries. With Cursor CLI, place local environments at absolute paths without spaces: the current CLI splits a no-argument stdio command containing spaces. A locally created executable symlink at a path without spaces is also suitable; it must point to the verified installed product executable. In native Cursor 3.29.15, Inspector's project-scoped Configure action returned "Plugin not installed". The tested recovery was to select Add for Myself, remove the failed project scope, save the declared variables in the private plugin configuration, and use the MCP server's Reload action. Verify Connected and the expected tools before running a task. This recovery does not require a second manually configured connection.

## Skill and first task

Read [supplier-feed-import](skills/contentsweep-supplier-feeds/SKILL.md) and its relative references. Use the repository-owned synthetic example first and inspect the substantive result, not just execution success. Fixture approval never authorizes customer uploads, business meanings, purchases or downstream writes.

## Price and supported scope

Five trials per verified organization; $20/10 evaluations or $99/month/100. Completed rejections consume an evaluation; exact retries do not.

Flat CSV/JSONL, approved mappings, 10 MiB, 50,000 records, 100 fields. No automatic destination writes.

## Preserve complete file bytes

When uploading an on-disk CSV or JSONL file, preserve every byte, including the final newline. A model copying text into a tool argument can omit that newline or copy editor line numbers. Compare the returned upload SHA256 with the actual source file before quoting or starting work. Stop on a mismatch; do not approve an evaluation of a reconstructed variant.

If the client cannot supply the exact content through the MCP upload tool, its reviewed shell/file-transfer tool can use the existing binary HTTPS upload endpoint. Keep the key in the client's private launch environment, and send the complete file directly with `--data-binary`, without asking the model to print or retype the key or dataset. For an explicitly authorized owned CSV:

```bash
INPUT_FILE="/absolute/path/to/owned.csv"
curl --fail-with-body --silent --show-error --request POST "https://uploads?format=csv" \
  --header "Content-Type: application/octet-stream" \
  --header "X-API-Key: ${CONTENTSWEEP_SUPPLIER_FEEDS_API_KEY}" \
  --data-binary "@${INPUT_FILE}"
```

Use `format=jsonl` for JSONL. Check the source SHA256 with the operating system's hash tool, then use the returned upload ID with the native MCP profile/contract review, quote, start, report and retry tools. The upload itself does not start an evaluation. For Quality, an authorized checked-original download must also match the original file bytes; report JSON is never a replacement for that file.

## Recovery and removal

Keep private keys out of source control and command history. Remove only this product's plugin/server/owned companion skill. Keep unrelated tools and settings. Kilo 7.8.27's native skill Remove action deletes `SKILL.md` and leaves companion files. After native removal, preview cleanup of this exact skill directory using the supplied ownership manifest:

```bash
python scripts/remove-owned-agent-skill.py --skill-dir "/absolute/path/to/.kilo/skills/supplier-feed-import"
```

Review the matching paths, then repeat with `--apply` to remove only unchanged owned companion files. The helper refuses an active skill entry or a symlinked skill directory, and preserves modified files, unknown files and other skills. It does not edit client configuration. When names conflict, inspect the client's selected source path before installing or removing a skill. Client installation, marketplace acceptance, recommendations and paid adoption are separate outcomes.
