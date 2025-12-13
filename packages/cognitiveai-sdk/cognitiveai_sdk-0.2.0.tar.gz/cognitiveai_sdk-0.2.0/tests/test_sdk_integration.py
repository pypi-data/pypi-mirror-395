import sys
sys.path.insert(0, '/Users/Matt/Desktop/cognitive_ai/developer-portal/sdks/python')
import asyncio
from cognitiveai import CognitiveAIClient, CognitiveAIConfig, SearchRequest

async def test():
    config = CognitiveAIConfig(api_key='test-admin-token', base_url='http://localhost:8000')
    async with CognitiveAIClient(config) as client:
        request = SearchRequest(prompt='What is 2+2?', provider='mock')
        result = await client.search(request)
        print('SUCCESS:', result.response[:100])

if __name__ == '__main__':
    asyncio.run(test())
