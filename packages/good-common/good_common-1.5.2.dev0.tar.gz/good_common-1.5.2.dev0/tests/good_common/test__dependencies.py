import pytest
import warnings
from fast_depends import inject
from good_common.dependencies import BaseProvider, AsyncBaseProvider
from typing import Annotated


def test__basic_base_provider():
    class FakeClient:
        def __init__(self, host: str, port: int):
            self.host = host
            self.port = port

        def __str__(self):
            return f"{self.host}:{self.port}"

    class ClientProvider(BaseProvider[FakeClient]):
        pass

    @inject
    def test_client(
        client: Annotated[FakeClient, ClientProvider(host="localhost", port=8080)],
    ):
        assert client.host == "localhost"
        assert client.port == 8080

    test_client()


def test__dependency_with_runtime_config():
    class FakeClient:
        def __init__(self, host: str, port: int, db: str):
            self.host = host
            self.port = port
            self.db = db

        def __str__(self):
            return f"{self.host}:{self.port}:{self.db}"

    class ClientProvider(BaseProvider[FakeClient]):
        def initializer(self, cls_args: tuple, cls_kwargs: dict, fn_kwargs: dict):
            if fn_kwargs.get("db"):
                cls_kwargs["db"] = fn_kwargs["db"]
            return cls_args, cls_kwargs

    @inject
    def test_client(
        db: str,
        client: Annotated[FakeClient, ClientProvider(host="localhost", port=8080)],
    ):
        assert client.host == "localhost"
        assert client.port == 8080
        assert client.db == "test"

    test_client(db="test")


@pytest.mark.asyncio
async def test__basic_async_base_provider():
    class FakeClient:
        def __init__(self, host: str, port: int):
            self.host = host
            self.port = port

        def __str__(self):
            return f"{self.host}:{self.port}"

    class ClientProvider(AsyncBaseProvider[FakeClient]):
        pass

    @inject
    async def test_client(
        client: Annotated[
            FakeClient, ClientProvider(host="localhost", port=8080)
        ] = None,
    ):
        assert client.host == "localhost"
        assert client.port == 8080

    await test_client()


def test__old_pattern_backward_compatibility():
    """Test that the old pattern still works for backward compatibility"""

    # Suppress the deprecation warning for this test since we're testing backward compatibility
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)

        class LegacyClient:
            def __init__(self, url: str):
                self.url = url

        # Old pattern - inheriting from both BaseProvider[T] and T
        class LegacyClientProvider(BaseProvider[LegacyClient], LegacyClient):
            pass

        @inject
        def test_legacy(
            client: LegacyClient = LegacyClientProvider(url="http://example.com"),
        ):
            assert client.url == "http://example.com"

        test_legacy()


def test__provider_with_override_class():
    """Test provider with __override_class__"""

    # Suppress the deprecation warning since we're testing __override_class__ functionality
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)

        class BaseService:
            def __init__(self, name: str):
                self.name = name

        class ExtendedService(BaseService):
            def __init__(self, name: str, extra: str = "default"):
                super().__init__(name)
                self.extra = extra

        class ServiceProvider(BaseProvider[BaseService]):
            __override_class__ = ExtendedService

        @inject
        def test_service(
            service: BaseService = ServiceProvider(name="test", extra="custom"),
        ):
            assert service.name == "test"
            assert isinstance(service, ExtendedService)
            assert service.extra == "custom"

        test_service()


def test__missing_generic_type_error():
    """Test that we get a helpful error when generic type can't be determined"""

    # This should fail because BaseProvider is not parameterized
    class BadProvider(BaseProvider):  # type: ignore
        pass

    with pytest.raises(TypeError) as exc_info:
        BadProvider.provide(name="test")

    assert "Could not determine target class" in str(exc_info.value)
    assert "BaseProvider[YourClass]" in str(exc_info.value)


@pytest.mark.asyncio
async def test__async_provider_new_pattern():
    """Test async provider with new pattern"""

    class AsyncService:
        def __init__(self, endpoint: str):
            self.endpoint = endpoint
            self.initialized = False

    class AsyncServiceProvider(AsyncBaseProvider[AsyncService]):
        async def on_initialize(self, instance, **kwargs):
            instance.initialized = True

    @inject
    async def test_service(
        service: Annotated[
            AsyncService, AsyncServiceProvider(endpoint="http://api.example.com")
        ],
    ):
        assert service.endpoint == "http://api.example.com"
        assert service.initialized

    await test_service()


def test__deprecation_warning_for_old_pattern():
    """Test that deprecation warning is shown for old pattern"""

    class TestClient:
        def __init__(self, name: str):
            self.name = name

    class TestProvider(BaseProvider[TestClient]):
        pass

    # This should trigger a deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", DeprecationWarning)

        @inject
        def test_func(client: TestClient = TestProvider(name="test")):
            return client

        test_func()

        # Filter for only our specific deprecation warning (not library warnings)
        our_warnings = [
            x
            for x in w
            if issubclass(x.category, DeprecationWarning)
            and "Annotated" in str(x.message)
        ]

        # Check that our warning was issued
        assert len(our_warnings) == 1
        assert "deprecated" in str(our_warnings[0].message)
        assert "TestClient" in str(our_warnings[0].message)
        assert "TestProvider" in str(our_warnings[0].message)


def test__no_warning_for_new_pattern():
    """Test that NO deprecation warning is shown for new Annotated pattern"""

    class TestClient:
        def __init__(self, name: str):
            self.name = name

    class TestProvider(BaseProvider[TestClient]):
        pass

    # This should NOT trigger our deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", DeprecationWarning)

        @inject
        def test_func(client: Annotated[TestClient, TestProvider(name="test")]):
            return client

        test_func()

        # Filter for only our specific deprecation warning (not library warnings)
        our_warnings = [
            x
            for x in w
            if issubclass(x.category, DeprecationWarning)
            and "Annotated" in str(x.message)
        ]

        # Check that NO warning was issued for the new pattern
        assert len(our_warnings) == 0


def test__warning_shown_only_once():
    """Test that deprecation warning is only shown once per provider instance"""

    class TestClient:
        def __init__(self, name: str):
            self.name = name

    class TestProvider(BaseProvider[TestClient]):
        pass

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", DeprecationWarning)

        @inject
        def test_func(client: TestClient = TestProvider(name="test")):
            return client

        # Call multiple times
        test_func()
        test_func()
        test_func()

        # Filter for only our specific deprecation warning
        our_warnings = [
            x
            for x in w
            if issubclass(x.category, DeprecationWarning)
            and "Annotated" in str(x.message)
        ]

        # Should only have one warning
        assert len(our_warnings) == 1


@pytest.mark.asyncio
async def test__async_deprecation_warning():
    """Test deprecation warning for async providers"""

    class TestService:
        def __init__(self, url: str):
            self.url = url

    class TestProvider(AsyncBaseProvider[TestService]):
        pass

    # This should trigger a deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", DeprecationWarning)

        @inject
        async def test_func(
            service: TestService = TestProvider(url="http://example.com"),
        ):
            return service

        await test_func()

        # Filter for only our specific deprecation warning
        our_warnings = [
            x
            for x in w
            if issubclass(x.category, DeprecationWarning)
            and "Annotated" in str(x.message)
        ]

        # Check that our warning was issued
        assert len(our_warnings) == 1
        assert "deprecated" in str(our_warnings[0].message)
