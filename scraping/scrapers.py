"""
Advanced web scraping implementations with multiple strategies
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse, urljoin
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from .proxy_manager import AntiDetectionManager

logger = logging.getLogger(__name__)


@dataclass
class ScrapedPage:
    """Data structure for scraped page information"""
    url: str
    title: str
    description: str
    content: str
    success: bool = True
    error_message: str = ""


class BasicScraper:
    """Beautiful Soup + Requests scraper for static content"""

    def __init__(self, anti_detection: Optional[AntiDetectionManager] = None):
        self.session = requests.Session()
        self.anti_detection = anti_detection or AntiDetectionManager()

        # Apply initial configuration
        config = self.anti_detection.get_session_config()
        self.session.headers.update(config['headers'])
        if 'proxies' in config:
            self.session.proxies.update(config['proxies'])

    def scrape_page(self, url: str) -> ScrapedPage:
        """Scrape a single page using requests + BeautifulSoup"""
        try:
            # Add anti-detection delay
            self.anti_detection.add_random_delay()

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""

            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '').strip() if meta_desc else ""

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract main content
            content = self._extract_main_content(soup)

            return ScrapedPage(
                url=url,
                title=title,
                description=description,
                content=content,
                success=True
            )

        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            return ScrapedPage(
                url=url,
                title="",
                description="",
                content="",
                success=False,
                error_message=str(e)
            )

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        # Try to find main content containers
        main_selectors = [
            'main',
            '[role="main"]',
            '.main-content',
            '.content',
            '.post-content',
            '.entry-content',
            'article',
            '.container'
        ]

        content_text = ""

        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                content_text = main_content.get_text(separator='\n', strip=True)
                break

        # Fallback to body content
        if not content_text:
            body = soup.find('body')
            if body:
                content_text = body.get_text(separator='\n', strip=True)

        # Clean up the text
        lines = [line.strip() for line in content_text.split('\n') if line.strip()]
        return '\n'.join(lines)


class PlaywrightScraper:
    """Playwright scraper for dynamic content"""

    def __init__(self):
        self.playwright = None
        self.browser = None

    async def __aenter__(self):
        """Async context manager entry"""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            return self
        except ImportError:
            logger.error("Playwright not installed. Run: pip install playwright && playwright install")
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def scrape_page(self, url: str) -> ScrapedPage:
        """Scrape a single page using Playwright"""
        try:
            context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()

            await page.goto(url, wait_until='networkidle')

            # Extract data
            title = await page.title()

            # Extract meta description
            meta_desc = await page.get_attribute('meta[name="description"]', 'content')
            description = meta_desc or ""

            # Extract main content
            content = await page.evaluate('''
                () => {
                    // Remove scripts and styles
                    const scripts = document.querySelectorAll('script, style');
                    scripts.forEach(el => el.remove());

                    // Try to find main content
                    const selectors = ['main', '[role="main"]', '.main-content', '.content', 'article', 'body'];
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            return element.innerText;
                        }
                    }
                    return document.body.innerText;
                }
            ''')

            await context.close()

            return ScrapedPage(
                url=url,
                title=title,
                description=description,
                content=content,
                success=True
            )

        except Exception as e:
            logger.error(f"Failed to scrape {url} with Playwright: {str(e)}")
            return ScrapedPage(
                url=url,
                title="",
                description="",
                content="",
                success=False,
                error_message=str(e)
            )


class URLDiscoverer:
    """Discover URLs from a website"""

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session.headers.update(self.headers)

    def discover_urls(self, base_url: str, max_pages: int = 20) -> List[str]:
        """Discover URLs from a website"""
        discovered_urls = set()

        # Add common pages
        common_paths = [
            '',
            '/about',
            '/about-us',
            '/services',
            '/products',
            '/contact',
            '/contact-us',
            '/blog',
            '/news',
            '/team',
            '/careers',
            '/pricing',
            '/features'
        ]

        base_domain = urlparse(base_url).netloc

        for path in common_paths:
            url = urljoin(base_url.rstrip('/'), path)
            if self._is_valid_url(url, base_domain):
                discovered_urls.add(url)

        # Try to discover more URLs from the main page
        try:
            response = self.session.get(base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')

                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(base_url, href)

                    if (self._is_valid_url(full_url, base_domain) and
                        len(discovered_urls) < max_pages):
                        discovered_urls.add(full_url)

        except Exception as e:
            logger.warning(f"Could not discover URLs from {base_url}: {str(e)}")

        return list(discovered_urls)[:max_pages]

    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid for scraping"""
        try:
            parsed = urlparse(url)

            # Must be same domain
            if parsed.netloc != base_domain:
                return False

            # Skip common non-content URLs
            skip_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.xml'}
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return False

            # Skip common non-content paths
            skip_paths = {'wp-admin', 'wp-content', 'admin', 'api', 'assets', 'static'}
            if any(skip_path in url.lower() for skip_path in skip_paths):
                return False

            return True

        except Exception:
            return False


class AdvancedCrawlService:
    """Advanced crawling service with multiple scraping strategies"""

    def __init__(self):
        self.basic_scraper = BasicScraper()
        self.url_discoverer = URLDiscoverer()

    def crawl_website(self, url: str, max_pages: int = 10, use_playwright: bool = False) -> Dict:
        """
        Crawl website with advanced strategies

        Args:
            url: Website URL to crawl
            max_pages: Maximum number of pages to scrape
            use_playwright: Whether to use Playwright for dynamic content
        """
        try:
            # Discover URLs
            logger.info(f"Discovering URLs from {url}")
            urls = self.url_discoverer.discover_urls(url, max_pages)

            if not urls:
                return {
                    'success': False,
                    'error': 'No valid URLs discovered'
                }

            # Scrape pages
            pages = []
            successful_pages = 0

            if use_playwright:
                # Use Playwright for dynamic content
                pages = self._scrape_with_playwright(urls)
            else:
                # Use basic scraper
                for page_url in urls:
                    logger.info(f"Scraping: {page_url}")
                    result = self.basic_scraper.scrape_page(page_url)

                    if result.success:
                        pages.append({
                            'url': result.url,
                            'title': result.title,
                            'description': result.description,
                            'content': result.content
                        })
                        successful_pages += 1
                    else:
                        logger.warning(f"Failed to scrape {page_url}: {result.error_message}")

            if not pages:
                return {
                    'success': False,
                    'error': 'Failed to scrape any pages successfully'
                }

            return {
                'success': True,
                'pages': pages,
                'total_pages': len(pages),
                'urls_discovered': len(urls)
            }

        except Exception as e:
            logger.error(f"Error in advanced crawling: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _scrape_with_playwright(self, urls: List[str]) -> List[Dict]:
        """Scrape URLs using Playwright (sync wrapper)"""
        import asyncio

        async def scrape_async():
            pages = []
            async with PlaywrightScraper() as scraper:
                for url in urls:
                    logger.info(f"Scraping with Playwright: {url}")
                    result = await scraper.scrape_page(url)

                    if result.success:
                        pages.append({
                            'url': result.url,
                            'title': result.title,
                            'description': result.description,
                            'content': result.content
                        })
            return pages

        try:
            return asyncio.run(scrape_async())
        except Exception as e:
            logger.error(f"Playwright scraping failed: {str(e)}")
            return []