import pytest
import os
from tuul_ai import TuulClient, AsyncTuulClient
from tuul_ai.exceptions import AuthenticationError

# Skip if no key provided
pytestmark = pytest.mark.skipif(
    not os.getenv("TUUL_API_KEY"), 
    reason="TUUL_API_KEY not set"
)

INTEGRATION_GENERATIVE_ARGS = {
    "agent_id": "DGW-12345",
    "session_id": "live-test-session-001",
}

# --- Generative API Integration Tests ---
def test_sync_generative_flow():
    client = TuulClient(api_key=os.environ["TUUL_API_KEY"])
    response = client.generative.create(
        prompt="Say hello in one word",
        **INTEGRATION_GENERATIVE_ARGS
    )
    assert response.content is not None
    assert response.id is not None

@pytest.mark.asyncio
async def test_async_generative_flow():
    async with AsyncTuulClient(api_key=os.environ["TUUL_API_KEY"]) as client:
        response = await client.generative.create(
            prompt="Say hello in one word",
            **INTEGRATION_GENERATIVE_ARGS
        )
        assert response.content is not None


# --- Lite Mode API Integration Tests ---

def test_sync_lite_generate_flow():
    """Verifies synchronous Lite Mode generation against the live API."""
    client = TuulClient(api_key=os.environ["TUUL_API_KEY"])
    
    # We use a minimal request here for simplicity, focusing on connectivity
    response = client.lite.generate(
        prompt="Return the letter A",
        session_id="test-session-sync-01",  
        cache_session=False
    )
    
    assert response.content is not None
    assert isinstance(response.content, str)

@pytest.mark.asyncio
async def test_async_lite_generate_flow():
    """Verifies asynchronous Lite Mode generation against the live API."""
    async with AsyncTuulClient(api_key=os.environ["TUUL_API_KEY"]) as client:
        response = await client.lite.generate(
            prompt="Return the letter B",
            session_id="test-session-sync-01",  
            cache_session=False
        )
        assert response.content is not None
        assert isinstance(response.content, str)