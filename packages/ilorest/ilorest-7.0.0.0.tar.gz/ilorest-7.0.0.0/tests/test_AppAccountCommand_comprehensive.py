"""
Comprehensive unit tests for AppAccountCommand with focus on delete operations and edge cases
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, call

project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'ilorest'))
sys.path.insert(0, os.path.join(project_root, 'ilorest', 'extensions', 'iLO_COMMANDS'))

sys.modules['redfish'] = Mock()
sys.modules['redfish.ris'] = Mock()
sys.modules['redfish.ris.rmc_helper'] = Mock()
sys.modules['redfish.rest'] = Mock()
sys.modules['redfish.rest.v1'] = Mock()
sys.modules['redfish.rest.connections'] = Mock()
sys.modules['redfish.hpilo'] = Mock()
sys.modules['redfish.hpilo.vnichpilo'] = Mock()

mock_rdmc_helper = Mock()
exception_names = [
    'Encryption', 'GenerateAndSaveAccountError', 'RemoveAccountError', 'AppAccountExistsError',
    'ReturnCodes', 'InvalidCommandLineErrorOPTS', 'IncompatibleiLOVersionError',
    'InvalidCommandLineError', 'UsernamePasswordRequiredError', 'NoAppAccountError',
    'VnicExistsError', 'SavinginTPMError', 'SavinginiLOError', 'GenBeforeLoginError',
    'AppIdListError', 'UI', 'ReactivateAppAccountTokenError'
]
for exc_name in exception_names:
    if exc_name == 'ReturnCodes':
        mock_rdmc_helper.ReturnCodes = type('ReturnCodes', (), {
            'SUCCESS': 0,
            'ACCOUNT_DOES_NOT_EXIST_ERROR': 10
        })
    elif exc_name == 'Encryption':
        mock_encryption = Mock()
        mock_encryption.decode_credentials = Mock(return_value=b'decoded')
        mock_rdmc_helper.Encryption = mock_encryption
    elif exc_name == 'UI':
        mock_ui = Mock()
        mock_ui.print_out_json = Mock()
        mock_rdmc_helper.UI = mock_ui
    else:
        exc_class = type(exc_name, (Exception,), {'__module__': 'rdmc_helper'})
        setattr(mock_rdmc_helper, exc_name, exc_class)

sys.modules['rdmc_helper'] = mock_rdmc_helper
sys.modules['ilorest.rdmc_helper'] = mock_rdmc_helper

mock_app_account = Mock()
mock_app_account.AppAccount = Mock
sys.modules['redfish.hpilo.vnichpilo'].AppAccount = Mock
sys.modules['redfish.hpilo.vnichpilo'].AppAccountExistsError = type('AppAccountExistsError', (Exception,), {'__module__': 'redfish.hpilo.vnichpilo'})
sys.modules['redfish.hpilo.vnichpilo'].SavinginTPMError = type('SavinginTPMError', (Exception,), {'__module__': 'redfish.hpilo.vnichpilo'})
sys.modules['redfish.hpilo.vnichpilo'].SavinginiLOError = type('SavinginiLOError', (Exception,), {'__module__': 'redfish.hpilo.vnichpilo'})
sys.modules['redfish.hpilo.vnichpilo'].GenerateAndSaveAccountError = type('GenerateAndSaveAccountError', (Exception,), {'__module__': 'redfish.hpilo.vnichpilo'})
sys.modules['redfish.hpilo.vnichpilo'].InvalidCommandLineError = type('InvalidCommandLineError', (Exception,), {'__module__': 'redfish.hpilo.vnichpilo'})

sys.modules['redfish.rest.connections'].ChifDriverMissingOrNotFound = type('ChifDriverMissingOrNotFound', (Exception,), {'__module__': 'redfish.rest.connections'})
sys.modules['redfish.rest.connections'].VnicNotEnabledError = type('VnicNotEnabledError', (Exception,), {'__module__': 'redfish.rest.connections'})
sys.modules['redfish.rest.v1'].InvalidCredentialsError = type('InvalidCredentialsError', (Exception,), {'__module__': 'redfish.rest.v1'})
sys.modules['redfish.ris.rmc_helper'].UserNotAdminError = type('UserNotAdminError', (Exception,), {'__module__': 'redfish.ris.rmc_helper'})

try:
    from ilorest.extensions.iLO_COMMANDS.AppAccountCommand import AppAccountCommand
    from ilorest.rdmc_helper import ReturnCodes
    USING_REAL_IMPLEMENTATION = True
except ImportError as e:
    AppAccountCommand = None
    ReturnCodes = Mock()
    USING_REAL_IMPLEMENTATION = False
    pytest.skip(f"AppAccountCommand not available: {str(e)}", allow_module_level=True)


@pytest.fixture
def mock_rdmc():
    rdmc = Mock()
    rdmc.app = Mock()
    rdmc.app.current_client = Mock()
    rdmc.app.current_client.base_url = "blobstore://16.1.15.1/rest/v1"
    rdmc.app.typepath = Mock()
    rdmc.app.typepath.adminpriv = True
    rdmc.app.token_exists = Mock(return_value=False)
    rdmc.app.generate_save_token = Mock(return_value=0)
    rdmc.app.delete_token = Mock(return_value=0)
    rdmc.app.delete_handler = Mock()
    rdmc.app.ListAppIds = Mock(return_value=[])
    rdmc.app.ExpandAppId = Mock(return_value="12345678")
    rdmc.app.getilover_beforelogin = Mock(return_value=(7, "Production"))
    rdmc.app.reactivate_token = Mock(return_value=0)
    rdmc.ui = Mock()
    rdmc.ui.printer = Mock()
    rdmc.ui.error = Mock()
    rdmc.ui.print_out_json = Mock()
    rdmc.rdmc_parse_arglist = Mock()
    rdmc.login_select_validation = Mock(return_value=Mock(base_url="blobstore://16.1.15.1/rest/v1"))
    rdmc.log_dir = "/tmp/logs"
    return rdmc


@pytest.fixture
def command(mock_rdmc):
    cmd = AppAccountCommand()
    cmd.rdmc = mock_rdmc
    cmd.cmdbase = Mock()
    return cmd


@pytest.fixture
def mock_options():
    options = Mock()
    def contains_check(self, key):
        return hasattr(options, key) and getattr(options, key) is not None
    options.__contains__ = contains_check
    options.command = None
    options.hostappid = None
    options.hostappname = None
    options.salt = None
    options.user = "admin"
    options.password = "password"
    options.encode = False
    options.self_register = False
    options.json = False
    options.onlytoken = False
    options.onlyaccount = False
    return options


@pytest.fixture
def mock_app_account_obj():
    app_obj = Mock()
    app_obj.appname = "TestApp"
    app_obj.appid = "12345678"
    app_obj.salt = "test_salt"
    return app_obj


def test_deletes_non_self_account_from_both_tpm_and_ilo_with_credentials(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "06f8"
    mock_options.hostappname = None
    mock_options.salt = None
    mock_options.user = "Administrator"
    mock_options.password = "password123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = True
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "1234567806f8", "ApplicationName": "CustomApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        mock_app_account_obj.appid = "06f8"
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_token.assert_called_once()
    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/1234567806f8")
    mock_rdmc.ui.printer.assert_called_with("Application account has been deleted successfully.\n")


def test_deletes_self_account_from_both_tpm_and_ilo(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.self_register = True
    mock_options.hostappid = None
    mock_options.user = "Administrator"
    mock_options.password = "password123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = True
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "00b5-12345678", "ApplicationName": "SelfRegistered"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        mock_app_account_obj.appid = "self_register"
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_token.assert_called_once()
    mock_rdmc.app.delete_handler.assert_called_once()


def test_deletes_account_from_ilo_only_when_tpm_deletion_fails(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "abc1"
    mock_options.user = "Administrator"
    mock_options.password = "password123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = True
    mock_rdmc.app.delete_token.side_effect = Exception("TPM not accessible")
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abc1", "ApplicationName": "TestApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/12345678abc1")


def test_deletes_account_from_tpm_only_when_ilo_deletion_fails(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "def2"
    mock_options.hostappname = "MyApp"
    mock_options.salt = "salt123"
    mock_options.user = "Administrator"
    mock_options.password = "password123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = True
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.delete_handler.side_effect = Exception("iLO REST API error")
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "87654321def2", "ApplicationName": "MyApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_token.assert_called_once()


def test_creates_app_account_with_correct_appid_parameter_for_non_self_account(command, mock_rdmc, mock_options):
    mock_options.command = "create"
    mock_options.hostappid = "1a2b"
    mock_options.hostappname = "MyTestApp"
    mock_options.salt = "testsalt"
    mock_options.user = "admin"
    mock_options.password = "pass123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.generate_save_token.return_value = 0

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

        mock_app_class.assert_called_once()
        call_kwargs = mock_app_class.call_args[1]
        assert call_kwargs['appid'] == "1a2b"
        assert call_kwargs['appname'] == "MyTestApp"
        assert call_kwargs['salt'] == "testsalt"


def test_creates_app_account_with_self_register_appid_for_self_account(command, mock_rdmc, mock_options):
    mock_options.command = "create"
    mock_options.self_register = True
    mock_options.hostappid = None
    mock_options.hostappname = None
    mock_options.salt = None
    mock_options.user = "admin"
    mock_options.password = "pass123"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.generate_save_token.return_value = 0

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

        mock_app_class.assert_called_once()
        call_kwargs = mock_app_class.call_args[1]
        assert call_kwargs['appid'] == "self_register"


def test_deletes_account_matching_short_app_id_four_characters(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "9abc"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "123456789abc", "ApplicationName": "ShortIDApp"},
        {"ApplicationID": "abcdef123456", "ApplicationName": "OtherApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/123456789abc")


def test_deletes_account_matching_full_app_id(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "abcdef123456"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "123456789abc", "ApplicationName": "App1"},
        {"ApplicationID": "abcdef123456", "ApplicationName": "App2"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/abcdef123456")


def test_deletes_self_registered_account_identified_by_00b5_prefix(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.self_register = True
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "00b5-abcd1234", "ApplicationName": "iLORest"},
        {"ApplicationID": "12345678abcd", "ApplicationName": "CustomApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/00b5-abcd1234")


def test_raises_error_when_deleting_without_credentials_or_app_info(command, mock_rdmc, mock_options):
    mock_options.command = "delete"
    mock_options.hostappid = "1234"
    mock_options.user = None
    mock_options.password = None
    mock_options.hostappname = None
    mock_options.salt = None
    mock_options.self_register = False
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

    with patch.object(command, 'get_ilover_beforelogin'):
        with pytest.raises(Exception) as exc_info:
            command.run([])
        assert "please provide either" in str(exc_info.value).lower()


def test_accepts_delete_with_only_hostappid_and_credentials(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "5678"
    mock_options.hostappname = None
    mock_options.salt = None
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0


def test_accepts_delete_with_hostappid_and_full_app_info(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "abcd"
    mock_options.hostappname = "MyApp"
    mock_options.salt = "salt"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "1234abcd", "ApplicationName": "MyApp"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0


def test_raises_error_when_deleting_with_partial_app_info(command, mock_rdmc, mock_options):
    mock_options.command = "delete"
    mock_options.hostappid = "1234"
    mock_options.hostappname = "MyApp"
    mock_options.salt = None
    mock_options.user = None
    mock_options.password = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

    with patch.object(command, 'get_ilover_beforelogin'):
        with pytest.raises(Exception) as exc_info:
            command.run([])
        assert "please provide either" in str(exc_info.value).lower()


def test_treats_00b5_hostappid_as_self_registered_account(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "00b5"
    mock_options.self_register = False
    mock_options.hostappname = None
    mock_options.salt = None
    mock_options.user = None
    mock_options.password = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "00b5-12345678", "ApplicationName": "Self"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0


def test_shows_details_for_self_registered_account_with_self_flag(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.self_register = True
    mock_options.hostappid = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "00b5-abcd1234", "ApplicationName": "iLORest", "ExistsInTPM": True, "ExistsIniLO": True},
        {"ApplicationID": "12345678abcd", "ApplicationName": "OtherApp", "ExistsInTPM": False, "ExistsIniLO": True}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.ui.printer.assert_called()
    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "iLORest" in printer_output
    assert "OtherApp" not in printer_output


def test_shows_message_when_no_self_registered_account_exists(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.self_register = True
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "CustomApp", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    assert mock_rdmc.ui.printer.call_count >= 2
    calls = [call[0][0] for call in mock_rdmc.ui.printer.call_args_list]
    assert any("No self-registered" in call for call in calls)


def test_expands_short_app_id_using_expand_app_id_method(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = "abcd"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ExpandAppId.return_value = "12345678abcd"
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "App", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.ExpandAppId.assert_called_once()


def test_lists_all_accounts_when_hostappid_is_all(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = "all"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App1", "ExistsInTPM": True, "ExistsIniLO": True},
        {"ApplicationID": "87654321", "ApplicationName": "App2", "ExistsInTPM": False, "ExistsIniLO": True},
        {"ApplicationID": "00b5-1234", "ApplicationName": "Self", "ExistsInTPM": True, "ExistsIniLO": False}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "App1" in printer_output
    assert "App2" in printer_output
    assert "Self" in printer_output


def test_excludes_ilo_info_when_only_token_flag_set(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = "all"
    mock_options.onlytoken = True
    mock_options.onlyaccount = False
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "TPM" in printer_output
    assert "iLO" not in printer_output or "App account exists in iLO" not in printer_output


def test_excludes_tpm_info_when_only_account_flag_set(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = "all"
    mock_options.onlytoken = False
    mock_options.onlyaccount = True
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "iLO" in printer_output
    assert "TPM" not in printer_output or "App account exists in TPM" not in printer_output


def test_checks_token_existence_using_list_app_ids_for_short_id(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "exists"
    mock_options.hostappid = "abcd"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "App"}
    ]

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.ui.printer.assert_called_with("Application account exists for this host application.\n")


def test_returns_does_not_exist_when_short_id_not_found(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "exists"
    mock_options.hostappid = "9999"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "App"}
    ]
    mock_rdmc.app.token_exists.return_value = False

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 10
    mock_rdmc.ui.printer.assert_called_with("Application account does not exist for this hostapp.\n")


def test_raises_error_for_invalid_command(command, mock_rdmc, mock_options):
    mock_options.command = "invalid_command"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = False

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance
        with patch.object(command, 'get_ilover_beforelogin'):
            from ilorest.rdmc_helper import InvalidCommandLineError
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "invalid" in str(exc_info.value).lower()


def test_raises_error_when_ilo_version_below_7(command, mock_rdmc, mock_options):
    mock_options.command = "create"
    mock_options.self_register = True
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

    with patch('redfish.hpilo.vnichpilo.AppAccount'):
        with patch.object(command, 'get_ilover_beforelogin') as mock_ilo_ver:
            mock_ilo_ver.side_effect = Exception("This feature is only available for iLO 7 or higher")
            with pytest.raises(Exception) as exc_info:
                command.run([])
            assert "iLO 7" in str(exc_info.value)


def test_masks_last_four_characters_of_app_id_in_output(command):
    test_data = [
        {"ApplicationName": "TestApp", "ApplicationID": "abcdef123456"},
        {"ApplicationName": "MyApp", "ApplicationID": "00b5-1234abcd"}
    ]

    result = command.print_json_app_details(test_data)

    assert result[0]["ApplicationID"] == "**3456"
    assert result[1]["ApplicationID"] == "**abcd"


def test_formats_plain_text_output_with_masked_app_ids(command, mock_rdmc):
    command.rdmc = mock_rdmc
    test_data = [
        {"ApplicationName": "App1", "ApplicationID": "12345678", "ExistsInTPM": True, "ExistsIniLO": False}
    ]

    command.print_app_details(test_data)

    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "Application Name: App1" in printer_output
    assert "Application Id: **5678" in printer_output
    assert "App account exists in TPM: yes" in printer_output
    assert "App account exists in iLO: no" in printer_output


def test_reactivates_existing_application_account_successfully(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "reactivate"
    mock_options.hostappname = "MyApp"
    mock_options.hostappid = "1234"
    mock_options.salt = "salt"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = True
    mock_rdmc.app.reactivate_token.return_value = 0

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.ui.printer.assert_called_with("Application account has been reactivated successfully.\n")


def test_raises_error_when_reactivating_non_existent_account(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "reactivate"
    mock_options.hostappname = "MyApp"
    mock_options.hostappid = "1234"
    mock_options.salt = "salt"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists.return_value = False

    with patch('redfish.hpilo.vnichpilo.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            with pytest.raises(Exception) as exc_info:
                command.run([])
            assert "does not exist" in str(exc_info.value).lower()


def test_raises_error_when_reactivating_without_credentials(command, mock_rdmc, mock_options):
    mock_options.command = "reactivate"
    mock_options.hostappname = "MyApp"
    mock_options.hostappid = "1234"
    mock_options.salt = "salt"
    mock_options.user = None
    mock_options.password = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

    with patch.object(command, 'get_ilover_beforelogin'):
        with pytest.raises(Exception) as exc_info:
            command.run([])
        assert "username and password" in str(exc_info.value).lower()


def test_raises_error_when_reactivating_without_app_info(command, mock_rdmc, mock_options):
    mock_options.command = "reactivate"
    mock_options.hostappname = None
    mock_options.hostappid = None
    mock_options.salt = None
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

    with patch.object(command, 'get_ilover_beforelogin'):
        with pytest.raises(Exception) as exc_info:
            command.run([])
        assert "host application" in str(exc_info.value).lower()


def test_details_command_skips_token_existence_check(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = "all"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.token_exists = Mock(side_effect=Exception("Should not be called"))
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App1", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.token_exists.assert_not_called()


def test_details_command_works_without_specific_hostappid(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "details"
    mock_options.hostappid = None
    mock_options.self_register = False
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App1", "ExistsInTPM": True, "ExistsIniLO": True},
        {"ApplicationID": "87654321", "ApplicationName": "App2", "ExistsInTPM": False, "ExistsIniLO": True}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    printer_output = mock_rdmc.ui.printer.call_args[0][0]
    assert "App1" in printer_output
    assert "App2" in printer_output


def test_delete_self_account_attempts_ilo_deletion_without_credentials_when_tpm_fails(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.self_register = True
    mock_options.hostappid = None
    mock_options.user = None
    mock_options.password = None
    mock_options.hostappname = None
    mock_options.salt = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.side_effect = Exception("TPM reset - token not found")
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "00b5-12345678", "ApplicationName": "iLORest"}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/00b5-12345678")
    mock_rdmc.ui.printer.assert_called_with("Application account has been deleted successfully.\n")


def test_delete_with_app_info_attempts_ilo_deletion_even_without_credentials(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.self_register = False
    mock_options.hostappid = "abcd"
    mock_options.user = None
    mock_options.password = None
    mock_options.hostappname = "MyApp"
    mock_options.salt = "mysalt"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "MyApp"}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/12345678abcd")


def test_delete_succeeds_when_only_tpm_deletion_works(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "1234"
    mock_options.hostappname = "App"
    mock_options.salt = "salt"
    mock_options.user = None
    mock_options.password = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.side_effect = Exception("Cannot list app IDs")

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.ui.printer.assert_called_with("Application account has been deleted successfully.\n")


def test_delete_succeeds_when_only_ilo_deletion_works_and_tpm_fails(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "5678"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.side_effect = Exception("TPM error")
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "abcd12345678", "ApplicationName": "TestApp"}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_handler.assert_called_once()


def test_delete_raises_error_when_both_tpm_and_ilo_deletion_fail(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "9999"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.side_effect = Exception("TPM error")
    mock_rdmc.app.ListAppIds.return_value = []

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            with pytest.raises(Exception) as exc_info:
                command.run([])
            assert "does not exist" in str(exc_info.value).lower()


def test_exists_command_checks_using_list_app_ids_for_short_hostappid(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "exists"
    mock_options.hostappid = "1234"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "abcdef781234", "ApplicationName": "TestApp"}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.ui.printer.assert_called_with("Application account exists for this host application.\n")


def test_exists_command_returns_not_found_when_short_id_doesnt_match(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "exists"
    mock_options.hostappid = "9999"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "abcdef781234", "ApplicationName": "TestApp"}
    ]
    mock_rdmc.app.token_exists.return_value = False

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 10
    mock_rdmc.ui.printer.assert_called_with("Application account does not exist for this hostapp.\n")


def test_delete_command_matches_short_hostappid_case_insensitive(command, mock_rdmc, mock_options, mock_app_account_obj):
    mock_options.command = "delete"
    mock_options.hostappid = "ABCD"
    mock_options.user = "admin"
    mock_options.password = "pass"
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.delete_token.return_value = 0
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678abcd", "ApplicationName": "TestApp"}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_class.return_value = mock_app_account_obj
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    mock_rdmc.app.delete_handler.assert_called_once_with("/redfish/v1/AccountService/Accounts/12345678abcd")


def test_details_command_uses_no_credentials_in_app_object_construction(command, mock_rdmc, mock_options):
    mock_options.command = "details"
    mock_options.hostappid = "all"
    mock_options.user = None
    mock_options.password = None
    mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
    mock_rdmc.app.ListAppIds.return_value = [
        {"ApplicationID": "12345678", "ApplicationName": "App", "ExistsInTPM": True, "ExistsIniLO": True}
    ]

    with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount') as mock_app_class:
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance
        with patch.object(command, 'get_ilover_beforelogin'):
            result = command.run([])

    assert result == 0
    call_kwargs = mock_app_class.call_args[1]
    assert call_kwargs['username'] is None
    assert call_kwargs['password'] is None

