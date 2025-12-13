"""
Unit tests for ComputeOpsManagementCommand
Comprehensive test suite covering cloud operations, NTP, Proxy, iLO Reset, and bulk operations
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, mock_open
import requests
from requests.exceptions import ConnectionError, Timeout

# Add the necessary paths to sys.path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'ilorest'))
sys.path.insert(0, os.path.join(project_root, 'ilorest', 'extensions', 'iLO_COMMANDS'))

# Mock the dependencies before importing the module
sys.modules['redfish'] = Mock()
sys.modules['redfish.ris'] = Mock()
sys.modules['redfish.ris.ris'] = Mock()
sys.modules['redfish.ris.ris'].SessionExpired = type('SessionExpired', (Exception,), {})

# Mock the rdmc_helper module with all exception classes
mock_rdmc_helper = Mock()
exception_names = [
    'CloudConnectFailedError', 'CloudConnectTimeoutError', 'IncompatibleiLOVersionError',
    'InvalidCommandLineError', 'InvalidCommandLineErrorOPTS', 'NoCurrentSessionEstablished',
    'ProxyConfigFailedError', 'ReturnCodes'
]
for exc_name in exception_names:
    if exc_name == 'ReturnCodes':
        mock_rdmc_helper.ReturnCodes = type('ReturnCodes', (), {'SUCCESS': 0})
    else:
        setattr(mock_rdmc_helper, exc_name, type(exc_name, (Exception,), {}))
mock_rdmc_helper.LOGGER = Mock()
sys.modules['rdmc_helper'] = mock_rdmc_helper
sys.modules['ilorest.rdmc_helper'] = mock_rdmc_helper

# Mock InputTemplate module
mock_input_template = Mock()
mock_input_template.template = {}
sys.modules['ilorest.extensions.iLO_COMMANDS.data'] = Mock()
sys.modules['ilorest.extensions.iLO_COMMANDS.data.InputTemplate'] = mock_input_template

try:
    from ilorest.extensions.iLO_COMMANDS.ComputeOpsManagementCommand import ComputeOpsManagementCommand
    from ilorest.rdmc_helper import (
        CloudConnectFailedError,
        CloudConnectTimeoutError,
        IncompatibleiLOVersionError,
        InvalidCommandLineError,
        NoCurrentSessionEstablished,
        ReturnCodes,
    )
    from redfish.ris.ris import SessionExpired
    USING_REAL_IMPLEMENTATION = True
except ImportError as e:
    # Define fallback classes if import fails
    ComputeOpsManagementCommand = None
    CloudConnectFailedError = type('CloudConnectFailedError', (Exception,), {})
    CloudConnectTimeoutError = type('CloudConnectTimeoutError', (Exception,), {})
    IncompatibleiLOVersionError = type('IncompatibleiLOVersionError', (Exception,), {})
    InvalidCommandLineError = type('InvalidCommandLineError', (Exception,), {})
    NoCurrentSessionEstablished = type('NoCurrentSessionEstablished', (Exception,), {})
    ReturnCodes = type('ReturnCodes', (), {'SUCCESS': 0})
    SessionExpired = type('SessionExpired', (Exception,), {})
    USING_REAL_IMPLEMENTATION = False
    pytest.skip(f"ComputeOpsManagementCommand not available: {str(e)}", allow_module_level=True)


# Module-level fixtures to avoid duplication
@pytest.fixture
def mock_session():
    """Create a mock requests Session"""
    session = Mock(spec=requests.Session)
    session.auth = ('admin', 'password')
    session.verify = False
    return session


@pytest.fixture
def mock_rdmc():
    """Create a mock rdmc object"""
    rdmc = Mock()
    rdmc.app = Mock()
    rdmc.app.typepath = Mock()
    rdmc.app.typepath.defs = Mock()
    rdmc.app.typepath.defs.managerpath = "/redfish/v1/Managers/1/"
    rdmc.app.typepath.defs.oempath = "/Oem/Hpe"
    rdmc.ui = Mock()
    rdmc.ui.printer = Mock()
    rdmc.ui.print_out_json = Mock()
    rdmc.rdmc_parse_arglist = Mock()
    return rdmc


@pytest.fixture
def command(mock_rdmc):
    """Create a ComputeOpsManagementCommand instance with mocked rdmc"""
    cmd = ComputeOpsManagementCommand()
    cmd.rdmc = mock_rdmc
    cmd.cmdbase = Mock()
    return cmd


@pytest.fixture
def mock_response():
    """Create a standard mock response for cloud operations"""
    response = Mock()
    response.status = 200
    response.dict = {
        "Oem": {
            "Hpe": {
                "CloudConnect": {
                    "CloudConnectStatus": "Connected",
                    "FailReason": "",
                    "CloudActivateURL": "https://example.com",
                    "ActivationKey": "XXXX-YYYY-ZZZZ-AAAA",
                    "ExtendedStatusInfo": {
                        "NetworkConfig": "Configured",
                        "WebConnectivity": "Connected",
                        "iLOConfigForCloudConnect": "Configured"
                    }
                },
                "Actions": {
                    "#HpeiLO.EnableCloudConnect": {},
                    "#HpeiLO.DisableCloudConnect": {}
                }
            }
        }
    }
    return response


def create_mock_http_response(status_code=200, json_data=None):
    """Helper function to create mock HTTP responses for requests library"""
    mock_response = Mock()
    mock_response.status_code = status_code
    if json_data:
        mock_response.json.return_value = json_data
    return mock_response


class TestCloudOperations:
    """Test cloud connection and status operations"""

    def test_cloud_status_returns_connected_when_status_is_connected(self, command, mock_rdmc, mock_response):
        mock_rdmc.app.get_handler.return_value = mock_response
        status = command.get_cloud_status()
        assert status == "Connected"

    def test_cloud_status_returns_status_and_reason_when_need_reason_is_true(self, command, mock_rdmc, mock_response):
        mock_response.dict["Oem"]["Hpe"]["CloudConnect"]["FailReason"] = "TestReason"
        mock_rdmc.app.get_handler.return_value = mock_response
        status, reason = command.get_cloud_status(need_reason=True)
        assert status == "Connected"
        assert reason == "TestReason"

    def test_cloud_status_raises_session_expired_when_response_status_not_200(self, command, mock_rdmc):
        mock_resp = Mock()
        mock_resp.status = 401
        mock_rdmc.app.get_handler.return_value = mock_resp
        with pytest.raises(SessionExpired):
            command.get_cloud_status()

    def test_connect_cloud_shows_warning_when_already_connected(self, command, mock_rdmc, mock_response):
        mock_rdmc.app.get_handler.return_value = mock_response
        result = command.connect_cloud()
        assert result == ReturnCodes.SUCCESS
        mock_rdmc.ui.printer.assert_called_with("Warning: ComputeOpsManagement is already connected.\n")

    def test_cloudconnectvalidation_passes_when_actions_available(self, command, mock_rdmc, mock_response):
        mock_rdmc.app.get_handler.return_value = mock_response
        command.cloudconnectvalidation(Mock())

    def test_cloudconnectvalidation_raises_error_when_enable_action_missing(self, command, mock_rdmc, mock_response):
        del mock_response.dict["Oem"]["Hpe"]["Actions"]["#HpeiLO.EnableCloudConnect"]
        mock_rdmc.app.get_handler.return_value = mock_response
        with pytest.raises(CloudConnectFailedError):
            command.cloudconnectvalidation(Mock())


class TestNTPConfigurationChecking:
    """Test NTP configuration checking and comparison logic"""

    def test_ntp_servers_match_configured_servers_returns_list(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'StaticNTPServers': ['10.0.0.1', '10.0.0.2']
        })
        mock_session.get.return_value = mock_response

        current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
        assert current_ntp == ['10.0.0.1', '10.0.0.2']

    def test_ntp_servers_differ_from_configured(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'StaticNTPServers': ['10.0.0.1', '10.0.0.2']
        })
        mock_session.get.return_value = mock_response

        current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
        assert current_ntp != ['10.0.0.3', '10.0.0.4']

    def test_empty_ntp_servers_handled_correctly(self, command, mock_session):
        mock_response = create_mock_http_response(200, {'StaticNTPServers': []})
        mock_session.get.return_value = mock_response

        current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
        assert current_ntp == []

    def test_ntp_servers_with_empty_strings_filtered(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'StaticNTPServers': ['10.0.0.1', '', None, '10.0.0.2']
        })
        mock_session.get.return_value = mock_response

        current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
        assert current_ntp == ['10.0.0.1', '10.0.0.2']

    def test_ntp_configuration_fails_gracefully_when_connection_error(self, command, mock_session):
        mock_session.get.side_effect = ConnectionError("Connection failed")

        current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
        assert current_ntp is None

    def test_ntp_configuration_returns_none_when_http_error(self, command, mock_session):
        mock_response = create_mock_http_response(404)

        with patch('requests.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.auth = None
            mock_session_instance.verify = False
            mock_session_instance.get.return_value = mock_response
            mock_session_class.return_value = mock_session_instance

            current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
            assert current_ntp is None

    def test_ntp_configuration_returns_none_when_timeout(self, command, mock_session):
        with patch('requests.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.auth = None
            mock_session_instance.verify = False
            mock_session_instance.get.side_effect = Timeout("Request timeout")
            mock_session_class.return_value = mock_session_instance

            current_ntp = command._get_current_ntp_servers(mock_session, 'https://10.0.0.100')
            assert current_ntp is None


class TestProxyConfigurationChecking:
    """Test proxy configuration checking and comparison logic"""

    def test_proxy_settings_match_configured_proxy_returns_settings(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'Oem': {'Hpe': {'WebProxyConfiguration': {
                'ProxyServer': 'proxy.example.com',
                'ProxyPort': 8080,
                'ProxyUserName': 'proxyuser'
            }}}
        })
        mock_session.get.return_value = mock_response

        current_proxy = command._get_current_proxy_settings(mock_session, 'https://10.0.0.100')
        assert current_proxy == {
            'server': 'proxy.example.com',
            'port': 8080,
            'username': 'proxyuser'
        }

    def test_proxy_settings_differ_from_configured(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'Oem': {'Hpe': {'WebProxyConfiguration': {
                'ProxyServer': 'proxy.example.com',
                'ProxyPort': 8080,
                'ProxyUserName': ''
            }}}
        })
        mock_session.get.return_value = mock_response

        current_proxy = command._get_current_proxy_settings(mock_session, 'https://10.0.0.100')
        assert current_proxy['server'] != 'newproxy.example.com'

    def test_empty_proxy_settings_normalized_correctly(self, command, mock_session):
        mock_response = create_mock_http_response(200, {
            'Oem': {'Hpe': {'WebProxyConfiguration': {
                'ProxyServer': '',
                'ProxyPort': None,
                'ProxyUserName': None
            }}}
        })
        mock_session.get.return_value = mock_response

        current_proxy = command._get_current_proxy_settings(mock_session, 'https://10.0.0.100')
        assert current_proxy['server'] == ''
        assert current_proxy['username'] == ''

    def test_proxy_configuration_fails_gracefully_when_connection_error(self, command, mock_session):
        mock_session.get.side_effect = ConnectionError("Connection failed")

        current_proxy = command._get_current_proxy_settings(mock_session, 'https://10.0.0.100')
        assert current_proxy is None

    def test_proxy_configuration_returns_none_when_http_error(self, command, mock_session):
        mock_response = create_mock_http_response(500)
        mock_session.get.return_value = mock_response

        current_proxy = command._get_current_proxy_settings(mock_session, 'https://10.0.0.100')
        assert current_proxy is None

    def test_skip_proxy_flag_prevents_proxy_configuration(self, command, mock_session):
        with patch.object(command, '_configure_proxy') as mock_configure:
            command._configure_proxy_for_ilo_requests(
                mock_session, 'https://10.0.0.100',
                {'server': 'proxy.example.com', 'port': 8080},
                {'skipProxy': True}
            )
            mock_configure.assert_not_called()


class TestiLOResetHandling:
    """Test iLO reset detection and handling during configuration"""

    def test_ilo_reset_during_ntp_configuration_returns_reset_flag(self, command, mock_session):
        with patch.object(command, '_get_current_ntp_servers', return_value=['9.9.9.9']):
            # Mock enabled interface
            eth_response = create_mock_http_response(200, {'Members': [{'@odata.id': '/eth/1'}]})
            enabled_interface = create_mock_http_response(200, {
                'Status': {'State': 'Enabled'},
                'Oem': {'Hpe': {'DHCPv4': {}, 'DHCPv6': {}}},
                '@odata.id': '/eth/1'
            })
            mock_session.get.side_effect = [eth_response, enabled_interface]
            mock_session.patch.return_value = create_mock_http_response(200)
            mock_session.post.return_value = create_mock_http_response(200)

            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=True)
            assert result[0] is True  # ilo_was_reset

    def test_ilo_reset_not_allowed_skips_explicit_reset(self, command, mock_session):
        # _get_current_ntp_servers returns different servers
        with patch.object(command, '_get_current_ntp_servers', return_value=['9.9.9.9']):
            # Mock enabled interface
            eth_response = create_mock_http_response(200, {'Members': [{'@odata.id': '/eth/1'}]})
            enabled_interface = create_mock_http_response(200, {
                'Status': {'State': 'Enabled'},
                'Oem': {'Hpe': {'DHCPv4': {}, 'DHCPv6': {}}},
                '@odata.id': '/eth/1'
            })
            # Use consistent mocking pattern like other tests
            with patch('requests.Session') as mock_session_class:
                mock_session_instance = Mock()
                mock_session_instance.auth = None
                mock_session_instance.verify = False
                mock_session_instance.patch.return_value = create_mock_http_response(200)
                mock_session_instance.get.return_value = create_mock_http_response(200)
                mock_session_instance.get.side_effect = [eth_response, enabled_interface]
                mock_session_class.return_value = mock_session_instance
                
                result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=False)
                assert result[0] is False  # ilo_was_not_reset

    def test_connection_error_during_reset_indicates_ilo_is_resetting(self, command, mock_session):
        # _get_current_ntp_servers returns different servers
        with patch.object(command, '_get_current_ntp_servers', return_value=['9.9.9.9']):
            # Mock enabled interface
            eth_response = create_mock_http_response(200, {'Members': [{'@odata.id': '/eth/1'}]})
            enabled_interface = create_mock_http_response(200, {
                'Status': {'State': 'Enabled'},
                'Oem': {'Hpe': {'DHCPv4': {}, 'DHCPv6': {}}},
                '@odata.id': '/eth/1'
            })
            mock_session.patch.return_value = create_mock_http_response(200)
            mock_session.post.return_value = create_mock_http_response(500)
            mock_session.post.side_effect = ConnectionError("Remote end closed connection")
            mock_session.get.return_value = create_mock_http_response(200)
            mock_session.get.side_effect = [eth_response, enabled_interface]

            ilo_was_reset, _ = command._configure_ntp(
                mock_session, 'https://10.0.0.100',
                ['10.0.0.1', '10.0.0.2'], allow_ilo_reset=True
            )
            assert ilo_was_reset is True


class TestCOMConnectionStatus:
    """Test COM connection status checking logic"""

    def test_com_already_connected_returns_true(self, command, mock_session):
        mock_session.get.return_value = create_mock_http_response(200, {
            'Oem': {'Hpe': {'CloudConnect': {'CloudConnectStatus': 'Connected'}}}
        })

        status = command._check_com_connection_status(mock_session, 'https://10.0.0.100')
        assert status is True

    def test_com_not_connected_returns_false(self, command, mock_session):
        mock_session.get.return_value = create_mock_http_response(200, {
            'Oem': {'Hpe': {'CloudConnect': {'CloudConnectStatus': 'NotConnected'}}}
        })

        status = command._check_com_connection_status(mock_session, 'https://10.0.0.100')
        assert status is False

    def test_connection_error_during_status_check_treated_as_connected(self, command, mock_session):
        mock_session.get.side_effect = ConnectionError("Connection aborted")

        status = command._check_com_connection_status(mock_session, 'https://10.0.0.100')
        assert status is True

    def test_timeout_during_status_check_treated_as_connected(self, command, mock_session):
        mock_session.get.side_effect = Timeout("Connection timeout")

        status = command._check_com_connection_status(mock_session, 'https://10.0.0.100')
        assert status is True

    def test_http_error_during_status_check_returns_false(self, command, mock_session):
        mock_session.get.return_value = create_mock_http_response(401)

        status = command._check_com_connection_status(mock_session, 'https://10.0.0.100')
        assert status is False


class TestPINOnboardingSupport:
    """Test PIN-based onboarding version support logic"""

    @pytest.mark.parametrize("version,major,expected", [
        (1.64, 6, True),   # iLO 6 version 1.64+ supported
        (1.65, 6, True),   # iLO 6 version above 1.64
        (1.63, 6, False),  # iLO 6 below 1.64
        (3.09, 5, True),   # iLO 5 version 3.09+ supported
        (3.10, 5, True),   # iLO 5 version above 3.09
        (3.08, 5, False),  # iLO 5 below 3.09
        (2.80, 4, False),  # iLO 4 not supported
    ])
    def test_pin_onboarding_version_support(self, command, version, major, expected):
        supported = command._is_pin_onboarding_supported(version, major)
        assert supported is expected


class TestTargetIPExtraction:
    """Test IP target extraction from configuration"""

    def test_individual_ips_extracted_correctly(self, command):
        targets = {
            'ilos': {
                'individual': [
                    {'ip': '10.0.0.1'},
                    {'ip': '10.0.0.2'}
                ]
            }
        }

        ips = command._get_all_target_ips(targets)
        assert len(ips) == 2
        assert [ip['ip'] for ip in ips] == ['10.0.0.1', '10.0.0.2']

    def test_ip_range_expanded_correctly(self, command):
        targets = {
            'ilos': {
                'ranges': [
                    {'start': '10.0.0.1', 'end': '10.0.0.3'}
                ]
            }
        }

        ips = command._get_all_target_ips(targets)
        assert len(ips) == 3
        assert [ip['ip'] for ip in ips] == ['10.0.0.1', '10.0.0.2', '10.0.0.3']

    def test_mixed_individual_and_range_ips_extracted_correctly(self, command):
        targets = {
            'ilos': {
                'individual': [{'ip': '10.0.0.10'}],
                'ranges': [{'start': '10.0.0.1', 'end': '10.0.0.2'}]
            }
        }

        ips = command._get_all_target_ips(targets)
        assert len(ips) == 3
        assert '10.0.0.10' in [ip['ip'] for ip in ips]

    def test_empty_targets_returns_empty_list(self, command):
        ips = command._get_all_target_ips({'ilos': {}})
        assert len(ips) == 0


class TestTemplateGeneration:
    """Test template file generation functionality"""

    def test_generate_template_file_creates_file_when_filename_provided(self, command, mock_rdmc):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dumps', return_value='{"test": "data"}'):
                command.generate_template_file("template.json")
                mock_rdmc.ui.printer.assert_called_with("Template written to: template.json\n", verbose_override=True)

    def test_generate_template_file_writes_to_default_file_when_no_filename(self, command, mock_rdmc):
        with patch('builtins.open', mock_open()):
            with patch('json.dumps', return_value='{"test": "data"}'):
                command.generate_template_file()
                mock_rdmc.ui.printer.assert_called_with("Template written to: multiconnect_input_template.json\n", verbose_override=True)


class TestBulkOperations:
    """Test bulk connect and precheck operations"""

    @patch('os.path.exists')
    def test_bulk_connect_raises_error_when_config_file_not_found(self, mock_exists, command):
        mock_exists.return_value = False
        with pytest.raises(InvalidCommandLineError, match="Configuration file not found"):
            command.bulk_connect("nonexistent.json")

    def test_validate_bulk_connect_input_valid(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        valid_config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "AAAA-BBBB-CCCC"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"},
            },
            "targets": {
                "ilos": {
                    "individual": [
                        {"ip": "192.168.1.10"}
                    ],
                    "ranges": []
                }
            }
        }
        # Should not raise
        command._validate_bulk_connect_input(valid_config)

    def test_validate_bulk_connect_input_valid_with_workspace_id_only(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"workspace_id": "WORKSPACE-ID-XYZ-999"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"},
            },
            "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}], "ranges": []}}
        }
        command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_missing_common_settings_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {"targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}]}}}
        with pytest.raises(InvalidCommandLineError, match="Missing 'commonSettings'"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_missing_activation_key_and_workspace_id_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"}
            },
            "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}]}}
        }
        with pytest.raises(InvalidCommandLineError, match="activationKey.*workspace_id.*must be provided"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_valid_individual_authentication(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "KEY-1234"}
            },
            "targets": {
                "ilos": {
                    "individual": [
                        {
                            "ip": "192.168.1.10",
                            "iloAuthentication": {"iloUser": "admin1", "iloPassword": "pass1"}

                        }
                    ],
                    "ranges": [
                        {
                            "start": "192.168.1.20",
                            "end": "192.168.1.21",
                            "iloAuthentication": {"iloUser": "admin2", "iloPassword": "pass2"}
                        }
                    ]
                }
            }
        }
        # Should not raise
        command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_missing_ilo_authentication_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {"computeOpsManagement": {"activationKey": "KEY-1234"}},
            "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}]}}
        }
        with pytest.raises(InvalidCommandLineError, match="The operation failed as iLO credential is not provided in the input json"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_missing_targets_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "KEY-1234"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"}
            }
        }
        with pytest.raises(InvalidCommandLineError, match="Missing 'targets'"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_no_ilo_ips_specified_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "KEY-1234"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"}
            },
            "targets": {"ilos": {"individual": [], "ranges": []}}
        }
        with pytest.raises(InvalidCommandLineError, match="At least one iLO IP must be specified"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_invalid_individual_entry_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "KEY-1234"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"}
            },
            "targets": {"ilos": {"individual": [{"hostname": "server1"}]}}
        }
        with pytest.raises(InvalidCommandLineError, match="must be an object with an 'ip' field"):
            command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_invalid_range_entry_raises_error(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "KEY-1234"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pass123"}
            },
            "targets": {"ilos": {"ranges": [{"start": "10.0.0.1"}]}}
        }
        with pytest.raises(InvalidCommandLineError, match="must be an object with 'start' and 'end' fields"):
            command._validate_bulk_connect_input(config)


class TestOptimizedGeneratorFunction:
    """Test the optimized generator function for IP extraction"""

    def test_generator_yields_individual_ips_correctly(self, command):
        targets = {
            'ilos': {
                'individual': [
                    {'ip': '10.0.0.1', 'network': {'dns': ['8.8.8.8']}},
                    {'ip': '10.0.0.2'}
                ]
            }
        }

        result = list(command._get_all_target_ips_optimized(targets))
        assert len(result) == 2
        assert result[0]['ip'] == '10.0.0.1'
        assert result[1]['ip'] == '10.0.0.2'

    def test_generator_yields_range_ips_correctly(self, command):
        targets = {
            'ilos': {
                'ranges': [
                    {'start': '192.168.1.1', 'end': '192.168.1.3'}
                ]
            }
        }

        result = list(command._get_all_target_ips_optimized(targets))
        assert len(result) == 3
        assert [r['ip'] for r in result] == ['192.168.1.1', '192.168.1.2', '192.168.1.3']

    def test_generator_preserves_settings_from_individual_entries(self, command):
        targets = {
            'ilos': {
                'individual': [
                    {'ip': '10.0.0.1', 'skipDns': True, 'skipNtp': False}
                ]
            }
        }

        result = list(command._get_all_target_ips_optimized(targets))
        assert result[0]['settings']['skipDns'] is True
        assert result[0]['settings']['skipNtp'] is False

    def test_generator_preserves_settings_from_range_entries(self, command):
        targets = {
            'ilos': {
                'ranges': [
                    {'start': '10.0.0.1', 'end': '10.0.0.2', 'skipProxy': True}
                ]
            }
        }

        result = list(command._get_all_target_ips_optimized(targets))
        assert all(r['settings']['skipProxy'] is True for r in result)

    def test_generator_raises_error_for_range_exceeding_max_size(self, command):
        targets = {
            'ilos': {
                'ranges': [
                    {'start': '10.0.0.1', 'end': '10.4.0.1'}  # More than 1000 IPs
                ]
            }
        }

        with pytest.raises(InvalidCommandLineError, match="Maximum allowed range size is 1000"):
            list(command._get_all_target_ips_optimized(targets))

    def test_generator_handles_empty_targets(self, command):
        targets = {'ilos': {}}
        result = list(command._get_all_target_ips_optimized(targets))
        assert len(result) == 0

    def test_generator_handles_mixed_individual_and_ranges(self, command):
        targets = {
            'ilos': {
                'individual': [{'ip': '10.0.0.100'}],
                'ranges': [{'start': '10.0.0.1', 'end': '10.0.0.2'}]
            }
        }

        result = list(command._get_all_target_ips_optimized(targets))
        assert len(result) == 3
        ips = [r['ip'] for r in result]
        assert '10.0.0.100' in ips
        assert '10.0.0.1' in ips
        assert '10.0.0.2' in ips


class TestDNSConfiguration:
    """Test DNS configuration with IPv4 and IPv6 support"""

    def test_ipv4_address_detected_correctly(self, command):
        assert command._is_ipv6_address('192.168.1.1') is False
        assert command._is_ipv6_address('10.0.0.1') is False
        assert command._is_ipv6_address('8.8.8.8') is False

    def test_ipv6_address_detected_correctly(self, command):
        assert command._is_ipv6_address('2001:db8::1') is True
        assert command._is_ipv6_address('fe80::1') is True
        assert command._is_ipv6_address('::1') is True

    def test_invalid_ip_address_returns_false(self, command):
        assert command._is_ipv6_address('not.an.ip') is False
        assert command._is_ipv6_address('256.256.256.256') is False
        assert command._is_ipv6_address('') is False

    def test_dns_servers_match_configured_servers_skips_configuration(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=(['8.8.8.8', '8.8.4.4'], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                mock_session.patch = Mock(return_value=create_mock_http_response(200))
                command._configure_dns(mock_session, 'https://10.0.0.100', ['8.8.4.4', '8.8.8.8'])
                mock_session.patch.assert_not_called()

    def test_dns_configuration_separates_ipv4_and_ipv6_servers(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                with patch('requests.Session') as mock_session_class:
                    mock_session_instance = Mock()
                    mock_session_instance.auth = mock_session.auth
                    mock_session_instance.verify = False
                    mock_session_instance.patch = Mock(return_value=create_mock_http_response(200))
                    mock_session_class.return_value = mock_session_instance

                    dns_servers = ['8.8.8.8', '2001:4860:4860::8888', '8.8.4.4']
                    command._configure_dns(mock_session, 'https://10.0.0.100', dns_servers)

                    mock_session_instance.patch.assert_called_once()
                    call_args = mock_session_instance.patch.call_args
                    payload = call_args[1]['json']
                    assert 'IPv4' in payload['Oem']['Hpe']
                    assert 'IPv6' in payload['Oem']['Hpe']

    def test_dns_configuration_disables_dhcp_for_dns(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                with patch('requests.Session') as mock_session_class:
                    mock_session_instance = Mock()
                    mock_session_instance.auth = mock_session.auth
                    mock_session_instance.verify = False
                    mock_session_instance.patch = Mock(return_value=create_mock_http_response(200))
                    mock_session_class.return_value = mock_session_instance

                    command._configure_dns(mock_session, 'https://10.0.0.100', ['8.8.8.8'])

                    call_args = mock_session_instance.patch.call_args
                    payload = call_args[1]['json']
                    assert payload['DHCPv4']['UseDNSServers'] is False
                    assert payload['DHCPv6']['UseDNSServers'] is False

    def test_dns_configuration_handles_connection_error_gracefully(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                with patch('requests.Session') as mock_session_class:
                    mock_session_instance = Mock()
                    mock_session_instance.auth = mock_session.auth
                    mock_session_instance.verify = False
                    mock_session_instance.patch = Mock(side_effect=ConnectionError("Connection lost"))
                    mock_session_class.return_value = mock_session_instance

                    # Should handle connection error gracefully without raising
                    command._configure_dns(mock_session, 'https://10.0.0.100', ['8.8.8.8'])

    def test_dns_configuration_skipped_when_com_already_connected(self, command, mock_session):
        with patch.object(command, '_check_com_connection_status', return_value=True):
            with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
                mock_session.patch = Mock()
                command._configure_dns(mock_session, 'https://10.0.0.100', ['8.8.8.8'])
                mock_session.patch.assert_not_called()

    def test_dns_servers_with_whitespace_stripped_correctly(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                with patch('requests.Session') as mock_session_class:
                    mock_session_instance = Mock()
                    mock_session_instance.auth = mock_session.auth
                    mock_session_instance.verify = False
                    mock_session_instance.patch = Mock(return_value=create_mock_http_response(200))
                    mock_session_class.return_value = mock_session_instance

                    command._configure_dns(mock_session, 'https://10.0.0.100', [' 8.8.8.8 ', '8.8.4.4'])

                    call_args = mock_session_instance.patch.call_args
                    payload = call_args[1]['json']
                    ipv4_dns = payload['Oem']['Hpe']['IPv4']['DNSServers']
                    assert '8.8.8.8' in ipv4_dns

    def test_empty_dns_servers_filtered_out(self, command, mock_session):
        with patch.object(command, '_get_current_dns_servers', return_value=([], False, True)):
            with patch.object(command, '_check_com_connection_status', return_value=False):
                with patch('requests.Session') as mock_session_class:
                    mock_session_instance = Mock()
                    mock_session_instance.auth = mock_session.auth
                    mock_session_instance.verify = False
                    mock_session_instance.patch = Mock(return_value=create_mock_http_response(200))
                    mock_session_class.return_value = mock_session_instance

                    command._configure_dns(mock_session, 'https://10.0.0.100', ['8.8.8.8', '', '  ', '8.8.4.4'])

                    call_args = mock_session_instance.patch.call_args
                    payload = call_args[1]['json']
                    ipv4_dns = payload['Oem']['Hpe']['IPv4']['DNSServers']
                    assert len(ipv4_dns) == 2


class TestiLOVersionDetection:
    """Test iLO version detection and parsing"""

    def test_ilo_version_returns_defaults_when_managers_not_in_response(self, command):
        redfish_data = {'ServiceVersion': '1.0'}
        version, major = command._get_ilo_version_from_response(redfish_data)
        assert version == 0.0
        assert major == 0

    def test_ilo_version_handles_missing_data_gracefully(self, command):
        redfish_data = {}
        version, major = command._get_ilo_version_from_response(redfish_data)
        assert version == 0.0
        assert major == 0

    def test_ilo_info_returns_defaults_on_connection_error(self, command):
        with patch('requests.get', side_effect=ConnectionError("Network error")):
            model, firmware, version, major = command._get_ilo_info('https://10.0.0.100', 'admin', 'password')
            assert model == "iLO5"
            assert firmware == "3.09"
            assert version == 3.09
            assert major == 5


class TestiLOWaitAfterReset:
    """Test waiting for iLO to come back online after reset"""

    def test_ilo_comes_back_online_within_timeout_returns_true(self, command):
        with patch('requests.get') as mock_get:
            mock_get.return_value = create_mock_http_response(200)
            with patch('time.sleep'):
                result = command._wait_for_ilo_after_reset('10.0.0.100', 'admin', 'password')
                assert result is True

    def test_ilo_remains_offline_returns_false_after_timeout(self, command):
        with patch('requests.get', side_effect=ConnectionError("iLO unreachable")):
            with patch('time.sleep'):
                with patch('time.time', side_effect=[0, 10, 20, 30, 181]):
                    result = command._wait_for_ilo_after_reset('10.0.0.100', 'admin', 'password', timeout_minutes=3)
                    assert result is False

    def test_ilo_comes_online_after_initial_failures(self, command):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [
                ConnectionError("Rebooting"),
                ConnectionError("Still rebooting"),
                create_mock_http_response(200)
            ]
            with patch('time.sleep'):
                result = command._wait_for_ilo_after_reset('10.0.0.100', 'admin', 'password')
                assert result is True

    def test_unexpected_error_during_wait_continues_checking(self, command):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [
                Exception("Unexpected error"),
                create_mock_http_response(200)
            ]
            with patch('time.sleep'):
                result = command._wait_for_ilo_after_reset('10.0.0.100', 'admin', 'password')
                assert result is True


class TestCOMConnectionEnabling:
    """Test enabling COM connection with retries and error handling"""

    def test_com_already_connected_returns_success_immediately(self, command, mock_session):
        mock_session.get.return_value = create_mock_http_response(200, {
            'Oem': {
                'Hpe': {
                    'CloudConnect': {'CloudConnectStatus': 'Connected'},
                    'Actions': {'#HpeiLO.EnableCloudConnect': {}}
                }
            }
        })

        success, reason = command._enable_com_connection_requests(
            mock_session, 'https://10.0.0.100', 'ACTIVATION-KEY'
        )
        assert success is True
        assert reason is None

    def test_com_enable_succeeds_after_retry_on_connection_error(self, command, mock_session):
        manager_response = create_mock_http_response(200, {
            'Oem': {
                'Hpe': {
                    'CloudConnect': {'CloudConnectStatus': 'NotEnabled'},
                    'Actions': {'#HpeiLO.EnableCloudConnect': {}}
                }
            }
        })

        connected_response = create_mock_http_response(200, {
            'Oem': {
                'Hpe': {
                    'CloudConnect': {'CloudConnectStatus': 'Connected'},
                    'Actions': {'#HpeiLO.EnableCloudConnect': {}}
                }
            }
        })

        mock_session.get.side_effect = [manager_response, connected_response]

        with patch('requests.Session') as mock_session_class:
            mock_post_session = Mock()
            mock_post_session.auth = mock_session.auth
            mock_post_session.verify = False
            mock_post_session.post.return_value = create_mock_http_response(202)
            mock_session_class.return_value = mock_post_session

            with patch('time.sleep'):
                success, reason = command._enable_com_connection_requests(
                    mock_session, 'https://10.0.0.100', 'KEY'
                )
                assert success is True

    def test_com_enable_fails_when_feature_not_available(self, command, mock_session):
        mock_session.get.return_value = create_mock_http_response(200, {
            'Oem': {'Hpe': {'CloudConnect': {}, 'Actions': {}}}
        })

        success, reason = command._enable_com_connection_requests(
            mock_session, 'https://10.0.0.100', 'KEY'
        )
        assert success is False
        assert reason == "COM feature not available"

    def test_com_enable_timeout_returns_failure(self, command, mock_session):
        manager_response = create_mock_http_response(200, {
            'Oem': {
                'Hpe': {
                    'CloudConnect': {'CloudConnectStatus': 'Connecting'},
                    'Actions': {'#HpeiLO.EnableCloudConnect': {}}
                }
            }
        })

        mock_session.get.return_value = manager_response

        with patch('requests.Session') as mock_session_class:
            mock_post_session = Mock()
            mock_post_session.post.return_value = create_mock_http_response(202)
            mock_session_class.return_value = mock_post_session

            with patch('time.sleep'):
                with patch('time.time', side_effect=[0] + list(range(0, 200, 12))):
                    success, reason = command._enable_com_connection_requests(
                        mock_session, 'https://10.0.0.100', 'KEY'
                    )
                    assert success is False
                    assert "timeout" in reason.lower() or "unknown error" in reason.lower()


class TestJSONReportSaving:
    """Test JSON report saving functionality"""

    def test_save_json_report_creates_file_with_proper_formatting(self, command):
        report = {'iloOnboard': [], 'resultCount': {'ilos': '0'}}

        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_dump:
                command._save_json_report(report, 'output.json')
                mock_dump.assert_called_once()
                assert mock_dump.call_args[1]['indent'] == 2
                assert mock_dump.call_args[1]['sort_keys'] is True

    def test_save_json_report_raises_exception_on_write_failure(self, command):
        with patch('builtins.open', side_effect=IOError("Disk full")):
            with pytest.raises(Exception, match="Failed to save report"):
                command._save_json_report({}, 'output.json')


class TestNetworkSettingsConfiguration:
    """Test network settings configuration including DNS and NTP"""

    def test_network_settings_skipped_when_both_dns_and_ntp_skipped(self, command, mock_session):
        individual_settings = {'skipDns': True, 'skipNtp': True}
        ilo_reset, ntp_needs_reset = command._configure_network_settings_requests(
            mock_session, 'https://10.0.0.100', {}, individual_settings, False
        )
        assert ilo_reset is False
        assert ntp_needs_reset is False

    def test_network_settings_skipped_when_com_already_connected(self, command, mock_session):
        with patch.object(command, '_check_com_connection_status', return_value=True):
            ilo_reset, ntp_needs_reset = command._configure_network_settings_requests(
                mock_session, 'https://10.0.0.100',
                {'dns': ['8.8.8.8'], 'ntp': ['time.google.com']},
                {}, False
            )
            assert ilo_reset is False
            assert ntp_needs_reset is False

    def test_ntp_configured_but_reset_not_allowed_sets_needs_reset_flag(self, command, mock_session):
        with patch.object(command, '_check_com_connection_status', return_value=False):
            with patch.object(command, '_configure_ntp', return_value=(False, False)):
                with patch.object(command, '_configure_dns'):
                    ilo_reset, ntp_needs_reset = command._configure_network_settings_requests(
                        mock_session, 'https://10.0.0.100',
                        {'ntp': ['time.google.com']},
                        {}, False
                    )


class TestProxyConfigurationSkipLogic:
    """Test proxy configuration skip and comparison logic"""

    def test_proxy_configuration_skipped_when_no_proxy_settings_provided(self, command, mock_session):
        with patch.object(command, '_configure_proxy') as mock_configure:
            command._configure_proxy_for_ilo_requests(mock_session, 'https://10.0.0.100', None, {})
            mock_configure.assert_not_called()

    def test_proxy_configuration_skipped_when_proxy_server_empty(self, command, mock_session):
        with patch.object(command, '_configure_proxy') as mock_configure:
            command._configure_proxy_for_ilo_requests(
                mock_session, 'https://10.0.0.100', {'server': '', 'port': 8080}, {}
            )
            mock_configure.assert_not_called()

    def test_proxy_configuration_proceeds_when_valid_server_provided(self, command, mock_session):
        with patch.object(command, '_check_com_connection_status', return_value=False):
            with patch.object(command, '_configure_proxy') as mock_configure:
                with patch('time.sleep'):
                    command._configure_proxy_for_ilo_requests(
                        mock_session, 'https://10.0.0.100',
                        {'server': 'proxy.example.com', 'port': 8080}, {}
                    )
                    mock_configure.assert_called_once()

    def test_proxy_matches_existing_configuration_skips_update(self, command, mock_session):
        current_proxy = {'server': 'proxy.example.com', 'port': 8080, 'username': ''}
        with patch.object(command, '_get_current_proxy_settings', return_value=current_proxy):
            mock_session.patch = Mock()
            command._configure_proxy(
                mock_session, 'https://10.0.0.100',
                {'server': 'proxy.example.com', 'port': 8080}
            )
            mock_session.patch.assert_not_called()

    def test_proxy_port_normalized_to_int_for_comparison(self, command, mock_session):
        current_proxy = {'server': 'proxy.example.com', 'port': 8080, 'username': ''}
        with patch.object(command, '_get_current_proxy_settings', return_value=current_proxy):
            mock_session.patch = Mock()
            command._configure_proxy(
                mock_session, 'https://10.0.0.100',
                {'server': 'proxy.example.com', 'port': '8080'}
            )
            mock_session.patch.assert_not_called()


class TestLargeRangeValidation:
    """Test validation of IP ranges to prevent memory issues"""

    def test_range_exceeding_1000_ips_raises_error_in_list_function(self, command):
        targets = {
            'ilos': {
                'ranges': [{'start': '10.0.0.1', 'end': '10.4.0.1'}]
            }
        }
        with pytest.raises(InvalidCommandLineError, match="Maximum allowed range size is 1000"):
            command._get_all_target_ips(targets)

    def test_range_exactly_1000_ips_succeeds(self, command):
        targets = {
            'ilos': {
                'ranges': [{'start': '10.0.0.1', 'end': '10.0.3.232'}]
            }
        }
        ips = command._get_all_target_ips(targets)
        assert len(ips) == 1000

    def test_multiple_small_ranges_totaling_over_1000_succeeds(self, command):
        targets = {
            'ilos': {
                'ranges': [
                    {'start': '10.0.0.1', 'end': '10.0.2.1'},
                    {'start': '10.1.0.1', 'end': '10.1.2.1'}
                ]
            }
        }
        ips = command._get_all_target_ips(targets)
        assert len(ips) > 1000

    def test_validate_bulk_connect_input_valid_both_activation_and_workspace_id(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"activationKey": "PIN-AAAA-1111", "workspace_id": "WORKSPACE-ID-XYZ-999"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "secret"},
            },
            "targets": {
                "ilos": {
                    "individual": [
                        {"ip": "10.0.0.5"}
                    ],
                    "ranges": []
                }
            }
        }
        command._validate_bulk_connect_input(config)

    def test_validate_bulk_connect_input_valid_individual_and_ranges(self, command):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        config = {
            "commonSettings": {
                "computeOpsManagement": {"workspace_id": "WORKSPACE-ID-12345"},
                "iloAuthentication": {"iloUser": "admin", "iloPassword": "pw"},
            },
            "targets": {
                "ilos": {
                    "individual": [
                        {"ip": "172.16.0.10"}
                    ],
                    "ranges": [
                        {"start": "172.16.0.20", "end": "172.16.0.21"}
                    ]
                }
            }
        }
        command._validate_bulk_connect_input(config)

    @pytest.mark.parametrize(
        "config,expected",
        [
            # Missing top-level commonSettings
            ({}, "Missing 'commonSettings' section in configuration"),
            # commonSettings wrong type
            ({"commonSettings": []}, "'commonSettings' must be a JSON object"),
            # Neither activationKey nor workspace_id
            ({"commonSettings": {"iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {}}, "In 'commonSettings.computeOpsManagement', either 'activationKey' or 'workspace_id' must be provided"),
            # Missing iloAuthentication (after activation key present)
            ({"commonSettings": {"computeOpsManagement": {"activationKey": "X"}}, "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}]}}}, "The operation failed as iLO credential is not provided in the input json"),
            # iloAuthentication not a dict
            ({"commonSettings": {"computeOpsManagement": {"activationKey": "X"}, "iloAuthentication": []}, "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}]}}}, "The operation failed as iLO credential is not provided in the input json"),
            # Missing iloUser or iloPassword
            ({"commonSettings": {"computeOpsManagement": {"activationKey": "X"}, "iloAuthentication": {"iloUser": "u"}}, "targets": {"ilos": {"individual": [{"ip": "192.168.1.10"}], "ranges": []}}}, "The operation failed as iLO credential is not provided in the input json"),
            # Missing targets section
            ({"commonSettings": {"computeOpsManagement": {"activationKey": "X"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}}, "Missing 'targets' section in configuration"),
            # targets wrong type
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": []}, "'targets' must be a JSON object"),
            # Missing ilos
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {}}, "Missing 'ilos' section in 'targets'"),
            # ilos wrong type
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": []}}, "'ilos' in 'targets' must be a JSON object"),
            # individual wrong type
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": {"individual": {}, "ranges": []}}}, "'individual' in 'ilos' must be an array"),
            # ranges wrong type
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": {"individual": [], "ranges": {}}}}, "'ranges' in 'ilos' must be an array"),
            # bad individual entry
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": {"individual": [{}], "ranges": []}}}, "Each entry in 'individual' must be an object with an 'ip' field"),
            # bad range entry
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": {"individual": [], "ranges": [{"start": "192.168.1.1"}]}}}, "Each entry in 'ranges' must be an object with 'start' and 'end' fields"),
            # no ips specified
            ({"commonSettings": {"computeOpsManagement": {"workspace_id": "WORKSPACE-ID-123"}, "iloAuthentication": {"iloUser": "u", "iloPassword": "p"}}, "targets": {"ilos": {"individual": [], "ranges": []}}}, "At least one iLO IP must be specified in 'individual' or 'ranges'"),
        ]
    )
    def test_validate_bulk_connect_input_invalid(self, command, config, expected):
        if not USING_REAL_IMPLEMENTATION:
            pytest.skip("Validation method only exists in real implementation")
        with pytest.raises(InvalidCommandLineError, match=expected):
            command._validate_bulk_connect_input(config)


class TestConfigureNTP:
    """Unit tests for ComputeOpsManagementCommand._configure_ntp"""

    @pytest.fixture
    def patch_requests_session(self):
        with patch('requests.Session') as mock_session_class:
            yield mock_session_class

    def test_configure_ntp_skips_when_already_configured(self, command, mock_session, patch_requests_session):
        # _get_current_ntp_servers returns desired servers
        desired_ntp = ['1.2.3.4', '5.6.7.8']
        with patch.object(command, '_get_current_ntp_servers', return_value=desired_ntp):
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', desired_ntp, allow_ilo_reset=True)
            assert result == (False, False)

    def test_configure_ntp_proceeds_when_servers_differ(self, command, mock_session, patch_requests_session):
        # _get_current_ntp_servers returns different servers
        with patch.object(command, '_get_current_ntp_servers', return_value=['9.9.9.9']):
            # Mock enabled interface
            eth_response = create_mock_http_response(200, {'Members': [{'@odata.id': '/eth/1'}]})
            enabled_interface = create_mock_http_response(200, {
                'Status': {'State': 'Enabled'},
                'Oem': {'Hpe': {'DHCPv4': {}, 'DHCPv6': {}}},
                '@odata.id': '/eth/1'
            })
            mock_session.get.side_effect = [eth_response, enabled_interface]
            mock_session.patch.return_value = create_mock_http_response(200)
            mock_session.post.return_value = create_mock_http_response(200)

            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=True)
            assert result[0] is True  # ilo_was_reset

    def test_configure_ntp_handles_no_enabled_interface(self, command, mock_session, patch_requests_session):
        # No enabled interface found
        with patch.object(command, '_get_current_ntp_servers', return_value=None):
            eth_response = create_mock_http_response(200, {'Members': []})
            mock_session.get.return_value = eth_response
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=False)
            assert result[0] is False

    def test_configure_ntp_handles_patch_failure(self, command, mock_session, patch_requests_session):
        # Patch returns error code
        with patch.object(command, '_get_current_ntp_servers', return_value=None):
            eth_response = create_mock_http_response(200, {'Members': [{'@odata.id': '/eth/1'}]})
            enabled_interface = create_mock_http_response(200, {
                'Status': {'State': 'Enabled'},
                'Oem': {'Hpe': {'DHCPv4': {}, 'DHCPv6': {}}},
                '@odata.id': '/eth/1'
            })
            patch_requests_session.return_value.patch.return_value = create_mock_http_response(500)
            mock_session.get.side_effect = [eth_response, enabled_interface]
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=False)
            assert result[0] is False

    def test_configure_ntp_handles_connection_error(self, command, mock_session, patch_requests_session):
        # Simulate ConnectionError during ethernet interface check
        # Connection errors are caught and logged, but don't trigger reset
        with patch.object(command, '_get_current_ntp_servers', return_value=None):
            mock_session.get.side_effect = ConnectionError("Connection failed")
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=True)
            assert result[0] is False  # Connection error caught, no reset occurs

    def test_configure_ntp_handles_timeout(self, command, mock_session, patch_requests_session):
        # Simulate Timeout during ethernet interface check
        # Timeout errors are caught and logged, but don't trigger reset
        with patch.object(command, '_get_current_ntp_servers', return_value=None):
            mock_session.get.side_effect = Timeout("Timeout")
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=True)
            assert result[0] is False  # Timeout caught, no reset occurs

    def test_configure_ntp_handles_generic_exception(self, command, mock_session, patch_requests_session):
        # Simulate generic Exception
        with patch.object(command, '_get_current_ntp_servers', return_value=None):
            mock_session.get.side_effect = Exception("Generic error")
            result = command._configure_ntp(mock_session, 'https://ilo.example.com', ['1.2.3.4'], allow_ilo_reset=True)
            assert result[0] is False

class TestPrecheckValidateDNSSettings:
    """Unit tests for ComputeOpsManagementCommand._precheck_validate_dns_settings"""

    @pytest.fixture
    def command_with_logger(self, command):
        # Patch LOGGER for info/error calls
        with patch('ilorest.extensions.iLO_COMMANDS.ComputeOpsManagementCommand.LOGGER', Mock()) as mock_logger:
            yield command

    @pytest.fixture
    def validation_data(self):
        return {
            "status": "FAILED",
             "error": "",
            "recommendation": "",
            "managementProcessorModel": "",
            "iloVersion": "",
        }

    def test_returns_error_when_dhcp_check_not_attempted(self, command_with_logger, validation_data):
        # Simulate _get_current_dns_servers returns dhcp_check_attempted=False
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=([], False, False)):
            merged_network = {}
            individual_network = {}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is False
            assert result["error"] == "Unable to retrieve DNS settings from iLO"
            assert "Check iLO connectivity" in result["recommendation"]

    def test_skipdns_flag_set_and_no_dns_configured_sets_error(self, command_with_logger, validation_data):
        # No DNS servers, skipDns True, merged_network has dns
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=([], False, True)):
            merged_network = {"dns": ["8.8.8.8"]}
            individual_network = {"skipDns": True}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is False
            assert result["error"] == "No DNS configuration found in iLO"
            assert "Remove skipDns" in result["recommendation"]

    def test_skipdns_flag_set_and_no_dns_in_input_sets_error(self, command_with_logger, validation_data):
        # No DNS servers, skipDns True, merged_network has no dns
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=([], False, True)):
            merged_network = {}
            individual_network = {"skipDns": True}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is False
            assert result["error"] == "No DNS configuration found in iLO"
            assert "Configure DNS in iLO" in result["recommendation"]

    def test_no_dns_in_input_and_no_dns_configured_sets_error(self, command_with_logger, validation_data):
        # No DNS servers, merged_network has no dns, skipDns False
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=([], False, True)):
            merged_network = {}
            individual_network = {}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is False
            assert result["error"] == "No DNS configuration found in iLO"
            assert "Configure DNS in iLO" in result["recommendation"]

    def test_dns_precheck_passed_when_dns_configured(self, command_with_logger, validation_data):
        # DNS servers present, dhcp enabled, dhcp_check_attempted True
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=(["8.8.8.8"], True, True)):
            merged_network = {"dns": ["8.8.8.8"]}
            individual_network = {}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is True
            assert result["error"] == ""
            assert result["recommendation"] == ""

    def test_dns_precheck_passed_when_skipdns_false_and_dns_configured(self, command_with_logger, validation_data):
        # DNS servers present, skipDns False
        with patch.object(command_with_logger, '_get_current_dns_servers', return_value=(["8.8.8.8"], False, True)):
            merged_network = {"dns": ["8.8.8.8"]}
            individual_network = {"skipDns": False}
            status, result = command_with_logger._precheck_validate_dns_settings(
                Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
            )
            assert status is True
            assert result["error"] == ""
            assert result["recommendation"] == ""


class TestPrecheckValidateNTPSettings:
    """Unit tests for ComputeOpsManagementCommand._precheck_validate_ntp_settings"""

    @pytest.fixture
    def command_with_logger(self, command):
        # Patch LOGGER for info/error calls
        with patch('ilorest.extensions.iLO_COMMANDS.ComputeOpsManagementCommand.LOGGER', Mock()) as mock_logger:
            yield command

    @pytest.fixture
    def validation_data(self):
         return {
            "status": "FAILED",
            "error": "",
            "recommendation": "",
            "managementProcessorModel": "",
            "iloVersion": "",
        }

    def test_returns_error_when_dhcp_check_not_attempted(self, command_with_logger, validation_data):
        # Simulate _check_dhcp_ntp_config_on_interfaces returns dhcp_check_attempted=False
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, False)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=['time.google.com']):
                merged_network = {}
                individual_network = {}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is False
                assert result["error"] == "Unable to retrieve NTP settings from iLO"
                assert "Check iLO connectivity" in result["recommendation"]

    def test_returns_error_when_ntp_servers_none(self, command_with_logger, validation_data):
        # Simulate _get_current_ntp_servers returns None
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=None):
                merged_network = {}
                individual_network = {}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is False
                assert result["error"] == "Unable to retrieve NTP settings from iLO"
                assert "Check iLO connectivity" in result["recommendation"]

    def test_skipntp_flag_set_and_no_ntp_configured_sets_error(self, command_with_logger, validation_data):
        # No NTP servers, skipNtp True, merged_network has ntp
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=[]):
                merged_network = {"ntp": ["time.google.com"]}
                individual_network = {"skipNtp": True}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is True
                assert result["error"] == "No NTP configuration found in iLO"
                assert "Remove skipNtp" in result["recommendation"]

    def test_skipntp_flag_set_and_no_ntp_in_input_sets_error(self, command_with_logger, validation_data):
        # No NTP servers, skipNtp True, merged_network has no ntp
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=[]):
                merged_network = {}
                individual_network = {"skipNtp": True}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is True
                assert result["error"] == "No NTP configuration found in iLO"
                assert "Configure NTP in iLO" in result["recommendation"]

    def test_no_ntp_in_input_and_no_ntp_configured_sets_error(self, command_with_logger, validation_data):
        # No NTP servers, merged_network has no ntp, skipNtp False
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=[]):
                merged_network = {}
                individual_network = {}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is True
                assert result["error"] == "No NTP configuration found in iLO"
                assert "Configure NTP in iLO" in result["recommendation"]

    def test_ntp_precheck_passed_when_ntp_configured(self, command_with_logger, validation_data):
        # NTP servers present, dhcp enabled, dhcp_check_attempted True
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(True, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=["time.google.com"]):
                merged_network = {"ntp": ["time.google.com"]}
                individual_network = {}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is True
                assert result["error"] == ""
                assert result["recommendation"] == ""

    def test_ntp_precheck_passed_when_skipntp_false_and_ntp_configured(self, command_with_logger, validation_data):
        # NTP servers present, skipNtp False
        with patch.object(command_with_logger, '_check_dhcp_ntp_config_on_interfaces', return_value=(False, None, True)):
            with patch.object(command_with_logger, '_get_current_ntp_servers', return_value=["time.google.com"]):
                merged_network = {"ntp": ["time.google.com"]}
                individual_network = {"skipNtp": False}
                status, result = command_with_logger._precheck_validate_ntp_settings(
                    Mock(), "https://ilo.example.com", merged_network, individual_network, validation_data.copy()
                )
                assert status is True
                assert result["error"] == ""
                assert result["recommendation"] == ""


class TestValidateSingleILOForPrecheck:
    """Unit tests for ComputeOpsManagementCommand._validate_single_ilo_for_precheck"""

    @pytest.fixture
    def command(self, mock_rdmc):
        cmd = ComputeOpsManagementCommand()
        cmd.rdmc = mock_rdmc
        return cmd

    @pytest.fixture
    def ilo_auth(self):
        return {"iloUser": "admin", "iloPassword": "pw"}

    @pytest.fixture
    def com_settings(self):
        return {"activationKey": "KEY-123", "workspace_id": "WORKSPACE-ID-456"}

    @pytest.fixture
    def network_settings(self):
        return {"dns": ["8.8.8.8"], "ntp": ["time.google.com"]}

    @pytest.fixture
    def individual_settings(self):
        return {"network": {"dns": ["1.1.1.1"]}}

    def test_returns_error_when_no_password(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        ilo_auth = {"iloUser": "admin"}
        result = command._validate_single_ilo_for_precheck(
            "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
        )
        assert result["status"] == "FAILED"
        assert "No password provided" in result["error"]

    def test_returns_error_when_connectivity_fails(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        with patch("requests.get", side_effect=Exception("Conn error")):
            result = command._validate_single_ilo_for_precheck(
                "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
            )
            assert result["status"] == "FAILED"
            assert "Authentication or connectivity failed" in result["error"]

    def test_returns_error_when_http_status_not_200(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 401
        with patch("requests.get", return_value=mock_resp):
            result = command._validate_single_ilo_for_precheck(
                "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
            )
            assert result["status"] == "FAILED"
            assert "HTTP 401" in result["error"]

    def test_returns_error_when_version_not_compatible(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 4)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(False, "bad", "rec")):
                    result = command._validate_single_ilo_for_precheck(
                        "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                    )
                    assert result["status"] == "FAILED"
                    assert result["error"] == "bad"
                    assert result["recommendation"] == "rec"

    def test_returns_passed_when_ilo_already_connected(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session") as mock_session_class:
                        mock_session = Mock()
                        mock_session_class.return_value = mock_session
                        with patch.object(command, "_check_com_connection_status", return_value=True):
                            result = command._validate_single_ilo_for_precheck(
                                "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                            )
                            assert result["status"] == "PASSED"

    def test_returns_error_when_workspace_id_required_and_missing(self, command, ilo_auth, network_settings, individual_settings):
        com_settings = {}
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session"):
                        with patch.object(command, "_check_com_connection_status", return_value=False):
                            with patch.object(command, "_is_pin_onboarding_supported", return_value=False):
                                result = command._validate_single_ilo_for_precheck(
                                    "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                                )
                                assert "requires a valid workspace_id" in result["error"]

    def test_returns_error_when_activation_key_required_and_missing(self, command, ilo_auth, network_settings, individual_settings):
        com_settings = {}
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session"):
                        with patch.object(command, "_check_com_connection_status", return_value=False):
                            with patch.object(command, "_is_pin_onboarding_supported", return_value=True):
                                result = command._validate_single_ilo_for_precheck(
                                    "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                                )
                                assert "requires a valid activation Key" in result["error"]

    def test_returns_failed_when_dns_precheck_fails(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session"):
                        with patch.object(command, "_check_com_connection_status", return_value=False):
                            with patch.object(command, "_is_pin_onboarding_supported", return_value=True):
                                with patch.object(command, "_precheck_validate_dns_settings", return_value=(False, {"status": "FAILED", "error": "dns error"})):
                                    result = command._validate_single_ilo_for_precheck(
                                        "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                                    )
                                    assert result["status"] == "FAILED"
                                    assert "dns error" in result["error"]

    def test_returns_failed_when_ntp_precheck_fails(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session"):
                        with patch.object(command, "_check_com_connection_status", return_value=False):
                            with patch.object(command, "_is_pin_onboarding_supported", return_value=True):
                                with patch.object(command, "_precheck_validate_dns_settings", return_value=(True, {})):
                                    with patch.object(command, "_precheck_validate_ntp_settings", return_value=(False, {"status": "FAILED", "error": "ntp error"})):
                                        result = command._validate_single_ilo_for_precheck(
                                            "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                                        )
                                        assert result["status"] == "FAILED"
                                        assert "ntp error" in result["error"]

    def test_returns_passed_when_all_checks_pass(self, command, ilo_auth, com_settings, network_settings, individual_settings):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        with patch("requests.get", return_value=mock_resp):
            with patch.object(command, "_get_ilo_version_from_response", return_value=(5, 5)):
                with patch.object(command, "_check_ilo_version_compatibility", return_value=(True, "", "")):
                    with patch("requests.Session"):
                        with patch.object(command, "_check_com_connection_status", return_value=False):
                            with patch.object(command, "_is_pin_onboarding_supported", return_value=True):
                                with patch.object(command, "_precheck_validate_dns_settings", return_value=(True, {})):
                                    with patch.object(command, "_precheck_validate_ntp_settings", return_value=(True, {})):
                                        result = command._validate_single_ilo_for_precheck(
                                            "10.0.0.1", ilo_auth, com_settings, network_settings, individual_settings
                                        )
                                        assert result["status"] == "PASSED"

