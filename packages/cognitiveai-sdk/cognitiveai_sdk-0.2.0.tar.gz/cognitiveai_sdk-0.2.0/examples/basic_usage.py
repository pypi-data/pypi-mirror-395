#!/usr/bin/env python3
"""
Example usage of the CognitiveAI Python SDK

This script demonstrates various features of the CognitiveAI SDK including:
- Basic search reasoning
- Grid search for parameter optimization
- Job management
- Error handling
"""

import asyncio
import os
from cognitiveai import (
    CognitiveAIClient,
    CognitiveAIConfig,
    SearchRequest,
    GridRequest,
    CognitiveAIError,
    search,
    grid_search
)


async def basic_search_example():
    """Demonstrate basic search reasoning."""
    print("🔍 Basic Search Example")
    print("=" * 50)

    # Get API key from environment
    api_key = os.getenv("COGNITIVEAI_API_KEY")
    if not api_key:
        print("Please set COGNITIVEAI_API_KEY environment variable")
        return

    # Configure client for local development
    config = CognitiveAIConfig(
        api_key=api_key,
        base_url="http://localhost:8000",  # Local development server
        timeout=60.0
    )

    try:
        async with CognitiveAIClient(config) as client:
            # Simple search request
            request = SearchRequest(
                prompt="What are the three fundamental laws of thermodynamics?",
                provider="mock",  # Use mock provider for testing
                beam=2,
                steps=1
            )

            print(f"Searching: {request.prompt}")
            result = await client.search(request)

            print("✅ Search completed!")
            print(f"Job ID: {result.job_id}")
            print(f"Response: {result.response}")
            print(f"Tokens used: {result.tokens_used}")
            print(".4f")
            print(f"Reasoning steps: {len(result.reasoning_trace)}")

    except CognitiveAIError as e:
        print(f"❌ CognitiveAI Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def grid_search_example():
    """Demonstrate grid search for parameter optimization."""
    print("\n🔬 Grid Search Example")
    print("=" * 50)

    api_key = os.getenv("COGNITIVEAI_API_KEY")
    if not api_key:
        print("Please set COGNITIVEAI_API_KEY environment variable")
        return

    config = CognitiveAIConfig(api_key=api_key, base_url="http://localhost:8000")

    try:
        async with CognitiveAIClient(config) as client:
            # Grid search across different beam/step combinations
            request = GridRequest(
                beams=[2, 3, 4],
                steps=[1, 2],
                prompt="Solve this complex reasoning problem: If a plane crashes on the border of the US and Canada, where do they bury the survivors?",
                provider="mock"
            )

            print("Starting grid search...")
            print(f"Testing beams: {request.beams}")
            print(f"Testing steps: {request.steps}")

            result = await client.grid_search(request)

            print("✅ Grid search completed!")
            print(f"Job ID: {result.job_id}")
            print(f"Total combinations tested: {len(result.results)}")
            print(f"Total tokens: {result.total_tokens_used}")

            # Show best result
            best = result.best_result
            print(f"\n🏆 Best result (beam={best.get('beam')}, steps={best.get('steps')}):")
            print(f"Score: {best.get('score', 'N/A')}")

    except CognitiveAIError as e:
        print(f"❌ CognitiveAI Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def job_management_example():
    """Demonstrate job management features."""
    print("\n⚙️  Job Management Example")
    print("=" * 50)

    api_key = os.getenv("COGNITIVEAI_API_KEY")
    if not api_key:
        print("Please set COGNITIVEAI_API_KEY environment variable")
        return

    config = CognitiveAIConfig(api_key=api_key, base_url="http://localhost:8000")

    try:
        async with CognitiveAIClient(config) as client:
            # Start a search job
            request = SearchRequest(
                prompt="Explain the concept of neural networks in simple terms.",
                provider="mock",
                beam=3,
                steps=2
            )

            print("Starting async job...")
            result = await client.search(request)
            job_id = result.job_id

            print(f"Job started: {job_id}")

            # Monitor job progress
            print("Monitoring job progress...")
            while True:
                status = await client.get_job_status(job_id)
                print(f"Status: {status.status}", end="")

                if status.progress is not None:
                    print(f" ({status.progress:.1%})", end="")

                print()

                if status.status == "completed":
                    print("✅ Job completed!")
                    print(f"Final result: {result.response}")
                    break
                elif status.status == "failed":
                    print(f"❌ Job failed: {status.error}")
                    break

                await asyncio.sleep(2)  # Check every 2 seconds

    except CognitiveAIError as e:
        print(f"❌ CognitiveAI Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def convenience_functions_example():
    """Demonstrate convenience functions for quick usage."""
    print("\n🚀 Convenience Functions Example")
    print("=" * 50)

    api_key = os.getenv("COGNITIVEAI_API_KEY")
    if not api_key:
        print("Please set COGNITIVEAI_API_KEY environment variable")
        return

    try:
        # Quick search
        print("Quick search:")
        result = await search(
            prompt="What is the capital of France?",
            api_key=api_key,
            provider="mock",
            beam=2,
            steps=1,
            base_url="http://localhost:8000"
        )
        print(f"Answer: {result.response}")

        # Quick grid search
        print("\nQuick grid search:")
        result = await grid_search(
            beams=[2, 3],
            steps=[1, 2],
            api_key=api_key,
            prompt="Simple test question",
            provider="mock",
            base_url="http://localhost:8000"
        )
        print(f"Best result score: {result.best_result.get('score', 'N/A')}")

    except CognitiveAIError as e:
        print(f"❌ CognitiveAI Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def api_key_management_example():
    """Demonstrate API key management."""
    print("\n🔑 API Key Management Example")
    print("=" * 50)

    api_key = os.getenv("COGNITIVEAI_API_KEY")
    if not api_key:
        print("Please set COGNITIVEAI_API_KEY environment variable")
        return

    config = CognitiveAIConfig(api_key=api_key, base_url="http://localhost:8000")

    try:
        async with CognitiveAIClient(config) as client:
            # List existing keys
            print("Existing API keys:")
            keys = await client.get_api_keys()
            for key in keys:
                print(f"  - {key['name']} ({key['id']})")

            # Create a new key
            print("\nCreating new API key...")
            new_key = await client.create_api_key(
                name="Example SDK Key",
                permissions=["read", "write"]
            )
            print(f"Created key: {new_key['name']}")
            print(f"Key value: {new_key['key'][:20]}...")  # Show first 20 chars

            # Note: In production, save this key securely!
            # await client.delete_api_key(new_key['id'])  # Uncomment to clean up

    except CognitiveAIError as e:
        print(f"❌ CognitiveAI Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def main():
    """Run all examples."""
    print("🧠 CognitiveAI Python SDK Examples")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("COGNITIVEAI_API_KEY"):
        print("⚠️  Please set the COGNITIVEAI_API_KEY environment variable to run examples")
        print("   Example: export COGNITIVEAI_API_KEY='your-api-key-here'")
        return

    # Run examples
    await basic_search_example()
    await grid_search_example()
    await job_management_example()
    await convenience_functions_example()
    await api_key_management_example()

    print("\n🎉 All examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
