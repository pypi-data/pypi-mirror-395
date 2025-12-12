import argparse
import sys
from getpass import getpass
from pathlib import Path
from time import monotonic

from ttcrypto.aes import decrypt_gcm_io, encrypt_gcm_io

parser = argparse.ArgumentParser(
    description='AES 256 GCM encryptor / decryptor util',
    epilog=(
        'You can only run encryption or decryption at a time. '
        'If a passphrase is not specified, it will be requested interactively.'
    )
)
parser.add_argument('-d', '--decrypt', action='store_true', help='Ecncrypt file(s)')
parser.add_argument('-e', '--encrypt', action='store_true', help='Decrypt file(s)')
parser.add_argument('-n', '--name', type=str, help='Matching file name patterns in a dir')
parser.add_argument('-f', '--force', action='store_true', help='Force overwrite existing files')
parser.add_argument('-p', '--passphrase', type=str, help='Set passphrase')
parser.add_argument('source', type=Path, help='Source file or dir')
parser.add_argument('target', type=Path, help='Target file or dir')


def run() -> None:
    call_args = parser.parse_args()

    if call_args.encrypt and not call_args.decrypt:
        action = 'encrypt'
    elif not call_args.encrypt and call_args.decrypt:
        action = 'decrypt'
    else:
        parser.exit(1, '\x1b[33mChoose one: encrypt or decrypt\x1b[0m\n')

    try:
        passphrase_raw = call_args.passphrase or getpass(
            f'Enter \x1b[36m{action}ion\x1b[0m passphrase: ')
    except KeyboardInterrupt:
        parser.exit(1, '\n\x1b[33mInterrupted by user\x1b[0m\n')

    if not (passphrase := bytes(passphrase_raw, 'utf8')):
        parser.exit(1, '\x1b[33mEmpty passphrase\x1b[0m\n')

    start_time = monotonic()

    if call_args.source.is_file():
        _single_file(passphrase, call_args)
    elif call_args.source.is_dir() and call_args.target.is_dir():
        _many_files(passphrase, call_args)
    else:
        parser.exit(1, '\x1b[33mError: the source and target must be a file or dir\x1b[0m\n')

    parser.exit(0, f'\x1b[32mSuccess\x1b[0m {monotonic() - start_time:.3f} sec\n')


def _single_file(passphrase: bytes, call_args: argparse.Namespace) -> None:
    if (exists := call_args.target.exists()) and not call_args.force:
        parser.exit(1, f'\x1b[33mError: source file exists\x1b[0m `{call_args.target}`\n')

    if call_args.encrypt:
        _encrypt_file(passphrase, call_args.source, call_args.target, exists)
    elif call_args.decrypt:
        _decrypt_file(passphrase, call_args.source, call_args.target, exists)


def _many_files(passphrase: bytes, call_args: argparse.Namespace) -> None:
    file_paths = sorted(tuple(call_args.source.glob(call_args.name or '*')))
    file_qty = len(file_paths)

    text = f'Find \x1b[36m{file_qty}\x1b[0m files in dir \x1b[36m`{call_args.source}`\x1b[0m'
    if call_args.name:
        text += f' with name \x1b[36m`{call_args.name}`\x1b[0m'
    sys.stdout.write(text + '\n')

    for num, _path in enumerate(file_paths):
        target = call_args.target / _path.name

        if (exists := target.exists()) and not call_args.force:
            parser.exit(1, f'\x1b[33mError: source file exists\x1b[0m `{target}`\n')

        sys.stdout.write(f'\x1b[36m[{num + 1}/{file_qty}]\x1b[0m  ')

        if call_args.encrypt:
            _encrypt_file(passphrase, _path, target, exists)
        elif call_args.decrypt:
            _decrypt_file(passphrase, _path, target, exists)


def _encrypt_file(passphrase: bytes, source_path: Path, target_path: Path, force: bool) -> None:
    size = human_size(source_path.stat().st_size)
    _force = '\x1b[33m[rewrite]\x1b[0m' if force else ''
    sys.stdout.write(f'Run encryption `{source_path}` ({size}) > `{target_path}` {_force}\n')

    with source_path.open('rb') as source:
        with target_path.open('wb') as target:
            encrypt_gcm_io(passphrase, source, target)


def _decrypt_file(passphrase: bytes, source_path: Path, target_path: Path, force: bool) -> None:
    size = human_size(source_path.stat().st_size)
    _force = '\x1b[33m[rewrite]\x1b[0m' if force else ''
    sys.stdout.write(f'Run decryption `{source_path}` ({size}) > `{target_path}` {_force}\n')

    with source_path.open('rb') as source:
        with target_path.open('wb') as target:
            decrypt_gcm_io(passphrase, source, target)


def human_size(size: int, units: list[str] = [' bytes', ' KB', ' MB', ' GB', ' TB']) -> str:  # noqa
    if not units:
        return str(size) + ' PB'
    return str(size) + units[0] if size < 1024 else human_size(size >> 10, units[1:])  # noqa
