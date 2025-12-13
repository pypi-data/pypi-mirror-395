from typing import Literal

import numpy as np

from classiq.qmod.builtins.functions.allocation import free
from classiq.qmod.builtins.functions.standard_gates import CX, SWAP, X
from classiq.qmod.builtins.operations import allocate, bind, control, invert, repeat
from classiq.qmod.qfunc import qperm
from classiq.qmod.qmod_variable import Input, Output, QArray, QBit, QNum


def get_rewire_list(qvars: list[QBit]) -> list[QBit]:
    rewire_list = qvars[int(np.log2(len(qvars))) :]
    for i, qvar in enumerate(qvars[: int(np.log2(len(qvars)))]):
        rewire_list.insert(2 ** (i + 1) - 1, qvar)
    return rewire_list


@qperm
def inplace_binary_to_one_hot(qvar: QArray) -> None:
    """
    Inplace conversion of binary encoded value to one-hot encoding.
    The implementation is based on https://quantumcomputing.stackexchange.com/questions/5526/garbage-free-reversible-binary-to-unary-decoder-construction.
    The input is assumed to be of size 2^n, where n is the number of bits in the binary representation.
    For example, the state |01000>=|2> will be converted to |00100> (one-hot for 2).

    Args:
        qvar: binary input array padded with 0's to be converted to one-hot encoding.
    """
    temp_qvars = [QBit(f"x{i}") for i in range(qvar.len)]
    bind(qvar, temp_qvars)  # type: ignore[arg-type]
    bind(get_rewire_list(temp_qvars), qvar)  # type: ignore[arg-type]

    # logic
    X(qvar[0])
    for i in range(int(np.log2(qvar.len))):
        index = 2 ** (i + 1) - 1
        for j in range(2**i - 1):
            control(qvar[index], lambda i=i, j=j: SWAP(qvar[j], qvar[j + 2**i]))  # type: ignore[misc]
        for j in range(2**i - 1):
            CX(qvar[j + 2**i], qvar[index])

        CX(qvar[index], qvar[index - 2**i])


@qperm
def inplace_one_hot_to_unary(qvar: QArray) -> None:
    """
    Inplace conversion of one-hot encoded value to unary encoding.
    The input is assumed to be of size n, where n is the number of bits in the one-hot representation.
    The remaining unary representation will at the higher n-1 bits, where the lsb is cleared to 0.
    For example, the state |0010> (one-hot for 2) will be converted to |0>|110> (unary for 2).

    Args:
        qvar: one-hot input array to be converted to unary encoding.
    """
    # fill with 1s after the leading 1 bit
    repeat(qvar.len - 1, lambda i: CX(qvar[qvar.len - i - 1], qvar[qvar.len - i - 2]))
    # clear the 0 bit, to be excluded from the unary encoding
    X(qvar[0])


@qperm
def one_hot_to_unary(one_hot: Input[QArray], unary: Output[QArray]) -> None:
    """
    Conversion of one-hot encoded value to unary encoding. The output `unary` variable
    is smaller in 1 qubit than the input `one_hot` variable.
    For example, the state |0010> (one-hot for 2) will be converted to |110> (unary for 2).

    Args:
        one_hot: one-hot input array to be converted to unary encoding.
        unary: unary output array.
    """
    inplace_one_hot_to_unary(one_hot)
    lsb: QBit = QBit()
    bind(one_hot, [lsb, unary])
    free(lsb)


@qperm
def one_hot_to_binary(
    one_hot: Input[QArray],
    binary: Output[QNum[Literal["ceiling(log(one_hot.len, 2))"]]],
) -> None:
    """
    Conversion of one-hot encoded value to binary encoding. The output `binary` variable
    is of size log2(one_hot.size) rounded up.
    For example, the state |0010> (one-hot for 2) will be converted to |01>=|2>.

    Args:
        one_hot: one-hot input array to be converted to binary encoding.
        binary: binary output variable.
    """
    extension: QArray = QArray()
    invert(lambda: inplace_binary_to_one_hot(one_hot))
    bind(one_hot, [binary, extension])
    free(extension)


@qperm
def unary_to_binary(unary: Input[QArray], binary: Output[QNum]) -> None:
    """
    Conversion of unary encoded value to binary encoding.  The output `binary` variable
    is of size log2(unary.size + 1) rounded up.
    For example, the state |110> (unary for 2) will be converted to |01>=|2>.

    Args:
        unary: unary input array to be converted to binary encoding.
        binary: binary output variable.
    """
    one_hot: QArray = QArray()
    unary_to_one_hot(unary, one_hot)
    one_hot_to_binary(one_hot, binary)


@qperm
def unary_to_one_hot(unary: Input[QArray], one_hot: Output[QArray]) -> None:
    """
    Conversion of unary encoded value to one-hot encoding. The output `one_hot` variable
    is larger in 1 qubit than the input `unary` variable.
    For example, the state |110> (unary for 2) will be converted to |0010> (one-hot for 2).

    Args:
        unary: unary input array to be converted to one-hot encoding.
        one_hot: one-hot output array.
    """
    lsb: QBit = QBit()
    allocate(lsb)
    bind([lsb, unary], one_hot)
    invert(lambda: inplace_one_hot_to_unary(one_hot))


@qperm
def binary_to_one_hot(binary: Input[QNum], one_hot: Output[QArray]) -> None:
    """
    Conversion of binary encoded value to one-hot encoding. The output `one_hot` variable
    is of size 2^n, where n is the number of bits in the binary representation.
    For example, the state |01>=|2> will be converted to |0010> (one-hot for 2).

    Args:
        binary: binary input variable to be converted to one-hot encoding.
        one_hot: one-hot output array.
    """
    extension: QArray = QArray()
    allocate(2**binary.size - binary.size, extension)
    bind([binary, extension], one_hot)

    inplace_binary_to_one_hot(one_hot)


@qperm
def binary_to_unary(binary: Input[QNum], unary: Output[QArray]) -> None:
    """
    Conversion of binary encoded value to unary encoding. The output `unary` variable
    is of size 2^n - 1, where n is the number of bits in the binary representation.
    For example, the state |01>=|2> will be converted to |110> (unary for 2).

    Args:
        binary: binary input variable to be converted to unary encoding.
        unary: unary output array.
    """
    one_hot: QArray = QArray()
    binary_to_one_hot(binary, one_hot)
    one_hot_to_unary(one_hot, unary)


@qperm
def pad_zeros(total_size: int, qvar: Input[QArray], padded: Output[QArray]) -> None:
    """
    Pad the input qvar with additional qubits at the end to reach the total_size.

    Args:
        total_size: The desired total size after padding.
        qvar: The input quantum array to be padded.
        padded: The output quantum array after padding.
    """
    extension: QArray = QArray()
    allocate(total_size - qvar.len, extension)
    bind([qvar, extension], padded)


# TODO: when the functions can have default arguments, add `pad` function with direction and value
