# CNCF TAG-Security project assessments

The files under this directory are copied from the CNCF **TAG-Security** repository:

> https://github.com/cncf/tag-security — `community/assessments/projects/`

Documentation in that repository is licensed **CC BY 4.0**; its source code is MIT. These are documents, so CC BY
4.0 applies, and this notice is the attribution it asks for. Nothing here has been edited — the assessments are
verbatim, because an edited reference is not a reference.

## Why these ten, out of fifty

Every project in that repository was measured for one thing: does a human being sit down and **enumerate the
threats**, so there is a list to grade against? Ten do. The other forty discuss security posture in prose, which is
useful reading and useless as ground truth.

The enumeration is written four different ways, and the first survey found only eight projects because it
understood one of them:

| notation | what it looks like | projects |
|---|---|---|
| `numbered` | `Threat-01-S: an outside attacker could…` | external-secrets, karmada, operator-framework, openkruise |
| `bulleted` | a STRIDE heading, then `* Threat : …` | emissary-ingress, nats, cortex, thanos |
| `matrix` | a table of STRIDE rows against component columns, one threat per cell | tikv |
| `structured` | indented records with `attack:`, `component:`, `impact:` keys | openfga |

`tikv` alone carries 59 threats because its matrix names a threat for each STRIDE category against each of eleven
components. The naive counter scored it 0, then 6 — it was counting rows.

## What this corpus is, and what it is not

**It is** ten real systems, described by the people who built them, with diagrams, and with threats a security
reviewer considered and wrote down. That is the triple this floor needs and cannot manufacture.

**It is not** exhaustive, and no judge here may treat it as though it were. These lists are what one review found
on one day. A threat our pipeline reports that is absent from the list is not thereby wrong — it may be a real
threat the reviewers missed, and grading it as a false positive would train the pipeline to be as incomplete as
its reference. Every judge prompt says so explicitly.

**It is also overwhelmingly Go.** Eight of the ten, with one Rust. That is fine for the threat-model tap, which
never sees source. It is not a code-scanning dataset, and choosing it as one would measure our scanner against a
single language and call the result general.
