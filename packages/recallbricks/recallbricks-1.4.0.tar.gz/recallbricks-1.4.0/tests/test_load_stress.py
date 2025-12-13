"""
Load and stress tests for Phase 2A metacognition features
Tests concurrent requests, retry logic, large payloads, and edge cases
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os
import time
import threading
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recallbricks import RecallBricks
from recallbricks.exceptions import APIError, RateLimitError, RecallBricksError, AuthenticationError
from recallbricks.types import PredictedMemory, SuggestedMemory, LearningMetrics, PatternAnalysis, WeightedSearchResult


class TestPhase2ALoadStress(unittest.TestCase):
    """Load and stress tests for Phase 2A metacognition features"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_predict_memories_concurrent_requests(self):
        """Test concurrent predict_memories requests"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'predictions': [
                    {
                        'id': 'pred_1',
                        'content': 'Test memory',
                        'confidence_score': 0.85,
                        'reasoning': 'High relevance',
                        'metadata': {}
                    }
                ]
            }

            results = []
            errors = []

            def predict_task():
                try:
                    predictions = self.client.predict_memories(context="test", limit=5)
                    results.append(predictions)
                except Exception as e:
                    errors.append(e)

            threads = [threading.Thread(target=predict_task) for _ in range(50)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=10)

            # All requests should complete successfully
            assert len(results) == 50
            assert len(errors) == 0

    def test_suggest_memories_large_context(self):
        """Test suggest_memories with very large context"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'suggestions': [
                    {
                        'id': 'sug_1',
                        'content': 'Suggested memory',
                        'confidence': 0.9,
                        'reasoning': 'Test',
                        'relevance_context': 'Test context'
                    }
                ]
            }

            # 9000 character context (close to max 10000)
            large_context = "A" * 9000
            suggestions = self.client.suggest_memories(large_context, limit=5)

            assert len(suggestions) == 1
            assert isinstance(suggestions[0], SuggestedMemory)

    def test_predict_memories_max_limit(self):
        """Test predict_memories with maximum limit"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'predictions': [
                    {
                        'id': f'pred_{i}',
                        'content': f'Memory {i}',
                        'confidence_score': 0.8,
                        'reasoning': 'Test',
                        'metadata': {}
                    } for i in range(100)
                ]
            }

            predictions = self.client.predict_memories(limit=100)
            assert len(predictions) == 100

    def test_search_weighted_retry_on_500(self):
        """Test search_weighted retries on server errors"""
        with patch.object(self.client, 'session') as mock_session:
            # First two attempts return 500, third succeeds
            mock_response_error = Mock()
            mock_response_error.status_code = 500
            mock_response_error.content = b'{"message": "Server error"}'
            mock_response_error.json.return_value = {'message': 'Server error'}

            mock_response_success = Mock()
            mock_response_success.status_code = 200
            mock_response_success.content = b'{"results": []}'
            mock_response_success.json.return_value = {'results': []}

            mock_session.request.side_effect = [
                mock_response_error,
                mock_response_error,
                mock_response_success
            ]

            # Should succeed after retries
            results = self.client.search_weighted("test query")
            assert results == []
            # Should have been called 3 times
            assert mock_session.request.call_count == 3

    def test_rate_limiting_with_retry(self):
        """Test rate limiting handling with automatic retry"""
        with patch.object(self.client, 'session') as mock_session:
            # First attempt returns 429, second succeeds
            mock_response_rate_limit = Mock()
            mock_response_rate_limit.status_code = 429
            mock_response_rate_limit.headers = {'X-RateLimit-Reset': '1'}
            mock_response_rate_limit.content = b''

            mock_response_success = Mock()
            mock_response_success.status_code = 200
            mock_response_success.content = b'{"predictions": []}'
            mock_response_success.json.return_value = {'predictions': []}

            mock_session.request.side_effect = [
                mock_response_rate_limit,
                mock_response_success
            ]

            # Should succeed after retry
            with patch('time.sleep'):  # Mock sleep to speed up test
                predictions = self.client.predict_memories(limit=5)
            assert predictions == []

    def test_timeout_recovery(self):
        """Test timeout recovery with retry logic"""
        with patch.object(self.client, 'session') as mock_session:
            # First two attempts timeout, third succeeds
            mock_session.request.side_effect = [
                requests.exceptions.Timeout(),
                requests.exceptions.Timeout(),
                Mock(status_code=200, content=b'{"predictions": []}',
                     json=lambda: {'predictions': []})
            ]

            with patch('time.sleep'):  # Mock sleep to speed up test
                predictions = self.client.predict_memories(limit=5)
            assert predictions == []

    def test_connection_error_recovery(self):
        """Test connection error recovery"""
        with patch.object(self.client, 'session') as mock_session:
            # First attempt fails with connection error, second succeeds
            mock_session.request.side_effect = [
                requests.exceptions.ConnectionError("Network unreachable"),
                Mock(status_code=200, content=b'{"suggestions": []}',
                     json=lambda: {'suggestions': []})
            ]

            with patch('time.sleep'):  # Mock sleep to speed up test
                suggestions = self.client.suggest_memories("test", limit=5)
            assert suggestions == []

    def test_predict_memories_many_recent_ids(self):
        """Test predict_memories with many recent memory IDs"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            # 50 recent memory IDs
            recent_ids = [f'mem_{i}' for i in range(50)]
            predictions = self.client.predict_memories(
                recent_memory_ids=recent_ids,
                limit=10
            )

            assert predictions == []
            # Verify all IDs were passed
            call_args = mock_request.call_args
            assert len(call_args[1]['json']['recent_memory_ids']) == 50

    def test_get_learning_metrics_concurrent(self):
        """Test concurrent get_learning_metrics requests"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'avg_helpfulness': 0.85,
                'total_usage': 1000,
                'active_memories': 50,
                'total_memories': 100,
                'trends': {
                    'helpfulness_trend': 'increasing',
                    'usage_trend': 'stable',
                    'growth_rate': 0.05
                }
            }

            results = []
            errors = []

            def metrics_task():
                try:
                    metrics = self.client.get_learning_metrics(days=30)
                    results.append(metrics)
                except Exception as e:
                    errors.append(e)

            threads = [threading.Thread(target=metrics_task) for _ in range(20)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=10)

            assert len(results) == 20
            assert len(errors) == 0
            assert all(isinstance(m, LearningMetrics) for m in results)

    def test_get_patterns_large_dataset(self):
        """Test get_patterns with large dataset response"""
        with patch.object(self.client, '_request') as mock_request:
            # Simulate large pattern analysis
            mock_request.return_value = {
                'summary': 'Test summary',
                'most_useful_tags': [f'tag_{i}' for i in range(100)],
                'frequently_accessed_together': [[f'mem_{i}', f'mem_{i+1}'] for i in range(50)],
                'underutilized_memories': [
                    {'id': f'mem_{i}', 'text': f'Memory {i}'}
                    for i in range(200)
                ]
            }

            patterns = self.client.get_patterns(days=30)
            assert isinstance(patterns, PatternAnalysis)
            assert len(patterns.most_useful_tags) == 100
            assert len(patterns.frequently_accessed_together) == 50
            assert len(patterns.underutilized_memories) == 200

    def test_search_weighted_empty_results(self):
        """Test search_weighted with empty results"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            results = self.client.search_weighted("nonexistent query")
            assert results == []

    def test_search_weighted_max_results(self):
        """Test search_weighted with maximum results"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {
                'results': [
                    {
                        'id': f'mem_{i}',
                        'text': f'Memory {i}',
                        'source': 'api',
                        'project_id': 'default',
                        'tags': ['test'],
                        'metadata': {},
                        'created_at': '2024-01-01T00:00:00Z',
                        'relevance_score': 0.9,
                        'usage_boost': 0.1,
                        'helpfulness_boost': 0.05,
                        'recency_boost': 0.02
                    } for i in range(100)
                ]
            }

            results = self.client.search_weighted("test", limit=100)
            assert len(results) == 100
            assert all(isinstance(r, WeightedSearchResult) for r in results)

    def test_exponential_backoff_timing(self):
        """Test that exponential backoff uses correct delays"""
        with patch.object(self.client, 'session') as mock_session:
            mock_response_error = Mock()
            mock_response_error.status_code = 500
            mock_response_error.content = b'{"message": "Server error"}'
            mock_response_error.json.return_value = {'message': 'Server error'}

            mock_session.request.side_effect = [
                mock_response_error,
                mock_response_error,
                mock_response_error
            ]

            sleep_times = []
            original_sleep = time.sleep

            def mock_sleep(duration):
                sleep_times.append(duration)

            with patch('time.sleep', side_effect=mock_sleep):
                try:
                    self.client.predict_memories(limit=5)
                except APIError:
                    pass

            # Should have exponential backoff: 1s, 2s
            assert len(sleep_times) == 2
            assert sleep_times[0] == 1  # 2^0
            assert sleep_times[1] == 2  # 2^1

    def test_malformed_response_handling(self):
        """Test handling of malformed API responses"""
        with patch.object(self.client, '_request') as mock_request:
            # Missing required fields
            mock_request.return_value = {}

            predictions = self.client.predict_memories(limit=5)
            # Should return empty list for missing predictions key
            assert predictions == []

    def test_predict_memories_invalid_limit(self):
        """Test predict_memories with invalid limit values"""
        with self.assertRaises(ValueError):
            self.client.predict_memories(limit=0)

        with self.assertRaises(ValueError):
            self.client.predict_memories(limit=101)

        with self.assertRaises(ValueError):
            self.client.predict_memories(limit=-5)

    def test_suggest_memories_invalid_confidence(self):
        """Test suggest_memories with invalid confidence values"""
        with self.assertRaises(ValueError):
            self.client.suggest_memories("test", min_confidence=-0.1)

        with self.assertRaises(ValueError):
            self.client.suggest_memories("test", min_confidence=1.5)

    def test_get_learning_metrics_invalid_days(self):
        """Test get_learning_metrics with invalid days values"""
        with self.assertRaises(ValueError):
            self.client.get_learning_metrics(days=0)

        with self.assertRaises(ValueError):
            self.client.get_learning_metrics(days=400)

        with self.assertRaises(ValueError):
            self.client.get_learning_metrics(days=-10)

    def test_search_weighted_all_options(self):
        """Test search_weighted with all optional parameters"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'results': []}

            results = self.client.search_weighted(
                "test query",
                limit=20,
                weight_by_usage=True,
                decay_old_memories=True,
                adaptive_weights=False,
                min_helpfulness_score=0.8
            )

            # Verify all parameters were passed
            call_args = mock_request.call_args
            payload = call_args[1]['json']
            assert payload['weight_by_usage'] is True
            assert payload['decay_old_memories'] is True
            assert payload['adaptive_weights'] is False
            assert payload['min_helpfulness_score'] == 0.8


