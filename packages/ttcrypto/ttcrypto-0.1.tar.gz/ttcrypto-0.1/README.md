[![Version][version-image]][pypi-url]
[![Supported Python Version][py-versions-image]][pypi-url]
[![Downloads][downloads-image]][pypi-url]

---

# ttCrypto

Утилита для шифрования и расшифровки данных в буфере, поточно или в файле.

Библиотека содержит функции и консольную утилиту для работы с файлами.


## Установка

```sh
pip install ttcrypto
```


## Использование в коде

Простое шифрование/расшифровка (AES-256-GCM)

```python
from ttcrypto import aes

encrypted_bytes = aes.encrypt_gcm_plain(text_bytes, passphrase)
decrypted_bytes = aes.decrypt_gcm_plain(encrypted_bytes, passphrase)

assert to_string(decrypted_bytes) == text
```

Проточное шифрования по AES-256-GCM

```python
from ttcrypto import encrypt_gcm_generator

enc = encrypt_gcm_generator(passphrase)         # инициализируем генератор
encrypted_bytes = enc.send(None)                # генерируем salt + nonce для сессии
encrypted_bytes += enc.send(b'123')             # отправляем порцию данных (в цикле)
encrypted_bytes += enc.send(b'')                # отправляем пустую строку для финализации
encrypted_bytes = next(enc) + encrypted_bytes   # next вычисляет tag, ставим его в начало
# encrypted_bytes = tag(16) + salt(16) + nonce(16) + ciphertext
```

Проточная расшифровка по AES-256-GCM

```python
from ttcrypto import decrypt_gcm_generator

dec = decrypt_gcm_generator(passphrase) # инициализируем генератор
dec.send(None)                          # инициализируем ввод (всегда отвечает b'')
data = dec.send(encrypted_bytes)    # отправляем порцию данных (в цикле) - не менее 45 байт
data += dec.send(b'')               # отправляем b'' для финализации
# data - оригинальные расшифрованные данные
```


## Консольная утилита

Шифрование/расшифровка файла (интерактивный ввод секрета)

```sh
$ ttcrypto -e source.txt target.enc
$ ttcrypto -d source.enc target.txt
```

Шифрование с перезаписью целевого файла и передаченй секрета в команде

```sh
$ export TTCRYPTO_PASSPHRASE=123
$ ttcrypto -efp `echo $TTCRYPTO_PASSPHRASE` source.txt target.enc
```

Шифрование/расшифровке всех файлов в директории

```sh
$ ttcrypto -e source_dir encrypted_files_dir
$ ttcrypto -d encrypted_files_dir origin_files_dir
```

Шифрование файлов в директории, подходящих по имени

```sh
$ ttcrypto -e -n '*.txt' source_dir encrypted_files_dir
```


## Модуль криптографии AES-256-GCM (PBKDF2HMAC)

Cодержит:
- функции шифрования/расшифровки байтов (с полной буферизацией),
- функции-генераторы для поточного шифрования/расшифровки (без полной буферизации)
- функции для работы с BufferedIOBase объектами (с интерфейсов файлов)

Сложность реализации поточной обработки при использовании GCM алгоритма заключается в том,
что подпись (tag) вычисляется после обратки всех данных и как правило дописывается в конец файла.
Но при расшифровке подпись нужна до обратки данных - а чтение файла с конца не всегда возвожно.
Поэтому решено записывать тег в начало контейнера, вместе с другими метаданными:

`    tag(16) + salt(16) + nonce(12) + ciphertext`

При работе с файловыми объектами в начало записывается 16 нулевых байт - чтоб
зарезервировать место для подписи (tag). В конце шифрования, когда будет вычислен tag -
курсор переставляется в начало файла и 16 нулевых байт перезаписываются подписью.
Для системы которая один раз пишет - много читает, возможность сразу направить поток
расшифрованных данных потребителю критически важна.

- Файл 3,5Гб: шифрование ~ 4 сек, расшифровка ~ 3.8 сек (1 CPU ~ 70%, RAM ~ 50Мб)
- Файл 9,4Мб: шифрование ~ 17.7 мс, расшифровка ~ 16.8 мс
- Файл 68Кб: шифрование ~ 11 мс, расшифровка ~ 9.5 мс


<!-- Badges -->
[pypi-url]: https://pypi.org/project/ttcrypto
[version-image]: https://img.shields.io/pypi/v/ttcrypto.svg
[py-versions-image]: https://img.shields.io/pypi/pyversions/ttcrypto.svg
[downloads-image]: https://img.shields.io/pypi/dm/ttcrypto.svg
