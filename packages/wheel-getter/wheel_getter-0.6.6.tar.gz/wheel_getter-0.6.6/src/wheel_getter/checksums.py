from enum import StrEnum
from hashlib import sha256


class Algo(StrEnum):
    SHA256 = "sha256"


def get_checksum(
        data: bytes,
        *,
        algo: str = Algo.SHA256,
        ) -> str:
    """
    Calculates the hash of a byte string and returns it (with an algorithm id).
    
    Currently only sha256 is supported.
    """
    if algo not in Algo:
        raise ValueError(f"invalid checksum algorithm “{algo}”")
    return f"sha256:{sha256(data).hexdigest()}"


def verify_checksum(
        data: bytes,
        hash: str,
        ) -> bool:
    """
    Verifies that the hash of a byte string agrees with a given value.
    
    The hash is always prefixed with an algorith id.
    Currently only sha256 is supported.
    """
    for algo in Algo:
        if hash.startswith(f"{algo}:"):
            ref = get_checksum(data, algo=algo)
            return hash == ref
    return False
