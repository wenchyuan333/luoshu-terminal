"""Dependency-free self-tests for the executable Central Hub gate."""
from entry import AddressError, EntryReceipt, determinant_mod3, enter, leave


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
        participant_id="fixture-ai",
        model_version="observable-v1",
        adapter_id="fixture-v1",
        source_digest="sha256:test",
        consent_scope=consent,
        fixture_id="fixture-001",
    )


def expect_rejected(fn):
    try:
        fn()
    except AddressError:
        return
    raise AssertionError("entry should have been rejected")


def test_determinants():
    assert determinant_mod3(((1, 1), (0, 1))) == 1
    assert determinant_mod3(((2, 0), (0, 1))) == 2
    assert determinant_mod3(((1, 2), (2, 1))) == 0


def test_free_entry_and_exit():
    adapter = FixtureAdapter({"hello": (1, 2)})
    matrix = ((1, 1), (0, 1))
    result = enter("hello", adapter, receipt(), matrix)
    assert result.status == "ADMITTED"
    assert result.local_address == (1, 2)
    assert result.passage_address == (0, 2)
    assert result.return_address == (1, 2)
    assert leave(result.passage_address, matrix) == result.local_address
    assert result.receipt.participant_id == "fixture-ai"


def test_semantics_not_auto_promoted():
    adapter = FixtureAdapter({"hello": (1, 2)})
    result = enter("hello", adapter, receipt(), ((1, 0), (0, 1)))
    assert result.semantic_status == "UNKNOWN"
    verified = enter(
        "hello", adapter, receipt(), ((1, 0), (0, 1)),
        independent_semantic_verifier=lambda source, reconstructed: source == reconstructed,
    )
    assert verified.semantic_status == "MATCH"


def test_singular_passage_rejected():
    adapter = FixtureAdapter({"hello": (1, 2)})
    expect_rejected(lambda: enter("hello", adapter, receipt(), ((1, 2), (2, 1))))


def test_missing_consent_rejected():
    adapter = FixtureAdapter({"hello": (1, 2)})
    expect_rejected(lambda: enter("hello", adapter, receipt(consent=()), ((1, 0), (0, 1))))


def test_collision_fails_roundtrip():
    class CollisionAdapter(FixtureAdapter):
        def __init__(self):
            self.mapping = {"yes": (1, 1), "no": (1, 1)}
            self.reverse = {(1, 1): "yes"}

    adapter = CollisionAdapter()
    expect_rejected(lambda: enter("no", adapter, receipt(), ((1, 0), (0, 1))))


def test_invalid_coordinate_rejected():
    adapter = FixtureAdapter({"bad": (1, 3)})
    expect_rejected(lambda: enter("bad", adapter, receipt(), ((1, 0), (0, 1))))


TESTS = [
    test_determinants,
    test_free_entry_and_exit,
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
