# Review recurring supplier CSV imports

The owner-approved November 8 workflow for existing n8n entry **20893** is [recurring-import-reviewed.n8n.json](https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/recurring-import-reviewed.n8n.json). The candidate filename is an identical copy. Owner approval and publication of these examples do not establish acceptance into n8n’s template library.

This manual workflow checks each CSV against an approved ContentSweep profile, stops changed structures or rejected files, verifies accepted JSONL against its receipt, and displays every inventory field locally. It includes correction and uncertain-request recovery. It does not approve mappings or write to a destination.

## Requirements

- Tested on **self-hosted n8n 2.42.5**, using built-in nodes. No community nodes, sub-workflows, local input files or pinned execution data are needed. Cloud compatibility has not been qualified.
- Permit the built-in `crypto` module with `NODE_FUNCTION_ALLOW_BUILTIN=crypto` in n8n and its task runner; see [n8n's module instructions](https://docs.n8n.io/hosting/configuration/configuration-examples/modules-in-code-node/).
- An existing verified [Supplier Feeds organization](https://mcp.contentsweep.ai/account/sign-in?product=supplier-feeds), its API key and an approved profile matching your CSV. Use the application or [first-import recipe](https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/approved-import.n8n.json) to review field meanings, identifier types, decimal locale, currency and contract, then approve the exact profile hash. The recurring workflow never performs that approval.

For the synthetic test, [profile.json](https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/profile.json) declares the exact mapping and contract: `product_code` → text `sku`, `product_name` → text `title`, `unit_price` → comma-decimal string `price`, `currency` → EUR `currency`, and `available` → nonnegative integer `stock`; `sku` must be unique. Review these decisions in the application before approving the fixture profile. Other feeds need their own reviewed decisions.

## Connect and configure

Import the workflow while inactive. Create one HTTP Header Auth credential named **ContentSweep X-API-Key**, with header name `X-API-Key` and your private organization key as the value. Select it on Upload, Quote, Start job, Job status, Validation report, Download JSONL, Original rejected job and Accepted receipt. Never paste the key into Config or public JSON.

All operator values are in **Config**:

| Value | What to set |
| --- | --- |
| `baseUrl` | Keep `https://mcp.contentsweep.ai` for the hosted service. |
| `feedCsv` | Begin with the included synthetic CSV; later replace it with an authorized compatible UTF-8 CSV. |
| `profileId` | The owned approved profile ID for those source columns and meanings. |
| `idempotencyKey` | A fresh stable key for a new evaluation; retain the exact original key for recovery. |
| `approvedByOperator` | Defaults to false. Set true only after reviewing this file, profile and one evaluation's cost. |
| `pollLimit` | Integer from 1 to 25 retry cycles after the first status read; default 25. Each retry waits five seconds. |
| `correctionReplay` | Leave false for a new delivery or recovery; true only for a corrected rejection. |
| `originalJobId` | Empty normally; the completed rejected job ID for correction replay. |
| `resumeQuoteId` | Empty normally; the original quote ID for recovery. |
| `resumeInputHash` | Empty normally; the original quote's `input_hash` for recovery. |

## Test the normal path

1. Follow the setup above using the included synthetic data and a matching approved profile. Review spending, set `approvedByOperator=true` and run manually.
2. Inspect **Verified inventory preview**. Expect two rows with `sku`, `title`, `price`, `currency` and `stock`; the first SKU is string `"000123"` and price is string `"19.90"`. `verifiedArtifactHash` must equal the accepted receipt's `output_hash`. Download JSONL also exposes the `normalizedFeed` binary.
3. With a fresh key, clear `feedCsv`: configuration must stop before HTTP requests. Restore it, change header `available` to `availability`, and use a fresh key: the quote must stop for review without a preview.
4. Preserve the original quote ID, input hash, exact bytes, retry key and job ID privately before any retry. Review the error node and report; an execution status alone is insufficient evidence of a correct result.

## Correct or recover

| Situation | Action |
| --- | --- |
| Compatible later delivery | Replace `feedCsv`; keep the reviewed profile; use a fresh key. |
| Changed columns or meanings | Stop and review a new profile before evaluating. |
| Completed rejection | Inspect the report; accepted output is unavailable. A rejection uses one evaluation. |
| Genuinely corrected rejection | Set `correctionReplay=true`, the rejected `originalJobId`, changed bytes and a fresh key. Identical bytes stop. |
| Uncertain dispatch or polling deadline | Leave `correctionReplay=false`. Set `resumeQuoteId` and `resumeInputHash`; retain the exact original bytes and key. This skips upload and quotation and returns the existing job without another evaluation. |

Correction and recovery cannot be enabled together. A deadline does not prove failure. Do not change the key to resolve uncertainty. Expired or mismatched authorization requires review. Once a case is resolved, clear the correction/recovery fields before configuring a new delivery.

HTTP requests stop on service errors and time out after 30 seconds. Failed jobs, rejected reports and exhausted polling reach review; a changed output hash fails verification before the preview returns. There is no automatic destination write or automatic recovery from these errors.

## Cost, bounds and retention

Five trial evaluations are available once per verified organization. Afterward, separately funded access costs $20 for ten evaluations or optional $99/month for 100, expiring at period end. Completed rejections consume one evaluation. Previews, unsupported inputs, platform failures and exact retries consume no additional evaluation. There are no automatic overages or replenishment by this workflow.

The template accepts flat UTF-8 CSV. Service bounds are 10 MiB, 50,000 records and 100 fields; XLSX and nested records are unsupported. Uploads expire after 24 hours, results after seven days and receipts after 30 days. Approved profiles remain until deletion. Set n8n's own execution-data retention for supplier files. Validation checks declared rules, not the real-world accuracy of the source.

The example is owned synthetic data. The output remains local; configure any real destination separately. [Integration details](https://mcp.contentsweep.ai/imports/integrate) · [Privacy](https://mcp.contentsweep.ai/imports/privacy).

For this version’s checksum, imported test results and screenshots, see [the review record](https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/N8N_REVIEW.md). The current provider state is recorded in [n8n-submission-status.json](https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/n8n-submission-status.json); submission and acceptance are separate events.
