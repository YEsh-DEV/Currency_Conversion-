import asyncio
from backend.schemas import ConvertRequest
from backend.agent import Agent


async def test_agent_convert_simple():
    agent = Agent()
    req = ConvertRequest(amount=1.0, base='USD', quote='EUR')
    res = await agent.handle_convert(req)
    assert res.converted >= 0


def test_agent_convert():
    asyncio.run(test_agent_convert_simple())
