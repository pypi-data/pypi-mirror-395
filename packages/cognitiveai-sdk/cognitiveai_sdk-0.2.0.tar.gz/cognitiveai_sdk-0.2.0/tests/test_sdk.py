"""
Tests for CognitiveAI Python SDK
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from cognitiveai import (
    CognitiveAIClient,
    CognitiveAIConfig,
    SearchRequest,
    GridRequest,
    CognitiveAIError,
    CognitiveAIAuthenticationError,
    CognitiveAIRateLimitError,
    CognitiveAIServerError,
    search,
    grid_search
)


@pytest.fixture
def config():
    return CognitiveAIConfig(
        api_key="test-key",
        base_url="https://api.test.cognitiveai.ai",
        timeout=30.0,
        max_retries=1
    )


@pytest.fixture
def client(config):
    return CognitiveAIClient(config)


class TestCognitiveAIClient:
    """Test CognitiveAIClient functionality."""

    @pytest.mark.asyncio
    async def test_search_sync_response(self, client):
        """Test search with synchronous response."""
        mock_response = {
            "job_id": "test-job-123",
            "prompt": "Test prompt",
            "response": "Test response",
            "reasoning_trace": [{"step": 1, "thought": "Thinking..."}],
            "provider": "mock",
            "beam": 2,
            "steps": 1,
            "tokens_used": 150,
            "cost": 0.002,
            "created_at": "2024-01-01T00:00:00Z"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            request = SearchRequest(prompt="Test prompt")
            result = await client.search(request)

            assert result.job_id == "test-job-123"
            assert result.prompt == "Test prompt"
            assert result.response == "Test response"
            assert result.tokens_used == 150
            assert result.cost == 0.002

    @pytest.mark.asyncio
    async def test_search_async_job(self, client):
        """Test search with async job processing."""
        # Mock initial job creation response
        job_response = {"job_id": "async-job-456"}

        # Mock job status responses
        status_responses = [
            {"job_id": "async-job-456", "status": "running", "created_at": "2024-01-01T00:00:00Z", "updated_at": "2024-01-01T00:00:01Z"},
            {"job_id": "async-job-456", "status": "completed", "created_at": "2024-01-01T00:00:00Z", "updated_at": "2024-01-01T00:00:05Z"}
        ]

        # Mock final result
        final_result = {
            "job_id": "async-job-456",
            "prompt": "Async test prompt",
            "response": "Async response",
            "reasoning_trace": [{"step": 1, "thought": "Async thinking..."}],
            "provider": "mock",
            "beam": 2,
            "steps": 1,
            "tokens_used": 200,
            "cost": 0.003,
            "created_at": "2024-01-01T00:00:00Z"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request, \
             patch.object(client, 'get_job_status', new_callable=AsyncMock) as mock_status:

            mock_request.side_effect = [job_response, final_result]
            mock_status.side_effect = status_responses

            request = SearchRequest(prompt="Async test prompt")
            result = await client.search(request)

            assert result.job_id == "async-job-456"
            assert result.response == "Async response"
            assert result.tokens_used == 200

    @pytest.mark.asyncio
    async def test_grid_search(self, client):
        """Test grid search functionality."""
        mock_response = {
            "job_id": "grid-job-789",
            "prompt": "Grid test prompt",
            "results": [
                {"beam": 2, "steps": 1, "score": 0.8},
                {"beam": 2, "steps": 2, "score": 0.9}
            ],
            "best_result": {"beam": 2, "steps": 2, "score": 0.9},
            "provider": "mock",
            "beams": [2],
            "steps": [1, 2],
            "total_tokens_used": 300,
            "total_cost": 0.005,
            "created_at": "2024-01-01T00:00:00Z"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            request = GridRequest(beams=[2], steps=[1, 2], prompt="Grid test prompt")
            result = await client.grid_search(request)

            assert result.job_id == "grid-job-789"
            assert len(result.results) == 2
            assert result.best_result["score"] == 0.9
            assert result.total_tokens_used == 300

    @pytest.mark.asyncio
    async def test_get_job_status(self, client):
        """Test getting job status."""
        mock_response = {
            "job_id": "status-job-101",
            "status": "running",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:05Z",
            "progress": 0.5,
            "artifacts_url": "https://example.com/artifacts.zip"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            status = await client.get_job_status("status-job-101")

            assert status.job_id == "status-job-101"
            assert status.status == "running"
            assert status.progress == 0.5
            assert status.artifacts_url == "https://example.com/artifacts.zip"

    @pytest.mark.asyncio
    async def test_list_jobs(self, client):
        """Test listing jobs."""
        mock_response = {
            "jobs": [
                {
                    "job_id": "job-1",
                    "status": "completed",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:01:00Z"
                },
                {
                    "job_id": "job-2",
                    "status": "running",
                    "created_at": "2024-01-01T00:02:00Z",
                    "updated_at": "2024-01-01T00:02:30Z",
                    "progress": 0.3
                }
            ]
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            jobs = await client.list_jobs(limit=10, status="completed")

            assert len(jobs) == 2
            assert jobs[0].job_id == "job-1"
            assert jobs[0].status == "completed"
            assert jobs[1].progress == 0.3

    @pytest.mark.asyncio
    async def test_api_key_management(self, client):
        """Test API key management."""
        # Test get_api_keys
        keys_response = {
            "keys": [
                {"id": "key-1", "name": "Test Key 1", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "key-2", "name": "Test Key 2", "created_at": "2024-01-01T00:01:00Z"}
            ]
        }

        # Test create_api_key
        create_response = {
            "id": "key-3",
            "name": "New Key",
            "key": "cognitiveai-new-key-123",
            "created_at": "2024-01-01T00:02:00Z"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [keys_response, create_response]

            # Test listing keys
            keys = await client.get_api_keys()
            assert len(keys) == 2
            assert keys[0]["name"] == "Test Key 1"

            # Test creating key
            new_key = await client.create_api_key("New Key", ["read", "write"])
            assert new_key["key"] == "cognitiveai-new-key-123"


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_authentication_error(self, client):
        """Test authentication error handling."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = CognitiveAIAuthenticationError("Invalid API key")

            with pytest.raises(CognitiveAIAuthenticationError):
                await client.search("Test prompt")

    @pytest.mark.asyncio
    async def test_rate_limit_error(self, client):
        """Test rate limit error handling."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = CognitiveAIRateLimitError("Rate limit exceeded")

            with pytest.raises(CognitiveAIRateLimitError):
                await client.search("Test prompt")

    @pytest.mark.asyncio
    async def test_server_error(self, client):
        """Test server error handling."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = CognitiveAIServerError("Internal server error")

            with pytest.raises(CognitiveAIServerError):
                await client.search("Test prompt")


