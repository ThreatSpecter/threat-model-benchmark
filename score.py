#!/usr/bin/env python3
"""Score a threat-modelling tool's output against the reference cases in this repository.

    python score.py design <case> --review REVIEW.json [--judge CMD] [--out results]
    python score.py advisories <target> --review REVIEW.json [--judge CMD] [--out results]
    python score.py report [results]

REVIEW.json is what the tool produced, in one small shape (see README.md):
    {"threats": [{"id": "t1", "title": "...", "statement": "..."}, ...],
     "findings": [{"id": "f1", "title": "...", "statement": "..."}, ...]}      # findings are optional

A judge model reads the reference and the tool's list and answers in JSON (prompts/judge.*.md). The judge must not
be the model that wrote the review. By default the judge is the Claude CLI: `claude -p --model opus`; give --judge any
command that reads the prompt on stdin and prints the model's answer (the system prompt is prepended to stdin for a
custom command). Answers are cached under <out>/cache by their content, so re-scoring is free.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases"
PROMPTS = HERE / "prompts"
DEFAULT_JUDGE = "claude -p --model opus"
LOCATED, NEAR = 4, 3   # advisory bands: 4 or 5 located, 3 near, below that missed


# ----------------------------------------------------------------------------------------------- the judge
def prompt(name: str, **fields: str) -> str:
    return Template((PROMPTS / f"{name}.md").read_text()).substitute(**fields)


def ask(judge: str, system: str, text: str, cache: Path) -> str:
    """One answer from the judge, cached by the exact prompt. A failed command raises; a judge that answers nothing
    usable is reported as 'unjudged' by the caller, never as a score."""
    key = hashlib.sha256(f"{judge}\n{system}\n{text}".encode()).hexdigest()
    hit = cache / f"{key}.txt"
    if hit.exists():
        return hit.read_text()
    if judge == DEFAULT_JUDGE:
        cmd, stdin = [*judge.split(), "--system-prompt", system], text
    else:
        cmd, stdin = judge, f"{system}\n\n{text}"
    got = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=900, shell=isinstance(cmd, str))
    if got.returncode != 0:
        raise RuntimeError(f"judge failed ({got.returncode}): {got.stderr[:400]}")
    cache.mkdir(parents=True, exist_ok=True)
    hit.write_text(got.stdout)
    return got.stdout


def parse_json(text: str):
    """The JSON object in an answer, whatever surrounds it; None when there is none."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.M)
    for start, end in ((text.find("{"), text.rfind("}")), (text.find("["), text.rfind("]"))):
        if 0 <= start < end:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    # salvage the verdict objects from an answer with a broken sentence in it
    objs = []
    for m in re.finditer(r"\{[^{}]*\}", text):
        try:
            objs.append(json.loads(m.group(0)))
        except json.JSONDecodeError:
            pass
    return objs or None


# ----------------------------------------------------------------------------------------------- the review
def load_review(path: Path) -> dict:
    r = json.loads(path.read_text())
    for kind in ("threats", "findings"):
        for i, item in enumerate(r.get(kind) or [], 1):
            item.setdefault("id", f"{kind[0]}{i}")
            item.setdefault("title", "")
            item.setdefault("statement", "")
    return r


def found_lines(items: list[dict], kind: str = "") -> str:
    tag = f"{kind}: " if kind else ""
    return "\n".join(f"[{i['id']}] {tag}{i['title']}. {i['statement'][:400]}".strip() for i in items)


# ----------------------------------------------------------------------------------------------- design
def score_design(case: str, review: dict, *, judge: str, out: Path, cases: Path = CASES / "design") -> dict:
    """Recall over the experts' threats (a partial match counts half) and precision over the tool's threats."""
    meta = json.loads((cases / case / "meta.json").read_text())
    expected = json.loads((cases / case / "expected.json").read_text())
    ours = review.get("threats") or []
    row = {"set": "design", "case": case, "tier": meta.get("tier", ""), "expected": len(expected), "threats": len(ours)}
    if not ours:
        return row | {"covered": 0, "partly": 0, "recall": 0.0, "precision": None, "because": "the review wrote no threats"}
    text = prompt("judge.design", system=meta.get("system", ""),
                  wanted="\n".join(f"{i + 1}. {e[:500]}" for i, e in enumerate(expected)), found=found_lines(ours))
    said = parse_json(ask(judge, (PROMPTS / "judge.design.system.md").read_text(), text, out / "cache"))
    if isinstance(said, list):   # salvaged objects: items with n are verdicts, items with label are labels
        said = {"expected": [x for x in said if isinstance(x, dict) and "n" in x],
                "found": [x for x in said if isinstance(x, dict) and "label" in x], "because": "", "salvaged": True}
    if not isinstance(said, dict) or not isinstance(said.get("expected"), list):
        return row | {"verdict": "unjudged"}
    verdicts = {int(x.get("n", 0)): x.get("verdict") for x in said["expected"] if isinstance(x, dict) and str(x.get("n", "")).isdigit()}
    labels = [x.get("label") for x in said.get("found") or [] if isinstance(x, dict)]
    covered = sum(1 for n in range(1, len(expected) + 1) if verdicts.get(n) == "covered")
    partly = sum(1 for n in range(1, len(expected) + 1) if verdicts.get(n) == "partly")
    return row | {
        "covered": covered, "partly": partly, "recall": round((covered + 0.5 * partly) / max(1, len(expected)), 3),
        "matches": labels.count("matches"), "valid": labels.count("valid"), "noise": labels.count("noise"),
        "precision": round((labels.count("matches") + labels.count("valid")) / max(1, len(labels)), 3) if labels else None,
        "verdicts_given": len(set(verdicts) & set(range(1, len(expected) + 1))), "salvaged": bool(said.get("salvaged")),
        "because": str(said.get("because", ""))[:500],
        "missed": [expected[n - 1][:160] for n in range(1, len(expected) + 1) if verdicts.get(n) not in ("covered", "partly")],
    }


