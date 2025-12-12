import argparse
from pathlib import Path

from ttcrypt.aes import decrypt_gcm_io, encrypt_gcm_io

parser = argparse.ArgumentParser(description='AES 256 GCM encryptor / decryptor util')
parser.add_argument('-d', '--decrypt', action='store_true')
parser.add_argument('-e', '--encrypt', action='store_true')
parser.add_argument('-f', '--find', type=str)
parser.add_argument('source', type=Path)
parser.add_argument('target', type=Path)


def run() -> None:
    call_args = parser.parse_args()

    if (call_args.encrypt and call_args.decrypt) or not (call_args.encrypt or call_args.decrypt):
        parser.exit(1, '\x1b[33mChoose one: encrypt or decrypt\x1b[0m\n')

    if not (passphrase := bytes(input('Passphrase:'), 'utf8')):
        parser.exit(1, '\x1b[33mEmpty passphrase\x1b[0m\n')

    if call_args.find:
        for _path in Path(call_args.source).glob(call_args.find):
            if call_args.encrypt:
                _encrypt_file(passphrase, _path, Path(call_args.target) / _path)
            elif call_args.decrypt:
                _decrypt_file(passphrase, _path, Path(call_args.target) / _path)
    elif call_args.encrypt:
        _encrypt_file(passphrase, Path(call_args.source), Path(call_args.target))
    elif call_args.decrypt:
        _decrypt_file(passphrase, Path(call_args.source), Path(call_args.target))

    parser.exit(0, '\x1b[32mSuccess\x1b[0m\n')


def _encrypt_file(passphrase: bytes, source_filename: Path, target_filename: Path) -> None:
    with Path(target_filename).open('wb') as target:
        with Path(target_filename).open('rb') as source:
            encrypt_gcm_io(passphrase, source, target)  # type: ignore


def _decrypt_file(passphrase: bytes, source_filename: Path, target_filename: Path) -> None:
    with Path(target_filename).open('wb') as target:
        with Path(target_filename).open('rb') as source:
            decrypt_gcm_io(passphrase, source, target)  # type: ignore
