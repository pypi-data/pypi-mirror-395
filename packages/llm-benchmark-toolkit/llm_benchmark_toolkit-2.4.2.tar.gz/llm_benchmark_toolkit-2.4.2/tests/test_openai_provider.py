"""
Tests for OpenAI Provider

Mocks OpenAI API calls to test provider logic without actual API requests.
"""

from unittest.mock import Mock, patch

import pytest

# Skip all tests if openai not installed
pytest.importorskip("openai", reason="openai not installed")

from llm_evaluator.providers import GenerationConfig, RateLimitError, TimeoutError
from llm_evaluator.providers.openai_provider import OpenAIProvider


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Hello, world!"
    mock_response.choices[0].finish_reason = "stop"

    mock_response.usage = Mock()
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 5
    mock_response.usage.total_tokens = 15

    return mock_response


@pytest.fixture
def provider():
    """Create OpenAI provider with mocked client"""
    with patch("llm_evaluator.providers.openai_provider.OpenAI"):
        return OpenAIProvider(model="gpt-3.5-turbo", api_key="test-key")


def test_init(provider):
    """Test provider initialization"""
    assert provider.model == "gpt-3.5-turbo"
    assert provider.api_key == "test-key"
    assert isinstance(provider.config, GenerationConfig)


def test_generate_success(provider, mock_openai_response):
    """Test successful generation"""
    provider.client.chat.completions.create = Mock(return_value=mock_openai_response)

    result = provider.generate("Test prompt")

    assert result.text == "Hello, world!"
    assert result.total_tokens == 15
    assert result.model == "gpt-3.5-turbo"
    assert result.provider == "openai"
    assert result.finish_reason == "stop"


def test_generate_with_system_prompt(provider, mock_openai_response):
    """Test generation with system prompt"""
    provider.client.chat.completions.create = Mock(return_value=mock_openai_response)

    provider.generate("Test prompt", system_prompt="You are a helpful assistant")

    # Verify messages structure
    call_args = provider.client.chat.completions.create.call_args
    messages = call_args.kwargs["messages"]

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_generate_rate_limit_retry(provider):
    """Test retry logic on rate limit"""
    from openai import RateLimitError as OpenAIRateLimitError

    # First call fails, second succeeds
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock(content="Success")
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage = Mock(prompt_tokens=10, completion_tokens=5, total_tokens=15)

    provider.client.chat.completions.create = Mock(
        side_effect=[
            OpenAIRateLimitError("Rate limited", response=Mock(status_code=429), body=None),
            mock_response,
        ]
    )

    # Should succeed after retry
    result = provider.generate("Test prompt")
    assert result.text == "Success"
    assert provider.client.chat.completions.create.call_count == 2


def test_generate_rate_limit_exhausted(provider):
    """Test rate limit error after all retries exhausted"""
    from openai import RateLimitError as OpenAIRateLimitError

    provider.client.chat.completions.create = Mock(
        side_effect=OpenAIRateLimitError("Rate limited", response=Mock(status_code=429), body=None)
    )

    config = GenerationConfig(retry_attempts=2)

    with pytest.raises(RateLimitError):
        provider.generate("Test prompt", config=config)


def test_generate_timeout(provider):
    """Test timeout error"""
    from openai import APITimeoutError

    provider.client.chat.completions.create = Mock(side_effect=APITimeoutError(request=Mock()))

    config = GenerationConfig(retry_attempts=1)

    with pytest.raises(TimeoutError):
        provider.generate("Test prompt", config=config)


def test_generate_batch(provider, mock_openai_response):
    """Test batch generation"""
    provider.client.chat.completions.create = Mock(return_value=mock_openai_response)

    prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
    results = provider.generate_batch(prompts)

    assert len(results) == 3
    assert all(r.text == "Hello, world!" for r in results)
    assert provider.client.chat.completions.create.call_count == 3


def test_is_available_success(provider):
    """Test is_available when API is accessible"""
    provider.client.models.list = Mock(return_value=[])

    assert provider.is_available() is True


def test_is_available_failure(provider):
    """Test is_available when API is not accessible"""
    provider.client.models.list = Mock(side_effect=Exception("API error"))

    assert provider.is_available() is False


def test_get_model_info(provider):
    """Test getting model information"""
    mock_model_info = Mock()
    mock_model_info.id = "gpt-3.5-turbo"
    mock_model_info.owned_by = "openai"
    mock_model_info.created = 1677649963

    provider.client.models.retrieve = Mock(return_value=mock_model_info)

    info = provider.get_model_info()

    assert info["model_id"] == "gpt-3.5-turbo"
    assert info["owned_by"] == "openai"
    assert info["provider"] == "openai"


def test_custom_config(provider, mock_openai_response):
    """Test generation with custom config"""
    provider.client.chat.completions.create = Mock(return_value=mock_openai_response)

    custom_config = GenerationConfig(
        temperature=0.9,
        max_tokens=2000,
        top_p=0.95,
    )

    provider.generate("Test", config=custom_config)

    call_args = provider.client.chat.completions.create.call_args
    assert call_args.kwargs["temperature"] == 0.9
    assert call_args.kwargs["max_tokens"] == 2000
    assert call_args.kwargs["top_p"] == 0.95
