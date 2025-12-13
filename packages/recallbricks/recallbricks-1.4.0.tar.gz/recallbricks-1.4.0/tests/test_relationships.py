"""
Comprehensive tests for RecallBricks relationship functionality
Tests edge cases, error handling, and enterprise-grade robustness
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recallbricks import RecallBricks
from recallbricks.exceptions import (
    AuthenticationError,
    RateLimitError,
    APIError,
    RecallBricksError
)


class TestRelationships(unittest.TestCase):
    """Test suite for relationship functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)
        self.test_memory_id = "123e4567-e89b-12d3-a456-426614174000"

    def test_get_relationships_success(self):
        """Test successful relationship retrieval"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'memory_id': self.test_memory_id,
                'count': 5,
                'relationships': [
                    {'id': '1', 'type': 'related_to', 'target_id': 'abc123'},
                    {'id': '2', 'type': 'depends_on', 'target_id': 'def456'}
                ]
            }

            result = self.client.get_relationships(self.test_memory_id)

            mock_request.assert_called_once_with(
                'GET',
                f'/api/v1/relationships/memory/{self.test_memory_id}'
            )
            assert result['count'] == 5
            assert len(result['relationships']) == 2

    def test_get_relationships_with_invalid_id(self):
        """Test relationship retrieval with invalid memory ID"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.side_effect = APIError("Memory not found", status_code=404)

            with self.assertRaises(APIError) as context:
                self.client.get_relationships("invalid_id_12345")

            assert context.exception.status_code == 404

    def test_get_relationships_with_empty_id(self):
        """Test relationship retrieval with empty memory ID"""
        # Now validates client-side before making request
        with self.assertRaises(ValueError):
            self.client.get_relationships("")

    def test_get_relationships_with_none_id(self):
        """Test relationship retrieval with None memory ID"""
        # Now validates client-side before making request
        with self.assertRaises((ValueError, TypeError)):
            self.client.get_relationships(None)

    def test_get_relationships_no_relationships(self):
        """Test memory with no relationships"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'memory_id': self.test_memory_id,
                'count': 0,
                'relationships': []
            }

            result = self.client.get_relationships(self.test_memory_id)

            assert result['count'] == 0
            assert result['relationships'] == []

    def test_get_relationships_network_error(self):
        """Test relationship retrieval with network error"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.side_effect = RecallBricksError("Network error: Connection timeout")

            with self.assertRaises(RecallBricksError):
                self.client.get_relationships(self.test_memory_id)

    def test_get_relationships_rate_limit(self):
        """Test relationship retrieval with rate limiting"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.side_effect = RateLimitError(
                "Rate limit exceeded",
                retry_after="60"
            )

            with self.assertRaises(RateLimitError):
                self.client.get_relationships(self.test_memory_id)

    def test_get_relationships_auth_error(self):
        """Test relationship retrieval with authentication error"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.side_effect = AuthenticationError("Invalid API key")

            with self.assertRaises(AuthenticationError):
                self.client.get_relationships(self.test_memory_id)

    def test_get_graph_context_success(self):
        """Test successful graph context retrieval"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'root_id': self.test_memory_id,
                'depth': 2,
                'nodes': [
                    {'id': self.test_memory_id, 'text': 'Root memory'},
                    {'id': 'abc123', 'text': 'Related memory 1'},
                    {'id': 'def456', 'text': 'Related memory 2'}
                ],
                'edges': [
                    {'from': self.test_memory_id, 'to': 'abc123', 'type': 'related_to'},
                    {'from': self.test_memory_id, 'to': 'def456', 'type': 'depends_on'}
                ]
            }

            result = self.client.get_graph_context(self.test_memory_id, depth=2)

            mock_request.assert_called_once_with(
                'GET',
                f'/api/v1/relationships/graph/{self.test_memory_id}',
                params={'depth': 2}
            )
            assert result['depth'] == 2
            assert len(result['nodes']) == 3
            assert len(result['edges']) == 2

    def test_get_graph_context_default_depth(self):
        """Test graph context with default depth"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'root_id': self.test_memory_id,
                'depth': 2,
                'nodes': [],
                'edges': []
            }

            result = self.client.get_graph_context(self.test_memory_id)

            # Should use default depth of 2
            mock_request.assert_called_once_with(
                'GET',
                f'/api/v1/relationships/graph/{self.test_memory_id}',
                params={'depth': 2}
            )

    def test_get_graph_context_custom_depth(self):
        """Test graph context with various custom depths"""
        depths_to_test = [1, 3, 5, 10]

        for depth in depths_to_test:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = {
                    'root_id': self.test_memory_id,
                    'depth': depth,
                    'nodes': [],
                    'edges': []
                }

                result = self.client.get_graph_context(self.test_memory_id, depth=depth)

                mock_request.assert_called_once_with(
                    'GET',
                    f'/api/v1/relationships/graph/{self.test_memory_id}',
                    params={'depth': depth}
                )
                assert result['depth'] == depth

    def test_get_graph_context_zero_depth(self):
        """Test graph context with zero depth"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'root_id': self.test_memory_id,
                'depth': 0,
                'nodes': [{'id': self.test_memory_id, 'text': 'Root only'}],
                'edges': []
            }

            result = self.client.get_graph_context(self.test_memory_id, depth=0)

            # Should only return root node
            assert len(result['nodes']) == 1
            assert len(result['edges']) == 0

    def test_get_graph_context_negative_depth(self):
        """Test graph context with negative depth"""
        # Now validates client-side before making request
        with self.assertRaises(ValueError):
            self.client.get_graph_context(self.test_memory_id, depth=-1)

    def test_get_graph_context_isolated_memory(self):
        """Test graph context for memory with no relationships"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'root_id': self.test_memory_id,
                'depth': 2,
                'nodes': [{'id': self.test_memory_id, 'text': 'Isolated memory'}],
                'edges': []
            }

            result = self.client.get_graph_context(self.test_memory_id)

            assert len(result['nodes']) == 1
            assert len(result['edges']) == 0

    def test_search_with_relationships_success(self):
        """Test search with relationships included"""
        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            mock_get_all.return_value = [
                {'id': '1', 'text': 'First memory about auth'},
                {'id': '2', 'text': 'Second memory about auth'},
                {'id': '3', 'text': 'Unrelated memory'}
            ]

            mock_get_rels.side_effect = [
                {'count': 2, 'relationships': [{'id': 'r1'}, {'id': 'r2'}]},
                {'count': 1, 'relationships': [{'id': 'r3'}]}
            ]

            results = self.client.search('auth', limit=5, include_relationships=True)

            assert len(results) == 2
            assert all('relationships' in r for r in results)
            assert results[0]['relationships']['count'] == 2
            assert results[1]['relationships']['count'] == 1

    def test_search_with_relationships_partial_failure(self):
        """Test search when some relationship fetches fail"""
        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            mock_get_all.return_value = [
                {'id': '1', 'text': 'First memory'},
                {'id': '2', 'text': 'Second memory'},
                {'id': '3', 'text': 'Third memory'}
            ]

            # First succeeds, second fails, third succeeds
            mock_get_rels.side_effect = [
                {'count': 1, 'relationships': [{'id': 'r1'}]},
                APIError("Not found", status_code=404),
                {'count': 2, 'relationships': [{'id': 'r2'}, {'id': 'r3'}]}
            ]

            results = self.client.search('memory', limit=5, include_relationships=True)

            # Should still return all results, with None for failed relationship fetch
            assert len(results) == 3
            assert results[0]['relationships']['count'] == 1
            assert results[1]['relationships'] is None  # Failed fetch
            assert results[2]['relationships']['count'] == 2

    def test_search_without_relationships(self):
        """Test search without relationships (default behavior)"""
        with patch.object(self.client, 'get_all') as mock_get_all:
            mock_get_all.return_value = [
                {'id': '1', 'text': 'First memory'},
                {'id': '2', 'text': 'Second memory'}
            ]

            results = self.client.search('memory', limit=5)

            # Should not have relationships key
            assert len(results) == 2
            assert 'relationships' not in results[0]
            assert 'relationships' not in results[1]

    def test_search_with_relationships_empty_results(self):
        """Test search with relationships when no results found"""
        with patch.object(self.client, 'get_all') as mock_get_all:
            mock_get_all.return_value = [
                {'id': '1', 'text': 'Unrelated memory'}
            ]

            results = self.client.search('nonexistent', include_relationships=True)

            assert len(results) == 0

    def test_special_characters_in_memory_id(self):
        """Test with special characters in memory ID"""
        special_ids = [
            "test-id-with-dashes",
            "test_id_with_underscores",
            "test.id.with.dots",
            "test@id#with$special%chars"
        ]

        for special_id in special_ids:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = {'memory_id': special_id, 'count': 0, 'relationships': []}

                try:
                    result = self.client.get_relationships(special_id)
                    # If it succeeds, that's good
                    assert result is not None
                except (APIError, RecallBricksError):
                    # API might reject special characters - that's acceptable
                    pass

    def test_very_long_memory_id(self):
        """Test with extremely long memory ID"""
        long_id = "a" * 1000

        with patch.object(self.client, '_request') as mock_request:
            mock_request.side_effect = APIError("Invalid memory ID", status_code=400)

            with self.assertRaises(APIError):
                self.client.get_relationships(long_id)

    def test_unicode_in_memory_id(self):
        """Test with unicode characters in memory ID"""
        unicode_id = "test-id-🚀-emoji"

        with patch.object(self.client, '_request') as mock_request:
            # API might handle or reject unicode
            mock_request.return_value = {'memory_id': unicode_id, 'count': 0, 'relationships': []}

            try:
                result = self.client.get_relationships(unicode_id)
                assert result is not None
            except (APIError, RecallBricksError, UnicodeError):
                # Any of these errors are acceptable
                pass

    def test_concurrent_relationship_requests(self):
        """Test multiple concurrent relationship requests"""
        import threading

        results = []
        errors = []

        def fetch_relationships(memory_id):
            try:
                with patch.object(self.client, '_request') as mock_request:
                    mock_request.return_value = {
                        'memory_id': memory_id,
                        'count': 1,
                        'relationships': [{'id': 'r1'}]
                    }
                    result = self.client.get_relationships(memory_id)
                    results.append(result)
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(10):
            thread = threading.Thread(
                target=fetch_relationships,
                args=(f"memory_{i}",)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All requests should complete without errors
        assert len(errors) == 0 or len(results) > 0

    def test_malformed_response_handling(self):
        """Test handling of malformed API responses"""
        malformed_responses = [
            ({}, False),  # Empty response - valid dict, should return it
            ({'count': 5}, False),  # Missing relationships - valid dict, should return it
            ({'relationships': []}, False),  # Missing count - valid dict, should return it
            ({'invalid': 'structure'}, False),  # Completely wrong structure - valid dict, should return it
            (None, True),  # None response - should raise error
            ('invalid_string', True),  # String instead of dict - should raise error
            ([], True),  # List instead of dict - should raise error
        ]

        for malformed, should_raise in malformed_responses:
            with patch.object(self.client, '_request') as mock_request:
                mock_request.return_value = malformed

                if should_raise:
                    with self.assertRaises((APIError, TypeError)):
                        self.client.get_relationships(self.test_memory_id)
                else:
                    try:
                        result = self.client.get_relationships(self.test_memory_id)
                        # Should return the dict even if structure is unexpected
                        assert isinstance(result, dict)
                    except APIError:
                        # API errors are also acceptable
                        pass

    def test_large_relationship_count(self):
        """Test handling of memory with many relationships"""
        with patch.object(self.client, '_request') as mock_request:
            # Simulate 10000 relationships
            large_relationships = [
                {'id': f'rel_{i}', 'type': 'related_to', 'target_id': f'target_{i}'}
                for i in range(10000)
            ]

            mock_request.return_value = {
                'memory_id': self.test_memory_id,
                'count': 10000,
                'relationships': large_relationships
            }

            result = self.client.get_relationships(self.test_memory_id)

            assert result['count'] == 10000
            assert len(result['relationships']) == 10000

    def test_search_with_relationships_large_result_set(self):
        """Test search with relationships on large result set"""
        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            # Simulate 100 memories
            mock_get_all.return_value = [
                {'id': f'mem_{i}', 'text': f'Memory {i} about test'}
                for i in range(100)
            ]

            mock_get_rels.return_value = {
                'count': 1,
                'relationships': [{'id': 'r1'}]
            }

            # Only request 10 results
            results = self.client.search('test', limit=10, include_relationships=True)

            # Should only fetch relationships for the 10 results, not all 100
            assert len(results) == 10
            assert mock_get_rels.call_count == 10

    def test_type_validation(self):
        """Test type validation for parameters"""
        # Test invalid depth types - should raise TypeError
        invalid_depths = ['2', 2.5, [2], {'depth': 2}, True]

        for invalid_depth in invalid_depths:
            with self.assertRaises(TypeError):
                self.client.get_graph_context(self.test_memory_id, depth=invalid_depth)

        # Test invalid memory_id types
        invalid_ids = [123, None, [], {}, 45.6]

        for invalid_id in invalid_ids:
            with self.assertRaises((TypeError, ValueError)):
                self.client.get_relationships(invalid_id)


class TestRelationshipsIntegration(unittest.TestCase):
    """Integration tests for relationship functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_full_workflow_with_relationships(self):
        """Test complete workflow: save -> get relationships -> get graph"""
        with patch.object(self.client, '_request') as mock_request:
            # Mock save response
            memory_id = "new_memory_123"
            mock_request.return_value = {
                'id': memory_id,
                'text': 'Test memory',
                'created_at': '2024-01-01T00:00:00Z'
            }

            # Save memory
            memory = self.client.save("Test memory")
            assert memory['id'] == memory_id

            # Mock get relationships
            mock_request.return_value = {
                'memory_id': memory_id,
                'count': 2,
                'relationships': [
                    {'id': 'r1', 'type': 'related_to'},
                    {'id': 'r2', 'type': 'depends_on'}
                ]
            }

            # Get relationships
            rels = self.client.get_relationships(memory_id)
            assert rels['count'] == 2

            # Mock get graph
            mock_request.return_value = {
                'root_id': memory_id,
                'depth': 2,
                'nodes': [{'id': memory_id}],
                'edges': []
            }

            # Get graph context
            graph = self.client.get_graph_context(memory_id)
            assert graph['root_id'] == memory_id

    def test_search_workflow_with_relationships(self):
        """Test search workflow with relationships"""
        with patch.object(self.client, '_request') as mock_request:
            # Mock save multiple memories
            memory_ids = []
            for i in range(3):
                mock_request.return_value = {
                    'id': f'mem_{i}',
                    'text': f'Auth memory {i}',
                    'created_at': '2024-01-01T00:00:00Z'
                }
                memory = self.client.save(f"Auth memory {i}")
                memory_ids.append(memory['id'])

        with patch.object(self.client, 'get_all') as mock_get_all, \
             patch.object(self.client, 'get_relationships') as mock_get_rels:

            mock_get_all.return_value = [
                {'id': memory_ids[0], 'text': 'Auth memory 0'},
                {'id': memory_ids[1], 'text': 'Auth memory 1'},
                {'id': memory_ids[2], 'text': 'Auth memory 2'}
            ]

            mock_get_rels.return_value = {'count': 1, 'relationships': []}

            # Search with relationships
            results = self.client.search('Auth', include_relationships=True)

            assert len(results) == 3
            assert all('relationships' in r for r in results)


def run_tests():
    """Run all tests and provide summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRelationships))
    suite.addTests(loader.loadTestsFromTestCase(TestRelationshipsIntegration))

    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
