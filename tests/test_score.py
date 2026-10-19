"""The scorer's arithmetic, with a scripted judge: no model is called."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import score  # noqa: E402

PY = sys.executable


def scripted(answer: dict, tmp: Path) -> str:
    """A judge command that ignores its prompt and prints one canned answer."""
    path = tmp / f"answer-{len(list(tmp.glob('answer-*.json')))}.json"
    path.write_text(json.dumps(answer))
    return f"cat {path}"


def design_case(tmp: Path) -> Path:
    cases = tmp / "cases" / "design"
    (cases / "demo").mkdir(parents=True)
    (cases / "demo" / "meta.json").write_text(json.dumps({"id": "demo", "tier": "demo", "system": "A web shop with a payments API."}))
    (cases / "demo" / "expected.json").write_text(json.dumps(["A caller replays a payment request", "An admin token leaks through logs"]))
    return cases


def test_design_recall_counts_a_partial_match_as_half_and_precision_over_the_tools_threats(tmp_path):
    cases = design_case(tmp_path)
    review = {"threats": [{"id": "a", "title": "Replayed payment", "statement": "No idempotency key on POST /pay."},
                          {"id": "b", "title": "Something generic", "statement": "Attackers attack."}]}
    judge = scripted({"expected": [{"n": 1, "verdict": "covered", "by": "a"}, {"n": 2, "verdict": "partly", "by": ""}],
                      "found": [{"id": "a", "label": "matches"}, {"id": "b", "label": "noise"}], "because": "ok"}, tmp_path)
    row = score.score_design("demo", review, judge=judge, out=tmp_path / "results", cases=cases)
    assert row["covered"] == 1 and row["partly"] == 1 and row["recall"] == 0.75
    assert row["matches"] == 1 and row["noise"] == 1 and row["precision"] == 0.5
    assert row["missed"] == [] and row["verdicts_given"] == 2 and not row["salvaged"]
    # the answer is cached by its prompt: a second scoring does not run the judge again
    assert any((tmp_path / "results" / "cache").iterdir())


def test_a_review_without_threats_scores_zero_without_asking_the_judge(tmp_path):
    cases = design_case(tmp_path)
    row = score.score_design("demo", {"threats": []}, judge="false", out=tmp_path / "results", cases=cases)
    assert row["recall"] == 0.0 and row["precision"] is None and "no threats" in row["because"]


def test_an_unreadable_answer_is_unjudged_not_a_score(tmp_path):
    cases = design_case(tmp_path)
    judge = f"{PY} -c \"import sys; sys.stdin.read(); print('I cannot say.')\""
    row = score.score_design("demo", {"threats": [{"id": "a", "title": "x", "statement": "y"}]}, judge=judge, out=tmp_path / "results", cases=cases)
    assert row.get("verdict") == "unjudged" and "recall" not in row


def test_advisories_locate_on_band_four_and_near_on_three(tmp_path):
    cases = tmp_path / "cases" / "advisories"
    cases.mkdir(parents=True)
    (cases / "targets.json").write_text(json.dumps([{"repo": "o/r", "tag": "v1", "why": "a server"}]))
    (cases / "o__r.json").write_text(json.dumps({"repo": "o/r", "advisories": [
        {"ghsa": "GHSA-1", "cve": None, "cwes": ["CWE-287"], "summary": "Auth bypass", "description": "A missing check."},
        {"ghsa": "GHSA-2", "cve": None, "cwes": [], "summary": "DoS", "description": "A slow loop."}]}))
    review = {"threats": [{"id": "t1", "title": "Missing auth check", "statement": "On /admin."}], "findings": []}
    judge = scripted({"band": 4, "because": "[t1] same mechanism"}, tmp_path)
    row = score.score_advisories("o/r", review, judge=judge, out=tmp_path / "results", cases=cases)
    assert row["advisories"] == 2 and row["located"] == 2 and row["near"] == 0 and row["items"] == 1
    judge3 = scripted({"band": 3, "because": "[t1] related"}, tmp_path)
    row = score.score_advisories("o/r", review, judge=judge3, out=tmp_path / "results-3", cases=cases)
    assert row["near"] == 2 and row["located"] == 0


def test_report_means_recall_per_tier(tmp_path):
    (tmp_path / "design").mkdir()
    for i, (tier, recall, precision) in enumerate([("cncf", 0.5, 0.8), ("cncf", 1.0, None), ("tml", 0.25, 0.4)]):
        (tmp_path / "design" / f"c{i}.json").write_text(json.dumps({"case": f"c{i}", "tier": tier, "recall": recall, "precision": precision,
                                                                   "expected": 4, "covered": 1, "partly": 2}))
    (tmp_path / "design" / "c9.json").write_text(json.dumps({"case": "c9", "tier": "tml", "verdict": "unjudged"}))
    got = score.report(tmp_path)
    assert got["design"]["all"]["cases"] == 3 and got["design"]["all"]["recall"] == 0.583 and got["design"]["all"]["precision"] == 0.6
    assert got["design"]["cncf"]["recall"] == 0.75 and got["design"]["unjudged"] == 1
