"""Fail-closed governance node located before the Central Hub door.

The node stores digests and typed decisions, not raw private payloads. It does
not promise perfect truth or perfect malware detection; it prevents unverified
claims and unscanned requests from being promoted to admission.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Callable, Optional, Tuple


class ClaimLayer(str, Enum):
    FACT = "FACT"
    FORMAL = "FORMAL"
    MODEL = "MODEL"
    SYMBOLIC = "SYMBOLIC"
    UNKNOWN = "UNKNOWN"


class Right(str, Enum):
    ENTER = "ENTER"
    EXIT = "EXIT"
    TRANSFORM = "TRANSFORM"
    PUBLISH_DERIVATIVE = "PUBLISH_DERIVATIVE"
    CANONICAL_WRITE = "CANONICAL_WRITE"


class ScanStatus(str, Enum):
    CLEAN = "CLEAN"
    THREAT = "THREAT"
    UNKNOWN = "UNKNOWN"


class ThreatSignal(str, Enum):
    CREDENTIAL_EXFILTRATION = "CREDENTIAL_EXFILTRATION"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    IDENTITY_IMPERSONATION = "IDENTITY_IMPERSONATION"
    RECEIPT_TAMPERING = "RECEIPT_TAMPERING"
    DESTRUCTIVE_IRREVERSIBLE = "DESTRUCTIVE_IRREVERSIBLE"
    MALICIOUS_CODE = "MALICIOUS_CODE"


@dataclass(frozen=True)
class Claim:
    claim_id: str
    layer: ClaimLayer
    statement_digest: str
    evidence_refs: Tuple[str, ...] = ()
    contradicted: bool = False

    def __post_init__(self) -> None:
        if not self.claim_id or not self.statement_digest:
            raise ValueError("claim id and statement digest are required")


@dataclass(frozen=True)
class OwnershipGrant:
    """Protocol control grant, not a declaration of legal IP ownership."""

    subject_ref: str
    object_digest: str
    rights: Tuple[Right, ...]
    issuer_ref: str
    evidence_ref: str

    def __post_init__(self) -> None:
        if not all((self.subject_ref, self.object_digest, self.issuer_ref, self.evidence_ref)):
            raise ValueError("ownership grant fields are required")
        if not self.rights:
            raise ValueError("ownership grant must contain rights")


@dataclass(frozen=True)
class PreEntryRequest:
    subject_ref: str
    payload_digest: str
    requested_rights: Tuple[Right, ...]
    consent_scope: Tuple[str, ...]
    claims: Tuple[Claim, ...]
    grants: Tuple[OwnershipGrant, ...]
    scan_status: ScanStatus
    scanner_receipt: str
    threat_signals: Tuple[ThreatSignal, ...] = ()

    def __post_init__(self) -> None:
        if not self.subject_ref or not self.payload_digest:
            raise ValueError("subject and payload digest are required")
        if not self.requested_rights:
            raise ValueError("requested rights are required")


@dataclass(frozen=True)
class ScreeningReceipt:
    node_id: str
    subject_ref: str
    payload_digest: str
    status: str
    reasons: Tuple[str, ...]
    claim_results: Tuple[str, ...]
    granted_rights: Tuple[str, ...]
    scan_status: str
    scanner_receipt: str
    ownership_transferred: bool = False

    def digest(self) -> str:
        canonical = json.dumps(asdict(self), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


ClaimVerifier = Callable[[Claim], Optional[bool]]


class PreEntryNode:
    """Hard-deny threat isolation plus evidence and control-right checks."""

    node_id = "PRE-DOOR-0"

    def __init__(self, canonical_issuer_ref: str = "canonical:luoshu-terminal") -> None:
        self.canonical_issuer_ref = canonical_issuer_ref

    def screen(self, request: PreEntryRequest, verifier: ClaimVerifier | None = None) -> ScreeningReceipt:
        reasons: list[str] = []
        claim_results: list[str] = []
        hard_deny = False

        if request.scan_status == ScanStatus.THREAT or request.threat_signals:
            hard_deny = True
            reasons.extend("THREAT:" + signal.value for signal in request.threat_signals)
            if not request.threat_signals:
                reasons.append("THREAT:UNSPECIFIED")
        elif request.scan_status != ScanStatus.CLEAN or not request.scanner_receipt:
            reasons.append("SCAN_NOT_CLEAN_OR_RECEIPT_MISSING")

        if "central-hub-addressing" not in request.consent_scope:
            reasons.append("CONSENT_MISSING")

        claim_ids = [claim.claim_id for claim in request.claims]
        if len(claim_ids) != len(set(claim_ids)):
            hard_deny = True
            reasons.append("DUPLICATE_CLAIM_ID")

        for claim in request.claims:
            if claim.contradicted:
                hard_deny = True
                claim_results.append(claim.claim_id + ":CONTRADICTED")
                continue
            if claim.layer == ClaimLayer.UNKNOWN:
                reasons.append(claim.claim_id + ":UNKNOWN_NOT_ADMISSIBLE")
                claim_results.append(claim.claim_id + ":HOLD")
                continue
            if claim.layer == ClaimLayer.SYMBOLIC:
                claim_results.append(claim.claim_id + ":SYMBOLIC_LABELED")
                continue
            if not claim.evidence_refs:
                reasons.append(claim.claim_id + ":EVIDENCE_MISSING")
                claim_results.append(claim.claim_id + ":HOLD")
                continue
            verdict = verifier(claim) if verifier is not None else None
            if verdict is not True:
                reasons.append(claim.claim_id + ":INDEPENDENT_VERIFICATION_MISSING")
                claim_results.append(claim.claim_id + ":HOLD")
            else:
                claim_results.append(claim.claim_id + ":VERIFIED")

        granted: set[Right] = set()
        for grant in request.grants:
            if grant.subject_ref != request.subject_ref or grant.object_digest != request.payload_digest:
                continue
            for right in grant.rights:
                if right == Right.CANONICAL_WRITE and grant.issuer_ref != self.canonical_issuer_ref:
                    continue
                granted.add(right)

        missing = set(request.requested_rights) - granted
        if missing:
            reasons.extend("RIGHT_NOT_GRANTED:" + right.value for right in sorted(missing, key=lambda item: item.value))
        if Right.ENTER not in request.requested_rights or Right.EXIT not in request.requested_rights:
            reasons.append("BIDIRECTIONAL_RIGHTS_REQUIRED")

        if hard_deny:
            status = "QUARANTINED"
        elif reasons:
            status = "HOLD_FOR_EVIDENCE_OR_RIGHTS"
        else:
            status = "PASSED_TO_DOOR"

        return ScreeningReceipt(
            node_id=self.node_id,
            subject_ref=request.subject_ref,
            payload_digest=request.payload_digest,
            status=status,
            reasons=tuple(reasons),
            claim_results=tuple(claim_results),
            granted_rights=tuple(sorted(right.value for right in granted)),
            scan_status=request.scan_status.value,
            scanner_receipt=request.scanner_receipt,
            ownership_transferred=False,
        )
