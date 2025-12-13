from typing import Literal

import numpy as np

from classiq.open_library.functions.state_preparation import (
    apply_phase_table,
)
from classiq.open_library.functions.utility_functions import switch
from classiq.qmod.builtins.functions import IDENTITY, X, Y, Z, inplace_prepare_state
from classiq.qmod.builtins.operations import (
    control,
    if_,
    repeat,
    within_apply,
)
from classiq.qmod.builtins.structs import IndexedPauli, SparsePauliOp
from classiq.qmod.cparam import CArray
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit, QNum
from classiq.qmod.quantum_callable import QCallable, QCallableList


@qfunc
def apply_pauli_term(pauli_string: CArray[IndexedPauli], x: QArray[QBit]) -> None:
    repeat(
        count=pauli_string.len,
        iteration=lambda i: switch(
            pauli_string[i].pauli,
            [
                lambda: IDENTITY(x[pauli_string[i].index]),
                lambda: X(x[pauli_string[i].index]),
                lambda: Y(x[pauli_string[i].index]),
                lambda: Z(x[pauli_string[i].index]),
            ],
        ),
    )


@qfunc
def prepare_select(
    coefficients: list[float],
    select: QCallable[QNum],
    block: QNum[Literal["max(ceiling(log(coefficients.len, 2)), 1)"]],
) -> None:
    """
    [Qmod Classiq-library function]

    Applies the 'Prepare-Select' scheme used for Linear Combination of Unitaries (LCU).
    Compared to the `lcu` function, here the Select operator should be provided directly, allowing to take advantage of some structure for
    the unitaries of the LCU.
    The select operator is defined by: $\\mathrm{SELECT} = \\sum_{j=0}^{m-1} |j\rangle\\!\\langle j|_{block} \\otimes U_j$.

    Args:
        coefficients: L1-normalized array of  $\\{ \\alpha_j \\}$ of the LCU coefficients.
        select: A quantum callable to be applied between the state preparation and its inverse. Its input is the `block` variable, labeling the index of the unitaries in the LCU.
        block: A Quantum variable that holds the index used as input for the 'select' operator.
    """
    coefficients = coefficients + [0] * (
        2**block.size - len(coefficients)  # type:ignore[operator]
    )
    magnitudes = [np.abs(c) for c in coefficients]
    magnitudes = (np.array(magnitudes) / np.sum(magnitudes)).tolist()
    phases = [np.angle(complex(c)) for c in coefficients]

    within_apply(
        lambda: inplace_prepare_state(magnitudes, 0, block),
        lambda: [
            select(block),
            if_(
                not np.allclose(np.array(phases) % (2 * np.pi), 0),
                lambda: apply_phase_table(phases, block),
            ),
        ],
    )


@qfunc
def lcu(
    coefficients: list[float],
    unitaries: QCallableList,
    block: QNum[Literal["max(ceiling(log(coefficients.len, 2)), 1)"]],
) -> None:
    """
    [Qmod Classiq-library function]

    Implements a general linear combination of unitaries (LCU) procedure. The algorithm prepares a superposition
    over the `unitaries` according to the given `coefficients`, and then conditionally applies each unitary controlled by the `block`.

    The operation is of the form:

    $$\\sum_j \\alpha_j U_j$$

    where $U_j$ is a unitary operation applied to `data`.

    Args:
        coefficients: L1-normalized array of  $\\{ \\alpha_j \\}$ of the LCU coefficients.
        unitaries: A list of quantum callable functions to be applied conditionally.
        block: Quantum variable that holds the superposition index used for conditional application of each unitary.
    """
    prepare_select(
        coefficients,
        lambda _block: repeat(
            count=unitaries.len,
            iteration=lambda i: control(_block == i, lambda: unitaries[i]()),
        ),
        block,
    )


@qfunc
def lcu_pauli(
    operator: SparsePauliOp,
    data: QArray[QBit, Literal["operator.num_qubits"]],
    block: QNum[Literal["max(ceiling(log(operator.terms.len, 2)), 1)"]],
) -> None:
    """
    [Qmod Classiq-library function]

    Applies a linear combination of unitaries (LCU) where each unitary is a Pauli term,
    represented as a tensor product of Pauli operators. The function prepares a superposition
    over the unitaries according to the given magnitudes and phases, and applies the corresponding
    Pauli operators conditionally.

    This is useful for implementing Hamiltonian terms of the form:

    $$H=\\sum_j \\alpha_j P_j$$

    where $P_j$ is a tensor product of Pauli operators.

    Args:
        operator: Operator consists of pauli strings with their coefficients, represented in a sparse format.
        data: Quantum Variable on which the Pauli operators act. Its size must match the number of qubits required by the Pauli operator.
        block: Quantum variable that holds the superposition index used for conditional application of each term.
    """
    coefficients = [
        operator.terms[i].coefficient
        for i in range(operator.terms.len)  # type:ignore[attr-defined]
    ]
    lcu(
        coefficients,
        [
            lambda i=i: apply_pauli_term(operator.terms[i].paulis, data)
            for i in range(operator.terms.len)  # type:ignore[attr-defined]
        ],
        block,
    )
