# Recurring supplier workflow: November 8 review

Workflow SHA256: `b0a9b333c8b2cfa514b41a4175524fb15e5f2e5169386263e0baf7ef93dbde78`.

The owner approved this exact workflow on November 8, 2026 after feedback, documentation, simplicity and requirements reviews. It was imported and tested in self-hosted n8n **2.42.5**, using built-in nodes and the crypto module. Cloud compatibility has not been qualified.

All **19 imported scenarios passed**:

- Approval withheld, invalid profile, empty input, invalid polling budget and conflicting correction/recovery modes stop before HTTP requests.
- Accepted input and a compatible next delivery return two verified rows with all five fields, string SKU `000123`, and exact decimal-string prices.
- Structural drift, duplicate-SKU rejection, unchanged correction and changed recovery bytes stop without returning inventory.
- A genuinely corrected rejection completes under a new quote/key.
- Exact retries and recovery after the polling deadline retain the original job ID and consume no additional evaluation.
- Insufficient credit stops before dispatch.
- Injected HTTP 503, failed-job status and corrupted-download cases stop without returning a preview.

The fault cases use an isolated loopback proxy; other cases use the isolated Supplier API/worker/database. These are owned synthetic fixtures, not customer outcomes. No new payment or downstream destination write occurred during qualification.

The imported layout was inspected at full fit and readable zoom: one 247-word yellow overview, six short white/gray section notes and one red review-stop warning. All eight notes fit; labels and notes do not overlap. Re-exporting the import preserved every node and connection, inactive state and empty pin data.

[Full canvas](review/canvas.jpg) · [Readable instructions](review/overview.jpg) · [Configuration](review/configuration.jpg) · [Recovery](review/recovery-and-quote.jpg).

Follow [the setup guide](RECURRING_IMPORT_GUIDE.md) before running the inactive workflow. The [provider status](n8n-submission-status.json) records entry 20893 separately; publication of this example is not n8n acceptance.
