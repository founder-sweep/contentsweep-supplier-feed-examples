# ContentSweep supplier-feed examples

<!-- agent-current-status:start -->
## Current status — November 8, 2026

Hosted engine feeds-1.0; MCP server reports 1.1.0 and the existing active Registry descriptor is 1.1.1. These version labels describe different artifacts. Five trials once per verified organization; $20/10 evaluations or $99/month for 100. Existing organization key required. The owner approved the corrected n8n workflow and documentation on November 8. Download [the reviewed workflow](recurring-import-reviewed.n8n.json) and follow [the setup guide](RECURRING_IMPORT_GUIDE.md). See [the submission record](N8N_SUBMISSION.md) for existing entry 20893; owner approval does not establish n8n acceptance.

[Agent setup](https://mcp.contentsweep.ai/imports/integrate) · [Product skill](https://mcp.contentsweep.ai/imports/SKILL.md) · [Task-to-tool reference](https://mcp.contentsweep.ai/imports/agent-assets/TOOL_REFERENCE.md). Skills support Codex and Claude Code and grant no upload, business-meaning approval, spending or destination-write permission. Historical test notes below retain their original scope; synthetic/internal qualification is not paid adoption.
<!-- agent-current-status:end -->

Turn recurring supplier CSV/JSONL into an approved destination schema, validate the complete file, and stop for review when its source structure changes.

[Offer and synthetic demo](https://mcp.contentsweep.ai/imports) · [Integration guide](https://mcp.contentsweep.ai/imports/integrate) · [Request a pilot](https://mcp.contentsweep.ai/imports/pilot?source=github-examples)

Historical recipe evidence records n8n 2.42.5 and an HTTPS first-import proof. Current recurring-template testing and screenshots are in the [review record](N8N_REVIEW.md). Keep existing entry 20893 rather than creating another submission.

- `approved-import.n8n.json`: supplier feed → explicit mapping approval → validated JSONL.
- `drift-review.n8n.json`: saved profile → changed source → review notification.
- `correction-replay.n8n.json`: original rejection → corrected feed → re-evaluation.

Import an inactive workflow, set its Config values, and select an HTTP Header Auth credential named ContentSweep X-API-Key with header X-API-Key. Review field meanings, EUR currency, comma decimals, and contract rules before setting approvedByOperator=true. Use a fresh idempotency key per evaluation; retry the same request with its ORIGINAL quote and key. For recurring/corrected feeds, supply the saved profile ID. Correction replay also needs the original rejected job ID. Drift notification requires your SMTP credential and verified sender.

## Reference HTTP client

Set CONTENTSWEEP_API_KEY in your environment. Run:

```bash
python client.py --base-url https://mcp.contentsweep.ai
# After reviewing mapping and spending decisions:
python client.py --base-url https://mcp.contentsweep.ai --approve-mapping --approve-evaluation
```

The first command uploads the repository-owned fixture and prints the proposal. Evaluation requires an existing provisioned account and explicit flags. A completed rejection report uses one evaluation; previews and platform failures do not. Use the existing verified product account and live funding portal; purchases need separate authorization.

The approved fixture preserves SKU 000123 as a string and price 19.90 as an exact decimal string. normalized-example.jsonl is regenerated and checked before publication. These examples demonstrate supported behavior; they establish no comparative superiority or customer ROI.

Supported service bounds: flat UTF-8 CSV/JSONL, 10 MiB, 50,000 records. Raw uploads expire in 24 hours; results in seven days; job receipts in 30 days. Saved approved profiles remain until deletion. Use existing account authorization; never put real keys or customer files into examples.

MCP endpoint: https://mcp.contentsweep.ai/v1/feeds/mcp/ (Streamable HTTP). Authentication is an existing organization key via X-API-Key. OpenAPI, llms.txt, capabilities and emerging discovery metadata are available on the service domain.

The service is [published in the official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers/ai.contentsweep%2Fsupplier-feeds/versions/latest). Registry inclusion makes the descriptor available to clients that use that registry; configuring a client and obtaining account access are separate steps.

## Release publication

The Publish verified MCP release action runs on feeds-v* tags and manual dispatch. The tag must match the reviewed version in server.json. It checks inactive example workflows, fixture output, deployed readiness and capability bounds, and the official descriptor schema. The official publisher is pinned to v1.8.1 with its SHA256 checksum. A domain-scoped Ed25519 secret is held in the contentsweep-distribution GitHub environment. Publication is read back from the registry; rerunning an identical version verifies it without another mutation, and conflicting immutable versions fail. Version updates still require a reviewed release; this action does not deploy the service.

For existing Creator Hub entry 20893, use [the submission record](N8N_SUBMISSION.md) and the exact reviewed workflow. Other templates remain on hold until this entry is approved.

Example assets are published under Apache-2.0. The hosted service is operated separately. No customer files, contacts, keys, or private marketing records are included.

## Recurring imports and recovery

Follow the [worked example](https://mcp.contentsweep.ai/imports/workflows) or the
[repository walkthrough](RECURRING_IMPORT_GUIDE.md) for approved-profile reuse,
structural drift, rejection, genuinely corrected replay and uncertain-request
recovery. Download [the reviewed recurring workflow](recurring-import-reviewed.n8n.json).
It checks the complete output hash and presents a local inventory preview without
a storefront write or external email. Five trials; $20/10 evaluations or optional
$99/month/100, with no automatic overages. Completed rejections use one evaluation.

These are owned synthetic examples. The current workflow replaces the October version after owner approval. Its checksum and nineteen imported n8n test results are recorded in [N8N_REVIEW.md](N8N_REVIEW.md). The provider’s current state is recorded separately in [n8n-submission-status.json](n8n-submission-status.json); no acceptance or customer adoption is implied.
