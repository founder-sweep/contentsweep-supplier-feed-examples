"""Verify the published recurring workflow, documentation and layout evidence."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
release = json.loads((root / "n8n-release.json").read_text())
for name, expected in release["files"].items():
    path = (root / name).resolve()
    assert path.is_relative_to(root), "Unexpected release path"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name + ": release checksum mismatch"
workflow = json.loads((root / "recurring-import-reviewed.n8n.json").read_text())
assert workflow["active"] is False and not workflow.get("pinData")
notes = [n for n in workflow["nodes"] if n["type"].endswith(".stickyNote")]
overview = [n for n in notes if n["parameters"].get("color") == 1]
assert len(overview) == 1 and 100 <= len(overview[0]["parameters"]["content"].split()) <= 300
assert all(heading in overview[0]["parameters"]["content"] for heading in ("### How it works", "### Setup"))
assert all(len(n["parameters"]["content"].split()) < 50 for n in notes if n["parameters"].get("color") == 7)
print("Published recurring workflow, docs and screenshots match the reviewed release.")
