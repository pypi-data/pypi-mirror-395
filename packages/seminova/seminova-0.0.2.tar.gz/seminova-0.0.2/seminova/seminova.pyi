from typing import Any, List, Tuple, Optional


__all__ = [
    "PyR1CS",
    "DynProof",
    "r1cs_from_python",
    "make_empty_proof",
]


def r1cs_from_python(
    a: Any,
    b: Any,
    c: Any,
    num_instance_vars: int,
    num_witness_vars: int,
    instance_vals: Optional[Any] = ...,
    witness_vals: Optional[Any] = ...,
    z0: Optional[Any] = ...,
) -> "PyR1CS":
    """
    Build an R1CS instance from Python-provided sparse matrices and optional instance/witness vectors.

    Parameters
    ----------
    a, b, c: Any
        Each must be a Python ``list`` of rows where each row is a ``list`` of (coeff, index) tuples.
        - coeff may be one of: ``bytes`` (48-byte big-endian), ``int`` (small integer), or ``str`` (hex "0x..." or decimal string).
        - index must be an integer (usize).

    num_instance_vars, num_witness_vars: int
        Sizes used to populate the returned R1CS shape.

    instance_vals, witness_vals, z0: Optional[Any]
        Optional Python lists of field elements (same accepted formats as coeffs) to set the instance vector,
        witness vector, and initial output vector respectively.

    Returns
    -------
    PyR1CS
        A Python wrapper object exposing helper methods to inspect and manipulate the R1CS.

    Raises
    ------
    TypeError
        If inputs are malformed.
    """
    ...


def make_empty_proof(r1cs: "PyR1CS", generators_count: int) -> "DynProof":
    """
    Construct a fresh ``DynProof`` object from a single ``PyR1CS`` instance.

    Parameters
    ----------
    r1cs: PyR1CS
        The base R1CS instance to populate the proof state.
    generators_count: int
        Number of commitment generators to create/derive for the proof.

    Returns
    -------
    DynProof
        A newly-initialized DynProof configured with the provided R1CS and generators.
    """
    ...


class PyR1CS:
    """
    Python wrapper around the Rust ``R1CS`` structure.

    The object is opaque on the Python side but exposes helpers for
    serialization and basic checks. The underlying witness/instance are
    stored as lists of field elements (Fq) and may be set from Python
    using ``set_instance_and_witness``.
    """

    def __repr__(self) -> str: ...

    def is_satisfied(self) -> bool:
        """Return ``True`` if the current ``instance`` and ``witness`` satisfy
        all constraints in the R1CS shape.

        May raise runtime errors if the internal shape/state is inconsistent.
        """
        ...

    @property
    def num_constraints(self) -> int: ...

    def witness_bytes(self) -> List[bytes]:
        """Return the witness vector serialized as a list of 48-byte big-endian
        field element representations (``bytes`` objects).
        """
        ...

    def instance_bytes(self) -> List[bytes]:
        """Return the instance vector serialized as a list of 48-byte big-endian
        field element representations (``bytes`` objects).
        """
        ...

    def witness_commitment_bytes(self) -> bytes:
        """Return the witness commitment (G1 affine point) in canonical compressed
        form (``bytes``).
        """
        ...

    def comms_bytes(self) -> Tuple[bytes, bytes]:
        """Return a tuple ``(comm_E_bytes, comm_T_bytes)`` where each item is
        the canonical compressed encoding of a G1 affine point.
        """
        ...

    def output_bytes(self) -> List[bytes]:
        """Return the public output vector serialized to bytes (48-byte field
        element representations).
        """
        ...

    def set_instance_and_witness(self, instance_vals: Optional[Any] = ..., witness_vals: Optional[Any] = ...) -> None:
        """
        Set the internal instance and witness vectors from Python lists.

        Parameters
        ----------
        instance_vals, witness_vals: Optional[Any]
            Python lists of field elements. Each element may be a ``bytes`` (big-endian),
            ``int``, or decimal/hex string ("0x..."). The conversion rules match the
            helper used in the Rust implementation and will raise ``ValueError`` or
            ``TypeError`` for malformed elements.
        """
        ...


class DynProof:
    """
    Runtime-dynamic proof wrapper.

    A ``DynProof`` holds a sequence of folded ``R1CS`` instances, the current
    latest ``R1CS`` and commitment-related data required for iterative folding
    and verification.
    """

    def __init__(self, py_folded: Any, latest: PyR1CS, generators_count: int) -> None:
        """
        Construct a DynProof from a Python list of ``PyR1CS`` objects (folded list),
        a ``PyR1CS`` representing the latest state, and a generator count.

        Parameters
        ----------
        py_folded: Any
            Python iterable/list of ``PyR1CS`` objects representing the folded prefix.
        latest: PyR1CS
            The current latest R1CS instance.
        generators_count: int
            Number of G1 generators to derive/produce; if generator creation fails
            internally the implementation falls back to random generators.
        """
        ...

    def __repr__(self) -> str: ...

    @property
    def i(self) -> int: ...

    @i.setter
    def i(self, v: int) -> None: ...

    @property
    def latest(self) -> PyR1CS:
        """Return a copy of the latest ``PyR1CS`` state known to this proof.

        Note: the returned ``PyR1CS`` is a shallow-cloned wrapper of the underlying
        Rust ``R1CS`` (it is not a deep Python-native copy of all internal buffers).
        """
        ...

    def verify_latest_r1cs(self) -> bool:
        """Run a satisfaction check on the ``latest`` R1CS and return ``True`` if
        satisfied. Equivalent to ``latest.is_satisfied()``.
        """
        ...

    def update_with_latest(self, pc: int, python_new_latest: PyR1CS) -> None:
        """
        Update the proof state by folding the current folded entry referenced by
        the internal program counter with the existing ``latest`` and then replace
        ``latest`` with ``python_new_latest``.

        Parameters
        ----------
        pc: int
            New program-counter value (index into the folded list) to update to.
        python_new_latest: PyR1CS
            An authoritative ``PyR1CS`` produced by Python-side code representing
            the post-step new instance/witness pair. The method trusts this object
            and will replace the internal ``latest`` with it.

        Raises
        ------
        ValueError
            If the proof was constructed with an empty folded set or other
            preconditions fail.
        """
        ...

    def verify(self) -> None:
        """
        Perform a full verification of the proof state. On success returns ``None``.
        On failure it raises a ``RuntimeError`` (or a PyO3-wrapped exception) with
        a human-readable diagnostic message.
        """
        ...

    def latest_hash_bytes(self) -> bytes:
        """Return the Poseidon hash of the public IO of the latest folded entry
        as canonical serialized field bytes.
        """
        ...
