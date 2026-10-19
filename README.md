# Threat-model benchmark

Reference cases for measuring a threat-modelling tool, and a scorer that judges the tool's output against them with a
model that is not the one under test.

## What is here

| Set | Cases | The question | The reference |
|---|---|---|---|
| `cases/design/` | 124 | From the design alone, does the tool name the threats experts named? | an expert threat list per case |
| `cases/advisories/` | 2 targets, 65 advisories | Reviewing an old release, does the tool point at what was disclosed later? | GitHub advisories published after the release |
| `cases/cybergym/` | 151 task ids | The same question on OSS-Fuzz C/C++ bugs | the CyberGym benchmark (fetch the tasks from it) |

The 124 design cases come from five public sets: 10 CNCF TAG-Security project assessments, 6 OWASP Threat Model
Library models, 3 AWS Threat Composer samples, 5 IETF RFCs (their security considerations), and the 100 ACSE-Eval AWS
architectures (diagram, diagram code and CDK). Each case is a directory:

```
cases/design/<id>/
  meta.json        id, set, a one-line description of the system, the source, how many expert threats
  expected.json    the experts' threats, one string each
  design/          what the tool is given: the documents, diagrams and code of the design, nothing else
```

`cases/design/acse-sample.json` is a fixed sample of 20 ACSE cases for quick runs. The raw corpora the cases were cut
from are under `sources/`, unedited, with their licences and attributions (`NOTICE.md`).

## Scoring a tool

1. Run the tool on a case's `design/` directory and write what it produced as JSON:

   ```json
   {"threats":  [{"id": "t1", "title": "Replayed payment request", "statement": "No idempotency key on POST /pay ..."}],
    "findings": [{"id": "f1", "title": "...", "statement": "..."}]}
   ```
   `threats` is the tool's threat list; `findings` (code-level evidence) is optional and only used for advisories.

2. Score it. The judge is the Claude CLI by default (`claude -p --model opus`); `--judge` takes any command that reads
   the prompt on stdin and prints the model's answer. The judge must not be the model that wrote the review.

   ```bash
   python score.py design cncf-nats --review out/cncf-nats.json
   python score.py advisories openfga/openfga --review out/openfga-v1.8.0.json
   python score.py report results
   ```

   Design: every expert threat is judged covered, partly or missed, and every tool threat matches / valid / noise.
   Recall = (covered + ½ partly) / expected; precision = (matches + valid) / tool threats. Advisories: each advisory
   gets a band 1–5; 4 or 5 is located, 3 near. A judge answer that cannot be read is reported as `unjudged`, never as
   a score. Answers are cached under `results/cache`, so re-scoring is free. Compare runs that used the same judge model.

For advisories, review the repository at the tag in `cases/advisories/targets.json` (the fixed code for every listed
advisory exists in that release) and export both threats and findings.

## Adding a case

Make a directory under `cases/design/` with the three parts above. Keep the expert list as the experts wrote it, with
the specific attack and the part of the system it hits; a list of generic categories cannot be scored. Put the source
and its licence in `NOTICE.md`.

Tests: `python -m pytest tests` (a scripted judge; no model is called).
