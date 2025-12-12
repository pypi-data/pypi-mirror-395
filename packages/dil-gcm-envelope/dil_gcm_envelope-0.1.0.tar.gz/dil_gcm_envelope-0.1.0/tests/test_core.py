import json
from dil_gcm_envelope import encrypt, decrypt

PASSWORD = "test-password-123"

def test_encrypt_decrypt_sha256():
    payload = {"hello": "world", "n": 5}
    enc = encrypt(PASSWORD, payload, use_pbkdf2=False)
    assert set(enc.keys()) >= {"payload", "iv", "tag", "kdf"}
    assert enc["kdf"] == "sha256"
    pt_bytes = decrypt(PASSWORD, enc["payload"], enc["iv"], enc["tag"])
    assert json.loads(pt_bytes.decode("utf-8")) == payload

def test_encrypt_decrypt_pbkdf2():
    payload = "a simple string"
    enc = encrypt(PASSWORD, payload, use_pbkdf2=True, pbkdf2_iterations=5000)
    assert enc["kdf"] == "pbkdf2"
    assert "salt" in enc
    pt_bytes = decrypt(PASSWORD, enc["payload"], enc["iv"], enc["tag"], salt_b64=enc["salt"], pbkdf2_iterations=5000)
    assert pt_bytes.decode("utf-8") == payload