class TestPhase2AEdgeCases(unittest.TestCase):
    """Edge case tests for Phase 2A features"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key_12345"
        self.client = RecallBricks(self.api_key)

    def test_predict_memories_no_context_no_recent(self):
        """Test predict_memories with no context and no recent IDs"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'predictions': []}

            predictions = self.client.predict_memories(limit=5)
            assert predictions == []

    def test_suggest_memories_empty_context(self):
        """Test suggest_memories with empty context"""
        with self.assertRaises(ValueError):
            self.client.suggest_memories("", limit=5)

    def test_search_weighted_empty_query(self):
        """Test search_weighted with empty query"""
        with self.assertRaises(ValueError):
            self.client.search_weighted("")

    def test_predict_memories_invalid_recent_ids_type(self):
        """Test predict_memories with invalid recent_memory_ids type"""
        with self.assertRaises(TypeError):
            self.client.predict_memories(recent_memory_ids="not_a_list")

    def test_predict_memories_non_string_id(self):
        """Test predict_memories with non-string ID in list"""
        with self.assertRaises(TypeError):
            self.client.predict_memories(recent_memory_ids=[123, 456])

    def test_dataclass_creation(self):
        """Test that dataclasses are created correctly from API responses"""
        predicted = PredictedMemory.from_dict({
            'id': 'test_id',
            'content': 'Test content',
            'confidence_score': 0.95,
            'reasoning': 'Test reasoning',
            'metadata': {'key': 'value'}
        })

        assert predicted.id == 'test_id'
        assert predicted.confidence_score == 0.95

        suggested = SuggestedMemory.from_dict({
            'id': 'sug_id',
            'content': 'Suggestion',
            'confidence': 0.88,
            'reasoning': 'Reason',
            'relevance_context': 'Context'
        })

        assert suggested.confidence == 0.88

    def test_timeout_configuration(self):
        """Test that timeout is configurable"""
        client = RecallBricks(self.api_key, timeout=60)
        assert client.timeout == 60


def run_load_stress_tests():
    """Run all load and stress tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestPhase2ALoadStress))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase2AEdgeCases))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("PHASE 2A LOAD/STRESS TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_load_stress_tests()
    sys.exit(0 if success else 1)
