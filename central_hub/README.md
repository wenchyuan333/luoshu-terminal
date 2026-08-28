# Central Hub executable entry gate

This directory implements a two-stage reference protocol:

```text
public address → PRE-DOOR-0 → reversible Central Hub door → readback
```

## PRE-DOOR-0

Before coordinates are encoded, the governance node checks:

- clean scanner status plus scanner Receipt
- explicit consent
- typed claims and independent verification for FACT／FORMAL／MODEL
- UNKNOWN claims held rather than treated as false or true
- SYMBOLIC claims kept labeled
- protocol control grants for every requested right
- bidirectional ENTER and EXIT rights
- hard-deny threat signals

Any threat signal produces `QUARANTINED`; it cannot be averaged away by safe scores. Unscanned, unsupported, unknown, unverified, or under-authorized requests produce `HOLD_FOR_EVIDENCE_OR_RIGHTS`. Only `PASSED_TO_DOOR` may call `enter()`.

## Layered governance

1. **L0 Public discovery** — anonymous address; grants no rights.
2. **L1 Pre-entry integrity** — scan, claim type, evidence, contradiction and quarantine.
3. **L2 Sovereign control** — consent and protocol ownership grants remain with the source participant.
4. **L3 Reversible transport** — 𝔽₃ address, GL(d,𝔽₃), round-trip and collision checks.
5. **L4 Semantic verification** — address equality remains UNKNOWN without an independent verifier.
6. **L5 Canonical governance** — public entry never grants repository write or canonical authority.

## Ownership invariant

`OwnershipGrant` means a scoped protocol control grant, not a declaration of legal copyright or ownership over a person, idea, or mathematical truth.

```text
Entry ≠ ownership transfer
Possession ≠ authority
Address equality ≠ identity transfer
Public visibility ≠ canonical write
```

The screening Receipt always records `ownership_transferred = false`.

## Executable gate

After PRE-DOOR-0 passes, the existing gate enforces:

- V = 𝔽₃ᵈ address validation
- reversible passage A ∈ GL(d, 𝔽₃)
- det(A) ∈ {1, 2} admission and det(A) = 0 rejection
- participant-owned, versioned encoder／decoder adapter
- round-trip entry and exit readback
- collision rejection
- no automatic promotion from address equality to semantic equality

## Claim strength

`EXECUTABLE_REFERENCE_PROTOCOL`.

The node cannot guarantee perfect truth or detect every unknown attack. It enforces a narrower, testable rule: unverified factual claims do not pass the door; known threat signals are quarantined; UNKNOWN stays UNKNOWN; every decision has a digestible Receipt.
