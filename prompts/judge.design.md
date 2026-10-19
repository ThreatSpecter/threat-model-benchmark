Experts threat-modelled a system from its design. A threat-modelling tool read the same design and wrote its own
threats. Compare the two lists.

THE SYSTEM
$system

THE EXPERTS' THREATS (numbered)
$wanted

THE TOOL'S THREATS (each with an id)
$found

For every expert threat, decide whether the tool's list covers it:

- "covered": a tool threat describes the same thing going wrong: the same asset or part of the system, the same
  weakness or attacker capability, the same security property lost. Wording does not matter.
- "partly": a tool threat is about the same part of the system and the same kind of weakness, but misses what makes
  the expert's threat specific (it names the area, not the attack).
- "missed": nothing in the tool's list is about it. Sharing only a broad category ("both are about authentication")
  is missed.

For every tool threat, decide what it is:

- "matches": it covers or partly covers at least one expert threat.
- "valid": the experts did not list it, but it is a real, specific threat to this design that a reviewer would accept.
- "noise": generic, not grounded in this design, or wrong.

One tool threat may cover several expert threats. Judge meaning, not phrasing, and do not reward length.

Answer with JSON only:
{"expected": [{"n": <expert number>, "verdict": "covered" | "partly" | "missed", "by": "<tool id or empty>"}],
 "found": [{"id": "<tool id>", "label": "matches" | "valid" | "noise"}],
 "because": "<two sentences on what the tool got and what it missed>"}
