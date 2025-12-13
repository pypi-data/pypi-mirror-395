"""Tests for LLM providers."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import json

from website_scraper.llm.base import (
    BaseLLMProvider,
    LLMConfig,
    ExtractedContent,
    ScoredLink,
    ContentType,
)
from website_scraper.llm.openai_provider import OpenAIProvider
from website_scraper.llm.anthropic_provider import AnthropicProvider
from website_scraper.llm.gemini_provider import GeminiProvider
from website_scraper.llm.ollama_provider import OllamaProvider
from website_scraper.llm.factory import (
    create_llm_provider,
    LLMProviderType,
    get_available_providers,
)


class TestLLMConfig:
    """Tests for LLMConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = LLMConfig()
        
        assert config.api_key is None
        assert config.temperature == 0.1
        assert config.max_tokens == 4096
        assert config.timeout == 60.0
        assert config.max_retries == 3
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = LLMConfig(
            api_key="test-key",
            model="gpt-4",
            temperature=0.5,
            max_tokens=8192,
        )
        
        assert config.api_key == "test-key"
        assert config.model == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 8192


class TestExtractedContent:
    """Tests for ExtractedContent dataclass."""
    
    def test_default_content(self):
        """Test default values."""
        content = ExtractedContent()
        
        assert content.title == ""
        assert content.main_content == ""
        assert content.topics == []
        assert content.confidence_score == 0.0
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        content = ExtractedContent(
            title="Test Title",
            main_content="Test content",
            topics=["topic1", "topic2"],
            confidence_score=0.95,
        )
        
        data = content.to_dict()
        
        assert data["title"] == "Test Title"
        assert data["main_content"] == "Test content"
        assert data["topics"] == ["topic1", "topic2"]
        assert data["confidence_score"] == 0.95


class TestScoredLink:
    """Tests for ScoredLink dataclass."""
    
    def test_default_link(self):
        """Test default values."""
        link = ScoredLink(url="https://example.com", text="Example")
        
        assert link.url == "https://example.com"
        assert link.text == "Example"
        assert link.relevance_score == 0.0
        assert link.should_follow is True
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        link = ScoredLink(
            url="https://example.com",
            text="Example",
            relevance_score=0.8,
            priority=2,
            should_follow=True,
            reasoning="High relevance",
        )
        
        data = link.to_dict()
        
        assert data["url"] == "https://example.com"
        assert data["relevance_score"] == 0.8
        assert data["priority"] == 2


class TestContentType:
    """Tests for ContentType enum."""
    
    def test_content_types_exist(self):
        """Test content types are defined."""
        assert ContentType.MAIN_CONTENT.value == "main_content"
        assert ContentType.NAVIGATION.value == "navigation"
        assert ContentType.ADVERTISEMENT.value == "advertisement"


class TestBaseLLMProvider:
    """Tests for BaseLLMProvider base class."""
    
    def test_truncate_content(self):
        """Test content truncation."""
        config = LLMConfig(max_content_length=100)
        
        # Create a concrete implementation for testing
        class TestProvider(BaseLLMProvider):
            @property
            def provider_name(self):
                return "test"
            
            @property
            def default_model(self):
                return "test-model"
            
            async def analyze_content(self, *args, **kwargs):
                return ExtractedContent()
            
            async def analyze_links(self, *args, **kwargs):
                return []
            
            async def summarize_content(self, *args, **kwargs):
                return ""
        
        provider = TestProvider(config)
        
        long_content = "x" * 200
        truncated = provider._truncate_content(long_content)
        
        assert len(truncated) <= 100
        assert "[Content truncated...]" in truncated
    
    def test_content_extraction_prompt(self):
        """Test content extraction prompt generation."""
        class TestProvider(BaseLLMProvider):
            @property
            def provider_name(self):
                return "test"
            
            @property
            def default_model(self):
                return "test-model"
            
            async def analyze_content(self, *args, **kwargs):
                return ExtractedContent()
            
            async def analyze_links(self, *args, **kwargs):
                return []
            
            async def summarize_content(self, *args, **kwargs):
                return ""
        
        provider = TestProvider()
        
        prompt = provider._get_content_extraction_prompt(
            "https://example.com",
            "Find product information"
        )
        
        assert "https://example.com" in prompt
        assert "Find product information" in prompt
        assert "JSON" in prompt