class TestConvenienceFunctions:
    """Test convenience functions."""

    @pytest.mark.asyncio
    async def test_quick_search(self):
        """Test quick search function."""
        mock_result = SearchResult(
            job_id="quick-job-123",
            prompt="Quick test",
            response="Quick search response",
            reasoning_trace=[],
            provider="mock",
            beam=2,
            steps=1,
            tokens_used=100,
            cost=0.001,
            created_at=datetime.now()
        )

        with patch('cognitiveai.CognitiveAIClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client.search = AsyncMock(return_value=mock_result)
            mock_client_class.return_value.__aenter__.return_value = mock_client
            mock_client_class.return_value.__aexit__.return_value = None

            result = await search(
                prompt="Quick test",
                api_key="test-key",
                provider="mock"
            )

            assert result.response == "Quick search response"
            mock_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_quick_grid_search(self):
        """Test quick grid search function."""
        mock_result = GridResult(
            job_id="grid-job-456",
            prompt="Grid test",
            results=[],
            best_result={"score": 0.95},
            provider="mock",
            beams=[2, 3],
            steps=[1, 2],
            total_tokens_used=200,
            total_cost=0.003,
            created_at=datetime.now()
        )

        with patch('cognitiveai.CognitiveAIClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client.grid_search = AsyncMock(return_value=mock_result)
            mock_client_class.return_value.__aenter__.return_value = mock_client
            mock_client_class.return_value.__aexit__.return_value = None

            result = await grid_search(
                beams=[2, 3],
                steps=[1, 2],
                api_key="test-key",
                prompt="Grid test"
            )

            assert result.best_result["score"] == 0.95
            mock_client.grid_search.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
