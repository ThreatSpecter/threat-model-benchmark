# OWASP Threat Model Library

Copied from https://github.com/OWASP/www-project-threat-model-library — **MIT licensed**, so this notice is
courtesy rather than obligation. Six threat models in OWASP's own TMBOM schema (`threat-model.schema.json`,
included), unedited.

## Why these are here, and what they are *not* used for

TMBOM maps almost exactly onto our ontology — `components` and `data_stores`, `data_sets`, `data_flows` with a
source, a destination and whether the data is sensitive, `trust_zones`, `trust_boundaries`, `assumptions`,
`threats` carrying CWE and CAPEC identifiers, `controls`, and `risks` that aggregate named threats with a
likelihood and an impact. Across the six: 55 components, 94 data flows, 62 threats, 20 risks.

The obvious thing to do with that is grade extraction against it. **We cannot**, and the reason is worth writing
down: there is no input to extract *from*. The `description` fields run from eight to a hundred words and `scope`
from forty to three hundred. Nobody can derive twelve components and twenty-four data flows from two hundred words,
so a suite built on it would be scoring the pipeline on what it guessed, and the CNCF corpus — thousands of words
of real documentation per system — stays the input-to-output dataset.

## What they *are* used for: calibrating the judges

These models are curated. The repository's recent history is quality-control work on exactly the axis we care
about — *"Fix CAPEC ID/title mismatches"*, *"Fix coverage and traceability gaps in Kata Containers threat model"* —
and it shows in the writing. Kata's twenty-seven threats are CVE-class and specific: a vhost kernel backend
exploit, a virtiofsd seccomp bypass, ACPI-driven VM escape. Five of them roll into one *VM Escape* risk with a
written impact.

Set that beside `tikv` in the CNCF corpus, whose cells read *"If audit trails are poor, malicious activities may go
unrecorded, denying wrongdoing"* — the definition of repudiation, true of anything with logs.

So the two corpora together are an anchor pair. A relevance judge that cannot rate Kata above TiKV is not a judge,
whatever else it scores. That is what these six are for.

## The honest limit of that anchor

**These are not human labels.** The expectation that Kata rates high and TiKV rates low comes from OWASP's curation
and from reading the text, not from a person sitting down and assigning bands. `Judge.trusted` stays False and
every score carries its caveat until somebody does that. The anchors are a smoke test — they catch a judge that is
broken, and they cannot certify one that is working.
