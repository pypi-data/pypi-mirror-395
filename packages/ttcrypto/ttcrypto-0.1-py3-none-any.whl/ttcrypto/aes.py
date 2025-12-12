'''
Модуль криптографии AES-256-GCM (PBKDF2HMAC)

Содержит:
- функции шифрования/расшифровки байтов (с полной буферизацией),
- функции-генераторы для поточного шифрования/расшифровки (без полной буферизации)
- функции для работы с BufferedIOBase объектами (с интерфейсов файлов)

Сложность реализации поточной обработки при использовании GCM алгоритма заключается в том,
что подпись (tag) вычисляется после обратки всех данных и как правило дописывается в конец файла.
Но при расшифровке подпись нужна до обратки данных - а чтение файла с конца не всегда возвожно.
Поэтому решено записывать тег в начало контейнера, вместе с другими метаданными:
    tag(16) + salt(16) + nonce(12) + ciphertext

При работе с файловыми объектами в начало записывается 16 нулевых байт - чтоб
зарезервировать место для подписи (tag). В конце шифрования, когда будет вычислен tag -
курсор переставляется в начало файла и 16 нулевых байт перезаписываются подписью.
Для системы которая один раз пишет - много читает, возможность сразу направить поток
расшифрованных данных потребителю критически важна.

Выбор CHUNK_SIZE = 1Мб обусловлен компромисом между временем обработки и потребляемой памятью.
При уменьшении CHUNK_SIZE - растет время обработки (примерно на 20% при 64Кб)
При увеличении CHUNK_SIZE - растет потреблении памяти (примерно 2 раза при 16Мб, скорость +20%)
Для систем с высоким параллелизмом потребление памяти может быть критичным.

Файл 3,5Гб: шифрование ~ 4 сек, расшифровка ~ 3.8 сек (1 CPU ~ 70%, RAM ~ 50Мб)
Файл 9,4Мб: шифрование ~ 17.7 мс, расшифровка ~ 16.8 мс
Файл 68Кб: шифрование ~ 11 мс, расшифровка ~ 9.5 мс
'''
from collections.abc import Generator
from io import BufferedIOBase
from os import urandom

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CHUNK_SIZE = 2 ** 20  # 1Мб


def derive_key_pbkdf2(passphrase: bytes, salt: bytes, iterations: int = 100_000) -> bytes:
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    ).derive(passphrase)


def encrypt_gcm_plain(data: bytes, passphrase: bytes) -> bytes:
    ''' Простое шифрования по AES-256-GCM '''
    salt = urandom(16)
    nonce = urandom(12)  # iv

    key = derive_key_pbkdf2(passphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()

    return encryptor.tag + salt + nonce + ciphertext


def encrypt_gcm_generator(passphrase: bytes) -> Generator[bytes, bytes | None, None]:
    '''
        Проточное шифрования по AES-256-GCM

        enc = encrypt_gcm_generator(passphrase)         # инициализируем генератор
        encrypted_bytes = enc.send(None)                # генерируем salt + nonce для сессии
        encrypted_bytes += enc.send(b'123')             # отправляем порцию данных (в цикле)
        encrypted_bytes += enc.send(b'')                # отправляем пустую строку для финализации
        encrypted_bytes = next(enc) + encrypted_bytes   # next вычисляет tag, ставим его в начало
        # encrypted_bytes = tag(16) + salt(16) + nonce(16) + ciphertext
    '''
    salt = urandom(16)
    nonce = urandom(12)  # iv

    key = derive_key_pbkdf2(passphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    encryptor = cipher.encryptor()

    chunk = yield salt + nonce

    while chunk:  # продолжаем пока send(...) отправляет не пустые данные
        chunk = yield encryptor.update(chunk)

    yield encryptor.finalize()
    yield encryptor.tag


def encrypt_gcm_io(passphrase: bytes, input_io: BufferedIOBase, output_io: BufferedIOBase) -> None:
    '''
        Поточно забираем данные из readable объекта, шифруем и записываем в writeable объект.

        with Path('encrypted_data').open('wb') as target:
            with Path('origin_data').open('rb') as source:
                encrypt_gcm_io(passphrase, source, target)
    '''
    enc = encrypt_gcm_generator(passphrase)
    output_io.write(b'\x00' * 16 + enc.send(None))  # резервируем 16 байт для тега в начале

    while True:
        if _data := input_io.read(CHUNK_SIZE):
            output_io.write(enc.send(_data))
        else:
            output_io.write(enc.send(b''))
            output_io.seek(0)  # дописываем тег в начало
            output_io.write(next(enc))
            break

    output_io.seek(0)
    input_io.seek(0)


def decrypt_gcm_plain(data: bytes, passphrase: bytes) -> bytes:
    ''' Простая расшифровка по AES-256-GCM '''
    # первые 44 байта - служебная информация (tag(16) + salt(16) + nonce(12))
    tag = data[:16]
    salt = data[16:32]
    nonce = data[32:44]

    key = derive_key_pbkdf2(passphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()

    ciphertext = data[44:]

    return decryptor.update(ciphertext) + decryptor.finalize()


def decrypt_gcm_generator(passphrase: bytes) -> Generator[bytes, bytes, None]:
    '''
        Проточная расшифровка по AES-256-GCM

        dec = decrypt_gcm_generator(passphrase) # инициализируем генератор
        dec.send(None)                          # инициализируем ввод (всегда отвечает b'')
        data = dec.send(encrypted_bytes)    # отправляем порцию данных (в цикле) - не менее 45 байт
        data += dec.send(b'')               # отправляем b'' для финализации
        # data - оригинальные расшифрованные данные
    '''

    chunk = yield b''

    # первые 44 байта - служебная информация (tag(16) + salt(16) + nonce(12))
    tag = chunk[:16]
    salt = chunk[16:32]
    nonce = chunk[32:44]

    key = derive_key_pbkdf2(passphrase, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()

    # важно чтобы данных в первой порции было не менее 45 байт (44 служебных + 1)
    # иначе расшифровка прервется
    chunk = chunk[44:]

    while chunk:  # продолжаем, пока входящие данные не пустые
        chunk = yield decryptor.update(chunk)

    yield decryptor.finalize()


def decrypt_gcm_io(passphrase: bytes, input_io: BufferedIOBase, output_io: BufferedIOBase) -> None:
    '''
        Поточно забираем данные из readable объекта, шифруем и записываем в writeable объект.

        with Path('decrypted_data').open('wb') as target:
            with Path('encrypted_data').open('rb') as source:
                decrypt_gcm_io(passphrase, source, target)
    '''
    dec = decrypt_gcm_generator(passphrase)
    dec.send(None)  # type: ignore

    try:
        while True:
            output_io.write(dec.send(input_io.read(CHUNK_SIZE)))
    except StopIteration:
        pass

    input_io.seek(0)
    output_io.seek(0)
