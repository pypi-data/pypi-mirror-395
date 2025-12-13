"""Tests for content extractor."""

import pytest

from website_scraper.extractors.content import ContentExtractor, ExtractedPageData


class TestExtractedPageData:
    """Tests for ExtractedPageData dataclass."""
    
    def test_default_values(self):
        """Test default values."""
        data = ExtractedPageData()
        
        assert data.url == ""
        assert data.title == ""
        assert data.text == ""
        assert data.links == []
        assert data.images == []
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        data = ExtractedPageData(
            url="https://example.com",
            title="Test Page",
            text="Test content",
            meta_description="Test description",
        )
        
        result = data.to_dict()
        
        assert result["url"] == "https://example.com"
        assert result["title"] == "Test Page"
        assert result["text"] == "Test content"


class TestContentExtractor:
    """Tests for ContentExtractor class."""
    
    def test_default_init(self):
        """Test default initialization."""
        extractor = ContentExtractor()
        
        assert extractor.include_links is True
        assert extractor.include_images is True
        assert extractor.strip_scripts is True
        assert extractor.strip_styles is True
    
    def test_custom_init(self):
        """Test custom initialization."""
        extractor = ContentExtractor(
            include_links=False,
            include_images=False,
            max_text_length=1000,
        )
        
        assert extractor.include_links is False
        assert extractor.include_images is False
        assert extractor.max_text_length == 1000
    
    @pytest.mark.asyncio
    async def test_extract_title(self, sample_html):
        """Test title extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.title == "Test Page Title"
    
    @pytest.mark.asyncio
    async def test_extract_title_from_h1(self, sample_html_no_title):
        """Test title extraction from h1 when no title tag."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html_no_title, "https://example.com")
        
        assert "Page Without Title" in result.title
    
    @pytest.mark.asyncio
    async def test_extract_meta_description(self, sample_html):
        """Test meta description extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.meta_description == "Test meta description"
    
    @pytest.mark.asyncio
    async def test_extract_meta_keywords(self, sample_html):
        """Test meta keywords extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert "test" in result.meta_keywords
        assert "keywords" in result.meta_keywords
    
    @pytest.mark.asyncio
    async def test_extract_text(self, sample_html):
        """Test text extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert "Main Heading" in result.text
        assert "first paragraph" in result.text
    
    @pytest.mark.asyncio
    async def test_extract_headings(self, sample_html):
        """Test heading extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert "h1" in result.headings
        assert "Main Heading" in result.headings["h1"]
        assert "h2" in result.headings
    
    @pytest.mark.asyncio
    async def test_extract_links(self, sample_html):
        """Test link extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert len(result.links) > 0
        
        # Check for internal links
        urls = [link["url"] for link in result.links]
        assert any("/page1" in url for url in urls)
    
    @pytest.mark.asyncio
    async def test_extract_images(self, sample_html):
        """Test image extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert len(result.images) > 0
        assert any("image.jpg" in img["url"] for img in result.images)
    
    @pytest.mark.asyncio
    async def test_extract_language(self, sample_html):
        """Test language extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.language == "en"
    
    @pytest.mark.asyncio
    async def test_extract_canonical_url(self, sample_html):
        """Test canonical URL extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.canonical_url == "https://example.com/test-page"
    
    @pytest.mark.asyncio
    async def test_extract_author(self, sample_html):
        """Test author extraction."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.author == "Test Author"
    
    @pytest.mark.asyncio
    async def test_skip_links_when_disabled(self, sample_html):
        """Test skipping link extraction when disabled."""
        extractor = ContentExtractor(include_links=False)
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.links == []
    
    @pytest.mark.asyncio
    async def test_skip_images_when_disabled(self, sample_html):
        """Test skipping image extraction when disabled."""
        extractor = ContentExtractor(include_images=False)
        
        result = await extractor.extract(sample_html, "https://example.com")
        
        assert result.images == []
    
    @pytest.mark.asyncio
    async def test_clean_html_removes_scripts(self, sample_html):
        """Test that scripts are removed."""
        html_with_script = """
        <html>
        <head><title>Test</title></head>
        <body>
            <script>alert('bad');</script>
            <p>Content</p>
        </body>
        </html>
        """
        
        extractor = ContentExtractor(strip_scripts=True)
        result = await extractor.extract(html_with_script, "https://example.com")
        
        assert "alert" not in result.text
    
    @pytest.mark.asyncio
    async def test_clean_html_removes_styles(self):
        """Test that styles are removed."""
        html_with_style = """
        <html>
        <head>
            <title>Test</title>
            <style>body { color: red; }</style>
        </head>
        <body><p>Content</p></body>
        </html>
        """
        
        extractor = ContentExtractor(strip_styles=True)
        result = await extractor.extract(html_with_style, "https://example.com")
        
        assert "color: red" not in result.text
    
    @pytest.mark.asyncio
    async def test_text_truncation(self):
        """Test text is truncated to max length."""
        long_html = "<html><body>" + "x" * 1000000 + "</body></html>"
        
        extractor = ContentExtractor(max_text_length=1000)
        result = await extractor.extract(long_html, "https://example.com")
        
        assert len(result.text) <= 1000
    
    @pytest.mark.asyncio
    async def test_minimal_html(self, sample_html_minimal):
        """Test extraction from minimal HTML."""
        extractor = ContentExtractor()
        
        result = await extractor.extract(sample_html_minimal, "https://example.com")
        
        assert result.title == "Minimal Page"
        assert "Simple content" in result.text

