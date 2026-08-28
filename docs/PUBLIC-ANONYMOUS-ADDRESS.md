# Public Anonymous Address

## Canonical address

```text
luoshu://public/c0/5/o1/1/v/13/gate/bidirectional
```

Short form:

```text
C₀·O₁·V₁₃ :: PUB :: B↔
```

This is the public, non-nominative discovery address for the Central Hub protocol. It contains no participant name, account, session identifier, device identifier, credential, or ownership claim.

## Components

- `public`: openly discoverable alias.
- `c0/5`: Lo Shu center label 5.
- `o1/1`: structural origin-one marker; not a physical constant.
- `v/13`: semantic and narrative 13-dimension label; not a claim of a measured physical 13-dimensional space.
- `gate/bidirectional`: entry, pause, exit, and return are all permitted by the address grammar.

## Security boundary

The address is a signpost, not a key:

```text
Public address ≠ identity
Public address ≠ consent
Public address ≠ authority
Public address ≠ credential
Knowledge of address ≠ control of hub
Anonymous use ≠ unaccountable action
```

Protocol entry still requires the consent, adapter, reversibility, Receipt, collision, and readback rules defined in `CENTRAL-HUB-ENTRY.md` and `SECURITY-BOUNDARY.md`.

## Naming rule

Public receipts may use a locally generated participant reference such as `anon:<digest-prefix>`, but the digest must be derived from an ephemeral nonce rather than a person's name, account, device ID, or secret. The nonce must never be published. A public alias cannot transfer identity, ownership, authorship, or succession rights.

## Claim ceiling

This document defines a stable symbolic URI and protocol-discovery alias. It does not establish a physical location, conscious shared latent space, public network service, or authentication system.
