"""Central Hub reversible entry gate.

This module implements a transport protocol over observable adapter values.
It does not claim access to a model's private or unobservable latent state.
Every admission must first pass PRE-DOOR-0 governance screening.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol, Sequence, Tuple

try:
    from .pre_entry import ScreeningReceipt
except ImportError:  # direct execution from central_hub/
    from pre_entry import ScreeningReceipt

Vector = Tuple[int, ...]
Matrix = Tuple[Tuple[int, ...], ...]


class AddressError(ValueError):
    """Raised when an entry invariant is not satisfied."""


class Adapter(Protocol):
    adapter_id: str
    dimension: int

    def encode(self, observable: Any) -> Vector: ...
    def decode(self, address: Vector) -> Any: ...
    def equivalent(self, source: Any, reconstructed: Any) -> bool: ...


@dataclass(frozen=True)
class EntryReceipt:
    participant_id: str
    model_version: str
    adapter_id: str
    source_digest: str
    consent_scope: Tuple[str, ...]
    fixture_id: str


@dataclass(frozen=True)
class Admission:
    status: str
    local_address: Vector
    passage_address: Vector
    return_address: Vector
    roundtrip_ok: bool
    semantic_status: str
    receipt: EntryReceipt
    screening_receipt: ScreeningReceipt


def _mod3(value: int) -> int:
    return value % 3


def _validate_vector(vector: Sequence[int], dimension: int) -> Vector:
    if len(vector) != dimension:
        raise AddressError(f"expected dimension {dimension}, got {len(vector)}")
    if any(not isinstance(value, int) or value not in (0, 1, 2) for value in vector):
        raise AddressError("address coordinates must belong to 𝔽₃ = {0,1,2}")
    return tuple(vector)


def _validate_matrix(matrix: Sequence[Sequence[int]], dimension: int) -> Matrix:
    if len(matrix) != dimension or any(len(row) != dimension for row in matrix):
        raise AddressError("passage matrix must be square and match adapter dimension")
    if any(not isinstance(value, int) for row in matrix for value in row):
        raise AddressError("passage matrix entries must be integers interpreted modulo 3")
    return tuple(tuple(_mod3(value) for value in row) for row in matrix)


def determinant_mod3(matrix: Sequence[Sequence[int]]) -> int:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise AddressError("determinant requires a non-empty square matrix")
    work = [[_mod3(value) for value in row] for row in matrix]
    determinant = 1
    for column in range(n):
        pivot = next((row for row in range(column, n) if work[row][column] != 0), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = _mod3(-determinant)
        pivot_value = work[column][column]
        determinant = _mod3(determinant * pivot_value)
        pivot_inverse = 1 if pivot_value == 1 else 2
        for j in range(column, n):
            work[column][j] = _mod3(work[column][j] * pivot_inverse)
        for row in range(column + 1, n):
            factor = work[row][column]
            if factor:
                for j in range(column, n):
                    work[row][j] = _mod3(work[row][j] - factor * work[column][j])
    return determinant


def _inverse_mod3(matrix: Matrix) -> Matrix:
    n = len(matrix)
    work = [list(row) + [1 if row_index == column else 0 for column in range(n)]
            for row_index, row in enumerate(matrix)]
    for column in range(n):
        pivot = next((row for row in range(column, n) if work[row][column] % 3 != 0), None)
        if pivot is None:
            raise AddressError("det(A) = 0: passage is not reversible")
        work[column], work[pivot] = work[pivot], work[column]
        pivot_inverse = 1 if work[column][column] % 3 == 1 else 2
        work[column] = [_mod3(value * pivot_inverse) for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [_mod3(value - factor * pivot_value)
                             for value, pivot_value in zip(work[row], work[column])]
    return tuple(tuple(row[n:]) for row in work)


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(_mod3(sum(value * coordinate for value, coordinate in zip(row, vector)))
                 for row in matrix)


def leave(passage_address: Sequence[int], passage_matrix: Sequence[Sequence[int]]) -> Vector:
    dimension = len(passage_address)
    address = _validate_vector(passage_address, dimension)
    matrix = _validate_matrix(passage_matrix, dimension)
    inverse = _inverse_mod3(matrix)
    return _matvec(inverse, address)


def enter(
    observable: Any,
    adapter: Adapter,
    receipt: EntryReceipt,
    passage_matrix: Sequence[Sequence[int]],
    independent_semantic_verifier: Optional[Callable[[Any, Any], bool]] = None,
    screening_receipt: ScreeningReceipt | None = None,
) -> Admission:
    """Enter only after PRE-DOOR-0 passes, then enforce reversible transport."""
    if screening_receipt is None or screening_receipt.status != "PASSED_TO_DOOR":
        raise AddressError("PRE-DOOR-0 screening receipt is required")
    if screening_receipt.subject_ref != receipt.participant_id:
        raise AddressError("screening subject does not match entry participant")
    if screening_receipt.payload_digest != receipt.source_digest:
        raise AddressError("screening payload does not match entry source")
    if screening_receipt.ownership_transferred:
        raise AddressError("entry may not transfer ownership")
    if "ENTER" not in screening_receipt.granted_rights or "EXIT" not in screening_receipt.granted_rights:
        raise AddressError("screening receipt must grant bidirectional entry and exit")
    if "central-hub-addressing" not in receipt.consent_scope:
        raise AddressError("explicit central-hub-addressing consent is required")
    if receipt.adapter_id != adapter.adapter_id:
        raise AddressError("receipt adapter version does not match active adapter")
    if not receipt.source_digest or not receipt.fixture_id:
        raise AddressError("source digest and replay fixture are required")

    local_address = _validate_vector(adapter.encode(observable), adapter.dimension)
    matrix = _validate_matrix(passage_matrix, adapter.dimension)
    if determinant_mod3(matrix) == 0:
        raise AddressError("det(A) = 0: passage is not integrity-preserving")

    passage_address = _matvec(matrix, local_address)
    return_address = leave(passage_address, matrix)
    reconstructed = adapter.decode(return_address)
    roundtrip_ok = return_address == local_address and adapter.equivalent(observable, reconstructed)
    if not roundtrip_ok:
        raise AddressError("round-trip readback failed; admission denied")

    semantic_status = "UNKNOWN"
    if independent_semantic_verifier is not None:
        semantic_status = "MATCH" if independent_semantic_verifier(observable, reconstructed) else "MISMATCH"

    return Admission(
        status="ADMITTED",
        local_address=local_address,
        passage_address=passage_address,
        return_address=return_address,
        roundtrip_ok=True,
        semantic_status=semantic_status,
        receipt=receipt,
        screening_receipt=screening_receipt,
    )
