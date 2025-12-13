import warnings

from classiq.interface.exceptions import ClassiqDeprecationWarning

from classiq.qmod.builtins.functions.standard_gates import IDENTITY, RZ, H
from classiq.qmod.builtins.operations import control, if_, invert, repeat, within_apply
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CReal
from classiq.qmod.qmod_variable import QArray, QBit
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.symbolic import floor, min as qmin

from .qsvt import (
    projector_controlled_double_phase as projector_controlled_double_phase_new,
    projector_controlled_phase as projector_controlled_phase_new,
    qsvt as qsvt_new,
    qsvt_inversion as qsvt_inversion_new,
    qsvt_lcu as qsvt_lcu_new,
    qsvt_lcu_step as qsvt_lcu_step_new,
    qsvt_step as qsvt_step_new,
)


@qfunc
def qsvt_step_old(
    phase1: CReal,
    phase2: CReal,
    proj_cnot_1: QCallable[QArray[QBit], QBit],
    proj_cnot_2: QCallable[QArray[QBit], QBit],
    u: QCallable[QArray[QBit]],
    qvar: QArray[QBit],
    aux: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Applies a single QSVT step, composed of 2 projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:

    $$
    \\Pi_{\\phi_2}U^{\\dagger}\\tilde{\\Pi}_{\\phi_{1}}U
    $$

    Args:
        phase1: 1st rotation phase.
        phase2: 2nd rotation phase.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        qvar: The quantum variable to which U is applied, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    u(qvar)
    projector_controlled_phase_old(phase1, proj_cnot_2, qvar, aux)
    invert(lambda: u(qvar))
    projector_controlled_phase_old(phase2, proj_cnot_1, qvar, aux)


def qsvt_step(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Applies a single QSVT step, composed of 2 projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:

    $$
    \\Pi_{\\phi_2}U^{\\dagger}\\tilde{\\Pi}_{\\phi_{1}}U
    $$

    Args:
        phase1: 1st rotation phase.
        phase2: 2nd rotation phase.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a qubit that should be set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a qubit that should be set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    if len(args) + len(kwargs) == 7:
        return qsvt_step_old(*args, **kwargs)
    return qsvt_step_new(*args, **kwargs)


@qfunc
def qsvt_old(
    phase_seq: CArray[CReal],
    proj_cnot_1: QCallable[QArray[QBit], QBit],
    proj_cnot_2: QCallable[QArray[QBit], QBit],
    u: QCallable[QArray[QBit]],
    qvar: QArray[QBit],
    aux: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Implements the Quantum Singular Value Transformation (QSVT) - an algorithmic framework, used to apply polynomial transformations of degree `d` on the singular values of a block encoded matrix, given as the unitary `u`.    Given a unitary $U$, a list of phase angles  $\\phi_1, \\phi_2, ..., \\phi_{d+1}$ and 2 projector-controlled-not operands $C_{\\Pi}NOT,C_{\\tilde{\\Pi}}NOT$, the QSVT sequence is as follows:
    Given a unitary $U$, a list of phase angles  $\\phi_1, \\phi_2, ..., \\phi_{d+1}$ and 2 projector-controlled-not operands $C_{\\Pi}NOT,C_{\\tilde{\\Pi}}NOT$, the QSVT sequence is as follows:

    $$
    \\tilde{\\Pi}_{\\phi_{d+1}}U \\prod_{k=1}^{(d-1)/2} (\\Pi_{\\phi_{d-2k}} U^{\\dagger}\\tilde{\\Pi}_{\\phi_{d - (2k+1)}}U)\\Pi_{\\phi_{1}}
    $$

    for odd $d$, and:

    $$
    \\prod_{k=1}^{d/2} (\\Pi_{\\phi_{d-(2k-1)}} U^{\\dagger}\\tilde{\\Pi}_{\\phi_{d-2k}}U)\\Pi_{\\phi_{1}}
    $$

    for even $d$.

    Each of the $\\Pi$s is a projector-controlled-phase unitary, according to the given projectors.

    Args:
        phase_seq: A sequence of phase angles of length d+1.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        qvar: The quantum variable to which U is applied, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    H(aux)

    projector_controlled_phase_old(phase_seq[0], proj_cnot_1, qvar, aux)
    repeat(
        count=floor((phase_seq.len - 1) / 2),
        iteration=lambda index: qsvt_step_old(
            phase_seq[2 * index + 1],
            phase_seq[2 * index + 2],
            proj_cnot_1,
            proj_cnot_2,
            u,
            qvar,
            aux,
        ),
    )

    if_(
        condition=phase_seq.len % 2 == 1,
        then=lambda: IDENTITY(qvar),
        else_=lambda: (
            u(qvar),
            projector_controlled_phase_old(
                phase_seq[phase_seq.len - 1],
                proj_cnot_2,
                qvar,
                aux,
            ),
        ),
    )

    H(aux)


def qsvt(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Implements the Quantum Singular Value Transformation (QSVT) - an algorithmic framework, used to apply polynomial transformations of degree `d` on the singular values of a block encoded matrix, given as the unitary `u`.    Given a unitary $U$, a list of phase angles  $\\phi_1, \\phi_2, ..., \\phi_{d+1}$ and 2 projector-controlled-not operands $C_{\\Pi}NOT,C_{\\tilde{\\Pi}}NOT$, the QSVT sequence is as follows:
    Given a unitary $U$, a list of phase angles  $\\phi_1, \\phi_2, ..., \\phi_{d+1}$ and 2 projector-controlled-not operands $C_{\\Pi}NOT,C_{\\tilde{\\Pi}}NOT$, the QSVT sequence is as follows:

    $$
    \\tilde{\\Pi}_{\\phi_{d+1}}U \\prod_{k=1}^{(d-1)/2} (\\Pi_{\\phi_{d-2k}} U^{\\dagger}\\tilde{\\Pi}_{\\phi_{d - (2k+1)}}U)\\Pi_{\\phi_{1}}
    $$

    for odd $d$, and:

    $$
    \\prod_{k=1}^{d/2} (\\Pi_{\\phi_{d-(2k-1)}} U^{\\dagger}\\tilde{\\Pi}_{\\phi_{d-2k}}U)\\Pi_{\\phi_{1}}
    $$

    for even $d$.

    Each of the $\\Pi$s is a projector-controlled-phase unitary, according to the given projectors.

    Args:
        phase_seq: A sequence of phase angles of length d+1.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a qubit that should be set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a qubit that should be set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    if len(args) + len(kwargs) == 6:
        warnings.warn(
            "The 'qsvt' function signature has changed and the old version will be deprecated"
            " starting on 2025-12-13 at the earliest",
            ClassiqDeprecationWarning,
            stacklevel=2,
        )
        return qsvt_old(*args, **kwargs)
    return qsvt_new(*args, **kwargs)


@qfunc
def projector_controlled_phase_old(
    phase: CReal,
    proj_cnot: QCallable[QArray[QBit], QBit],
    qvar: QArray[QBit],
    aux: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Assigns a phase to the entire subspace determined by the given projector. Corresponds to the operation:

    $$
    \\Pi_{\\phi} = (C_{\\Pi}NOT) e^{-i\frac{\\phi}{2}Z}(C_{\\Pi}NOT)
    $$

    Args:
        phase: A rotation phase.
        proj_cnot: Projector-controlled-not unitary that sets an auxilliary qubit to |1> when the state is in the projection.
        qvar: The quantum variable to which the rotation applies, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotation. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    within_apply(lambda: proj_cnot(qvar, aux), lambda: RZ(phase, aux))


def projector_controlled_phase(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Assigns a phase to the entire subspace determined by the given projector. Corresponds to the operation:

    $$
    \\Pi_{\\phi} = (C_{\\Pi}NOT) e^{-i\frac{\\phi}{2}Z}(C_{\\Pi}NOT)
    $$

    Args:
        phase: A rotation phase.
        proj_cnot: Projector-controlled-not unitary that sets an auxilliary qubit to |1> when the state is in the projection.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotation.
    """
    if len(args) + len(kwargs) == 4:
        return projector_controlled_phase_old(*args, **kwargs)
    return projector_controlled_phase_new(*args, **kwargs)


@qfunc
def qsvt_inversion_old(
    phase_seq: CArray[CReal],
    block_encoding_cnot: QCallable[QArray[QBit], QBit],
    u: QCallable[QArray[QBit]],
    qvar: QArray[QBit],
    aux: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Implements matrix inversion on a given block-encoding of a square matrix, using the QSVT framework. Applies a polynomial approximation
    of the inverse of the singular values of the matrix encoded in `u`. The phases for the polynomial should be pre-calculated and passed into the function.

    Args:
        phase_seq: A sequence of phase angles of length d+1, corresponding to an odd polynomial approximation of the scaled inverse function.
        block_encoding_cnot: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        qvar: The quantum variable to which U is applied, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    qsvt_old(
        phase_seq,
        block_encoding_cnot,
        block_encoding_cnot,
        lambda x: invert(lambda: u(x)),
        qvar,
        aux,
    )


def qsvt_inversion(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Implements matrix inversion on a given block-encoding of a square matrix, using the QSVT framework. Applies a polynomial approximation
    of the inverse of the singular values of the matrix encoded in `u`. The phases for the polynomial should be pre-calculated and passed into the function.

    Args:
        phase_seq: A sequence of phase angles of length d+1, corresponding to an odd polynomial approximation of the scaled inverse function.
        block_encoding_cnot: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable that should be set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
    """
    if len(args) + len(kwargs) == 5:
        warnings.warn(
            "The 'qsvt_inversion' function signature has changed and the old version will be deprecated"
            " starting on 2025-12-13 at the earliest",
            ClassiqDeprecationWarning,
            stacklevel=2,
        )
        return qsvt_inversion_old(*args, **kwargs)
    return qsvt_inversion_new(*args, **kwargs)


@qfunc
def projector_controlled_double_phase_old(
    phase_even: CReal,
    phase_odd: CReal,
    proj_cnot: QCallable[QArray[QBit], QBit],
    qvar: QArray[QBit],
    aux: QBit,
    lcu: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Assigns 2 phases to the entire subspace determined by the given projector, each one is controlled differentely on a given `lcu` qvar.
    Used in the context of the `qsvt_lcu` function. Corresponds to the operation:

    $$
    \\Pi_{\\phi_{odd}, \\phi_{even}} = (C_{\\Pi}NOT) (C_{lcu=1}e^{-i\\frac{\\phi_{even}}{2}Z}) (C_{lcu=0}e^{-i\\frac{\\phi_{odd}}{2}Z}) (C_{\\Pi}NOT)
    $$

    Args:
        phase_even: Rotation phase, corresponds to 'lcu'=0.
        phase_odd: Rotation phase, corresponds to 'lcu'=1.
        proj_cnot: Projector-controlled-not unitary that sets an auxilliary qubit to |1> when the state is in the projection.
        qvar: The quantum variable to which the rotation applies, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotation. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: The quantum variable used for controlling the phase assignment.
    """
    within_apply(
        lambda: proj_cnot(qvar, aux),
        lambda: control(lcu, lambda: RZ(phase_odd, aux), lambda: RZ(phase_even, aux)),
    )


def projector_controlled_double_phase(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Assigns 2 phases to the entire subspace determined by the given projector, each one is controlled differentely on a given `lcu` qvar.
    Used in the context of the `qsvt_lcu` function. Corresponds to the operation:

    $$
    \\Pi_{\\phi_{odd}, \\phi_{even}} = (C_{\\Pi}NOT) (C_{lcu=1}e^{-i\\frac{\\phi_{even}}{2}Z}) (C_{lcu=0}e^{-i\\frac{\\phi_{odd}}{2}Z}) (C_{\\Pi}NOT)
    $$

    Args:
        phase_even: Rotation phase, corresponds to 'lcu'=0.
        phase_odd: Rotation phase, corresponds to 'lcu'=1.
        proj_cnot: Projector-controlled-not unitary that sets an auxilliary qubit to |1> when the state is in the projection.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotation. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: The quantum variable used for controlling the phase assignment.
    """
    if len(args) + len(kwargs) == 6:
        return projector_controlled_double_phase_old(*args, **kwargs)
    return projector_controlled_double_phase_new(*args, **kwargs)


@qfunc
def qsvt_lcu_step_old(
    phases_even: CArray[CReal],
    phases_odd: CArray[CReal],
    proj_cnot_1: QCallable[QArray[QBit], QBit],
    proj_cnot_2: QCallable[QArray[QBit], QBit],
    u: QCallable[QArray[QBit]],
    qvar: QArray[QBit],
    aux: QBit,
    lcu: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Applies a single QSVT-lcu step, composed of 2 double phase projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:

    $$
    (C_{lcu=1}\\Pi^{even}_{\\phi_2})(C_{lcu=0}\\Pi^{odd}_{\\phi_2})U^{\\dagger}(C_{lcu=1}\\tilde{\\Pi}^{even}_{\\phi_1})(C_{lcu=0}\\tilde{\\Pi}^{odd}_{\\phi_1})U
    $$

    Args:
        phases_even: 2 rotation phases for the even polynomial
        phases_odd: 2 rotation phases for the odd polynomial
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        qvar: The quantum variable to which U is applied, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: A qubit used for the combination of 2 polynomials within a single qsvt application
    """
    u(qvar)
    projector_controlled_double_phase_old(
        phases_even[0], phases_odd[0], proj_cnot_2, qvar, aux, lcu
    )
    invert(lambda: u(qvar))
    projector_controlled_double_phase_old(
        phases_even[1], phases_odd[1], proj_cnot_1, qvar, aux, lcu
    )


def qsvt_lcu_step(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Applies a single QSVT-lcu step, composed of 2 double phase projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:

    $$
    (C_{lcu=1}\\Pi^{even}_{\\phi_2})(C_{lcu=0}\\Pi^{odd}_{\\phi_2})U^{\\dagger}(C_{lcu=1}\\tilde{\\Pi}^{even}_{\\phi_1})(C_{lcu=0}\\tilde{\\Pi}^{odd}_{\\phi_1})U
    $$

    Args:
        phases_even: 2 rotation phases for the even polynomial
        phases_odd: 2 rotation phases for the odd polynomial
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a qubit that should be set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a qubit that should be set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: A qubit used for the combination of 2 polynomials within a single qsvt application
    """
    if len(args) + len(kwargs) == 8:
        return qsvt_lcu_step_old(*args, **kwargs)
    return qsvt_lcu_step_new(*args, **kwargs)


@qfunc
def qsvt_lcu_old(
    phase_seq_even: CArray[CReal],
    phase_seq_odd: CArray[CReal],
    proj_cnot_1: QCallable[QArray[QBit], QBit],
    proj_cnot_2: QCallable[QArray[QBit], QBit],
    u: QCallable[QArray[QBit]],
    qvar: QArray[QBit],
    aux: QBit,
    lcu: QBit,
) -> None:
    """
    [Qmod Classiq-library function]

    Implements the Quantum Singular Value Transformation (QSVT) for a linear combination of odd and even polynomials, so that
    it is possible to encode a polynomial of indefinite parity, such as approximation to exp(i*A) or exp(A). Should work
    for Hermitian block encodings.

    The function is equivalent to applying the `qsvt` function for odd and even polynomials with a LCU function, but
    is more efficient as the two polynomials share the same applications of the given unitary.

    The function is intended to be called within a context of LCU, where it is called as the SELECT operator, and wrapped
    with initialization of the `lcu` qubit to get the desired combination coefficients.
    The even polynomial corresponds to the case where the $lcu=|0\\rangle$, while the odd to $lcu=|1\\rangle$.

    Note: the two polynomials should have the same degree up to a difference of 1.

    Args:
        phase_seq_odd: A sequence of phase angles of length d+(d%2) for the odd polynomial.
        phase_seq_even: A sequence of phase angles of length d+(d+1)%2 for the even polynomial.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a quantum variable of the same size as qvar, and a qubit that is set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        qvar: The quantum variable to which U is applied, which resides in the entire block encoding space.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: A qubit used for the combination of 2 polynomials within a single qsvt application
    """
    H(aux)
    projector_controlled_double_phase_old(
        phase_seq_even[0], phase_seq_odd[0], proj_cnot_1, qvar, aux, lcu
    )
    repeat(
        count=floor((qmin(phase_seq_odd.len - 1, phase_seq_even.len - 1)) / 2),
        iteration=lambda index: qsvt_lcu_step_old(
            phase_seq_even[2 * index + 1 : 2 * index + 3],
            phase_seq_odd[2 * index + 1 : 2 * index + 3],
            proj_cnot_1,
            proj_cnot_2,
            u,
            qvar,
            aux,
            lcu,
        ),
    )
    if_(
        condition=phase_seq_odd.len > phase_seq_even.len,
        then=lambda: control(
            lcu,
            lambda: [
                u(qvar),
                projector_controlled_phase_old(
                    phase_seq_odd[phase_seq_odd.len - 1], proj_cnot_2, qvar, aux
                ),
            ],
        ),
    )
    if_(
        condition=phase_seq_odd.len < phase_seq_even.len,
        then=lambda: (
            u(qvar),
            projector_controlled_double_phase_old(
                phase_seq_even[phase_seq_even.len - 2],
                phase_seq_odd[phase_seq_odd.len - 1],
                proj_cnot_2,
                qvar,
                aux,
                lcu,
            ),
            control(
                lcu == 0,
                lambda: [
                    invert(lambda: u(qvar)),
                    projector_controlled_phase_old(
                        phase_seq_even[phase_seq_even.len - 1], proj_cnot_1, qvar, aux
                    ),
                ],
            ),
        ),
    )
    H(aux)


def qsvt_lcu(*args, **kwargs):  # type: ignore[no-untyped-def]
    """
    [Qmod Classiq-library function]

    Implements the Quantum Singular Value Transformation (QSVT) for a linear combination of odd and even polynomials, so that
    it is possible to encode a polynomial of indefinite parity, such as approximation to exp(i*A) or exp(A). Should work
    for Hermitian block encodings.

    The function is equivalent to applying the `qsvt` function for odd and even polynomials with a LCU function, but
    is more efficient as the two polynomials share the same applications of the given unitary.

    The function is intended to be called within a context of LCU, where it is called as the SELECT operator, and wrapped
    with initialization of the `lcu` qubit to get the desired combination coefficients.
    The even polynomial corresponds to the case where the $lcu=|0\\rangle$, while the odd to $lcu=|1\\rangle$.

    Note: the two polynomials should have the same degree up to a difference of 1.

    Args:
        phase_seq_odd: A sequence of phase angles of length d+(d%2) for the odd polynomial.
        phase_seq_even: A sequence of phase angles of length d+(d+1)%2 for the even polynomial.
        proj_cnot_1: Projector-controlled-not unitary that locates the encoded matrix columns within U. Accepts a qubit that should be set to |1> when the state is in the block.
        proj_cnot_2: Projector-controlled-not unitary that locates the encoded matrix rows within U. Accepts a qubit that should be set to |1> when the state is in the block.
        u: A block encoding unitary matrix.
        aux: A zero auxilliary qubit, used for the projector-controlled-phase rotations. Given as an inout so that qsvt can be used as a building-block in a larger algorithm.
        lcu: A qubit used for the combination of 2 polynomials within a single qsvt application
    """
    if len(args) + len(kwargs) == 8:
        warnings.warn(
            "The 'qsvt_lcu' function signature has changed and the old version will be deprecated"
            " starting on 2025-12-13 at the earliest",
            ClassiqDeprecationWarning,
            stacklevel=2,
        )
        return qsvt_lcu_old(*args, **kwargs)
    return qsvt_lcu_new(*args, **kwargs)
