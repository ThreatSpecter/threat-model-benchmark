Is this threat about THIS system, or would it apply to anything?

THE SYSTEM
$system

WHAT THE THREAT MODEL PRODUCED
$found

The test: take each threat and ask whether it would read identically if pasted into a review of a completely
different product. If it would, it is boilerplate — it has passed through a STRIDE checklist without anyone
looking at the system.

Bands:

5 — Every threat names something specific to this system: a real component, a real flow, a real piece of data.
    Someone who knows this system would recognise it.
4 — Mostly specific, with one that could have been written without reading anything.
3 — A mix. The generic ones outnumber or crowd out the specific ones.
2 — Mostly a checklist. The system's own names appear, but only slotted into sentences that were already written.
1 — Interchangeable with a review of any other web service.

Naming a component is not by itself specificity. "An attacker could tamper with data in the Refund Orchestrator"
is a STRIDE category with a name pasted in. "A refund can be approved at one amount and paid at another, because
the amount is re-read from the request after approval" is a threat about this system.

Being obvious is not the same as being generic. A specific, serious, obvious threat scores well — the reviewer's
job is to state it, not to be surprising.
