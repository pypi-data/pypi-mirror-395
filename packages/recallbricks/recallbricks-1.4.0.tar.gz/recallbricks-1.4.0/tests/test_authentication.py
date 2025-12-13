"""
Test authentication functionality for RecallBricks Python SDK
Tests both API key and service token authentication methods
"""

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False

from recallbricks import RecallBricks, AuthenticationError


class TestAuthenticationMethods:
    """Test various authentication scenarios"""

    def test_api_key_authentication(self):
        """Test API key authentication creates correct headers"""
        client = RecallBricks(api_key="rb_dev_test123")
        assert client.api_key == "rb_dev_test123"
        assert client.service_token is None
        assert 'X-API-Key' in client.session.headers
        assert client.session.headers['X-API-Key'] == "rb_dev_test123"
        assert 'X-Service-Token' not in client.session.headers

    def test_service_token_authentication(self):
        """Test service token authentication creates correct headers"""
        client = RecallBricks(service_token="rbk_service_test123")
        assert client.service_token == "rbk_service_test123"
        assert client.api_key is None
        assert 'X-Service-Token' in client.session.headers
        assert client.session.headers['X-Service-Token'] == "rbk_service_test123"
        assert 'X-API-Key' not in client.session.headers

    def test_no_authentication_raises_error(self):
        """Test that missing both api_key and service_token raises error"""
        if HAS_PYTEST:
            with pytest.raises(AuthenticationError) as exc_info:
                RecallBricks()
            assert "Either api_key or service_token is required" in str(exc_info.value)
        else:
            try:
                RecallBricks()
                raise AssertionError("Expected AuthenticationError")
            except AuthenticationError as e:
                assert "Either api_key or service_token is required" in str(e)

    def test_both_authentication_methods_raises_error(self):
        """Test that providing both api_key and service_token raises error"""
        if HAS_PYTEST:
            with pytest.raises(AuthenticationError) as exc_info:
                RecallBricks(api_key="rb_dev_test", service_token="rbk_service_test")
            assert "Provide either api_key or service_token, not both" in str(exc_info.value)
        else:
            try:
                RecallBricks(api_key="rb_dev_test", service_token="rbk_service_test")
                raise AssertionError("Expected AuthenticationError")
            except AuthenticationError as e:
                assert "Provide either api_key or service_token, not both" in str(e)

    def test_empty_api_key_raises_error(self):
        """Test that empty api_key is treated as missing"""
        if HAS_PYTEST:
            with pytest.raises(AuthenticationError) as exc_info:
                RecallBricks(api_key="")
            assert "Either api_key or service_token is required" in str(exc_info.value)
        else:
            try:
                RecallBricks(api_key="")
                raise AssertionError("Expected AuthenticationError")
            except AuthenticationError as e:
                assert "Either api_key or service_token is required" in str(e)

    def test_empty_service_token_raises_error(self):
        """Test that empty service_token is treated as missing"""
        if HAS_PYTEST:
            with pytest.raises(AuthenticationError) as exc_info:
                RecallBricks(service_token="")
            assert "Either api_key or service_token is required" in str(exc_info.value)
        else:
            try:
                RecallBricks(service_token="")
                raise AssertionError("Expected AuthenticationError")
            except AuthenticationError as e:
                assert "Either api_key or service_token is required" in str(e)

    def test_api_key_with_custom_base_url(self):
        """Test API key authentication with custom base URL"""
        client = RecallBricks(
            api_key="rb_dev_test",
            base_url="https://custom.api.com"
        )
        assert client.api_key == "rb_dev_test"
        assert client.base_url == "https://custom.api.com"
        assert 'X-API-Key' in client.session.headers

    def test_service_token_with_custom_base_url(self):
        """Test service token authentication with custom base URL"""
        client = RecallBricks(
            service_token="rbk_service_test",
            base_url="https://custom.api.com"
        )
        assert client.service_token == "rbk_service_test"
        assert client.base_url == "https://custom.api.com"
        assert 'X-Service-Token' in client.session.headers

    def test_content_type_header_always_set(self):
        """Test that Content-Type header is always set regardless of auth method"""
        api_key_client = RecallBricks(api_key="test")
        assert api_key_client.session.headers['Content-Type'] == 'application/json'

        service_token_client = RecallBricks(service_token="test")
        assert service_token_client.session.headers['Content-Type'] == 'application/json'


if __name__ == "__main__":
    print("Running RecallBricks Authentication Tests\n")
    print("=" * 60)

    # Run tests manually without pytest
    test_suite = TestAuthenticationMethods()

    tests = [
        ("API Key Authentication", test_suite.test_api_key_authentication),
        ("Service Token Authentication", test_suite.test_service_token_authentication),
        ("No Authentication Error", test_suite.test_no_authentication_raises_error),
        ("Both Auth Methods Error", test_suite.test_both_authentication_methods_raises_error),
        ("Empty API Key Error", test_suite.test_empty_api_key_raises_error),
        ("Empty Service Token Error", test_suite.test_empty_service_token_raises_error),
        ("API Key with Custom URL", test_suite.test_api_key_with_custom_base_url),
        ("Service Token with Custom URL", test_suite.test_service_token_with_custom_base_url),
        ("Content-Type Header", test_suite.test_content_type_header_always_set),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"[PASS] {test_name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test_name}: {str(e)}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"\nResults: {passed} passed, {failed} failed")

    if failed == 0:
        print("All authentication tests passed!")
    else:
        print(f"{failed} test(s) failed")