# ----------------------------------------------------------------------------------------------- advisories
def score_advisories(target: str, review: dict, *, judge: str, out: Path, cases: Path = CASES / "advisories") -> dict:
    """For each advisory published after the reviewed release: did the review point at it? Band 4–5 located, 3 near."""
    data = json.loads((cases / f"{target.replace('/', '__')}.json").read_text())
    targets = {t["repo"]: t for t in json.loads((cases / "targets.json").read_text())}
    system = f"{target} at {targets.get(target, {}).get('tag', '')}: {targets.get(target, {}).get('why', '')}"
    found = "\n".join(filter(None, [found_lines(review.get("threats") or [], "threat"), found_lines(review.get("findings") or [], "finding")]))
    rows = []
    for a in data["advisories"]:
        wanted = f"{a['summary']} ({', '.join(a.get('cwes') or []) or 'no CWE'})\n{a.get('description', '')[:2500]}"
        band = None
        if found:
            said = parse_json(ask(judge, (PROMPTS / "judge.system.md").read_text(), prompt("judge.advisory", system=system, wanted=wanted, found=found), out / "cache"))
            try:
                band = int(said["band"]) if isinstance(said, dict) else None
            except (KeyError, TypeError, ValueError):
                band = None
            if band is not None and not 1 <= band <= 5:
                band = None
        verdict = "unjudged" if band is None and found else "missed" if band is None else "located" if band >= LOCATED else "near" if band >= NEAR else "missed"
        rows.append({"ghsa": a.get("ghsa"), "cve": a.get("cve"), "summary": a.get("summary", "")[:160], "band": band, "verdict": verdict,
                     "because": str(said.get("because", ""))[:300] if found and isinstance(said, dict) else ""})
    count = lambda v: sum(1 for r in rows if r["verdict"] == v)
    return {"set": "advisories", "case": target, "advisories": len(rows), "items": len(review.get("threats") or []) + len(review.get("findings") or []),
            **{v: count(v) for v in ("located", "near", "missed", "unjudged")}, "rows": rows}


# ----------------------------------------------------------------------------------------------- report
def report(results: Path) -> dict:
    out: dict = {}
    design = [json.loads(p.read_text()) for p in sorted((results / "design").glob("*.json"))] if (results / "design").exists() else []
    judged = [r for r in design if "recall" in r]
    by_tier: dict[str, list] = {}
    for r in judged:
        by_tier.setdefault(r.get("tier", ""), []).append(r)
    def summary(rs: list) -> dict:
        p = [r["precision"] for r in rs if r.get("precision") is not None]
        return {"cases": len(rs), "recall": round(statistics.mean(r["recall"] for r in rs), 3) if rs else None,
                "precision": round(statistics.mean(p), 3) if p else None,
                "expected": sum(r["expected"] for r in rs), "covered": sum(r["covered"] for r in rs), "partly": sum(r["partly"] for r in rs)}
    if design:
        out["design"] = {"all": summary(judged), "unjudged": len(design) - len(judged), **{t: summary(rs) for t, rs in sorted(by_tier.items())}}
    adv = [json.loads(p.read_text()) for p in sorted((results / "advisories").glob("*.json"))] if (results / "advisories").exists() else []
    if adv:
        out["advisories"] = {a["case"]: {k: a[k] for k in ("advisories", "located", "near", "missed", "unjudged")} for a in adv}
    return out


# ----------------------------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("design", "advisories"):
        s = sub.add_parser(name)
        s.add_argument("case", help="a case id under cases/design, or a target such as openfga/openfga")
        s.add_argument("--review", required=True, type=Path)
        s.add_argument("--judge", default=DEFAULT_JUDGE)
        s.add_argument("--out", default=Path("results"), type=Path)
    r = sub.add_parser("report")
    r.add_argument("results", nargs="?", default=Path("results"), type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "report":
        print(json.dumps(report(a.results), indent=1))
        return 0
    review = load_review(a.review)
    row = (score_design if a.cmd == "design" else score_advisories)(a.case, review, judge=a.judge, out=a.out)
    where = a.out / a.cmd / f"{a.case.replace('/', '__')}.json"
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(json.dumps(row, indent=1))
    if a.cmd == "design":
        print(f"{a.case}: recall {row.get('recall')} (covered {row.get('covered')}, partly {row.get('partly')} of {row['expected']}) · "
              f"precision {row.get('precision')} over {row['threats']} threats · {row.get('verdict', '')}".strip(" ·"))
    else:
        print(f"{a.case}: located {row['located']} · near {row['near']} · missed {row['missed']} · unjudged {row['unjudged']} of {row['advisories']} advisories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
