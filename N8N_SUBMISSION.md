# First Creator Hub submission

Status: ready for submission; Creator Hub account access is still required. No submission or approval is claimed. Submit this one first; new creators may have one submission under review at a time.

Workflow JSON: `approved-import.n8n.json` (inactive, no API key, credential placeholders only). Category suggestions, if available in the actual form: Data & Storage, Sales, or Ecommerce. Choose the closest supported category in Creator Hub rather than inventing a category.

## Title

Validate supplier CSVs and preserve product IDs with ContentSweep

## Description to paste

Turn a flat supplier catalog into validated JSONL using an explicitly reviewed mapping. This workflow is for automation agencies and catalog operators who need to preserve identifiers and decimal prices when a supplier file arrives in a different format.

The included synthetic CSV demonstrates leading-zero product IDs, comma-decimal EUR prices, and inventory quantities. The workflow uploads the CSV to ContentSweep, requests a sampled preview, creates and approves your configured profile, obtains an evaluation quote, starts one complete-file evaluation, polls for its result, retrieves the validation report, and downloads JSONL only when validation passes. Source incompatibility or a rejected report prevents the output download.

The operator must review field meanings, mapping operations, currency and locale, contract rules, and the evaluation cost before enabling execution. A schema pass validates your approved rules; it does not establish that the supplier's data is factually correct. This recipe uses built-in HTTP Request nodes and a manual trigger, and returns a file rather than updating a storefront.

### What you need

An n8n instance and a provisioned ContentSweep organization API key. Request an agency pilot at https://mcp.contentsweep.ai/imports/pilot?source=n8n-approved-import. Pilot provisioning is manual; approved pilots receive five trial evaluations with no card required. The service is external, and usage beyond a trial requires separately enabled funded access. Live purchasing is not enabled yet; this template does not promise self-serve signup or accept payment.

### Setup

1. Import the workflow JSON into n8n. Keep it inactive while configuring it.
2. Create an HTTP Header Auth credential with header name `X-API-Key` and your organization key as its value. Select that credential on every HTTP Request node. Never place your key in the Config node, workflow JSON, or public examples.
3. In Config, keep `baseUrl` set to `https://mcp.contentsweep.ai`. Start with the included owned fixture in `feedCsv`. For your supplier, replace this with your flat CSV and explicitly configure `targetSchema`, `mapping`, and `contract` for its actual columns and meanings. The sample's currency is EUR and its decimal separator is a comma; use those decisions only when they apply to your source.
4. Set a fresh `idempotencyKey` for each new evaluation. Review the configured decisions and spending permission, then set `approvedByOperator` to `true`. That flag approves the configured mapping and one bounded evaluation; it is not an automatic approval of any new proposal.
5. Run manually. Inspect the Preview and Validation report nodes. After a passing result, download the `normalizedFeed` binary file from Download JSONL. The sample should produce two records and preserve SKU `000123` and price `19.90` as strings.

### Limits and result handling

The hosted service supports flat UTF-8 CSV/JSONL up to 10 MiB and 50,000 records per evaluation. This recipe uses CSV. Unsupported or over-limit inputs fail explicitly. A preview is sampled; the paid evaluation validates the complete bounded input. Quotes expire after ten minutes. A completed evaluation uses one credit even if it rejects a defective feed. Platform failures, previews, and retries of the original job request do not consume paid evaluations.

Polling stops after 60 retries at five-second intervals. A rejection has a report but no accepted output; inspect the report, correct the source or approved rules, and obtain a new quote for a new evaluation. A platform failure or exhausted polling budget requires inspecting Start job and the job status before retrying. To retry a job creation request, reuse its original quote ID and idempotency key; rerunning the entire template creates a fresh quote and is not that retry. For later feeds, save the approved profile ID and adapt the separately supplied recurring-feed recipe.

Raw uploads expire after 24 hours, result files after seven days, and operational receipts after 30 days. Approved profiles remain until deletion. Your n8n instance has its own execution-data retention settings; set them appropriately for supplier files.

### Verified example and resources

The first-import workflow passed in n8n 2.42.5 against the deployed HTTPS API on October 10, 2026, including downloading both records and verifying leading zeros and exact decimal strings. Evidence: https://github.com/founder-sweep/contentsweep-supplier-feed-examples/blob/main/n8n-hosted-verification.json. This is an owned fixture check, not a comparative performance or ROI claim.

Integration guide: https://mcp.contentsweep.ai/imports/integrate. Public examples and Apache-2.0 license: https://github.com/founder-sweep/contentsweep-supplier-feed-examples. Privacy and retention: https://mcp.contentsweep.ai/imports/privacy.

## Submission procedure

Sign into https://creators.n8n.io/ and use its current submission form. Supply the title, description above, and the workflow JSON as the form requests. Set any service/account requirement field accurately: this workflow uses an external API requiring a provisioned key. Review the rendered preview before submitting. Record the resulting template/submission ID, confirmation, and review state; publication is complete only after n8n approves and exposes a public listing.

Do not submit drift-review or correction-replay until this template is approved. Do not claim a verified custom ContentSweep node: this workflow uses built-in nodes.

Guidance checked October 10, 2026: [n8n Creator Hub and sequential submission rules](https://support.n8n.io/article/becoming-an-n8n-template-creator-and-getting-help).