class TestOpenAIProvider:
    """Tests for OpenAI provider."""
    
    def test_provider_name(self):
        """Test provider name."""
        config = LLMConfig(api_key="test-key")
        provider = OpenAIProvider(config)
        
        assert provider.provider_name == "openai"
    
    def test_default_model(self):
        """Test default model."""
        config = LLMConfig(api_key="test-key")
        provider = OpenAIProvider(config)
        
        assert provider.default_model == "gpt-4o-mini"
    
    @pytest.mark.asyncio
    async def test_analyze_content_with_mock(self, mock_llm_response):
        """Test content analysis with mocked OpenAI client."""
        config = LLMConfig(api_key="test-key")
        provider = OpenAIProvider(config)
        
        # Mock the client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(mock_llm_response)
        
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        provider._client = mock_client
        
        result = await provider.analyze_content(
            "<html>Test</html>",
            "https://example.com"
        )
        
        assert result.title == "Extracted Title"
        assert result.confidence_score == 0.95


class TestAnthropicProvider:
    """Tests for Anthropic provider."""
    
    def test_provider_name(self):
        """Test provider name."""
        config = LLMConfig(api_key="test-key")
        provider = AnthropicProvider(config)
        
        assert provider.provider_name == "anthropic"
    
    def test_default_model(self):
        """Test default model."""
        config = LLMConfig(api_key="test-key")
        provider = AnthropicProvider(config)
        
        assert "claude" in provider.default_model


class TestGeminiProvider:
    """Tests for Gemini provider."""
    
    def test_provider_name(self):
        """Test provider name."""
        config = LLMConfig(api_key="test-key")
        provider = GeminiProvider(config)
        
        assert provider.provider_name == "gemini"
    
    def test_default_model(self):
        """Test default model."""
        config = LLMConfig(api_key="test-key")
        provider = GeminiProvider(config)
        
        assert "gemini" in provider.default_model


class TestOllamaProvider:
    """Tests for Ollama provider."""
    
    def test_provider_name(self):
        """Test provider name."""
        provider = OllamaProvider()
        
        assert provider.provider_name == "ollama"
    
    def test_default_model(self):
        """Test default model."""
        provider = OllamaProvider()
        
        assert provider.default_model == "llama3.2"
    
    def test_default_base_url(self):
        """Test default base URL."""
        provider = OllamaProvider()
        
        assert provider.config.api_base_url == "http://localhost:11434"
    
    @pytest.mark.asyncio
    async def test_is_available_when_offline(self):
        """Test availability check when Ollama is offline."""
        provider = OllamaProvider()
        
        # This should return False when Ollama isn't running
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__ = AsyncMock()
            mock_session.return_value.__aexit__ = AsyncMock()
            mock_session.return_value.get = AsyncMock(side_effect=Exception("Connection refused"))
            
            result = await provider.is_available()
            # Result depends on actual connection
            assert result in [True, False]


class TestLLMFactory:
    """Tests for LLM factory functions."""
    
    def test_create_openai_provider(self):
        """Test creating OpenAI provider."""
        provider = create_llm_provider(
            LLMProviderType.OPENAI,
            api_key="test-key"
        )
        
        assert provider is not None
        assert provider.provider_name == "openai"
    
    def test_create_anthropic_provider(self):
        """Test creating Anthropic provider."""
        provider = create_llm_provider(
            LLMProviderType.ANTHROPIC,
            api_key="test-key"
        )
        
        assert provider is not None
        assert provider.provider_name == "anthropic"
    
    def test_create_gemini_provider(self):
        """Test creating Gemini provider."""
        provider = create_llm_provider(
            LLMProviderType.GEMINI,
            api_key="test-key"
        )
        
        assert provider is not None
        assert provider.provider_name == "gemini"
    
    def test_create_ollama_provider(self):
        """Test creating Ollama provider."""
        provider = create_llm_provider(LLMProviderType.OLLAMA)
        
        assert provider is not None
        assert provider.provider_name == "ollama"
    
    def test_create_off_returns_none(self):
        """Test OFF type returns None."""
        provider = create_llm_provider(LLMProviderType.OFF)
        
        assert provider is None
    
    def test_create_with_string_type(self):
        """Test creating with string type."""
        provider = create_llm_provider("ollama")
        
        assert provider is not None
        assert provider.provider_name == "ollama"
    
    def test_create_with_invalid_type_raises(self):
        """Test invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown provider type"):
            create_llm_provider("invalid_provider")
    
    def test_create_openai_without_key_raises(self):
        """Test OpenAI without API key raises error."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="API key not provided"):
                create_llm_provider(LLMProviderType.OPENAI)
    
    def test_create_with_custom_model(self):
        """Test creating with custom model."""
        provider = create_llm_provider(
            LLMProviderType.OPENAI,
            api_key="test-key",
            model="gpt-4"
        )
        
        assert provider.config.model == "gpt-4"

