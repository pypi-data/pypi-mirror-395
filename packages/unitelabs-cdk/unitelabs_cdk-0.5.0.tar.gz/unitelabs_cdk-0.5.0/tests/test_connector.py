import unittest.mock

import pytest
from sila.server import discovery

from unitelabs.cdk.config.connector_base_config import ConnectorBaseConfig
from unitelabs.cdk.connector import Connector


@pytest.fixture
def no_broadcast(monkeypatch):
    class FakeBroadcaster(discovery.Discovery):
        """Fake Broadcaster."""

        def __init__(self, *args, **kwargs):
            self.start = unittest.mock.AsyncMock()
            self.stop = unittest.mock.AsyncMock()

    monkeypatch.setattr(discovery, "Discovery", FakeBroadcaster)


class TestConnector:
    # Create a new connector with default values
    async def test_create_new_connector_with_default_values(self, no_broadcast):
        connector = Connector()
        assert connector.config.sila_server is not None
        assert connector.config.sila_server.hostname == "0.0.0.0"
        assert connector.config.sila_server.port == 0
        assert not connector.config.sila_server.tls
        assert not connector.config.sila_server.require_client_auth
        assert not connector.config.sila_server.root_certificates
        assert not connector.config.sila_server.certificate_chain
        assert not connector.config.sila_server.private_key
        assert connector.config.sila_server.version == "0.1"
        assert connector.config.sila_server.name == "SiLA Server"
        assert connector.config.sila_server.type == "ExampleServer"
        assert connector.config.sila_server.vendor_url == "https://sila-standard.com"

        assert connector.config.cloud_server_endpoint is not None
        assert connector.config.cloud_server_endpoint.hostname == "localhost"
        assert connector.config.cloud_server_endpoint.port == 50000
        assert connector.config.cloud_server_endpoint.tls
        assert not connector.config.cloud_server_endpoint.root_certificates
        assert not connector.config.cloud_server_endpoint.certificate_chain
        assert not connector.config.cloud_server_endpoint.private_key
        assert connector.config.cloud_server_endpoint.reconnect_delay == 10000
        assert connector.config.cloud_server_endpoint.options == {
            "grpc.keepalive_time_ms": 60 * 1000,
            "grpc.keepalive_timeout_ms": 3 * 60 * 1000,
            "grpc.keepalive_permit_without_calls": 0,
            "grpc.http2.max_pings_without_data": 0,
        }

    async def test_default_config_starts_all_services(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            connector = Connector()
            assert connector.config
            assert connector._sila_server is not None
            assert connector._discovery is not None
            assert connector._cloud_server is not None

    @pytest.mark.parametrize(
        "sila_server_config,discovery_config,cloud_server_config",
        [
            pytest.param(None, None, None, id="no services"),
            pytest.param(None, None, {}, id="only cloud server"),
            pytest.param({}, None, None, id="only sila server"),
            pytest.param({}, {}, None, id="sila server and discovery"),
        ],
    )
    async def test_should_only_start_configured_services(
        self, no_broadcast, sila_server_config, discovery_config, cloud_server_config
    ):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            config = ConnectorBaseConfig()
            for config_value, key in [
                (sila_server_config, "sila_server"),
                (discovery_config, "discovery"),
                (cloud_server_config, "cloud_server_endpoint"),
            ]:
                if config_value is None:
                    setattr(config, key, None)

            connector = Connector(config=config)

            assert connector.config
            if sila_server_config is None:
                assert connector._sila_server is None
            if discovery_config is None:
                assert connector._discovery is None
            if cloud_server_config is None:
                assert connector._cloud_server is None

    async def test_should_not_allow_only_discovery(self, no_broadcast):
        config = ConnectorBaseConfig()
        config.sila_server = None
        config.cloud_server_endpoint = None

        connector = Connector(config=config)
        assert connector.sila_server is None
        assert connector._cloud_server is None
        assert connector._discovery is None


class TestRegister:
    async def test_register_feature_without_sila_server_raises_runtime_error(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            config = ConnectorBaseConfig(sila_server=None)
            connector = Connector(config=config)

            with pytest.raises(RuntimeError, match=r"Cannot register feature when SiLA server is not configured."):
                connector.register(unittest.mock.Mock())


class TestStart:
    # The start method calls stop after cancellation
    async def test_start_calls_stop_on_cancellation(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            connector = Connector()
            connector.stop = unittest.mock.AsyncMock()

            await connector.start()
            await connector.stop()

            connector.stop.assert_awaited_once_with()


class TestClose:
    # The stop method calls shutdown handlers
    async def test_stop_calls_shutdown_handlers(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            handler = unittest.mock.Mock()
            connector = Connector()
            connector.on_shutdown(handler=handler)

            await connector.stop()

            handler.assert_called_once_with()

    # The stop method calls shutdown handlers in order of registration
    async def test_stop_calls_shutdown_handlers_in_order(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            handler = unittest.mock.Mock()
            handler.handler_1 = unittest.mock.Mock()
            handler.handler_2 = unittest.mock.Mock()
            connector = Connector()
            connector.on_shutdown(handler=handler.handler_1)
            connector.on_shutdown(handler=handler.handler_2)

            await connector.stop()

            handler.assert_has_calls([unittest.mock.call.handler_1(), unittest.mock.call.handler_2()])

    # The stop method calls async shutdown handlers
    async def test_stop_calls_async_shutdown(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            handler = unittest.mock.AsyncMock()
            connector = Connector()
            connector.on_shutdown(handler=handler)

            await connector.start()
            await connector.stop()

            handler.assert_awaited_once_with()

    # The stop method ignores exception in shutdown handlers
    async def test_stop_ignores_exception_in_shutdown(self, no_broadcast):
        with (
            unittest.mock.patch("sila.server.Server", spec=True),
            unittest.mock.patch("sila.server.Discovery", spec=True),
            unittest.mock.patch("sila.server.CloudServer", spec=True),
        ):
            handler_1 = unittest.mock.Mock(side_effect=RuntimeError)
            handler_2 = unittest.mock.AsyncMock(side_effect=RuntimeError)
            connector = Connector()
            connector.on_shutdown(handler=handler_1)
            connector.on_shutdown(handler=handler_2)

            await connector.start()
            await connector.stop()

            handler_1.assert_called_once_with()
            handler_2.assert_awaited_once_with()


class TestOnShutdown:
    # Can add a shutdown handler to the list of handlers
    async def test_add_shutdown_handler(self, no_broadcast):
        connector = Connector()

        def shutdown_handler():
            print("Shutdown handler called")

        connector.on_shutdown(shutdown_handler)

        assert len(connector._shutdown_handlers) == 1
        assert connector._shutdown_handlers[0] == shutdown_handler

    # Adding a shutdown handler with a non-callable object raises a TypeError
    async def test_add_non_callable_handler_raises_type_error(self, no_broadcast):
        connector = Connector()
        non_callable_handler = "not a callable object"

        with pytest.raises(TypeError, match=r"The `handler` argument must be callable."):
            connector.on_shutdown(
                non_callable_handler,  # type: ignore
            )


class TestOffShutdown:
    # Can remove a previously added shutdown hook
    async def test_remove_shutdown_hook(self, no_broadcast):
        # Initialize the class object
        connector = Connector()

        # Define a mock handler
        mock_handler = unittest.mock.Mock()

        # Add the mock handler to the shutdown handlers list
        connector.on_shutdown(mock_handler)

        # Remove the mock handler using off_shutdown method
        connector.off_shutdown(mock_handler)

        # Assert that the mock handler is no longer in the shutdown handlers list
        assert mock_handler not in connector._shutdown_handlers

    # removing a shutdown hook from an empty list of shutdown handlers
    async def test_remove_shutdown_hook_from_empty_list(self, no_broadcast):
        # Initialize the class object
        connector = Connector()

        # Define a mock handler
        mock_handler = unittest.mock.Mock()

        # Remove the mock handler using off_shutdown method
        connector.off_shutdown(mock_handler)

        # Assert that the mock handler is still not in the shutdown handlers list
        assert mock_handler not in connector._shutdown_handlers
