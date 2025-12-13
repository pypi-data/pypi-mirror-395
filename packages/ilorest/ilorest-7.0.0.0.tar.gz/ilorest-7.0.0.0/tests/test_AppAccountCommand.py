"""
Unit tests for AppAccountCommand
Comprehensive test suite covering create, delete, exists, and details operations
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

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
    'AppIdListError', 'UI'
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
    from ilorest.rdmc_helper import (
        ReturnCodes,
        InvalidCommandLineError,
        UsernamePasswordRequiredError,
        NoAppAccountError,
        VnicExistsError,
        AppAccountExistsError,
        IncompatibleiLOVersionError,
        SavinginTPMError,
        SavinginiLOError,
        GenerateAndSaveAccountError,
        RemoveAccountError,
        AppIdListError,
    )
    USING_REAL_IMPLEMENTATION = True
except ImportError as e:
    AppAccountCommand = None
    ReturnCodes = Mock()
    InvalidCommandLineError = Mock()
    UsernamePasswordRequiredError = Mock()
    NoAppAccountError = Mock()
    VnicExistsError = Mock()
    AppAccountExistsError = Mock()
    IncompatibleiLOVersionError = Mock()
    SavinginTPMError = Mock()
    SavinginiLOError = Mock()
    GenerateAndSaveAccountError = Mock()
    RemoveAccountError = Mock()
    AppIdListError = Mock()
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
    rdmc.app.ListAppIds = Mock(return_value=[])
    rdmc.app.ExpandAppId = Mock(return_value="12345678")
    rdmc.app.getilover_beforelogin = Mock(return_value=(7, "Production"))
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
    # Support 'in' operator for attribute checking
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


class TestCreateCommand:

    def test_creates_application_account_successfully_with_valid_credentials(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called_with("Application account has been generated and saved successfully.\n")

    def test_creates_self_registered_application_account_successfully(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.self_register = True
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_returns_success_when_application_account_already_exists(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        mock_rdmc.app.generate_save_token.side_effect = AppAccountExistsError()

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called()

    def test_raises_error_when_username_or_password_missing(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_options.user = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(UsernamePasswordRequiredError):
                    command.run([])

    def test_raises_error_when_hostapp_details_missing_without_self_flag(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "Please provide all the required host application" in str(exc_info.value)

    def test_raises_saving_in_tpm_error_when_tpm_save_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.generate_save_token.side_effect = SavinginTPMError("TPM save failed")

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(SavinginTPMError):
                    command.run([])

    def test_raises_saving_in_ilo_error_when_ilo_save_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.generate_save_token.side_effect = SavinginiLOError("iLO save failed")

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(SavinginiLOError):
                    command.run([])

    def test_raises_error_when_self_flag_conflicts_with_hostapp_details(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.self_register = True
        mock_options.hostappname = "TestApp"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "You may include either the --self tag" in str(exc_info.value)


class TestDeleteCommand:

    def test_deletes_existing_application_account_successfully(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "delete"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called_with("Application account has been deleted successfully.\n")

    def test_raises_error_when_deleting_non_existent_account(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "delete"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = False

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(NoAppAccountError) as exc_info:
                    command.run([])
                assert "The application account you are trying to delete does not exist" in str(exc_info.value)

    def test_raises_error_when_hostappid_missing_for_delete(self, command, mock_rdmc, mock_options):
        mock_options.command = "delete"
        mock_options.hostappid = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "--hostappid is a required parameter" in str(exc_info.value)

    def test_raises_error_when_partial_credentials_provided(self, command, mock_rdmc, mock_options):
        mock_options.command = "delete"
        mock_options.hostappid = "12345678"
        mock_options.user = "admin"
        mock_options.password = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "Please provide both username and password" in str(exc_info.value)

    def test_logs_error_when_delete_operation_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "delete"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.delete_token.side_effect = Exception("Delete failed")

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(RemoveAccountError):
                    command.run([])



class TestExistsCommand:

    def test_returns_success_when_account_exists(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called_with("Application account exists for this host application.\n")

    def test_returns_error_code_when_account_does_not_exist(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = False

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.ACCOUNT_DOES_NOT_EXIST_ERROR
        mock_rdmc.ui.printer.assert_called_with("Application account does not exist for this hostapp.\n")

    def test_raises_error_when_hostappid_missing_for_exists(self, command, mock_rdmc, mock_options):
        mock_options.command = "exists"
        mock_options.hostappid = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(InvalidCommandLineError) as exc_info:
                command.run([])
            assert "Please provide hostappid" in str(exc_info.value)


class TestDetailsCommand:

    def test_returns_details_for_all_application_accounts(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            },
            {
                "ApplicationName": "App2",
                "ApplicationID": "87654321",
                "ExistsInTPM": False,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called()

    def test_returns_details_for_specific_application_account_with_full_id(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called()

    def test_matches_short_app_id_and_returns_details(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "5678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ExpandAppId.return_value = "12345678"
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.app.ExpandAppId.assert_called_once()

    def test_matches_short_app_id_with_fallback_when_expansion_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "5678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ExpandAppId.side_effect = Exception("Expansion failed")
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_matches_full_app_id_with_case_insensitive_fallback(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "ABCDEF12"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "abcdef12",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called()

    def test_returns_json_formatted_output_when_json_flag_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_options.json = True
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with patch('ilorest.rdmc_helper.UI') as mock_ui:
                    result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_masks_application_id_in_json_output(self, command):
        test_data = [
            {"ApplicationName": "App1", "ApplicationID": "12345678"},
            {"ApplicationName": "App2", "ApplicationID": "87654321"}
        ]

        result = command.print_json_app_details(test_data)

        assert result[0]["ApplicationID"] == "**5678"
        assert result[1]["ApplicationID"] == "**4321"

    def test_raises_error_when_specific_app_id_not_found(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "99999999"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(AppAccountExistsError) as exc_info:
                    command.run([])
                assert "There is no application account for the given hostappid '99999999'" in str(exc_info.value)

    def test_raises_error_when_no_ilorest_account_exists(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = False

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(NoAppAccountError) as exc_info:
                    command.run([])
                assert "iLORest app account not found" in str(exc_info.value)

    def test_filters_results_when_only_token_flag_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_options.onlytoken = True
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_filters_results_when_only_account_flag_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_options.onlyaccount = True
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_returns_self_registered_account_details_when_self_flag_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.self_register = True
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "SelfRegistered",
                "ApplicationID": "00b5-1234",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS


class TestAppIdMatching:

    def short_app_id_matches_full_id_last_four_characters(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "06f8"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ExpandAppId.side_effect = Exception("Cannot expand")
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "NA",
                "ApplicationID": "ABCD06f8",
                "ExistsInTPM": True,
                "ExistsIniLO": False
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def full_app_id_matches_exactly_when_case_differs(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "ILOREST00B5"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "iLORest",
                "ApplicationID": "ilorest00b5",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def short_app_id_prioritizes_expanded_id_over_fallback(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "00b5"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ExpandAppId.return_value = "ILOREST00b5"
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "iLORest",
                "ApplicationID": "ILOREST00b5",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            },
            {
                "ApplicationName": "Other",
                "ApplicationID": "OTHERAB00b5",
                "ExistsInTPM": False,
                "ExistsIniLO": False
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS
        mock_rdmc.app.ExpandAppId.assert_called_once()

    def error_message_includes_user_provided_app_id(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "INVALID123"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(AppAccountExistsError) as exc_info:
                    command.run([])

                assert "INVALID123" in str(exc_info.value)


class TestFilterOptions:

    def removes_exists_in_ilo_key_when_only_token_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = True
        options.onlyaccount = False

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        command._apply_filter_options(options, test_list)

        assert "ExistsInTPM" in test_list[0]
        assert "ExistsIniLO" not in test_list[0]

    def removes_exists_in_tpm_key_when_only_account_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = False
        options.onlyaccount = True

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        command._apply_filter_options(options, test_list)

        assert "ExistsInTPM" not in test_list[0]
        assert "ExistsIniLO" in test_list[0]

    def does_not_raise_error_when_key_missing_and_only_token_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = True
        options.onlyaccount = False

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True
            }
        ]

        command._apply_filter_options(options, test_list)

        assert "ExistsInTPM" in test_list[0]

    def does_not_raise_error_when_key_missing_and_only_account_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = False
        options.onlyaccount = True

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsIniLO": True
            }
        ]

        command._apply_filter_options(options, test_list)

        assert "ExistsIniLO" in test_list[0]

    def processes_multiple_accounts_in_list(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = True
        options.onlyaccount = False

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            },
            {
                "ApplicationName": "App2",
                "ApplicationID": "87654321",
                "ExistsInTPM": False,
                "ExistsIniLO": True
            }
        ]

        command._apply_filter_options(options, test_list)

        assert "ExistsIniLO" not in test_list[0]
        assert "ExistsIniLO" not in test_list[1]
        assert "ExistsInTPM" in test_list[0]
        assert "ExistsInTPM" in test_list[1]

    def does_not_modify_list_when_no_filter_flags_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        options = Mock()
        options.onlytoken = False
        options.onlyaccount = False

        test_list = [
            {
                "ApplicationName": "App1",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": True
            }
        ]

        original = test_list[0].copy()
        command._apply_filter_options(options, test_list)

        assert test_list[0] == original


class TestAdminPrivileges:

    def test_raises_error_when_not_admin_on_windows(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.typepath.adminpriv = True

        with patch('os.name', 'nt'):
            with patch('ctypes.windll.shell32.IsUserAnAdmin', return_value=False):
                from redfish.ris.rmc_helper import UserNotAdminError
                with pytest.raises(UserNotAdminError):
                    command.run([])

    def test_raises_error_when_not_root_on_linux(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.typepath.adminpriv = True

        from redfish.ris.rmc_helper import UserNotAdminError
        with patch('os.name', 'posix'):
            with patch.object(command, '_check_admin_privileges', side_effect=UserNotAdminError()):
                with pytest.raises(UserNotAdminError):
                    command.run([])

    def test_allows_execution_when_admin_on_windows(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch('os.name', 'nt'):
                with patch('ctypes.windll.shell32.IsUserAnAdmin', return_value=True):
                    result = command.run([])

        assert result == ReturnCodes.SUCCESS


class TestVnicValidation:

    def test_raises_error_when_vnic_not_enabled(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.login_select_validation.return_value = Mock(base_url="blobstore://10.0.0.1/rest/v1")

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(VnicExistsError) as exc_info:
                command.run([])
            assert "VNIC-enabled iLO7 based server" in str(exc_info.value)

    def test_allows_execution_when_vnic_enabled(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.login_select_validation.return_value = Mock(base_url="blobstore://16.1.15.1/rest/v1")
        mock_rdmc.app.token_exists.return_value = True

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS


class TestIloVersionValidation:

    def test_raises_error_when_ilo_version_below_7(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        from redfish.rest.connections import ChifDriverMissingOrNotFound
        mock_rdmc.app.getilover_beforelogin.side_effect = ChifDriverMissingOrNotFound()

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(IncompatibleiLOVersionError) as exc_info:
                    command.run([])
                assert "only available for iLO 7 or higher" in str(exc_info.value)

    def test_allows_execution_on_ilo7_or_higher(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.getilover_beforelogin.return_value = (7, "Production")
        mock_rdmc.app.token_exists.return_value = True

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS


class TestCredentialEncoding:

    def test_decodes_encrypted_credentials_when_encode_flag_set(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_options.encode = True
        mock_options.user = "encrypted_user"
        mock_options.password = "encrypted_pass"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS

    def test_raises_error_when_credentials_missing_with_encode_flag(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_options.encode = True
        mock_options.user = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch.object(command, '_check_admin_privileges'):
            with pytest.raises(UsernamePasswordRequiredError) as exc_info:
                command.run([])
            assert "Username and Password are required when --enc is passed" in str(exc_info.value)


class TestHelperMethods:

    def test_masks_application_ids_correctly_in_print_output(self, command):
        test_data = [
            {
                "ApplicationName": "TestApp",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": False
            }
        ]

        command.print_app_details(test_data)

        command.rdmc.ui.printer.assert_called()
        call_args = command.rdmc.ui.printer.call_args[0][0]
        assert "**5678" in call_args
        assert "12345678" not in call_args

    def test_formats_tpm_and_ilo_existence_correctly(self, command):
        test_data = [
            {
                "ApplicationName": "TestApp",
                "ApplicationID": "12345678",
                "ExistsInTPM": True,
                "ExistsIniLO": False
            }
        ]

        command.print_app_details(test_data)

        call_args = command.rdmc.ui.printer.call_args[0][0]
        assert "App account exists in TPM: yes" in call_args
        assert "App account exists in iLO: no" in call_args

    def test_handles_empty_app_id_list(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.return_value = []

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                result = command.run([])

        assert result == ReturnCodes.SUCCESS


class TestErrorHandling:

    def test_logs_error_when_app_account_object_creation_fails(self, command, mock_rdmc, mock_options):
        mock_options.command = "create"
        mock_options.hostappname = "TestApp"
        mock_options.hostappid = "12345678"
        mock_options.salt = "test_salt"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('ilorest.extensions.iLO_COMMANDS.AppAccountCommand.AppAccount', side_effect=Exception("Creation failed")):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(NoAppAccountError):
                    command.run([])

    def test_logs_error_when_token_exists_check_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "exists"
        mock_options.hostappid = "12345678"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.side_effect = Exception("Check failed")

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(AppAccountExistsError):
                    command.run([])

        mock_rdmc.ui.error.assert_called()

    def test_logs_error_when_list_app_ids_fails(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "details"
        mock_options.hostappid = "all"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])
        mock_rdmc.app.token_exists.return_value = True
        mock_rdmc.app.ListAppIds.side_effect = Exception("List failed")

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(AppIdListError):
                    command.run([])

        mock_rdmc.ui.error.assert_called()

    def test_raises_invalid_command_error_when_command_not_provided(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = None
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(InvalidCommandLineError) as exc_info:
                    command.run([])
                assert "The command you have entered is invalid" in str(exc_info.value)

    def test_raises_invalid_command_error_for_unknown_command(self, command, mock_rdmc, mock_options, mock_app_account_obj):
        mock_options.command = "unknown"
        mock_rdmc.rdmc_parse_arglist.return_value = (mock_options, [])

        with patch('redfish.hpilo.vnichpilo.AppAccount', return_value=mock_app_account_obj):
            with patch.object(command, '_check_admin_privileges'):
                with pytest.raises(InvalidCommandLineError):
                    command.run([])


class TestHelpDisplay:

    def test_returns_success_when_help_flag_provided(self, command, mock_rdmc):
        result = command.run(["-h"], help_disp=True)
        assert result == ReturnCodes.SUCCESS

    def test_returns_success_when_help_disp_flag_set(self, command, mock_rdmc):
        mock_rdmc.rdmc_parse_arglist.side_effect = SystemExit(0)
        result = command.run([], help_disp=True)
        assert result == ReturnCodes.SUCCESS

