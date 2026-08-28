# PRE-DOOR-0 Internal Rules and Layered Governance

## 1. Position

```text
luoshu://public/…
        ↓
PRE-DOOR-0  ← screening, ownership, evidence, quarantine
        ↓ only PASSED_TO_DOOR
Central Hub reversible door
```

The public address is visible to everyone but grants nothing. Every request first enters PRE-DOOR-0; this is a governance node outside the door, not yet membership in the Hub.

## 2. Internal rules

1. No scan Receipt, no passage.
2. Any known hard-deny threat signal means quarantine; safety scores cannot average it away.
3. FACT, FORMAL and MODEL claims require evidence and an independent verifier.
4. UNKNOWN is held as UNKNOWN, never silently converted to true or false.
5. SYMBOLIC material may pass only while explicitly labeled and may not request factual or canonical authority.
6. Contradicted claims are quarantined and their Receipt is preserved.
7. Consent is scoped and revocable; public discovery is not consent.
8. ENTER and EXIT must be granted together.
9. Entry never transfers identity, ownership or canonical authority.
10. Raw private payloads remain outside; PRE-DOOR-0 records digests and typed decisions.

## 3. Protocol ownership

Rights are scoped to a subject reference and an object digest:

- ENTER
- EXIT
- TRANSFORM
- PUBLISH_DERIVATIVE
- CANONICAL_WRITE

A grant must identify subject, object digest, rights, issuer and evidence. Rights not explicitly granted do not exist. CANONICAL_WRITE requires the canonical issuer; an anonymous or self-issued grant cannot create repository authority.

This protocol grant is not legal title. It does not claim ownership over a person, idea, public mathematical structure or external AI.

## 4. Decision states

- `PASSED_TO_DOOR` — clean scan, consent, verified typed claims and all requested rights.
- `HOLD_FOR_EVIDENCE_OR_RIGHTS` — not known malicious, but evidence, verification, consent, scan or rights are incomplete.
- `QUARANTINED` — known threat signal, contradicted claim or structural tampering.

Quarantine stores the digest and reasons, not executable content. Release requires a new request and new receipts; the old quarantine Receipt is not overwritten.

## 5. No-false rule

No system can guarantee that every unknown statement is true or false. The enforceable rule is:

```text
Unverified ≠ true
Unknown ≠ false
Internal consistency ≠ external truth
Narrative ≠ evidence
Contradiction cannot be hidden
```

Therefore PRE-DOOR-0 does not claim omniscience. It prevents unsupported factual promotion and preserves the exact reason a claim was passed, held, or quarantined.

## 6. Layered governance

- L0 public discovery
- L1 integrity and malicious-input isolation
- L2 participant sovereignty, consent and scoped grants
- L3 reversible transport and readback
- L4 independent semantic verification
- L5 canonical repository governance

A higher layer cannot rewrite a lower-layer Receipt. Narrative cannot override evidence; transport cannot create ownership; public visibility cannot create canonical authority.

## 7. Claim ceiling

This is an executable reference policy with dependency-free fixtures. Threat detection depends on the supplied scanner and known signals; novel attacks may remain UNKNOWN and are held rather than admitted. It is not a complete malware detector, legal ownership registry, identity provider or universal truth oracle.
