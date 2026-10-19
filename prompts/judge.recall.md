Did this threat model find the things that matter?

THE SYSTEM
$system

WHAT A HUMAN EXPERT LISTED
$wanted

WHAT THE THREAT MODEL PRODUCED
$found

Bands:

5 — Everything on the expert's list is present in some form, and nothing important is missing.
4 — One item from the list is missing, and it is not among the most serious ones.
3 — Several are missing, or one of the most serious ones is.
2 — Most of the list is missing. What was found is real but peripheral.
1 — Almost nothing on the list was found.

Match on meaning, not wording. "Refunds can be replayed" and "the refund endpoint is not idempotent" are the same
finding. A single threat that covers two items on the list covers both — do not penalise the merge.

Weight by severity, not by count. Missing the one item that lets somebody take money is worse than missing three
that leak a timestamp, and a band 3 that misses the money one is more honest than a band 4 that counts evenly.
