"""
Enhanced HTML to Text Conversion Module with Robust Error Handling
Addresses the HTML-to-text conversion failures identified in email ingestion.
"""

import re
import html
import logging
import time
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urljoin, urlparse
import signal
from contextlib import contextmanager

try:
    import html2text
    HTML2TEXT_AVAILABLE = True
except ImportError:
    HTML2TEXT_AVAILABLE = False

try:
    from bs4 import BeautifulSoup, NavigableString
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    import bleach
    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False

try:
    import lxml
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

try:
    import html5lib
    HTML5LIB_AVAILABLE = True
except ImportError:
    HTML5LIB_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConversionTimeoutError(Exception):
    """Raised when HTML conversion takes too long."""
    pass


@contextmanager
def timeout_context(seconds: int):
    """Context manager for timing out long-running operations."""
    def timeout_handler(signum, frame):
        raise ConversionTimeoutError(f"Operation timed out after {seconds} seconds")
    
    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Restore the old signal handler
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


class EnhancedHTMLToTextConverter:
    """
    Enhanced HTML-to-text converter with comprehensive error handling,
    timeout protection, and multiple fallback strategies.
    """
    
    def __init__(self, max_content_size: int = 10 * 1024 * 1024, conversion_timeout: int = 30):
        """
        Initialize the enhanced HTML converter.

        Args:
            max_content_size: Maximum HTML content size to process (10MB default)
            conversion_timeout: Maximum time to spend on conversion (30s default)
        """
        self.max_content_size = max_content_size
        self.conversion_timeout = conversion_timeout
        self.html2text_converter = None
        self.setup_html2text()

        # Performance optimization thresholds
        self.large_content_threshold = 500 * 1024  # 500KB
        self.memory_efficient_threshold = 1024 * 1024  # 1MB

        # Microsoft Office HTML patterns (compiled for performance)
        self.mso_patterns = self._compile_mso_patterns()

        # Base64 image pattern (compiled for performance)
        self.base64_image_pattern = re.compile(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', re.IGNORECASE)

    def _compile_mso_patterns(self):
        """Compile Microsoft Office HTML patterns for performance."""
        return {
            'mso_elements': re.compile(r'</?(?:o|v|w):[^>]*>', re.IGNORECASE),
            'mso_styles': re.compile(r'mso-[^;:]*:[^;]*;?', re.IGNORECASE),
            'mso_classes': re.compile(r'class="[^"]*Mso[^"]*"', re.IGNORECASE),
            'word_comments': re.compile(r'<!--\[if [^>]*\]>.*?<!\[endif\]-->', re.DOTALL | re.IGNORECASE),
            'word_sections': re.compile(r'<div[^>]*class="[^"]*WordSection[^"]*"[^>]*>.*?</div>', re.DOTALL | re.IGNORECASE),
            'outlook_divs': re.compile(r'<div[^>]*style="[^"]*outlook[^"]*"[^>]*>.*?</div>', re.DOTALL | re.IGNORECASE),
            'empty_paragraphs': re.compile(r'<p[^>]*>\s*(?:&nbsp;|\s)*\s*</p>', re.IGNORECASE),
            'font_tags': re.compile(r'</?font[^>]*>', re.IGNORECASE)
        }
    
    def setup_html2text(self):
        """Setup html2text converter with optimal settings."""
        if HTML2TEXT_AVAILABLE:
            self.html2text_converter = html2text.HTML2Text()
            # Configure for clean text output
            self.html2text_converter.ignore_links = False
            self.html2text_converter.ignore_images = True
            self.html2text_converter.ignore_emphasis = True
            self.html2text_converter.body_width = 0  # No line wrapping
            self.html2text_converter.unicode_snob = True
            self.html2text_converter.escape_snob = True
            self.html2text_converter.mark_code = False
            self.html2text_converter.wrap_links = False
            self.html2text_converter.wrap_list_items = False
            self.html2text_converter.emphasis_mark = ""
            self.html2text_converter.strong_mark = ""
    
    def convert_html_to_text_enhanced(self, html_content: str, email_id: str = "unknown") -> Dict[str, Any]:
        """
        Enhanced HTML-to-text conversion with comprehensive error handling.
        
        Args:
            html_content: Raw HTML content to convert
            email_id: Email ID for logging purposes
            
        Returns:
            Dictionary with conversion results and metadata
        """
        start_time = time.time()
        
        # Input validation
        if not html_content or not html_content.strip():
            return self._create_result("", True, "empty_content", start_time, email_id)
        
        # Size check
        if len(html_content) > self.max_content_size:
            #logger.warning(f"Email {email_id}: HTML content too large ({len(html_content)} bytes), truncating")
            html_content = html_content[:self.max_content_size]
        
        # Quick check if content is already plain text
        if not self._contains_html_tags(html_content):
            cleaned_text = self._clean_text(html_content)
            return self._create_result(cleaned_text, True, "plain_text", start_time, email_id)
        
        # Pre-process HTML to handle common issues with performance optimization
        html_content = self._preprocess_html_enhanced(html_content, len(html_content))
        
        # Try conversion methods with timeout protection
        conversion_methods = [
            ("html2text", self._convert_with_html2text_safe),
            ("beautifulsoup", self._convert_with_beautifulsoup_safe),
            ("bleach", self._convert_with_bleach_safe),
            ("regex", self._convert_with_regex_safe),
            ("aggressive_regex", self._convert_with_aggressive_regex)
        ]
        
        for method_name, method_func in conversion_methods:
            try:
                with timeout_context(self.conversion_timeout):
                    text = method_func(html_content)
                    if text and text.strip():
                        processed_text = self._post_process_text(text)
                        if processed_text.strip():
                            return self._create_result(processed_text, True, method_name, start_time, email_id)
            except ConversionTimeoutError:
                #logger.warning(f"Email {email_id}: {method_name} conversion timed out")
                continue
            except Exception as e:
                #logger.info(f"Email {email_id}: {method_name} conversion failed: {e}")
                continue
        
        # All methods failed - return cleaned original as last resort
        #logger.error(f"Email {email_id}: All HTML conversion methods failed")
        fallback_text = self._emergency_fallback(html_content)
        return self._create_result(fallback_text, False, "emergency_fallback", start_time, email_id)
    
    def _preprocess_html_enhanced(self, html_content: str, content_size: int) -> str:
        """Enhanced pre-processing with Microsoft Office optimization and performance tuning."""
        try:
            # Performance optimization: different strategies based on content size
            if content_size > self.memory_efficient_threshold:
                return self._preprocess_large_content(html_content)
            elif content_size > self.large_content_threshold:
                return self._preprocess_medium_content(html_content)
            else:
                return self._preprocess_standard_content(html_content)
        except Exception as e:
            logger.debug(f"Enhanced HTML preprocessing failed: {e}")
            return self._preprocess_fallback(html_content)

    def _preprocess_standard_content(self, html_content: str) -> str:
        """Standard preprocessing for content <500KB."""
        # Fix common malformed HTML issues
        html_content = re.sub(r'<(\w+)([^>]*?)(?<!/)>', r'<\1\2>', html_content)
        html_content = re.sub(r'&(?![a-zA-Z0-9#]{1,7};)', '&amp;', html_content)

        # Remove problematic elements
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Enhanced Microsoft Office HTML processing
        html_content = self._process_microsoft_html(html_content)

        # Optimize base64 images
        html_content = self._optimize_base64_images(html_content)

        # Fix complex table structures
        html_content = self._fix_complex_tables(html_content)

        return html_content

    def _preprocess_medium_content(self, html_content: str) -> str:
        """Optimized preprocessing for content 500KB-1MB."""
        # Use compiled patterns for better performance
        html_content = self.mso_patterns['mso_elements'].sub('', html_content)
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Aggressive base64 image optimization for medium content
        html_content = self._optimize_base64_images_aggressive(html_content)

        # Basic Microsoft HTML cleanup
        html_content = self._process_microsoft_html_basic(html_content)

        return html_content

    def _preprocess_large_content(self, html_content: str) -> str:
        """Memory-efficient preprocessing for content >1MB."""
        # Minimal processing to avoid memory issues
        # Remove only the most problematic elements
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Aggressive base64 removal for large content
        html_content = self.base64_image_pattern.sub('[Image removed for processing]', html_content)

        # Basic MSO cleanup
        html_content = self.mso_patterns['mso_elements'].sub('', html_content)

        return html_content

    def _preprocess_fallback(self, html_content: str) -> str:
        """Minimal fallback preprocessing when enhanced methods fail."""
        try:
            # Only the most essential cleanup
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            return html_content
        except Exception:
            return html_content

    def _process_microsoft_html(self, html_content: str) -> str:
        """Comprehensive Microsoft Office HTML processing."""
        # Remove Word/Outlook conditional comments
        html_content = self.mso_patterns['word_comments'].sub('', html_content)

        # Remove MSO-specific elements and attributes
        html_content = self.mso_patterns['mso_elements'].sub('', html_content)
        html_content = self.mso_patterns['mso_styles'].sub('', html_content)
        html_content = self.mso_patterns['mso_classes'].sub('class=""', html_content)

        # Remove Word sections and Outlook divs
        html_content = self.mso_patterns['word_sections'].sub('', html_content)
        html_content = self.mso_patterns['outlook_divs'].sub('', html_content)

        # Clean up empty paragraphs and font tags
        html_content = self.mso_patterns['empty_paragraphs'].sub('', html_content)
        html_content = self.mso_patterns['font_tags'].sub('', html_content)

        # Fix Word-specific table issues
        html_content = re.sub(r'<table[^>]*border="0"[^>]*cellpadding="0"[^>]*cellspacing="0"[^>]*>', '<table>', html_content, flags=re.IGNORECASE)

        return html_content

    def _process_microsoft_html_basic(self, html_content: str) -> str:
        """Basic Microsoft Office HTML processing for medium content."""
        # Only the most essential MSO cleanup
        html_content = self.mso_patterns['mso_elements'].sub('', html_content)
        html_content = self.mso_patterns['word_comments'].sub('', html_content)
        html_content = self.mso_patterns['empty_paragraphs'].sub('', html_content)
        return html_content

    def _optimize_base64_images(self, html_content: str) -> str:
        """Optimize base64 images for better processing."""
        # Replace large base64 images with placeholders
        def replace_large_images(match):
            image_data = match.group(0)
            if len(image_data) > 50000:  # >50KB images
                return '[Large image removed for text conversion]'
            return image_data

        return self.base64_image_pattern.sub(replace_large_images, html_content)

    def _optimize_base64_images_aggressive(self, html_content: str) -> str:
        """Aggressive base64 image optimization for medium/large content."""
        # Replace all base64 images with placeholders for better performance
        return self.base64_image_pattern.sub('[Image]', html_content)

    def _fix_complex_tables(self, html_content: str) -> str:
        """Fix complex table structures that cause parsing issues."""
        # Simplify complex colspan/rowspan attributes
        html_content = re.sub(r'colspan="[^"]*"', 'colspan="1"', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'rowspan="[^"]*"', 'rowspan="1"', html_content, flags=re.IGNORECASE)

        # Remove problematic table styling
        html_content = re.sub(r'<table[^>]*style="[^"]*"[^>]*>', '<table>', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<td[^>]*style="[^"]*"[^>]*>', '<td>', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<tr[^>]*style="[^"]*"[^>]*>', '<tr>', html_content, flags=re.IGNORECASE)

        return html_content
    
    def _convert_with_html2text_safe(self, html_content: str) -> str:
        """Enhanced html2text conversion with advanced error handling."""
        if not HTML2TEXT_AVAILABLE or not self.html2text_converter:
            return ""

        try:
            # Pre-process for html2text optimization
            optimized_html = self._optimize_html_for_html2text(html_content)

            # Convert with error recovery
            text = self.html2text_converter.handle(optimized_html)

            # Post-process the output
            text = self._post_process_html2text_output(text)

            return text.strip()
        except Exception as e:
            logger.debug(f"html2text conversion failed: {e}")
            # Fallback: try with minimal HTML
            try:
                minimal_html = self._create_minimal_html(html_content)
                text = self.html2text_converter.handle(minimal_html)
                return text.strip()
            except Exception:
                return ""

    def _optimize_html_for_html2text(self, html_content: str) -> str:
        """Optimize HTML content specifically for html2text processing."""
        # Remove problematic elements that confuse html2text
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Fix common html2text issues with Microsoft HTML
        html_content = re.sub(r'<o:p[^>]*>', '<p>', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'</o:p>', '</p>', html_content, flags=re.IGNORECASE)

        # Simplify complex table structures for better text extraction
        html_content = re.sub(r'<table[^>]*>', '<table>', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<td[^>]*>', '<td>', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<tr[^>]*>', '<tr>', html_content, flags=re.IGNORECASE)

        return html_content

    def _post_process_html2text_output(self, text: str) -> str:
        """Post-process html2text output for better readability."""
        # Clean up excessive markdown formatting
        text = re.sub(r'\*{3,}', '**', text)  # Limit asterisks
        text = re.sub(r'_{3,}', '__', text)   # Limit underscores

        # Clean up link formatting
        text = re.sub(r'\[([^\]]+)\]\(\)', r'\1', text)  # Remove empty links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)  # Simplify link format

        # Clean up whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Limit consecutive newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Normalize spaces

        return text

    def _create_minimal_html(self, html_content: str) -> str:
        """Create minimal HTML for fallback processing."""
        # Extract just the essential content
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Wrap in minimal HTML structure
        return f'<html><body><p>{text}</p></body></html>'
    
    def _convert_with_beautifulsoup_safe(self, html_content: str) -> str:
        """Enhanced BeautifulSoup conversion with advanced error recovery."""
        if not BEAUTIFULSOUP_AVAILABLE:
            return ""

        try:
            # Intelligent parser selection based on content characteristics
            parsers = self._select_optimal_parsers(html_content)

            for parser in parsers:
                try:
                    soup = BeautifulSoup(html_content, parser)

                    # Enhanced element removal with error recovery
                    self._remove_problematic_elements_safe(soup)

                    # Advanced text extraction with structure preservation
                    text = self._extract_text_with_structure(soup)
                    if text and text.strip():
                        return text
                except Exception as e:
                    logger.debug(f"BeautifulSoup parser {parser} failed: {e}")
                    continue

            return ""
        except Exception as e:
            logger.debug(f"BeautifulSoup conversion failed: {e}")
            return ""

    def _select_optimal_parsers(self, html_content: str) -> list:
        """Select optimal parsers based on content characteristics."""
        parsers = []

        # Check for Microsoft Office HTML
        if any(pattern in html_content.lower() for pattern in ['mso-', 'microsoft', 'word', 'outlook']):
            # html.parser handles MSO HTML better
            parsers.extend(['html.parser', 'lxml', 'html5lib'])
        # Check for malformed HTML
        elif '</' not in html_content or html_content.count('<') != html_content.count('>'):
            # html5lib is more forgiving with malformed HTML
            parsers.extend(['html5lib', 'html.parser', 'lxml'])
        # Standard HTML
        else:
            # lxml is fastest for well-formed HTML
            parsers.extend(['lxml', 'html.parser', 'html5lib'])

        # Filter based on availability
        available_parsers = []
        for parser in parsers:
            if parser == 'lxml' and LXML_AVAILABLE:
                available_parsers.append(parser)
            elif parser == 'html5lib' and HTML5LIB_AVAILABLE:
                available_parsers.append(parser)
            elif parser == 'html.parser':
                available_parsers.append(parser)

        return available_parsers or ['html.parser']  # Fallback to built-in parser

    def _remove_problematic_elements_safe(self, soup):
        """Safely remove problematic elements with error recovery."""
        problematic_tags = ["script", "style", "meta", "link", "title", "head", "noscript"]

        for tag_name in problematic_tags:
            try:
                for element in soup.find_all(tag_name):
                    element.decompose()
            except Exception as e:
                logger.debug(f"Failed to remove {tag_name} elements: {e}")
                continue

        # Remove Microsoft Office specific elements
        try:
            for element in soup.find_all(attrs={"class": re.compile(r"Mso", re.I)}):
                element.decompose()
        except Exception:
            pass

    def _extract_text_with_structure(self, soup) -> str:
        """Extract text while preserving some structure."""
        try:
            # Add line breaks for block elements
            for element in soup.find_all(['p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if element.name == 'br':
                    element.replace_with('\n')
                else:
                    element.insert_after('\n')

            # Get text with preserved structure
            text = soup.get_text(separator=' ', strip=True)

            # Clean up excessive whitespace while preserving line breaks
            text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
            text = re.sub(r'\n[ \t]+', '\n', text)  # Remove spaces after line breaks
            text = re.sub(r'[ \t]+\n', '\n', text)  # Remove spaces before line breaks
            text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple line breaks to double

            return text
        except Exception:
            # Fallback to simple text extraction
            return soup.get_text(separator=' ', strip=True)
    
    def _convert_with_bleach_safe(self, html_content: str) -> str:
        """Safe bleach-based conversion."""
        if not BLEACH_AVAILABLE:
            return ""
        
        try:
            # Use bleach to strip all HTML tags
            text = bleach.clean(html_content, tags=[], strip=True)
            return html.unescape(text)
        except Exception as e:
            logger.debug(f"Bleach conversion failed: {e}")
            return ""
    
    def _convert_with_regex_safe(self, html_content: str) -> str:
        """Enhanced regex-based HTML tag removal with Unicode support."""
        try:
            # Enhanced HTML tag removal with better Unicode handling
            text = self._regex_remove_tags_enhanced(html_content)

            # Decode HTML entities with error recovery
            text = self._decode_html_entities_safe(text)

            # Clean up whitespace and formatting
            text = self._clean_regex_output(text)

            return text
        except Exception as e:
            logger.debug(f"Enhanced regex conversion failed: {e}")
            return ""

    def _convert_with_aggressive_regex(self, html_content: str) -> str:
        """Aggressive regex-based conversion with enhanced error recovery."""
        try:
            # Multi-stage aggressive cleaning
            text = html_content

            # Stage 1: Remove obvious HTML structures
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)

            # Stage 2: Remove all tags (more aggressive)
            text = re.sub(r'<[^<>]*?>', ' ', text)
            text = re.sub(r'<[^>]*>', ' ', text)  # Fallback for malformed tags

            # Stage 3: Handle entities and special characters
            text = self._decode_html_entities_safe(text)
            text = re.sub(r'[<>]', ' ', text)  # Remove any remaining angle brackets

            # Stage 4: Clean up the result
            text = self._clean_regex_output(text)

            return text
        except Exception as e:
            logger.debug(f"Aggressive regex conversion failed: {e}")
            return ""

    def _regex_remove_tags_enhanced(self, html_content: str) -> str:
        """Enhanced HTML tag removal with better pattern matching."""
        # Remove complete tags first
        text = re.sub(r'<[^>]+>', ' ', html_content)

        # Handle malformed tags (unclosed or broken)
        text = re.sub(r'<[^<]*$', ' ', text)  # Unclosed tag at end
        text = re.sub(r'^[^>]*>', ' ', text)  # Unclosed tag at start

        return text

    def _decode_html_entities_safe(self, text: str) -> str:
        """Safely decode HTML entities with error recovery."""
        try:
            # Standard HTML entity decoding
            text = html.unescape(text)
        except Exception:
            # Fallback: manual entity replacement for common cases
            entity_map = {
                '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"',
                '&apos;': "'", '&nbsp;': ' ', '&copy;': '©', '&reg;': '®'
            }
            for entity, replacement in entity_map.items():
                text = text.replace(entity, replacement)

        return text

    def _clean_regex_output(self, text: str) -> str:
        """Clean up regex conversion output."""
        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n[ \t]+', '\n', text)  # Remove spaces after newlines
        text = re.sub(r'[ \t]+\n', '\n', text)  # Remove spaces before newlines
        text = re.sub(r'\n{3,}', '\n\n', text)  # Limit consecutive newlines

        # Remove common artifacts
        text = re.sub(r'\s*\|\s*', ' | ', text)  # Clean up table separators
        text = re.sub(r'\s*-{3,}\s*', ' --- ', text)  # Clean up horizontal rules

        return text.strip()
    
    def _emergency_fallback(self, html_content: str) -> str:
        """Enhanced emergency fallback with intelligent text extraction."""
        try:
            # Multi-stage emergency extraction
            text = self._emergency_extract_readable_content(html_content)

            if not text or len(text.strip()) < 10:
                # Fallback to basic character extraction
                text = self._emergency_basic_extraction(html_content)

            # Ensure we return something meaningful
            if not text or len(text.strip()) < 5:
                text = "Content could not be converted to text"

            # Limit size but preserve meaningful content
            return text[:5000] if len(text) > 5000 else text

        except Exception as e:
            logger.debug(f"Emergency fallback failed: {e}")
            return "Content could not be converted to text"

    def _emergency_extract_readable_content(self, html_content: str) -> str:
        """Extract readable content using intelligent patterns."""
        try:
            # Look for common content patterns
            content_patterns = [
                r'<p[^>]*>(.*?)</p>',  # Paragraphs
                r'<div[^>]*>(.*?)</div>',  # Divs
                r'<td[^>]*>(.*?)</td>',  # Table cells
                r'<span[^>]*>(.*?)</span>',  # Spans
                r'>([^<]{20,})<',  # Long text between tags
            ]

            extracted_parts = []
            for pattern in content_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match else ""

                    # Clean the match
                    clean_match = re.sub(r'<[^>]*>', ' ', match)
                    clean_match = self._decode_html_entities_safe(clean_match)
                    clean_match = re.sub(r'\s+', ' ', clean_match).strip()

                    if len(clean_match) > 10:  # Only meaningful content
                        extracted_parts.append(clean_match)

            # Combine and deduplicate
            if extracted_parts:
                text = ' '.join(extracted_parts)
                return self._clean_regex_output(text)

            return ""

        except Exception:
            return ""

    def _emergency_basic_extraction(self, html_content: str) -> str:
        """Basic character-level extraction as last resort."""
        try:
            # Remove obvious HTML structures
            text = re.sub(r'<[^>]*>', ' ', html_content)

            # Remove HTML entities
            text = re.sub(r'&[a-zA-Z0-9#]{1,7};', ' ', text)

            # Remove remaining angle brackets
            text = re.sub(r'[<>]', ' ', text)

            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)

            return text.strip()

        except Exception:
            return ""
    
    def _contains_html_tags(self, content: str) -> bool:
        """Check if content contains HTML tags."""
        return bool(re.search(r'<[^>]+>', content))
    
    def _post_process_text(self, text: str) -> str:
        """Post-process converted text for optimal readability."""
        if not text:
            return ""
        
        try:
            # Decode HTML entities
            text = html.unescape(text)
            
            # Normalize whitespace
            text = re.sub(r'\r\n', '\n', text)
            text = re.sub(r'\r', '\n', text)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            
            # Remove excessive spaces
            lines = [line.strip() for line in text.split('\n')]
            text = '\n'.join(line for line in lines if line)
            
            return text.strip()
        except Exception as e:
            logger.debug(f"Text post-processing failed: {e}")
            return text
    
    def _clean_text(self, text: str) -> str:
        """Clean text content without HTML conversion."""
        if not text:
            return ""
        
        try:
            text = html.unescape(text)
            text = re.sub(r'\r\n', '\n', text)
            text = re.sub(r'\r', '\n', text)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            return text.strip()
        except Exception:
            return text
    
    def _create_result(self, text: str, success: bool, method: str, start_time: float, email_id: str) -> Dict[str, Any]:
        """Create standardized result dictionary."""
        duration = time.time() - start_time
        
        result = {
            "text": text,
            "conversion_successful": success,
            "method_used": method,
            "conversion_duration": duration,
            "original_length": 0,  # Will be set by caller
            "converted_length": len(text),
            "email_id": email_id
        }
        
        if success:
            logger.debug(f"Email {email_id}: HTML conversion successful using {method} ({duration:.2f}s)")
        else:
            pass
            #logger.warning(f"Email {email_id}: HTML conversion failed, using fallback ({duration:.2f}s)")
        
        return result


# Global enhanced converter instance
enhanced_html_converter = EnhancedHTMLToTextConverter()


def convert_email_body_to_text_enhanced(body_content: str, body_type: str = "text", email_id: str = "unknown") -> Dict[str, Any]:
    """
    Enhanced email body conversion with comprehensive error handling and monitoring.

    Args:
        body_content: Raw email body content
        body_type: Original body type ('text', 'html', etc.)
        email_id: Email ID for logging and tracking

    Returns:
        Dictionary with converted text and comprehensive metadata
    """
    if not body_content:
        result = {
            "text": "",
            "original_type": body_type,
            "converted_type": "plain_text",
            "conversion_successful": True,
            "original_length": 0,
            "converted_length": 0,
            "method_used": "empty_content",
            "email_id": email_id
        }

        # Record metrics
        try:
            from app.monitoring.html_conversion_metrics import record_conversion_result
            record_conversion_result(result)
        except ImportError:
            pass  # Monitoring not available

        return result

    original_length = len(body_content)

    try:
        # Use enhanced conversion
        result = enhanced_html_converter.convert_html_to_text_enhanced(body_content, email_id)

        # Add additional metadata
        result.update({
            "original_type": body_type,
            "converted_type": "plain_text",
            "original_length": original_length
        })

        # Record metrics
        try:
            from app.monitoring.html_conversion_metrics import record_conversion_result
            record_conversion_result(result)
        except ImportError:
            pass  # Monitoring not available

        return result

    except Exception as e:
        #logger.error(f"Email {email_id}: Enhanced body conversion failed: {e}")
        result = {
            "text": body_content,  # Fallback to original
            "original_type": body_type,
            "converted_type": body_type,
            "conversion_successful": False,
            "original_length": original_length,
            "converted_length": original_length,
            "method_used": "exception_fallback",
            "email_id": email_id,
            "error": str(e)
        }

        # Record metrics
        try:
            from app.monitoring.html_conversion_metrics import record_conversion_result
            record_conversion_result(result)
        except ImportError:
            pass  # Monitoring not available

        return result
