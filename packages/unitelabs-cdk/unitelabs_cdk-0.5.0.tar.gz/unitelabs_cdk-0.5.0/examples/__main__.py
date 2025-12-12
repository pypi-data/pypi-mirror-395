import asyncio
import logging

from unitelabs.cdk import Connector, run
from unitelabs.cdk.config import CloudServerConfig, ConnectorBaseConfig, SiLAServerConfig
from unitelabs.cdk.features.core.authorization_service import AuthorizationService
from unitelabs.cdk.features.test.any_type_test import AnyTypeTest
from unitelabs.cdk.features.test.authentication_test import AuthenticationTest
from unitelabs.cdk.features.test.basic_data_types_test import BasicDataTypesTest
from unitelabs.cdk.features.test.binary_transfer_test import BinaryTransferTest
from unitelabs.cdk.features.test.error_handling_test import ErrorHandlingTest
from unitelabs.cdk.features.test.list_data_type_test import ListDataTypeTest
from unitelabs.cdk.features.test.metadata_consumer_test import MetadataConsumerTest
from unitelabs.cdk.features.test.metadata_provider import MetadataProvider
from unitelabs.cdk.features.test.observable_command_test import ObservableCommandTest
from unitelabs.cdk.features.test.observable_property_test import ObservablePropertyTest
from unitelabs.cdk.features.test.structure_data_type_test import StructureDataTypeTest
from unitelabs.cdk.features.test.unobservable_command_test import UnobservableCommandTest
from unitelabs.cdk.features.test.unobservable_property_test import UnobservablePropertyTest

from .features import AuthenticationService

logging.basicConfig(level=logging.INFO, force=True)


async def app_factory():
    app = Connector(
        ConnectorBaseConfig(
            sila_server=SiLAServerConfig(
                port=50052,
                tls=False,
                uuid="2be7e3fe-6a53-48fd-81d9-116f7cc5b59b",
                name="SiLA Python Interoperability Test Server",
                type="TestServer",
                version="0.1",
                description="This server aims to implement all features required for the SiLA Interoperability Test Suite",
                vendor_url="https://gitlab.com/SiLA2/sila_python",
            ),
            cloud_server_endpoint=CloudServerConfig(
                tls=False,
            ),
        )
    )
    app.register(AnyTypeTest())
    app.register(AuthenticationService())
    app.register(AuthenticationTest())
    app.register(AuthorizationService())
    app.register(BasicDataTypesTest())
    app.register(BinaryTransferTest())
    app.register(ErrorHandlingTest())
    app.register(ListDataTypeTest())
    app.register(MetadataConsumerTest())
    app.register(MetadataProvider())
    app.register(ObservableCommandTest())
    app.register(ObservablePropertyTest())
    app.register(StructureDataTypeTest())
    app.register(UnobservableCommandTest())
    app.register(UnobservablePropertyTest())

    yield app


if __name__ == "__main__":
    asyncio.run(run(app_factory))
