"""
CognitiveAI Python SDK

A comprehensive Python SDK for the Neural Multi-Level Reasoning (CognitiveAI) API.
Provides async support, error handling, and easy integration with Python applications.
"""

import asyncio
import json
from typing import Dict, List, Optional, Union, Any, AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
import aiohttp
import logging

__version__ = "0.2.0"

logger = logging.getLogger(__name__)


@dataclass
class CognitiveAIConfig:
    """Configuration for CognitiveAI client."""
    api_key: str
    base_url: str = "https://cognitiveai-api.fly.dev"
    timeout: float = 300.0  # 5 minutes default
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class SearchRequest:
    """Request parameters for search reasoning."""
    prompt: str
    provider: str = "mock"
    beam: Optional[int] = None  # None means auto-infer
    steps: Optional[int] = None  # None means auto-infer
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    model: Optional[str] = None


@dataclass
class GridRequest:
    """Request parameters for grid reasoning."""
    beams: List[int]
    steps: List[int]
    provider: str = "mock"
    prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    model: Optional[str] = None


@dataclass
class JobStatus:
    """Job status response."""
    job_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    progress: Optional[float] = None
    artifacts_url: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None


@dataclass
class SearchResult:
    """Search reasoning result."""
    job_id: str
    prompt: str
    response: str
    reasoning_trace: List[Dict[str, Any]]
    provider: str
    beam: int
    steps: int
    tokens_used: int
    cost: float
    created_at: datetime


@dataclass
class GridResult:
    """Grid reasoning result."""
    job_id: str
    prompt: Optional[str]
    results: List[Dict[str, Any]]
    best_result: Dict[str, Any]
    provider: str
    beams: List[int]
    steps: List[int]
    total_tokens_used: int
    total_cost: float
    created_at: datetime


class CognitiveAIError(Exception):
    """Base exception for CognitiveAI API errors."""
    pass


class CognitiveAIAuthenticationError(CognitiveAIError):
    """Authentication error."""
    pass


class CognitiveAIRateLimitError(CognitiveAIError):
    """Rate limit exceeded."""
    pass


class CognitiveAIServerError(CognitiveAIError):
    """Server error."""
    pass


