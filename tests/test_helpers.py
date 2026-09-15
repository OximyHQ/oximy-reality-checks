from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "oximy-reality-checks" / "skills"


def run(skill: str, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SKILLS / skill / "scripts" / script), *args],
        capture_output=True,
        text=True,
    )


class HelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, value: str) -> Path:
        path = self.root / name
        path.write_text(value)
        return path

    def payload(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return json.loads(result.stdout)

    def test_safe_to_paste_tokenizes_consistently_without_overwrite(self) -> None:
        source = self.write("source.txt", "Mail a@example.com then a@example.com. Host 10.0.0.4")
        output = self.root / "clean.txt"
        data = self.payload(run("safe-to-paste", "redact_text.py", str(source), "--output", str(output)))
        self.assertEqual(data["finding_count"], 3)
        self.assertEqual(output.read_text().count("[EMAIL_1]"), 2)
        refused = run("safe-to-paste", "redact_text.py", str(source), "--output", str(source))
        self.assertEqual(refused.returncode, 2)

    def test_did_it_land_rejects_unproved_completion(self) -> None:
        invalid = self.write("outcome.json", json.dumps({
            "task": "deploy", "checked_at": "2026-09-15T00:00:00Z",
            "overall_status": "verified-complete",
            "claims": [{"claim": "live", "required": True, "system_of_record": "production", "verdict": "claimed-only", "evidence_gap": "no readback"}],
        }))
        result = run("did-it-land", "validate_outcome.py", str(invalid))
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires every required claim", result.stdout)

    def test_human_review_tax_compares_text_and_docx(self) -> None:
        before = self.write("before.txt", "One\nTwo\n")
        after = self.write("after.txt", "One\nThree\n")
        data = self.payload(run("human-review-tax", "compare_artifacts.py", str(before), str(after)))
        self.assertLess(data["sequence_similarity"], 1)
        docx = self.root / "sample.docx"
        with ZipFile(docx, "w") as archive:
            archive.writestr("word/document.xml", "<w:document xmlns:w='x'><w:p><w:t>Hello</w:t></w:p></w:document>")
        same = self.payload(run("human-review-tax", "compare_artifacts.py", str(docx), str(docx)))
        self.assertEqual(same["sequence_similarity"], 1)

    def test_where_did_my_data_go_minimizes_paths(self) -> None:
        trace = self.write("trace.jsonl", json.dumps({"timestamp": "2026-09-15", "tool": "fetch", "value": "https://api.example.com/a /private/customer/file.txt"}) + "\n")
        data = self.payload(run("where-did-my-data-go", "trace_inventory.py", str(trace)))
        self.assertEqual(data["endpoint_hosts"][0][0], "api.example.com")
        self.assertNotIn("/private/customer", json.dumps(data["paths"]))

    def test_memory_inventory_requires_narrow_roots_and_excludes_content(self) -> None:
        folder = self.root / "memory"
        folder.mkdir()
        self.write("memory/note.md", "private memory")
        data = self.payload(run("what-does-my-ai-remember", "inventory_memory.py", str(folder)))
        self.assertFalse(data["content_included"])
        self.assertNotIn("private memory", json.dumps(data))
        refused = run("what-does-my-ai-remember", "inventory_memory.py", "/")
        self.assertEqual(refused.returncode, 2)

    def test_right_size_summarizes_observed_tool_use(self) -> None:
        trace = self.write("tools.jsonl", json.dumps({"tool_name": "browser.open", "result": "failed"}) + "\n")
        data = self.payload(run("right-size-my-agent", "summarize_tool_use.py", str(trace)))
        self.assertEqual(data["observed_tools"][0], {"tool": "browser.open", "events": 1, "error_records": 1})

    def test_agent_autopsy_surfaces_retries_and_failures(self) -> None:
        trace = self.write("session.jsonl", "\n".join([
            json.dumps({"tool": "deploy", "result": "error"}),
            json.dumps({"tool": "deploy", "result": "ok"}),
        ]) + "\n")
        data = self.payload(run("agent-autopsy", "session_stats.py", str(trace)))
        self.assertEqual(data["failure_signal_records"], 1)
        self.assertEqual(data["adjacent_repeated_tool_calls"], 1)

    def test_skill_sunset_classifies_activation_confusion(self) -> None:
        csv_file = self.write("activations.csv", "skill,expected,activated,outcome\nfoo,true,false,failed\nfoo,false,true,ok\n")
        data = self.payload(run("skill-sunset", "summarize_activations.py", str(csv_file)))
        self.assertEqual(data["skills"]["foo"]["missed_activation"], 1)
        self.assertEqual(data["skills"]["foo"]["false_activation"], 1)

    def test_bottleneck_shift_reports_phases_and_invalid_rows(self) -> None:
        csv_file = self.write("events.csv", "item_id,cohort,phase,started_at,ended_at\na,before,draft,2026-09-15T10:00:00Z,2026-09-15T10:30:00Z\n")
        data = self.payload(run("bottleneck-shift", "analyze_events.py", str(csv_file)))
        self.assertEqual(data["phase_durations"]["before"]["draft"]["median_minutes"], 30)

    def test_policy_matrix_requires_evidence_for_alignment(self) -> None:
        matrix = self.write("matrix.json", json.dumps([{
            "policy_statement": "No public sharing", "policy_source": "policy#1",
            "evidence_point": "share settings", "status": "aligned", "evidence": "", "gap": "",
        }]))
        result = run("policy-vs-reality", "validate_matrix.py", str(matrix))
        self.assertEqual(result.returncode, 1)
        self.assertIn("aligned without evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()

