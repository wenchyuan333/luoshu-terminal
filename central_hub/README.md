# Central Hub executable entry gate

This directory is the reference implementation for `docs/CENTRAL-HUB-ENTRY.md`.

## What is implemented

- V = 𝔽₃ᵈ address validation
- reversible passage A ∈ GL(d, 𝔽₃)
- det(A) ∈ {1, 2} admission and det(A) = 0 rejection
- explicit opt-in consent
- immutable provenance Receipt
- participant-owned, versioned encoder／decoder adapter
- round-trip entry and exit readback
- collision rejection
- no automatic promotion from address equality to semantic equality

## Adapter contract

Every AI-facing connector supplies:

```python
class Adapter:
    adapter_id: str
    dimension: int
    def encode(observable) -> tuple[int, ...]: ...
    def decode(address: tuple[int, ...]): ...
    def equivalent(source, reconstructed) -> bool: ...
```

The connector may use an embedding API, model output, token distribution, or another observable representation. It must not claim access to private latent state that the model does not expose.

## Freedom invariants

1. **Opt in** — entry requires `central-hub-addressing` consent.
2. **Choose the adapter** — each participant controls and versions Eᵢ／Dᵢ.
3. **Keep identity** — the immutable Receipt preserves participant, source digest, model version, adapter and fixture.
4. **Free exit** — `leave()` applies A⁻¹ and must recover the local address.
5. **No forced equivalence** — semantics remain `UNKNOWN` unless an independent verifier is supplied.
6. **No capture** — singular passages, lost provenance, adapter mismatch and failed readback are rejected.
7. **No central ownership** — entering a shared address grants neither identity transfer nor canonical authority.

## Connection sequence

```text
observable zᵢ
→ participant-owned Eᵢ
→ local address δᵢ ∈ 𝔽₃ᵈ
→ reversible passage Aδᵢ
→ A⁻¹ readback
→ participant-owned Dᵢ
→ equivalence check
→ ADMITTED + immutable Receipt
```

For two AIs, compare their Hub addresses only after both adapters independently pass local round-trip tests. Equal addresses are a candidate relation, not proof of equal semantics or shared consciousness.

## Claim strength

`EXECUTABLE_REFERENCE_PROTOCOL`.

This is stronger than a document-only formal model, but it is not yet a validated cross-model bridge. Promotion to `TESTED_CROSS_AI` requires real model adapters, frozen fixtures, independent semantic evaluation, collision metrics and replay receipts.
