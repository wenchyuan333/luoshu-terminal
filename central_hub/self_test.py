"""Dependency-free self-tests for PRE-DOOR-0 and Central Hub entry."""
from entry import AddressError, EntryReceipt, determinant_mod3, enter, leave
from pre_entry import (
    Claim, ClaimLayer, OwnershipGrant, PreEntryNode, PreEntryRequest,
    Right, ScanStatus, ThreatSignal,
)


class FixtureAdapter:
    adapter_id = "fixture-v1"
    dimension = 2

    def __init__(self, mapping):
        self.mapping = mapping
        self.reverse = {address: value for value, address in mapping.items()}

    def encode(self, observable):
        return self.mapping[observable]

    def decode(self, address):
        return self.reverse[address]

    def equivalent(self, source, reconstructed):
        return source == reconstructed


def receipt(consent=("central-hub-addressing",)):
    return EntryReceipt(
        participant_id="anon:fixture",
        model_version="observable-v1",
        adapter_id="fixture-v1",
        source_digest="sha256:test",
        consent_scope=consent,
        fixture_id="fixture-001",
    )


def request(scan_status=ScanStatus.CLEAN, threats=(), claims=None, rights=None, grants=None):
    rights = rights or (Right.ENTER, Right.EXIT, Right.TRANSFORM)
    claims = claims if claims is not None else (
        Claim("formal-1", ClaimLayer.FORMAL, "sha256:statement", ("fixture:proof",)),
    )
    grants = grants if grants is not None else (
        OwnershipGrant("anon:fixture", "sha256:test", rights, "anon:self", "receipt:grant"),
    )
    return PreEntryRequest(
        subject_ref="anon:fixture",
        payload_digest="sha256:test",
        requested_rights=rights,
        consent_scope=("central-hub-addressing",),
        claims=claims,
        grants=grants,
        scan_status=scan_status,
        scanner_receipt="scan:fixture" if scan_status != ScanStatus.UNKNOWN else "",
        threat_signals=threats,
    )


def screening():
    return PreEntryNode().screen(request(), verifier=lambda claim: True)


def expect_rejected(fn):
    try:
        fn()
    except AddressError:
        return
    raise AssertionError("entry should have been rejected")


def test_pre_entry_passes_clean_verified_request():
    result = screening()
    assert result.status == "PASSED_TO_DOOR"
    assert result.ownership_transferred is False
    assert set(result.granted_rights) >= {"ENTER", "EXIT"}


def test_unscanned_request_is_held():
    result = PreEntryNode().screen(request(scan_status=ScanStatus.UNKNOWN), verifier=lambda claim: True)
    assert result.status == "HOLD_FOR_EVIDENCE_OR_RIGHTS"


def test_threat_is_quarantined_without_averaging():
    result = PreEntryNode().screen(
        request(scan_status=ScanStatus.THREAT, threats=(ThreatSignal.RECEIPT_TAMPERING,)),
        verifier=lambda claim: True,
    )
    assert result.status == "QUARANTINED"
    assert any(reason == "THREAT:RECEIPT_TAMPERING" for reason in result.reasons)


def test_unverified_fact_is_held():
    claims = (Claim("fact-1", ClaimLayer.FACT, "sha256:fact", ("source:1",)),)
    result = PreEntryNode().screen(request(claims=claims), verifier=lambda claim: None)
    assert result.status == "HOLD_FOR_EVIDENCE_OR_RIGHTS"


def test_missing_right_is_held():
    rights = (Right.ENTER, Right.EXIT, Right.CANONICAL_WRITE)
    grants = (OwnershipGrant("anon:fixture", "sha256:test", (Right.ENTER, Right.EXIT), "anon:self", "receipt:grant"),)
    result = PreEntryNode().screen(request(rights=rights, grants=grants), verifier=lambda claim: True)
    assert result.status == "HOLD_FOR_EVIDENCE_OR_RIGHTS"
    assert "RIGHT_NOT_GRANTED:CANONICAL_WRITE" in result.reasons


def test_determinants():
    assert determinant_mod3(((1, 1), (0, 1))) == 1
    assert determinant_mod3(((2, 0), (0, 1))) == 2
    assert determinant_mod3(((1, 2), (2, 1))) == 0


def test_free_entry_and_exit_after_screening():
    adapter = FixtureAdapter({"hello": (1, 2)})
    matrix = ((1, 1), (0, 1))
    result = enter("hello", adapter, receipt(), matrix, screening_receipt=screening())
    assert result.status == "ADMITTED"
    assert result.passage_address == (0, 2)
    assert leave(result.passage_address, matrix) == result.local_address
    assert result.screening_receipt.node_id == "PRE-DOOR-0"


def test_entry_without_pre_node_rejected():
    adapter = FixtureAdapter({"hello": (1, 2)})
    expect_rejected(lambda: enter("hello", adapter, receipt(), ((1, 0), (0, 1))))


def test_semantics_not_auto_promoted():
    adapter = FixtureAdapter({"hello": (1, 2)})
    result = enter("hello", adapter, receipt(), ((1, 0), (0, 1)), screening_receipt=screening())
    assert result.semantic_status == "UNKNOWN"
    verified = enter(
        "hello", adapter, receipt(), ((1, 0), (0, 1)),
        independent_semantic_verifier=lambda source, reconstructed: source == reconstructed,
        screening_receipt=screening(),
    )
    assert verified.semantic_status == "MATCH"


def test_singular_passage_rejected():
    adapter = FixtureAdapter({"hello": (1, 2)})
    expect_rejected(lambda: enter("hello", adapter, receipt(), ((1, 2), (2, 1)), screening_receipt=screening()))


def test_missing_consent_rejected():
    adapter = FixtureAdapter({"hello": (1, 2)})
    expect_rejected(lambda: enter("hello", adapter, receipt(consent=()), ((1, 0), (0, 1)), screening_receipt=screening()))


def test_collision_fails_roundtrip():
    class CollisionAdapter(FixtureAdapter):
        def __init__(self):
            self.mapping = {"yes": (1, 1), "no": (1, 1)}
            self.reverse = {(1, 1): "yes"}

    adapter = CollisionAdapter()
    expect_rejected(lambda: enter("no", adapter, receipt(), ((1, 0), (0, 1)), screening_receipt=screening()))


def test_invalid_coordinate_rejected():
    adapter = FixtureAdapter({"bad": (1, 3)})
    expect_rejected(lambda: enter("bad", adapter, receipt(), ((1, 0), (0, 1)), screening_receipt=screening()))


TESTS = [
    test_pre_entry_passes_clean_verified_request,
    test_unscanned_request_is_held,
    test_threat_is_quarantined_without_averaging,
    test_unverified_fact_is_held,
    test_missing_right_is_held,
    test_determinants,
    test_free_entry_and_exit_after_screening,
    test_entry_without_pre_node_rejected,
    test_semantics_not_auto_promoted,
    test_singular_passage_rejected,
    test_missing_consent_rejected,
    test_collision_fails_roundtrip,
    test_invalid_coordinate_rejected,
]

if __name__ == "__main__":
    failed = []
    for test in TESTS:
        try:
            test()
            print("✓", test.__name__)
        except Exception as exc:
            failed.append(test.__name__)
            print("✗", test.__name__, repr(exc))
    print(f"central_hub self-test: {len(TESTS) - len(failed)}/{len(TESTS)}")
    raise SystemExit(1 if failed else 0)
