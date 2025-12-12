import argparse
from contextlib import suppress
from unittest.mock import Mock, patch

import pytest

from ttcrypto import cmd


@pytest.mark.parametrize('action, force', [
    ('encrypt', True),
    ('decrypt', True),
    ('encrypt', False),
    ('decrypt', False),
])
@patch.object(cmd, '_decrypt_file')
@patch.object(cmd, '_encrypt_file')
@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_ok_file(args_mock, exit_mock, enc_mock, dec_mock, action, force):
    source = Mock(is_file=lambda: True, is_dir=lambda: False, exists=lambda: force)
    target = Mock(is_file=lambda: True, is_dir=lambda: False, exists=lambda: force)
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=action == 'decrypt',
        encrypt=action == 'encrypt',
        name=None,
        passphrase='123',
        force=force,
        source=source,
        target=target
    )

    with suppress(SystemExit):
        cmd.run()

    if action == 'encrypt':
        enc_mock.assert_called_once_with(b'123', source, target, force)
        dec_mock.assert_not_called()
    if action == 'decrypt':
        dec_mock.assert_called_once_with(b'123', source, target, force)
        enc_mock.assert_not_called()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 0


@pytest.mark.parametrize('action, flt, force', [
    ('encrypt', None, True),
    ('decrypt', None, True),
    ('encrypt', '*txt', False),
    ('decrypt', '*dec', False),
])
@patch.object(cmd, '_decrypt_file')
@patch.object(cmd, '_encrypt_file')
@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_ok_dir(args_mock, exit_mock, enc_mock, dec_mock, action, flt, force):
    source_file = Mock(exists=lambda: force)
    target_file = Mock(exists=lambda: force)
    source = Mock(is_file=lambda: False, is_dir=lambda: True, glob=lambda x: [source_file])
    target = Mock(is_file=lambda: False, is_dir=lambda: True)
    target.configure_mock(**{'__truediv__': Mock(return_value=target_file)})
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=action == 'decrypt',
        encrypt=action == 'encrypt',
        name=flt,
        passphrase='123',
        force=force,
        source=source,
        target=target
    )

    with suppress(SystemExit):
        cmd.run()

    if action == 'encrypt':
        enc_mock.assert_called_once_with(b'123', source_file, target_file, force)
        dec_mock.assert_not_called()
    if action == 'decrypt':
        dec_mock.assert_called_once_with(b'123', source_file, target_file, force)
        enc_mock.assert_not_called()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 0


@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_dir_file_exists(args_mock, exit_mock):
    source_file = Mock(exists=lambda: True)
    target_file = Mock(exists=lambda: True)
    source = Mock(is_file=lambda: False, is_dir=lambda: True, glob=lambda x: [source_file])
    target = Mock(is_file=lambda: False, is_dir=lambda: True)
    target.configure_mock(**{'__truediv__': Mock(return_value=target_file)})
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=False,
        encrypt=True,
        name=None,
        passphrase='123',
        force=False,
        source=source,
        target=target
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_dir_to_file(args_mock, exit_mock):
    source = Mock(is_file=lambda: False, is_dir=lambda: True)
    target = Mock(is_file=lambda: True, is_dir=lambda: False)
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=False,
        encrypt=True,
        name=None,
        passphrase='123',
        force=False,
        source=source,
        target=target
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@pytest.mark.parametrize('action', [True, False])
@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_encdec(args_mock, exit_mock, action):
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=action,
        encrypt=action,
        name=None,
        passphrase='123',
        force=False,
        source=Mock(),
        target=Mock()
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_target_not_exists(args_mock, exit_mock):
    source = Mock(is_file=lambda: True, is_dir=lambda: False)
    target = Mock(is_file=lambda: False, is_dir=lambda: False)
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=False,
        encrypt=True,
        name=None,
        passphrase='123',
        force=False,
        source=source,
        target=target
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@patch.object(cmd, 'getpass', Mock(return_value=''))
@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_no_pass(args_mock, exit_mock):
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=False,
        encrypt=True,
        name=None,
        passphrase=None,
        force=False,
        source=Mock(),
        target=Mock()
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@patch.object(cmd, 'getpass', Mock(side_effect=KeyboardInterrupt))
@patch.object(argparse.ArgumentParser, 'exit')
@patch.object(argparse.ArgumentParser, 'parse_args')
def test_run_err_keyboard_interrupt(args_mock, exit_mock):
    exit_mock.side_effect = SystemExit
    args_mock.return_value = argparse.Namespace(
        decrypt=False,
        encrypt=True,
        name=None,
        passphrase=None,
        force=False,
        source=Mock(),
        target=Mock()
    )

    with suppress(SystemExit):
        cmd.run()

    exit_mock.assert_called_once()
    assert exit_mock.call_args[0][0] == 1


@patch.object(cmd, '_decrypt_file')
@patch.object(cmd, '_encrypt_file')
def test_single_file_ok_no_action(enc_mock, dec_mock):
    args = argparse.Namespace(
        decrypt=False,
        encrypt=False,
        name=None,
        passphrase=None,
        force=True,
        source=Mock(),
        target=Mock()
    )

    cmd._single_file(b'123', args)

    enc_mock.assert_not_called()
    dec_mock.assert_not_called()


@patch.object(cmd, '_decrypt_file')
@patch.object(cmd, '_encrypt_file')
def test_many_files_ok_no_action(enc_mock, dec_mock):
    args = argparse.Namespace(
        decrypt=False,
        encrypt=False,
        name=None,
        passphrase=None,
        force=True,
        source=Mock(glob=Mock(return_value=[Mock()])),
        target=Mock(__truediv__=Mock(return_value=Mock(exists=lambda: False)))
    )

    cmd._many_files(b'123', args)

    enc_mock.assert_not_called()
    dec_mock.assert_not_called()


@patch.object(cmd, 'encrypt_gcm_io')
def test_encrypt_file_ok(enc_mock):
    open_mock = Mock(return_value=Mock(__enter__=Mock(), __exit__=Mock()))
    source = Mock(stat=Mock(return_value=Mock(st_size=123)), open=open_mock)
    target = Mock(open=open_mock)

    cmd._encrypt_file(b'123', source, target, False)

    open_mock.assert_any_call('rb')
    open_mock.assert_any_call('wb')
    enc_mock.assert_called_once()


@patch.object(cmd, 'decrypt_gcm_io')
def test_decrypt_file_ok(dec_mock):
    open_mock = Mock(return_value=Mock(__enter__=Mock(), __exit__=Mock()))
    source = Mock(stat=Mock(return_value=Mock(st_size=123)), open=open_mock)
    target = Mock(open=open_mock)

    cmd._decrypt_file(b'123', source, target, False)

    open_mock.assert_any_call('rb')
    open_mock.assert_any_call('wb')
    dec_mock.assert_called_once()


@pytest.mark.parametrize('size, expected', [
    (0, '0 bytes'),
    (500, '500 bytes'),
    (1024, '1 KB'),
    (2048, '2 KB'),
    (2500, '2 KB'),
    (1024 * 1024, '1 MB'),
    (5 * 1024 * 1024, '5 MB'),
    (1024**3, '1 GB'),
    (1024**4, '1 TB'),
    (2 * 1024**4, '2 TB'),
    (1024**5, '1 PB')
])
def test_human_size_ok(size: int, expected: str) -> None:
    assert cmd.human_size(size) == expected
