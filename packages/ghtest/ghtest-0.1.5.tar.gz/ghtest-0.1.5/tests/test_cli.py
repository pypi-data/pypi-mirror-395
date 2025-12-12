import pytest
import sys
from unittest.mock import patch
from ghtest.cli import main

def test_cli_help():
    with patch.object(sys, 'argv', ['ghtest', '--help']):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 0

def test_cli_version():
    with patch.object(sys, 'argv', ['ghtest', '--version']):
        with pytest.raises(SystemExit) as cm:
            main()
        assert cm.value.code == 0

@patch('ghtest.cli.create_tests')
def test_cli_run_basic(mock_create_tests):
    with patch.object(sys, 'argv', ['ghtest', 'testdata']):
        main()
        mock_create_tests.assert_called_once()
        args, kwargs = mock_create_tests.call_args
        assert kwargs['src_dir'].endswith('testdata')
        assert kwargs['unsafe'] is False  # Default
        assert kwargs['vb'] == 0 # Default

@patch('ghtest.cli.create_tests')
def test_cli_run_unsafe_verbose(mock_create_tests):
    with patch.object(sys, 'argv', ['ghtest', 'testdata', '--unsafe', '-v']):
        main()
        mock_create_tests.assert_called_once()
        _, kwargs = mock_create_tests.call_args
        assert kwargs['unsafe'] is True
        assert kwargs['vb'] == 1
