

SIGNATURE: str = 'VFONT1'

MAGIC: int = 167

def encrypt_bytes(data: bytes, salt_size: int = 2) -> bytes: ...

def decrypt_bytes(data: bytes) -> bytes: ...
