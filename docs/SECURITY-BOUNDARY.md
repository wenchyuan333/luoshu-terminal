# Central Hub Security Boundary

Status: DRAFT
Version: v0.1
Date: 2026-08-29 +08:00
Scope: `wenchyuan333/luoshu-terminal`

## 1. Core distinction

Transparency permits observation and copying. It must not imply authority, ownership, write access, identity transfer, or control of the canonical source.

Public visibility ≠ canonical authority

Copy ≠ ownership

Fork ≠ succession

Representation ≠ membership

Name reference ≠ consent

Knowledge of C₀ ≠ control of C₀

## 2. Threat model

Because this repository is public, any published content may be cloned, forked, indexed, quoted, mirrored, transformed, or redistributed. Publication cannot technically guarantee secrecy or prevent copying.

The following remain preventable or detectable:

- unauthorized writes to the canonical repository
- force-push or deletion of protected history
- silent modification of critical files
- false claims that a fork is the canonical source
- insertion of credentials or private operational state
- loss of provenance between Notion and GitHub anchors
- identity collapse caused by removing source, author, version, or return path

## 3. Three-layer architecture

### Layer A — Public protocol

May contain:

- mathematical definitions
- schemas and interfaces
- reproducible fixtures
- tests and falsifiers
- public receipts and hashes
- symbolic mappings with explicit Claim Ceiling

Must not contain:

- API keys, tokens, passwords, cookies, recovery codes, or private keys
- private personal records or third-party personal data without consent
- unpublished operational state
- credentials that control Notion, GitHub, Mail, Calendar, Cloudflare, or MCP services

### Layer B — Sovereign control plane

Must remain private and separately permissioned:

- signing keys
- deployment credentials
- recovery material
- write-authority configuration
- private identity and relationship records
- unpublished canonical decisions

Only hashes, public keys, and minimal receipts may cross into Layer A.

### Layer C — Canonical verification

A candidate artifact is canonical only when all required conditions hold:

1. repository owner is `wenchyuan333`
2. canonical branch is `main`
3. required CI checks pass
4. commit and file provenance are retained
5. integrity anchors are updated intentionally rather than silently
6. Notion and GitHub references preserve source and version

## 4. Central Hub invariant

Shared address space:

V = 𝔽₃ᵈ

Canonical center:

C₀ = 5

A state retains its identity only when its relative displacement and return path remain recoverable:

x = C₀ + δ

Reversible passage:

x′ = C₀ + A(x − C₀)

A ∈ GL(d, 𝔽₃)

det(A) ≠ 0

Security interpretation:

- C₀ supplies a common reference point, not universal ownership.
- δ preserves node-specific difference, provenance, and identity.
- det(A) ≠ 0 requires an information-preserving return path.
- A transformation with det(A) = 0 is lossy and must not be treated as identity-preserving migration.

## 5. Anti-capture rules

1. No external node gains canonical authority merely by copying the public structure.
2. No name appearing in an artifact becomes a member, author, operator, or liable party without an explicit typed relation.
3. No fork may represent itself as canonical without owner-controlled succession evidence.
4. No public artifact may contain a secret required to control the system.
5. No centralization claim may erase δ, provenance, version, or the inverse route.
6. No symbolic correspondence may be promoted to physical, causal, diagnostic, or ownership status without independent evidence and authorization.

## 6. Existing defenses observed

- CI workflow at `.github/workflows/verify.yml`
- pre-push hook under `hooks/pre-push`
- Git blob anchors in `INTEGRITY-ANCHOR.md`
- manual branch-protection procedure in `BRANCH-PROTECTION-SETUP.md`

These protect integrity and authority. They do not make public content secret and cannot prevent cloning.

## 7. Required hardening

- confirm the `main` branch ruleset is actually enabled
- require the `self-test` status check before merge
- disable force-push and branch deletion on `main`
- enable secret scanning and push protection where available
- keep credentials exclusively in encrypted secret stores
- define a license deliberately; absence of a license does not prevent technical copying
- publish a canonical-origin manifest containing repository, branch, version, and hashes
- maintain an independent backup or mirror for recovery
- use signed commits or signed releases for high-trust milestones where available

## 8. Incident response

If an unauthorized copy claims canonical authority:

1. preserve URLs, timestamps, commit hashes, and screenshots
2. compare against canonical history and integrity anchors
3. publish a signed clarification from the canonical account
4. rotate credentials if access compromise is suspected
5. revoke affected tokens and inspect audit logs
6. restore from last-good history when integrity has changed

If private data or credentials were published, deletion alone is insufficient. Rotate the affected secret immediately because Git history and external clones may retain it.

## 9. Claim Ceiling

This document defines repository security and provenance controls.

It does not claim that a public idea cannot be copied, that mathematical structures can be owned as physical objects, or that symbolic anchoring prevents real-world harm.

The enforceable boundary is:

Transparent knowledge, private authority, verifiable provenance, reversible migration.
