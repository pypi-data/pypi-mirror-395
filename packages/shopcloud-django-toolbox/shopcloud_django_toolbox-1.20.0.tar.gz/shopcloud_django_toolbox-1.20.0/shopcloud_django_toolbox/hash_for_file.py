import base64
import hashlib


def hash_for_file(filepath: str, algorithm: str = "sha384") -> str:
    with open(filepath, "rb") as f:
        content = f.read()
    if algorithm not in dir(hashlib):
        raise NotImplementedError
    func = getattr(hashlib, algorithm)
    filehash = func(content).digest()
    hash_base64 = base64.b64encode(filehash).decode()
    return f"{algorithm}-{hash_base64}"
