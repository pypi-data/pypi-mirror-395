"""
RecallBricks Python SDK
The Memory Layer for AI - Persistent memory across all AI models
"""

import requests
import functools
import time
import re
from typing import List, Dict, Optional, Any
from .exceptions import AuthenticationError, RateLimitError, APIError, RecallBricksError
from .types import (
    PredictedMemory,
    SuggestedMemory,
    LearningMetrics,
    PatternAnalysis,
    WeightedSearchResult
)


class RecallBricks:
    """
    RecallBricks client for saving and retrieving AI memories.

    Usage with API key (user-level access):
        >>> from recallbricks import RecallBricks
        >>> memory = RecallBricks(api_key="rb_dev_xxx")
        >>> memory.save("Important context about the project")
        >>> memories = memory.get_all()

    Usage with service token (server-to-server access):
        >>> from recallbricks import RecallBricks
        >>> memory = RecallBricks(service_token="rbk_service_xxx")
        >>> # Note: user_id is required when using service token
        >>> memory.save("Important context", user_id="user_123")
        >>> memories = memory.get_all()
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        service_token: Optional[str] = None,
        base_url: str = "https://api.recallbricks.com/api/v1",
        timeout: int = 30
    ):
        """
        Initialize RecallBricks client.

        Args:
            api_key: Your RecallBricks API key (for user-level access)
            service_token: Your RecallBricks service token (for server-to-server access)
            base_url: API base URL (default: production)
            timeout: Request timeout in seconds (default: 30)

        Note:
            You must provide either api_key or service_token, but not both.
            - Use api_key for user-level access (X-API-Key header)
            - Use service_token for server-to-server access (X-Service-Token header)
        """
        # Validate that exactly one auth method is provided
        if not api_key and not service_token:
            raise AuthenticationError("Either api_key or service_token is required")

        if api_key and service_token:
            raise AuthenticationError("Provide either api_key or service_token, not both")

        self.api_key = api_key
        self.service_token = service_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # Set authentication header based on which credential was provided
        if service_token:
            self.session.headers.update({
                'X-Service-Token': service_token,
                'Content-Type': 'application/json'
            })
        else:
            self.session.headers.update({
                'X-API-Key': api_key,
                'Content-Type': 'application/json'
            })
    
    def _sanitize_input(self, value: str, max_length: int = 10000) -> str:
        """
        Sanitize string input to prevent injection attacks

        Args:
            value: Input string to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value).__name__}")

        # Remove null bytes and control characters (except tabs, newlines, carriage returns)
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)

        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    def _request(self, method: str, endpoint: str, max_retries: int = 3, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to RecallBricks API with retry logic

        Args:
            method: HTTP method
            endpoint: API endpoint
            max_retries: Maximum retry attempts (default: 3)
            **kwargs: Additional request parameters

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"

        # Set timeout if not specified
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        last_exception = None

        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)

                # Handle rate limiting with retry
                if response.status_code == 429:
                    retry_after = response.headers.get('X-RateLimit-Reset', '60')
                    wait_time = min(int(retry_after) if retry_after.isdigit() else 60, 60)

                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(
                            "Rate limit exceeded. Please try again later.",
                            retry_after=retry_after
                        )

                # Handle authentication errors
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")

                # Handle server errors with retry
                if response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                        time.sleep(wait_time)
                        continue
                    else:
                        error_data = response.json() if response.content else {}
                        raise APIError(
                            error_data.get('message', 'Server error'),
                            status_code=response.status_code
                        )

                # Handle other client errors
                if response.status_code >= 400:
                    try:
                        error_data = response.json() if response.content else {}
                    except ValueError:
                        error_data = {}
                    raise APIError(
                        error_data.get('message', 'API request failed'),
                        status_code=response.status_code
                    )

                # Parse JSON response
                try:
                    return response.json() if response.content else {}
                except ValueError as e:
                    raise RecallBricksError(f"Invalid JSON response: {str(e)}")

            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                else:
                    raise RecallBricksError(f"Request timeout after {max_retries} attempts")

            except requests.exceptions.ConnectionError as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                else:
                    raise RecallBricksError(f"Connection error after {max_retries} attempts: {str(e)}")

            except requests.exceptions.RequestException as e:
                # Other request exceptions - don't retry
                raise RecallBricksError(f"Network error: {str(e)}")

        # Should not reach here, but just in case
        if last_exception:
            raise RecallBricksError(f"Request failed after {max_retries} attempts: {str(last_exception)}")
    
    def save(
        self,
        text: str,
        user_id: Optional[str] = None,
        source: str = "api",
        project_id: str = "default",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Save a new memory with automatic retry on failure.

        Args:
            text: The memory content to save
            user_id: User ID to associate with the memory. Required when using
                    service token authentication. Optional when using API key
                    authentication (uses authenticated user by default).
            source: Source of the memory (default: "api")
            project_id: Project identifier (default: "default")
            tags: Optional list of tags
            metadata: Optional metadata dictionary
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            Dictionary containing the created memory with id, created_at, etc.

        Raises:
            ValueError: If user_id is required but not provided

        Example:
            >>> # With API key (user_id optional)
            >>> memory.save("User prefers dark mode and TypeScript")

            >>> # With service token (user_id required)
            >>> memory.save("User prefers dark mode", user_id="user_123")
        """
        # Validate user_id when using service token
        if self.service_token and not user_id:
            raise ValueError(
                "user_id is required when using service token authentication. "
                "Please provide a user_id parameter to identify the user."
            )

        # Validate user_id format if provided
        if user_id is not None:
            if not isinstance(user_id, str):
                raise TypeError(f"user_id must be a string, got {type(user_id).__name__}")
            if not user_id.strip():
                raise ValueError("user_id cannot be empty")
            # Sanitize user_id
            user_id = self._sanitize_input(user_id, max_length=256)

        payload = {
            "text": text,
            "source": source,
            "project_id": project_id,
        }

        # Include user_id in payload if provided
        if user_id:
            payload["user_id"] = user_id

        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/memories", json=payload, max_retries=max_retries)
    
    def get_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all memories.

        Args:
            limit: Optional limit on number of memories to return

        Returns:
            Dictionary with 'memories' list and 'count'

        Example:
            >>> response = memory.get_all(limit=10)
            >>> for mem in response['memories']:
            >>>     print(mem['text'])
        """
        params = {}
        if limit:
            params['limit'] = limit

        return self._request("GET", "/memories", params=params)
    
    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search memories by semantic similarity.

        Args:
            query: Search query
            limit: Maximum number of results (default: 10)

        Returns:
            Dictionary with 'memories' list and 'count'

        Example:
            >>> results = memory.search("dark mode", limit=5)
            >>> for mem in results['memories']:
            >>>     print(mem['text'])
        """
        payload = {
            "query": self._sanitize_input(query),
            "limit": limit
        }

        return self._request("POST", "/memories/search", json=payload)
    
    def get(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a specific memory by ID.
        
        Args:
            memory_id: The memory ID
            
        Returns:
            Memory dictionary
            
        Example:
            >>> specific = memory.get("123e4567-e89b-12d3-a456-426614174000")
        """
        return self._request("GET", f"/memories/{memory_id}")
    
    def delete(self, memory_id: str) -> Dict[str, Any]:
        """
        Delete a memory.
        
        Args:
            memory_id: The memory ID to delete
            
        Returns:
            Success confirmation
            
        Example:
            >>> memory.delete("123e4567-e89b-12d3-a456-426614174000")
        """
        return self._request("DELETE", f"/memories/{memory_id}")

    def update(
        self,
        memory_id: str,
        text: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing memory.

        Args:
            memory_id: The memory ID to update
            text: New text content (optional)
            tags: New tags list (optional)
            metadata: New metadata dictionary (optional)

        Returns:
            Updated memory dictionary

        Example:
            >>> memory.update("123e4567-...", text="Updated content", tags=["new-tag"])
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        payload = {}
        if text is not None:
            payload["text"] = self._sanitize_input(text)
        if tags is not None:
            payload["tags"] = tags
        if metadata is not None:
            payload["metadata"] = metadata

        if not payload:
            raise ValueError("At least one field (text, tags, or metadata) must be provided")

        return self._request("PUT", f"/memories/{memory_id}", json=payload)

    def health(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Dictionary with health status

        Example:
            >>> status = memory.health()
            >>> print(f"API status: {status['status']}")
        """
        return self._request("GET", "/health")

    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current rate limit status.

        Returns:
            Dictionary with limit, remaining, reset, percentUsed

        Example:
            >>> status = memory.get_rate_limit()
            >>> print(f"Remaining: {status['remaining']}/{status['limit']}")
        """
        return self._request("GET", "/rate-limit")

    def get_relationships(self, memory_id: str) -> Dict[str, Any]:
        """
        Get relationships for a specific memory.

        Args:
            memory_id: The memory ID to get relationships for

        Returns:
            Dictionary containing relationships information

        Raises:
            ValueError: If memory_id is None or empty
            APIError: If the API request fails

        Example:
            >>> rels = memory.get_relationships("123e4567-e89b-12d3-a456-426614174000")
            >>> print(f"Found {rels['count']} relationships")
        """
        if not memory_id:
            raise ValueError("memory_id cannot be None or empty")

        if not isinstance(memory_id, str):
            raise TypeError(f"memory_id must be a string, got {type(memory_id).__name__}")

        response = self._request("GET", f"/relationships/memory/{memory_id}")

        # Validate response structure
        if response is None:
            raise APIError("Received None response from API", status_code=500)

        # Return response even if it doesn't have expected structure - let caller handle it
        # But ensure it's at least a dictionary
        if not isinstance(response, dict):
            raise APIError(f"Invalid response type: expected dict, got {type(response).__name__}", status_code=500)

        return response

    def get_graph_context(self, memory_id: str, depth: int = 2) -> Dict[str, Any]:
        """
        Get memory graph with relationships at specified depth.

        Args:
            memory_id: The memory ID to get graph context for
            depth: Depth of relationships to traverse (default: 2)

        Returns:
            Dictionary containing memory graph with relationships

        Raises:
            ValueError: If memory_id is None/empty or depth is negative
            TypeError: If parameters have incorrect types
            APIError: If the API request fails

        Example:
            >>> graph = memory.get_graph_context("123e4567-e89b-12d3-a456-426614174000", depth=3)
            >>> print(f"Graph contains {len(graph['nodes'])} nodes")
        """
        if not memory_id:
            raise ValueError("memory_id cannot be None or empty")

        if not isinstance(memory_id, str):
            raise TypeError(f"memory_id must be a string, got {type(memory_id).__name__}")

        # Check for bool before int since bool is a subclass of int in Python
        if isinstance(depth, bool):
            raise TypeError(f"depth must be an integer, got {type(depth).__name__}")

        if not isinstance(depth, int):
            raise TypeError(f"depth must be an integer, got {type(depth).__name__}")

        if depth < 0:
            raise ValueError(f"depth must be non-negative, got {depth}")

        params = {"depth": depth}
        response = self._request("GET", f"/relationships/graph/{memory_id}", params=params)

        # Validate response structure
        if response is None:
            raise APIError("Received None response from API", status_code=500)

        if not isinstance(response, dict):
            raise APIError(f"Invalid response type: expected dict, got {type(response).__name__}", status_code=500)

        return response

    def capture_function(self, save_inputs: bool = True, save_outputs: bool = True, include_errors: bool = True):
        """
        Decorator that automatically captures function inputs and outputs.

        Args:
            save_inputs: Whether to save function inputs (default: True)
            save_outputs: Whether to save function outputs (default: True)
            include_errors: Whether to save errors (default: True)

        Usage:
            >>> @rb.capture_function()
            >>> def process_email(email):
            >>>     return email.reply()
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Save inputs
                if save_inputs:
                    input_data = f"[AUTO-CAPTURE] Function: {func.__name__}, Args: {args}, Kwargs: {kwargs}"
                    try:
                        self.save(input_data, source="api")
                    except Exception as e:
                        if include_errors:
                            print(f"Failed to save inputs: {e}")

                # Execute function
                try:
                    result = func(*args, **kwargs)

                    # Save outputs
                    if save_outputs:
                        output_data = f"[AUTO-CAPTURE] Function: {func.__name__}, Result: {result}"
                        try:
                            self.save(output_data, source="api")
                        except Exception as e:
                            if include_errors:
                                print(f"Failed to save outputs: {e}")

                    return result

                except Exception as e:
                    # Save errors
                    if include_errors:
                        error_data = f"[AUTO-CAPTURE-ERROR] Function: {func.__name__}, Error: {str(e)}"
                        try:
                            self.save(error_data, source="api")
                        except:
                            pass
                    raise

            return wrapper
        return decorator

    def predict_memories(
        self,
        context: Optional[str] = None,
        recent_memory_ids: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[PredictedMemory]:
        """
        Predict which memories might be useful based on context and recent usage.

        Args:
            context: Optional context string for prediction
            recent_memory_ids: Optional list of recently accessed memory IDs
            limit: Maximum number of predictions to return (default: 10)

        Returns:
            List of PredictedMemory objects

        Example:
            >>> predictions = rb.predict_memories(context="User is working on auth", limit=5)
            >>> for pred in predictions:
            >>>     print(f"{pred.content} (confidence: {pred.confidence_score})")
        """
        # Input validation and sanitization
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")

        payload = {"limit": limit}

        if context:
            payload["context"] = self._sanitize_input(context)

        if recent_memory_ids:
            if not isinstance(recent_memory_ids, list):
                raise TypeError("recent_memory_ids must be a list")
            # Validate each ID
            sanitized_ids = []
            for mem_id in recent_memory_ids:
                if not isinstance(mem_id, str):
                    raise TypeError(f"memory_id must be string, got {type(mem_id).__name__}")
                sanitized_ids.append(self._sanitize_input(mem_id, max_length=256))
            payload["recent_memory_ids"] = sanitized_ids

        response = self._request("POST", "/memories/predict", json=payload)

        # Parse response into PredictedMemory objects
        predictions = response.get('predictions', [])
        return [PredictedMemory.from_dict(p) for p in predictions]

    def suggest_memories(
        self,
        context: str,
        limit: int = 5,
        min_confidence: float = 0.6,
        include_reasoning: bool = True
    ) -> List[SuggestedMemory]:
        """
        Get memory suggestions based on current context.

        Args:
            context: Context string for suggestions
            limit: Maximum number of suggestions (default: 5)
            min_confidence: Minimum confidence threshold (default: 0.6)
            include_reasoning: Include reasoning in response (default: True)

        Returns:
            List of SuggestedMemory objects

        Example:
            >>> suggestions = rb.suggest_memories("Building login form", min_confidence=0.7)
            >>> for sug in suggestions:
            >>>     print(f"{sug.content} - {sug.reasoning}")
        """
        # Input validation
        if not context:
            raise ValueError("context is required")

        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")

        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence must be between 0.0 and 1.0")

        payload = {
            "context": self._sanitize_input(context),
            "limit": limit,
            "min_confidence": min_confidence,
            "include_reasoning": include_reasoning
        }

        response = self._request("POST", "/memories/suggest", json=payload)

        # Parse response into SuggestedMemory objects
        suggestions = response.get('suggestions', [])
        return [SuggestedMemory.from_dict(s) for s in suggestions]

    def get_learning_metrics(self, days: int = 30) -> LearningMetrics:
        """
        Get learning metrics showing memory usage patterns.

        Args:
            days: Number of days to analyze (default: 30)

        Returns:
            LearningMetrics object

        Example:
            >>> metrics = rb.get_learning_metrics(days=7)
            >>> print(f"Average helpfulness: {metrics.avg_helpfulness}")
            >>> print(f"Active memories: {metrics.active_memories}/{metrics.total_memories}")
        """
        # Input validation
        if not isinstance(days, int) or days < 1 or days > 365:
            raise ValueError("days must be an integer between 1 and 365")

        params = {"days": days}
        response = self._request("GET", "/learning/metrics", params=params)

        return LearningMetrics.from_dict(response)

    def get_patterns(self, days: int = 30) -> PatternAnalysis:
        """
        Analyze patterns in memory usage and access.

        Args:
            days: Number of days to analyze (default: 30)

        Returns:
            PatternAnalysis object

        Example:
            >>> patterns = rb.get_patterns(days=14)
            >>> print(f"Summary: {patterns.summary}")
            >>> print(f"Useful tags: {', '.join(patterns.most_useful_tags)}")
        """
        # Input validation
        if not isinstance(days, int) or days < 1 or days > 365:
            raise ValueError("days must be an integer between 1 and 365")

        params = {"days": days}
        response = self._request("GET", "/memories/meta/patterns", params=params)

        return PatternAnalysis.from_dict(response)

    def search_weighted(
        self,
        query: str,
        limit: int = 10,
        weight_by_usage: bool = False,
        decay_old_memories: bool = False,
        adaptive_weights: bool = True,
        min_helpfulness_score: Optional[float] = None
    ) -> List[WeightedSearchResult]:
        """
        Search memories with intelligent weighting based on usage, helpfulness, and recency.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)
            weight_by_usage: Boost frequently used memories (default: False)
            decay_old_memories: Reduce score for old memories (default: False)
            adaptive_weights: Use adaptive weighting algorithm (default: True)
            min_helpfulness_score: Minimum helpfulness score filter (optional)

        Returns:
            List of WeightedSearchResult objects

        Example:
            >>> results = rb.search_weighted(
            >>>     "authentication",
            >>>     weight_by_usage=True,
            >>>     min_helpfulness_score=0.7
            >>> )
            >>> for result in results:
            >>>     print(f"{result.text} (score: {result.relevance_score})")
        """
        # Input validation
        if not query:
            raise ValueError("query is required")

        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")

        if min_helpfulness_score is not None:
            if not 0.0 <= min_helpfulness_score <= 1.0:
                raise ValueError("min_helpfulness_score must be between 0.0 and 1.0")

        payload = {
            "query": self._sanitize_input(query),
            "limit": limit,
            "weight_by_usage": weight_by_usage,
            "decay_old_memories": decay_old_memories,
            "adaptive_weights": adaptive_weights
        }

        if min_helpfulness_score is not None:
            payload["min_helpfulness_score"] = min_helpfulness_score

        response = self._request("POST", "/memories/search", json=payload)

        # Parse response into WeightedSearchResult objects
        results = response.get('results', [])
        return [WeightedSearchResult.from_dict(r) for r in results]
