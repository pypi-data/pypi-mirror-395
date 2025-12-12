import pytest
import respx
import json
from httpx import Response
from tuul_ai import TuulClient, AsyncTuulClient
from tuul_ai.exceptions import AuthenticationError, PermissionError, RateLimitError
from tuul_ai.types.lite import LiteResponse # Assuming LiteResponse is updated to handle nested data

BASE_URL = "https://api.tuul.digitwhale.com"

# --- MOCK DATA FIXTURES ---

# Required arguments for the new Generative API payload
MOCK_GENERATIVE_ARGS = {
    "prompt": "Test prompt.",
    "agent_id": "mock_agent_id",
    "session_id": "mock_gen_session",
}

# The fully structured JSON body the SDK MUST send for Generative API
MOCK_GENERATIVE_REQUEST_BODY = {
    "promptOptions": {"prompt": "Test prompt."},
    "stateOptions": {"cancelGeneration": False},
    "sessionOptions": {"sessionId": "mock_gen_session"},
    "agentOptions": {"agentId": "mock_agent_id", "agentVersion": "v1.0"},
    "abilityOptions": {"reasoning": True, "webSearch": False},
    "authOptions": {"platformId": "mock_platform", "apiKey": "test_key"},
}

# The structured API response for the Lite API (based on observed failure)
MOCK_LITE_API_RESPONSE = {
    "status": True,
    "message": "Lite generation executed successfully",
    "data": {
        "messages": ["The generated content."],
        "sessionId": "session_986",
        "projectId": "DGW-fbdb2b4",
        "latency_ms": 55.2
    },
    "error": None
}

# --- GENERATIVE API TESTS (Updated for complex payload) ---

@respx.mock
def test_generative_success():
    # 1. Mock the API response
    respx.post(f"{BASE_URL}/v1beta/models/generate", json=MOCK_GENERATIVE_REQUEST_BODY).mock(
        return_value=Response(200, json={
            "id": "gen_123",
            "content": "Hello world",
            "usage": {"tokens": 10},
            "created_at": 1234567890
        })
    )

    client = TuulClient(api_key="test_key")
    # 2. Call the SDK method with all required arguments
    resp = client.generative.create(**MOCK_GENERATIVE_ARGS)
    
    # 3. Assertions
    assert resp.content == "Hello world"
    assert respx.calls.last.request.content.decode() == json.dumps(MOCK_GENERATIVE_REQUEST_BODY)

@respx.mock
def test_authentication_error_401():
    respx.post(f"{BASE_URL}/v1beta/models/generate").mock(
        return_value=Response(401, json={"error": {"message": "Invalid Key"}})
    )

    client = TuulClient(api_key="bad_key")
    
    with pytest.raises(AuthenticationError) as exc:
        client.generative.create(**MOCK_GENERATIVE_ARGS) # Pass required args
    assert "Invalid Key" in str(exc.value)

@respx.mock
def test_ip_whitelist_error_403():
    respx.post(f"{BASE_URL}/v1beta/models/generate").mock(
        return_value=Response(403, json={"error": {"message": "Forbidden"}})
    )

    client = TuulClient(api_key="test_key")
    
    with pytest.raises(PermissionError) as exc:
        client.generative.create(**MOCK_GENERATIVE_ARGS) # Pass required args
    
    assert "IP is whitelisted" in str(exc.value)

@respx.mock
def test_retry_mechanism():
    route = respx.post(f"{BASE_URL}/v1beta/models/generate")
    route.side_effect = [
        Response(500),
        Response(200, json={"id": "gen_retry", "content": "Success", "usage": {}, "created_at": 1})
    ]

    client = TuulClient(api_key="test_key", max_retries=2)
    resp = client.generative.create(**MOCK_GENERATIVE_ARGS) # Pass required args
    
    assert resp.content == "Success"
    assert route.call_count == 2

# --- CONVERSATION API TESTS (No change needed) ---

@pytest.mark.asyncio
@respx.mock
async def test_async_conversation_flow():
    respx.post(f"{BASE_URL}/conversation").mock(
        return_value=Response(200, json={
            "session_id": "sess_001",
            "message": {"role": "agent", "content": "I can help"},
            "metadata": {}
        })
    )

    async with AsyncTuulClient(api_key="test_key") as client:
        # Assuming conversation API uses query parameters or body based on previous discussion
        resp = await client.conversation.send("Help me", session_id="sess_001")
        assert resp.session_id == "sess_001"
        assert resp.message.content == "I can help"

# --- LITE API TESTS (Updated for nested response and required arguments) ---

@respx.mock
def test_lite_generate_sync_full():
    """Tests synchronous Lite API generation with full parameters and verifies nested response parsing."""
    
    expected_request_body = {
        "prompt": "return a greeting in french",
        "sessionId": "session_986",
        "characteristics": [
            {"key": "identity", "value": "greeter"}
        ],
        "cacheSession": True
    }
    
    # Mock the successful API response, using the structured MOCK_LITE_API_RESPONSE
    # NOTE: The content key in the response data is derived from the last item in messages.
    mock_response = MOCK_LITE_API_RESPONSE.copy()
    mock_response['data']['messages'] = ["Bonjour!"]
    mock_response['data']['latency_ms'] = 55.2

    respx.post(f"{BASE_URL}/v1beta/models/litegen", json=expected_request_body).mock(
        return_value=Response(200, json=mock_response)
    )

    client = TuulClient(api_key="test_key")
    
    resp = client.lite.generate(
        prompt="return a greeting in french",
        session_id="session_986", # Mandatory
        characteristics=[{"key": "identity", "value": "greeter"}], # Mandatory
        cache_session=True
    )
    
    # Assertions must match the final LiteResponse object returned by the SDK's resource method
    assert isinstance(resp, LiteResponse)
    assert resp.content == "Bonjour!"
    assert resp.latency_ms == 55.2
    
    # Verify the request content sent by the client matches the expected structure
    request = respx.calls.last.request
    assert request.content.decode() == json.dumps(expected_request_body)

@pytest.mark.asyncio
@respx.mock
async def test_lite_generate_async_minimal():
    """Tests asynchronous Lite API generation with minimal required parameters."""
    
    # Use minimal required fields for the request body
    expected_request_body = {
        "prompt": "describe a python class",
        "sessionId": "async_sess_01", # Mandatory
        "characteristics": [], # Mandatory (even if empty)
        "cacheSession": False
    }

    # Mock the successful API response
    mock_response = MOCK_LITE_API_RESPONSE.copy()
    mock_response['data']['messages'] = ["An object factory."]
    mock_response['data']['latency_ms'] = 12.0
    
    respx.post(f"{BASE_URL}/v1beta/models/litegen", json=expected_request_body).mock(
        return_value=Response(200, json=mock_response)
    )

    async with AsyncTuulClient(api_key="test_key") as client:
        # Call the async SDK method with required session_id
        resp = await client.lite.generate(
            prompt="describe a python class",
            session_id="async_sess_01", # Mandatory
            # characteristics defaults to []
        )
        
        # Assertions
        assert isinstance(resp, LiteResponse)
        assert resp.content == "An object factory."
        assert resp.latency_ms == 12.0