import numpy as np

NUMERIC_TYPES = (int, float, np.int32, np.int64, np.float32, np.float64)


def is_numeric(obj):
    return isinstance(obj, NUMERIC_TYPES)


def parse_pauli_sum_str(psum_str):
    psum_str = psum_str.replace(" ", "")
    # Rename ** so that it doesn't get removed
    psum_str = psum_str.replace("**", "EXPONENT")
    psum_str = psum_str.replace("*", "")
    psum_str = psum_str.replace("EXPONENT", "**")
    if "j" in psum_str:
        raise Exception("Pauli string coefficient must not be complex")
    if "x" in psum_str:
        raise Exception("Use * for multiplication instead of x")
    pstrings = psum_str.split("+")

    def parse_pauli_string(pstring):
        if len(pstring) == 0:
            raise Exception("Empty Pauli string element")
        first_operator_index = 0
        for i, c in enumerate(pstring):
            if c in "IXYZ":
                first_operator_index = i
                break
        if i == 0:
            # No number is specified
            coefficient = 1.0
        elif i == 1 and pstring[0] == "-":
            coefficient = -1.0
        else:
            coefficient = float(pstring[:first_operator_index])
        pstring_itself = pstring[first_operator_index:]
        return pstring_itself, coefficient

    out = [parse_pauli_string(pstring) for pstring in pstrings]

    # Sanity check
    pstring_length = len(out[0][0])
    for ps, _ in out:
        if len(ps) != pstring_length:
            raise Exception(
                "One of the Pauli strings has mismatched length with the first Pauli"
                " string"
            )

    return out


def format_pauli_sum(pauli_sum):
    if not isinstance(pauli_sum, (str, list, tuple)):
        raise TypeError(f"Unsupported format type for Pauli sum: {type(pauli_sum)}")
    if isinstance(pauli_sum, str):
        return [parse_pauli_sum_str(pauli_sum)]
    if len(pauli_sum) == 0:
        raise Exception("The Pauli sum is an empty list/tuple")

    def isa_pauli_string_tuple(e):
        first_condition = len(e) == 2 and isinstance(e[0], str)
        if first_condition and isinstance(e[1], complex):
            raise Exception(
                f"The Pauli string tuple coefficient must not be complex {e}"
            )
        return first_condition and is_numeric(e[1])

    def parse(e):
        if isinstance(e, str):
            return parse_pauli_sum_str(e)
        if isinstance(e, (list, tuple)):
            if isa_pauli_string_tuple(e):
                # pauli_sum is a single Pauli sum
                return e
            if all(isa_pauli_string_tuple(ee) for ee in e):
                # pauli_sum is a list of Pauli sum
                return e
            raise Exception(
                f"Unsupported format type for Pauli sum element {e}: {type(e)}"
            )
        raise Exception(f"Unsupported format type for Pauli sum element {e}: {type(e)}")

    return [parse(e) for e in pauli_sum]
