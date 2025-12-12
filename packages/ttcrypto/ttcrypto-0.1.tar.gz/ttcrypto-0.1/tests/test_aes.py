from io import BytesIO

from ttutils import to_bytes, to_string

from ttcrypto import aes

passphrase = b'asdqwe123zxc'
text = 'абвгд%asd^123'
text_bytes = to_bytes(text, 'utf8')


def test_encrypt_decrypt_gcm_plain_ok() -> None:
    encrypted_bytes = aes.encrypt_gcm_plain(text_bytes, passphrase)
    decrypted_bytes = aes.decrypt_gcm_plain(encrypted_bytes, passphrase)
    assert to_string(decrypted_bytes) == text


def test_encrypt_gcm_generator_ok() -> None:
    enc = aes.encrypt_gcm_generator(passphrase)
    encrypted_bytes = enc.send(None)
    encrypted_bytes += enc.send(text_bytes)
    encrypted_bytes += enc.send(b'')
    encrypted_bytes = next(enc) + encrypted_bytes

    decrypted_bytes = aes.decrypt_gcm_plain(encrypted_bytes, passphrase)
    assert to_string(decrypted_bytes) == text


def test_decrypt_gcm_generator_ok() -> None:
    encrypted_bytes = aes.encrypt_gcm_plain(text_bytes, passphrase)

    dec = aes.decrypt_gcm_generator(passphrase)
    dec.send(None)
    decrypted_bytes = dec.send(encrypted_bytes)
    decrypted_bytes += dec.send(b'')

    assert to_string(decrypted_bytes) == text


def test_encrypt_gcm_io_ok() -> None:
    input_io = BytesIO(text_bytes)
    output_io = BytesIO(b'')

    aes.encrypt_gcm_io(passphrase, input_io, output_io)

    decrypted_bytes = aes.decrypt_gcm_plain(output_io.read(), passphrase)
    assert to_string(decrypted_bytes) == text


def test_decrypt_gcm_io_ok() -> None:
    encrypted_bytes = aes.encrypt_gcm_plain(text_bytes, passphrase)

    input_io = BytesIO(encrypted_bytes)
    output_io = BytesIO(b'')

    aes.decrypt_gcm_io(passphrase, input_io, output_io)

    assert to_string(output_io.read()) == text
