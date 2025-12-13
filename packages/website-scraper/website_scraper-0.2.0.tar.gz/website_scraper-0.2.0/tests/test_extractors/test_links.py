"""Tests for link extractor."""

import pytest

from website_scraper.extractors.links import LinkExtractor, LinkInfo


class TestLinkInfo:
    """Tests for LinkInfo dataclass."""
    
    def test_default_values(self):
        """Test default values."""
        link = LinkInfo(url="https://example.com")
        
        assert link.url == "https://example.com"
        assert link.text == ""
        assert link.is_internal is True
        assert link.is_same_domain is True
        assert link.link_type == "content"
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        link = LinkInfo(
            url="https://example.com/page",
            text="Example Page",
            is_internal=True,
            link_type="content",
            depth=2,
        )
        
        result = link.to_dict()
        
        assert result["url"] == "https://example.com/page"
        assert result["text"] == "Example Page"
        assert result["depth"] == 2


class TestLinkExtractor:
    """Tests for LinkExtractor class."""
    
    def test_default_init(self):
        """Test default initialization."""
        extractor = LinkExtractor()
        
        assert extractor.base_domain is None
        assert extractor.include_external is False
        assert extractor.include_resources is False
    
    def test_custom_init(self):
        """Test custom initialization."""
        extractor = LinkExtractor(
            base_domain="example.com",
            include_external=True,
            max_depth=3,
        )
        
        assert extractor.base_domain == "example.com"
        assert extractor.include_external is True
        assert extractor.max_depth == 3
    
    def test_extract_basic_links(self, sample_html):
        """Test basic link extraction."""
        extractor = LinkExtractor(base_domain="example.com")
        
        links = extractor.extract(sample_html, "https://example.com")
        
        assert len(links) > 0
        
        # Check for internal links
        urls = [link.url for link in links]
        assert any("example.com" in url for url in urls)
    
    def test_extract_filters_external(self, sample_html):
        """Test external link filtering."""
        extractor = LinkExtractor(
            base_domain="example.com",
            include_external=False,
        )
        
        links = extractor.extract(sample_html, "https://example.com")
        
        # Should not include external.com
        external_links = [l for l in links if "external.com" in l.url]
        assert len(external_links) == 0
    
    def test_extract_includes_external(self, sample_html):
        """Test external link inclusion."""
        extractor = LinkExtractor(
            base_domain="example.com",
            include_external=True,
        )
        
        links = extractor.extract(sample_html, "https://example.com")
        
        # Should include external.com
        external_links = [l for l in links if "external.com" in l.url]
        assert len(external_links) > 0
    
    def test_extract_detects_internal_links(self, sample_html):
        """Test internal link detection."""
        extractor = LinkExtractor(base_domain="example.com")
        
        links = extractor.extract(sample_html, "https://example.com")
        
        internal_links = [l for l in links if l.is_internal]
        assert len(internal_links) > 0
    
    def test_extract_calculates_depth(self):
        """Test path depth calculation."""
        html = """
        <html><body>
            <a href="https://example.com/a/b/c/page">Deep Link</a>
            <a href="https://example.com/page">Shallow Link</a>
        </body></html>
        """
        
        extractor = LinkExtractor(base_domain="example.com", include_external=False)
        links = extractor.extract(html, "https://example.com")
        
        # Find the deep link
        deep_link = next((l for l in links if "/a/b/c/" in l.url), None)
        if deep_link:
            assert deep_link.depth == 4
    
    def test_extract_detects_resource_links(self):
        """Test resource link detection."""
        html = """
        <html><body>
            <a href="https://example.com/file.pdf">PDF</a>
            <a href="https://example.com/image.jpg">Image</a>
            <a href="https://example.com/page">Page</a>
        </body></html>
        """
        
        extractor = LinkExtractor(
            base_domain="example.com",
            include_resources=True,
        )
        links = extractor.extract(html, "https://example.com")
        
        resource_links = [l for l in links if l.is_resource]
        assert len(resource_links) >= 2
    
    def test_extract_filters_resources(self):
        """Test resource link filtering."""
        html = """
        <html><body>
            <a href="https://example.com/file.pdf">PDF</a>
            <a href="https://example.com/page">Page</a>
        </body></html>
        """
        
        extractor = LinkExtractor(
            base_domain="example.com",
            include_resources=False,
        )
        links = extractor.extract(html, "https://example.com")
        
        # Should not include PDF
        pdf_links = [l for l in links if ".pdf" in l.url]
        assert len(pdf_links) == 0
    
    def test_extract_detects_pagination(self):
        """Test pagination link detection."""
        html = """
        <html><body>
            <a href="https://example.com/list?page=2">Page 2</a>
            <a href="https://example.com/list/page/3">Page 3</a>
        </body></html>
        """
        
        extractor = LinkExtractor(base_domain="example.com")
        links = extractor.extract(html, "https://example.com")
        
        pagination_links = [l for l in links if l.is_pagination]
        assert len(pagination_links) >= 1
    
    def test_extract_classifies_navigation(self):
        """Test navigation link classification."""
        html = """
        <html><body>
            <a href="https://example.com/login">Login</a>
            <a href="https://example.com/signup">Sign Up</a>
            <a href="https://example.com/article">Article</a>
        </body></html>
        """
        
        extractor = LinkExtractor(base_domain="example.com")
        links = extractor.extract(html, "https://example.com")
        
        nav_links = [l for l in links if l.link_type == "navigation"]
        content_links = [l for l in links if l.link_type == "content"]
        
        assert len(nav_links) >= 1
        assert len(content_links) >= 1
    
    def test_extract_with_exclude_patterns(self):
        """Test exclude pattern filtering."""
        html = """
        <html><body>
            <a href="https://example.com/admin/page">Admin</a>
            <a href="https://example.com/public/page">Public</a>
        </body></html>
        """
        
        extractor = LinkExtractor(
            base_domain="example.com",
            exclude_patterns=[r"/admin/"],
        )
        links = extractor.extract(html, "https://example.com")
        
        # Should not include admin links
        admin_links = [l for l in links if "/admin/" in l.url]
        assert len(admin_links) == 0
    
    def test_extract_respects_max_depth(self):
        """Test max depth filtering."""
        html = """
        <html><body>
            <a href="https://example.com/a/b/c/d/e/page">Deep</a>
            <a href="https://example.com/page">Shallow</a>
        </body></html>
        """
        
        extractor = LinkExtractor(
            base_domain="example.com",
            max_depth=2,
        )
        links = extractor.extract(html, "https://example.com")
        
        # Should not include very deep links
        deep_links = [l for l in links if l.depth > 2]
        assert len(deep_links) == 0
    
    def test_filter_by_type(self):
        """Test filter_by_type method."""
        extractor = LinkExtractor()
        
        links = [
            LinkInfo(url="https://example.com/1", link_type="content"),
            LinkInfo(url="https://example.com/2", link_type="navigation"),
            LinkInfo(url="https://example.com/3", link_type="content"),
        ]
        
        content_links = extractor.filter_by_type(links, ["content"])
        
        assert len(content_links) == 2
    
    def test_get_content_links(self):
        """Test get_content_links method."""
        extractor = LinkExtractor()
        
        links = [
            LinkInfo(url="https://example.com/1", link_type="content"),
            LinkInfo(url="https://example.com/2", link_type="navigation"),
        ]
        
        content_links = extractor.get_content_links(links)
        
        assert len(content_links) == 1
        assert content_links[0].link_type == "content"
    
    def test_get_internal_links(self):
        """Test get_internal_links method."""
        extractor = LinkExtractor()
        
        links = [
            LinkInfo(url="https://example.com/1", is_internal=True),
            LinkInfo(url="https://external.com/2", is_internal=False),
        ]
        
        internal_links = extractor.get_internal_links(links)
        
        assert len(internal_links) == 1
        assert internal_links[0].is_internal is True
    
    def test_deduplicate(self):
        """Test deduplicate method."""
        extractor = LinkExtractor()
        
        links = [
            LinkInfo(url="https://example.com/page"),
            LinkInfo(url="https://example.com/page"),  # Duplicate
            LinkInfo(url="https://example.com/other"),
        ]
        
        unique = extractor.deduplicate(links)
        
        assert len(unique) == 2
    
    def test_deduplicate_ignores_fragment(self):
        """Test deduplication ignores fragments by default."""
        extractor = LinkExtractor()
        
        links = [
            LinkInfo(url="https://example.com/page#section1"),
            LinkInfo(url="https://example.com/page#section2"),
        ]
        
        unique = extractor.deduplicate(links, ignore_fragment=True)
        
        assert len(unique) == 1

