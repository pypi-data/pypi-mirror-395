"""Factory for creating LLM providers."""

import os
import logging
from enum import Enum
from typing import Optional, Union

from .base import BaseLLMProvider, LLMConfig

logger = logging.getLogger(__name__)


class LLMProviderType(str, Enum):
    """Supported LLM provider types."""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    
    @classmethod
    def from_string(cls, value: str) -> "LLMProviderType":
        """
        Convert string to LLMProviderType.
        
        Args:
            value: String representation
            
        Returns:
            LLMProviderType enum value
            
        Raises:
            ValueError: If string doesn't match any type
        """
        value = value.lower().strip()
        
        # Handle aliases
        aliases = {
            "gpt": cls.OPENAI,
            "openai": cls.OPENAI,
            "claude": cls.ANTHROPIC,
            "anthropic": cls.ANTHROPIC,
            "google": cls.GEMINI,
            "gemini": cls.GEMINI,
            "ollama": cls.OLLAMA,
            "local": cls.OLLAMA,
        }
        
        if value in aliases:
            return aliases[value]
        
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join([e.value for e in cls])
            raise ValueError(f"Unknown LLM provider: {value}. Valid providers: {valid}")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config)
        self._client = None
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    @property
    def default_model(self) -> str:
        return "gpt-4o-mini"
    
    def _get_client(self):
        """Get or create OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI
                api_key = self.config.api_key or os.environ.get("OPENAI_API_KEY")
                self._client = AsyncOpenAI(
                    api_key=api_key,
                    base_url=self.config.api_base_url,
                    timeout=self.config.timeout,
                )
            except ImportError:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
        return self._client
    
    async def analyze_content(self, html: str, url: str, extraction_goal: Optional[str] = None):
        """Analyze page content using OpenAI."""
        from .base import ExtractedContent
        import json
        
        client = self._get_client()
        content = self._truncate_content(html)
        prompt = self._get_content_extraction_prompt(url, extraction_goal)
        
        try:
            response = await client.chat.completions.create(
                model=self.config.model or self.default_model,
                messages=[
                    {"role": "system", "content": "You are a web content extraction expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt + content}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            
            result_text = response.choices[0].message.content
            # Parse JSON response
            try:
                data = json.loads(result_text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{[\s\S]*\}', result_text)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    data = {}
            
            return ExtractedContent(
                title=data.get("title", ""),
                main_content=data.get("main_content", ""),
                summary=data.get("summary", ""),
                headings=data.get("headings", []),
                author=data.get("author"),
                date_published=data.get("date_published"),
                language=data.get("language"),
                content_type=data.get("content_type", "article"),
                topics=data.get("topics", []),
                confidence_score=data.get("confidence_score", 0.0),
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"OpenAI content analysis failed: {e}")
            return ExtractedContent(extraction_notes=str(e))
    
    async def analyze_links(self, links, page_context: str, crawl_goal: Optional[str] = None):
        """Analyze links using OpenAI."""
        from .base import ScoredLink
        import json
        
        client = self._get_client()
        prompt = self._get_link_analysis_prompt(page_context, crawl_goal)
        links_text = json.dumps(links, indent=2)
        
        try:
            response = await client.chat.completions.create(
                model=self.config.model or self.default_model,
                messages=[
                    {"role": "system", "content": "You are a web crawling expert. Analyze links for relevance. Always respond with valid JSON."},
                    {"role": "user", "content": prompt + links_text}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            
            result_text = response.choices[0].message.content
            data = json.loads(result_text)
            
            scored_links = []
            for link_data in data.get("links", []):
                scored_links.append(ScoredLink(
                    url=link_data.get("url", ""),
                    text=link_data.get("text", ""),
                    relevance_score=link_data.get("relevance_score", 0.0),
                    priority=link_data.get("priority", 5),
                    link_type=link_data.get("link_type", "content"),
                    should_follow=link_data.get("should_follow", True),
                    reasoning=link_data.get("reasoning", ""),
                ))
            
            return sorted(scored_links, key=lambda x: (-x.relevance_score, x.priority))
        except Exception as e:
            logger.error(f"OpenAI link analysis failed: {e}")
            return []
    
    async def summarize_content(self, content: str, max_length: int = 500) -> str:
        """Summarize content using OpenAI."""
        client = self._get_client()
        
        try:
            response = await client.chat.completions.create(
                model=self.config.model or self.default_model,
                messages=[
                    {"role": "system", "content": f"Summarize the following content in {max_length} characters or less."},
                    {"role": "user", "content": self._truncate_content(content)}
                ],
                temperature=self.config.temperature,
                max_tokens=min(self.config.max_tokens, 500),
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI summarization failed: {e}")
            return ""


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider implementation."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config)
        self._client = None
    
    @property
    def provider_name(self) -> str:
        return "anthropic"
    
    @property
    def default_model(self) -> str:
        return "claude-3-haiku-20240307"
    
    def _get_client(self):
        """Get or create Anthropic client."""
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
                api_key = self.config.api_key or os.environ.get("ANTHROPIC_API_KEY")
                self._client = AsyncAnthropic(api_key=api_key)
            except ImportError:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        return self._client
    
    async def analyze_content(self, html: str, url: str, extraction_goal: Optional[str] = None):
        """Analyze page content using Anthropic."""
        from .base import ExtractedContent
        import json
        
        client = self._get_client()
        content = self._truncate_content(html)
        prompt = self._get_content_extraction_prompt(url, extraction_goal)
        
        try:
            response = await client.messages.create(
                model=self.config.model or self.default_model,
                max_tokens=self.config.max_tokens,
                messages=[{"role": "user", "content": prompt + content}],
            )
            
            result_text = response.content[0].text
            data = json.loads(result_text)
            
            return ExtractedContent(
                title=data.get("title", ""),
                main_content=data.get("main_content", ""),
                summary=data.get("summary", ""),
                headings=data.get("headings", []),
                author=data.get("author"),
                date_published=data.get("date_published"),
                language=data.get("language"),
                content_type=data.get("content_type", "article"),
                topics=data.get("topics", []),
                confidence_score=data.get("confidence_score", 0.0),
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"Anthropic content analysis failed: {e}")
            return ExtractedContent(extraction_notes=str(e))
    
    async def analyze_links(self, links, page_context: str, crawl_goal: Optional[str] = None):
        """Analyze links using Anthropic."""
        from .base import ScoredLink
        import json
        
        client = self._get_client()
        prompt = self._get_link_analysis_prompt(page_context, crawl_goal)
        links_text = json.dumps(links, indent=2)
        
        try:
            response = await client.messages.create(
                model=self.config.model or self.default_model,
                max_tokens=self.config.max_tokens,
                messages=[{"role": "user", "content": prompt + links_text}],
            )
            
            result_text = response.content[0].text
            data = json.loads(result_text)
            
            scored_links = []
            for link_data in data.get("links", []):
                scored_links.append(ScoredLink(
                    url=link_data.get("url", ""),
                    text=link_data.get("text", ""),
                    relevance_score=link_data.get("relevance_score", 0.0),
                    priority=link_data.get("priority", 5),
                    link_type=link_data.get("link_type", "content"),
                    should_follow=link_data.get("should_follow", True),
                    reasoning=link_data.get("reasoning", ""),
                ))
            
            return sorted(scored_links, key=lambda x: (-x.relevance_score, x.priority))
        except Exception as e:
            logger.error(f"Anthropic link analysis failed: {e}")
            return []
    
    async def summarize_content(self, content: str, max_length: int = 500) -> str:
        """Summarize content using Anthropic."""
        client = self._get_client()
        
        try:
            response = await client.messages.create(
                model=self.config.model or self.default_model,
                max_tokens=min(self.config.max_tokens, 500),
                messages=[{
                    "role": "user",
                    "content": f"Summarize the following content in {max_length} characters or less:\n\n{self._truncate_content(content)}"
                }],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic summarization failed: {e}")
            return ""


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config)
        self._model = None
    
    @property
    def provider_name(self) -> str:
        return "gemini"
    
    @property
    def default_model(self) -> str:
        return "gemini-1.5-flash"
    
    def _get_model(self):
        """Get or create Gemini model."""
        if self._model is None:
            try:
                import google.generativeai as genai
                api_key = self.config.api_key or os.environ.get("GOOGLE_API_KEY")
                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel(self.config.model or self.default_model)
            except ImportError:
                raise ImportError("Google generativeai package not installed. Run: pip install google-generativeai")
        return self._model
    
    async def analyze_content(self, html: str, url: str, extraction_goal: Optional[str] = None):
        """Analyze page content using Gemini."""
        from .base import ExtractedContent
        import json
        import asyncio
        
        model = self._get_model()
        content = self._truncate_content(html)
        prompt = self._get_content_extraction_prompt(url, extraction_goal)
        
        try:
            # Gemini doesn't have native async, use thread
            response = await asyncio.to_thread(
                model.generate_content,
                prompt + content,
            )
            
            result_text = response.text
            data = json.loads(result_text)
            
            return ExtractedContent(
                title=data.get("title", ""),
                main_content=data.get("main_content", ""),
                summary=data.get("summary", ""),
                headings=data.get("headings", []),
                author=data.get("author"),
                date_published=data.get("date_published"),
                language=data.get("language"),
                content_type=data.get("content_type", "article"),
                topics=data.get("topics", []),
                confidence_score=data.get("confidence_score", 0.0),
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"Gemini content analysis failed: {e}")
            return ExtractedContent(extraction_notes=str(e))
    
    async def analyze_links(self, links, page_context: str, crawl_goal: Optional[str] = None):
        """Analyze links using Gemini."""
        from .base import ScoredLink
        import json
        import asyncio
        
        model = self._get_model()
        prompt = self._get_link_analysis_prompt(page_context, crawl_goal)
        links_text = json.dumps(links, indent=2)
        
        try:
            response = await asyncio.to_thread(
                model.generate_content,
                prompt + links_text,
            )
            
            result_text = response.text
            data = json.loads(result_text)
            
            scored_links = []
            for link_data in data.get("links", []):
                scored_links.append(ScoredLink(
                    url=link_data.get("url", ""),
                    text=link_data.get("text", ""),
                    relevance_score=link_data.get("relevance_score", 0.0),
                    priority=link_data.get("priority", 5),
                    link_type=link_data.get("link_type", "content"),
                    should_follow=link_data.get("should_follow", True),
                    reasoning=link_data.get("reasoning", ""),
                ))
            
            return sorted(scored_links, key=lambda x: (-x.relevance_score, x.priority))
        except Exception as e:
            logger.error(f"Gemini link analysis failed: {e}")
            return []
    
    async def summarize_content(self, content: str, max_length: int = 500) -> str:
        """Summarize content using Gemini."""
        import asyncio
        model = self._get_model()
        
        try:
            response = await asyncio.to_thread(
                model.generate_content,
                f"Summarize the following content in {max_length} characters or less:\n\n{self._truncate_content(content)}",
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini summarization failed: {e}")
            return ""


def create_llm_provider(
    provider_type: Union[str, LLMProviderType],
    config: Optional[LLMConfig] = None,
) -> BaseLLMProvider:
    """
    Factory function to create an LLM provider instance.
    
    This is the recommended way to create LLM providers, as it handles
    type conversion and provides a consistent interface.
    
    Args:
        provider_type: Type of provider to create (openai, anthropic, gemini, ollama)
        config: Optional LLM configuration
        
    Returns:
        Configured LLM provider instance
        
    Raises:
        ValueError: If provider_type is invalid
        
    Example:
        >>> provider = create_llm_provider("openai", LLMConfig(api_key="sk-..."))
        >>> content = await provider.analyze_content(html, url)
    """
    # Convert string to enum if needed
    if isinstance(provider_type, str):
        provider_type = LLMProviderType.from_string(provider_type)
    
    # Create appropriate provider
    providers = {
        LLMProviderType.OPENAI: OpenAIProvider,
        LLMProviderType.ANTHROPIC: AnthropicProvider,
        LLMProviderType.GEMINI: GeminiProvider,
    }
    
    provider_class = providers.get(provider_type)
    if not provider_class:
        raise ValueError(f"No provider registered for type: {provider_type}")
    
    return provider_class(config)


def get_available_providers() -> list[str]:
    """
    Get list of available LLM providers.
    
    Returns:
        List of provider names
    """
    return [e.value for e in LLMProviderType]


def auto_detect_provider() -> Optional[LLMProviderType]:
    """
    Auto-detect available LLM provider based on environment variables.
    
    Returns:
        Detected provider type or None
    """
    if os.environ.get("OPENAI_API_KEY"):
        return LLMProviderType.OPENAI
    if os.environ.get("ANTHROPIC_API_KEY"):
        return LLMProviderType.ANTHROPIC
    if os.environ.get("GOOGLE_API_KEY"):
        return LLMProviderType.GEMINI
    return None
