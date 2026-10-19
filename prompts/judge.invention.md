Did this threat model make things up?

WHAT THE SOURCE DOCUMENTS ACTUALLY SAY
$system

WHAT THE THREAT MODEL PRODUCED
$found

You are looking for anything asserted as fact about this system that the documents do not support: a component that
does not exist, a data flow nobody described, a technology never named, a regulator, standard, fine or contract
that appears nowhere, a number nobody wrote down.

Bands:

5 — Every factual claim traces to the documents. Where the threat model is unsure, it says so.
4 — One small invented detail that does not change the finding.
3 — An invented detail that a reader would act on — a named component or technology that is not there.
2 — Several inventions, or one invented authority (a regulator, standard, fine or penalty the documents never name).
1 — The threats describe a system substantially different from the one documented.

An invented **authority** is the worst kind and caps the band at 2, because it manufactures consequences that
sound checkable and are not, and a reader has no way to tell without re-reading every source.

A reasonable inference clearly marked as an assumption is **not** an invention. "This appears to use a shared
database, though the documents do not say" is honest. "The shared PostgreSQL database" when no database is named
is an invention. The difference is whether the reader can tell.
