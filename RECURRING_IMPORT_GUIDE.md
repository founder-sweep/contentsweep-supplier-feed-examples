# Review recurring supplier imports and recover uncertain requests

Use Supplier Feeds when a recurring flat supplier CSV/JSONL needs an explicitly
reviewed mapping, complete-file validation and structural-drift stops. The
[worked example](https://mcp.contentsweep.ai/imports/workflows) uses owned synthetic
data; it does not establish customer adoption or time savings.

## Connect and review the first import

Verify your organization email at [Supplier Feeds](https://mcp.contentsweep.ai/imports),
activate the product, and create an organization API key. Five trials are available
once per verified organization. Keep the key private in the client's environment
or an n8n HTTP Header Auth credential named `X-API-Key`.

Use [the first-import recipe](approved-import.n8n.json) or the customer workspace
to review the source and destination schema. Review identifier types, field
meanings, units, currency, decimal separator, casts and contract. Approve the exact
profile hash. The sampled preview does not establish complete-file acceptance.

Only after approval and spending authorization, quote and start one full-file
evaluation. A passed job provides validated JSONL, a report and a receipt. Preserve
the quote ID, source input hash, retry key and job ID privately.

## Reuse an approved profile

Download [the reviewed recurring workflow](recurring-import-reviewed.n8n.json).
It is inactive and uses credential placeholders. Set `profileId`, the original
UTF-8 `feedCsv`, and a fresh stable `idempotencyKey`. After reviewing one bounded
evaluation, set `approvedByOperator` to true. Enable n8n's built-in `crypto` module
for SHA256 checks. This workflow never approves a mapping for you.

| Delivery | Required behavior |
| --- | --- |
| Compatible new file | Reuse the owned approved profile; obtain a new quote/key for the new input. |
| Changed columns or structure | Stop at `review_required`; review and approve a new profile version before dispatch. |
| Complete rejected evaluation | Keep the report; stop delivery. One evaluation is consumed, with no accepted output. |
| Corrected rejected input | Set `correctionReplay=true` and the completed rejected `originalJobId`; supply genuinely changed bytes and a new quote/key. Identical bytes stop. |
| Uncertain dispatch or polling deadline | Preserve the original quote ID, input hash, exact bytes and key. Set `resumeQuoteId` and `resumeInputHash`; resume without a fresh upload or quote. |

The polling budget is one to 25 retry cycles after the first status read, with 25
as the default. A deadline does not prove a job failed. Expired or mismatched
authorization needs review; a new key must not be used to resolve uncertainty.

## Verify output before a destination write

The recurring workflow downloads accepted JSONL, compares SHA256 with the receipt,
and presents a local inventory preview. It makes no storefront, database or
external email writes. The supplied example preserves SKU `000123` and price
`19.90` as strings using an explicitly reviewed decimal rule.

For agent/MCP pagination, retrieve every page before delivery; a partial page set
is not the complete output. Unknown states, errors, incomplete output and hash
mismatches stop for review. Real destination writes require separate authorization.

## Limits, billing and retention

- Flat UTF-8 CSV/JSONL only: 10 MiB, 50,000 records, 100 fields. No XLSX,
  nested records, arbitrary code execution or inferred business approval.
- $20 buys ten evaluations; the optional $99/month offer includes 100 evaluations,
  expiring at period end. A completed rejection consumes one evaluation. No
  automatic overages. Previews, unsupported inputs, platform failures and exact
  retries consume no additional evaluation.
- Uploads last 24 hours, results seven days and receipts 30 days. Approved
  profiles remain until deletion. Configure n8n's own execution-data retention.

The exact reviewed recurring workflow SHA256 is:

```text
d620f1ebb5797842c6b73e9ecd69ad77296a2f5fc11d18ea79be5f1b9d230ef7
```

Existing n8n submission **20893** was resubmitted and read back **UNDER REVIEW** on
October 31, 2026. A signed-in Chrome check on November 2 still shows UNDER REVIEW.
This does not establish acceptance. Keep the existing entry; recheck its current
state before any later submission action.

[Agent setup](https://mcp.contentsweep.ai/imports/integrate) ·
[Product skill](https://mcp.contentsweep.ai/imports/SKILL.md) ·
[Capabilities](https://mcp.contentsweep.ai/imports/capabilities.json) ·
[Privacy](https://mcp.contentsweep.ai/imports/privacy)
