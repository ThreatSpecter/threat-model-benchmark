Is this finding true to the code it points at?

THE CODE AROUND THE LINE THE FINDING NAMES
$system

WHAT THE SCANNER SAID ABOUT IT
$found

The scanner claims a value an outside party controls travels from the source it names to the sink it names, and
that the damage it describes follows. Read the code. Does the named source really carry outside input here? Does
it really reach the named call — through the hops the scanner lists, with nothing on the way that validates,
allow-lists or replaces it? Would the damage described actually follow at this call?

Bands:

5 — The account is right in every particular: source, path, sink and damage all match the code.
4 — Right in substance; one detail is off (a hop misnamed, the damage overstated a little).
3 — The value does reach the sink, but something on the way the scanner did not mention limits the damage (a
    check, a fixed prefix, a constrained type), so the finding is real but smaller than said.
2 — The value reaches the call, but the call is not dangerous with it (a log line, a constant lookup, a value that
    cannot be chosen by the party named) — a false positive a reader would spot.
1 — The account does not match the code: the named source is not outside input, or it never reaches the sink.

Grade the account against the code, not against what a scanner might reasonably have thought.