class CognitiveAIClient:
    """
    Async client for the CognitiveAI API.

    Example:
        async with CognitiveAIClient(api_key="your-api-key") as client:
            result = await client.search("What is the capital of France?")
            print(result.response)
    """

    def __init__(self, config: CognitiveAIConfig):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"cognitiveai-python-sdk/{__version__}",
        }

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _ensure_session(self):
        """Ensure we have an active session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )

    async def close(self):
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make an HTTP request with retry logic."""
        await self._ensure_session()

        url = f"{self.config.base_url}/api/{endpoint.lstrip('/')}"

        try:
            async with self._session.request(method, url, json=data) as response:
                response_data = await response.json()

                if response.status == 401:
                    raise CognitiveAIAuthenticationError("Invalid API key")
                elif response.status == 429:
                    raise CognitiveAIRateLimitError("Rate limit exceeded")
                elif response.status >= 500:
                    raise CognitiveAIServerError(f"Server error: {response.status}")
                elif not response.ok:
                    error_msg = response_data.get("detail", "Unknown error")
                    raise CognitiveAIError(f"Request failed: {error_msg}")

                return response_data

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if retry_count < self.config.max_retries:
                logger.warning(f"Request failed, retrying ({retry_count + 1}/{self.config.max_retries}): {e}")
                await asyncio.sleep(self.config.retry_delay * (2 ** retry_count))
                return await self._make_request(method, endpoint, data, retry_count + 1)
            else:
                raise CognitiveAIError(f"Request failed after {self.config.max_retries} retries: {e}")

    async def search(self, request: Union[SearchRequest, str]) -> SearchResult:
        """
        Perform search reasoning.

        Args:
            request: SearchRequest object or prompt string

        Returns:
            SearchResult with reasoning output

        Example:
            result = await client.search("What are the laws of thermodynamics?")
            print(result.response)
        """
        if isinstance(request, str):
            request = SearchRequest(prompt=request)

        data = {
            "prompt": request.prompt,
            "provider": request.provider,
            "beam": request.beam,
            "steps": request.steps,
        }

        if request.temperature is not None:
            data["temperature"] = request.temperature
        if request.max_tokens is not None:
            data["max_tokens"] = request.max_tokens
        if request.model is not None:
            data["model"] = request.model

        response = await self._make_request("POST", "search", data)

        # For async jobs, wait for completion
        if "job_id" in response:
            job_id = response["job_id"]
            logger.info(f"Search job started: {job_id}")

            # Wait for completion
            final_result = await self._wait_for_job(job_id)

            # Transform API result_data format to SDK format
            metadata = final_result.get("metadata", {})
            return SearchResult(
                job_id=job_id,
                prompt=metadata.get("prompt", "Unknown prompt"),  # API doesn't store prompt in result_data
                response=final_result.get("answer", ""),
                reasoning_trace=[{"reasoning": final_result.get("reasoning", "")}],
                provider=metadata.get("model", "unknown"),
                beam=metadata.get("beam", 1),
                steps=metadata.get("steps", 1),
                tokens_used=metadata.get("tokens_used", 0),  # API doesn't provide this
                cost=0.0,  # API doesn't provide this in result_data
                created_at=datetime.now()  # API doesn't provide this in result_data
            )
        else:
            # Synchronous response
            return SearchResult(
                job_id=response.get("job_id", ""),
                prompt=response["prompt"],
                response=response["response"],
                reasoning_trace=response["reasoning_trace"],
                provider=response["provider"],
                beam=response["beam"],
                steps=response["steps"],
                tokens_used=response["tokens_used"],
                cost=response["cost"],
                created_at=datetime.fromisoformat(response["created_at"])
            )

    async def grid_search(self, request: GridRequest) -> GridResult:
        """
        Perform grid reasoning across multiple beam/step combinations.

        Args:
            request: GridRequest with beam and step combinations

        Returns:
            GridResult with results from all combinations

        Example:
            result = await client.grid_search(GridRequest(
                beams=[2, 3, 4],
                steps=[1, 2],
                prompt="Solve this math problem..."
            ))
        """
        data = {
            "beams": request.beams,
            "steps": request.steps,
            "provider": request.provider,
        }

        if request.prompt is not None:
            data["prompt"] = request.prompt
        if request.temperature is not None:
            data["temperature"] = request.temperature
        if request.max_tokens is not None:
            data["max_tokens"] = request.max_tokens
        if request.model is not None:
            data["model"] = request.model

        response = await self._make_request("POST", "grid", data)

        # For async jobs, wait for completion
        if "job_id" in response:
            job_id = response["job_id"]
            logger.info(f"Grid search job started: {job_id}")

            # Wait for completion
            final_result = await self._wait_for_job(job_id)

            return GridResult(
                job_id=final_result["job_id"],
                prompt=final_result.get("prompt"),
                results=final_result["results"],
                best_result=final_result["best_result"],
                provider=final_result["provider"],
                beams=final_result["beams"],
                steps=final_result["steps"],
                total_tokens_used=final_result["total_tokens_used"],
                total_cost=final_result["total_cost"],
                created_at=datetime.fromisoformat(final_result["created_at"])
            )
        else:
            # Synchronous response
            return GridResult(
                job_id=response.get("job_id", ""),
                prompt=response.get("prompt"),
                results=response["results"],
                best_result=response["best_result"],
                provider=response["provider"],
                beams=response["beams"],
                steps=response["steps"],
                total_tokens_used=response["total_tokens_used"],
                total_cost=response["total_cost"],
                created_at=datetime.fromisoformat(response["created_at"])
            )

    async def get_job_status(self, job_id: str) -> JobStatus:
        """
        Get the status of a job.

        Args:
            job_id: The job ID to check

        Returns:
            JobStatus with current job information
        """
        response = await self._make_request("GET", f"job/{job_id}")

        return JobStatus(
            job_id=response["job_id"],
            status=response["status"],
            created_at=datetime.fromtimestamp(float(response["created_at"])),
            updated_at=datetime.fromtimestamp(float(response.get("updated_at", response["created_at"]))),
            progress=response.get("progress"),
            artifacts_url=response.get("artifacts_url"),
            error=response.get("error"),
            metadata=response.get("metadata"),
            result_data=response.get("result_data")
        )

    async def _wait_for_job(self, job_id: str, poll_interval: float = 2.0) -> Dict[str, Any]:
        """Wait for a job to complete."""
        while True:
            status = await self.get_job_status(job_id)

            if status.status == "completed":
                # The result is included in the job status response
                if status.result_data:
                    return status.result_data
                else:
                    raise CognitiveAIError("Job completed but no result data available")
            elif status.status == "failed":
                raise CognitiveAIError(f"Job failed: {status.error}")

            await asyncio.sleep(poll_interval)

    async def list_jobs(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[JobStatus]:
        """
        List jobs for the current user.

        Args:
            limit: Maximum number of jobs to return
            offset: Number of jobs to skip
            status: Filter by job status

        Returns:
            List of JobStatus objects
        """
        params = {
            "limit": limit,
            "offset": offset,
        }
        if status:
            params["status"] = status

        # Build query string
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        endpoint = f"jobs?{query_string}"

        response = await self._make_request("GET", endpoint)

        return [
            JobStatus(
                job_id=job["job_id"],
                status=job["status"],
                created_at=datetime.fromisoformat(job["created_at"]),
                updated_at=datetime.fromisoformat(job["updated_at"]),
                progress=job.get("progress"),
                artifacts_url=job.get("artifacts_url"),
                error=job.get("error"),
                metadata=job.get("metadata")
            )
            for job in response["jobs"]
        ]

    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running job.

        Args:
            job_id: The job ID to cancel

        Returns:
            True if successfully cancelled
        """
        try:
            await self._make_request("POST", f"job/{job_id}/cancel")
            return True
        except CognitiveAIError:
            return False

    async def get_api_keys(self) -> List[Dict[str, Any]]:
        """
        Get API keys for the current user.

        Returns:
            List of API key information
        """
        response = await self._make_request("GET", "keys")
        return response["keys"]

    async def create_api_key(self, name: str, permissions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new API key.

        Args:
            name: Name for the API key
            permissions: Optional list of permissions

        Returns:
            API key information including the key itself
        """
        data = {"name": name}
        if permissions:
            data["permissions"] = permissions

        response = await self._make_request("POST", "keys", data)
        return response

    async def delete_api_key(self, key_id: str) -> bool:
        """
        Delete an API key.

        Args:
            key_id: The ID of the API key to delete

        Returns:
            True if successfully deleted
        """
        try:
            await self._make_request("DELETE", f"keys/{key_id}")
            return True
        except CognitiveAIError:
            return False


# Convenience functions for quick usage
async def search(
    prompt: str,
    api_key: str,
    provider: str = "mock",
    beam: int = 2,
    steps: int = 1,
    **kwargs
) -> SearchResult:
    """
    Quick search function for simple use cases.

    Args:
        prompt: Reasoning prompt
        provider: LLM provider to use
        beam: Beam width for search
        steps: Number of reasoning steps
        api_key: Your CognitiveAI API key
        **kwargs: Additional parameters

    Returns:
        SearchResult
    """
    config = CognitiveAIConfig(api_key=api_key, **kwargs)
    async with CognitiveAIClient(config) as client:
        request = SearchRequest(
            prompt=prompt,
            provider=provider,
            beam=beam,
            steps=steps
        )
        return await client.search(request)


async def grid_search(
    beams: List[int],
    steps: List[int],
    api_key: str,
    prompt: Optional[str] = None,
    provider: str = "mock",
    **kwargs
) -> GridResult:
    """
    Quick grid search function for simple use cases.

    Args:
        beams: List of beam values to test
        steps: List of step values to test
        api_key: Your CognitiveAI API key
        prompt: Optional reasoning prompt
        provider: LLM provider to use
        **kwargs: Additional parameters

    Returns:
        GridResult
    """
    config = CognitiveAIConfig(api_key=api_key, **kwargs)
    async with CognitiveAIClient(config) as client:
        request = GridRequest(
            beams=beams,
            steps=steps,
            prompt=prompt,
            provider=provider
        )
        return await client.grid_search(request)
