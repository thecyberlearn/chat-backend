"""
Proxy rotation and anti-detection utilities
"""
import random
import time
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ProxyRotator:
    """Manage proxy rotation for web scraping"""

    def __init__(self, proxies: List[str] = None):
        """
        Initialize proxy rotator

        Args:
            proxies: List of proxy URLs in format 'http://user:pass@host:port'
        """
        self.proxies = proxies or []
        self.current_index = 0
        self.failed_proxies = set()

    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get next working proxy"""
        if not self.proxies:
            return None

        available_proxies = [p for i, p in enumerate(self.proxies)
                           if i not in self.failed_proxies]

        if not available_proxies:
            # Reset failed proxies if all failed
            self.failed_proxies.clear()
            available_proxies = self.proxies

        proxy_url = random.choice(available_proxies)

        return {
            'http': proxy_url,
            'https': proxy_url
        }

    def mark_proxy_failed(self, proxy_url: str):
        """Mark a proxy as failed"""
        try:
            index = self.proxies.index(proxy_url)
            self.failed_proxies.add(index)
        except ValueError:
            pass


class UserAgentRotator:
    """Rotate user agents to avoid detection"""

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]

    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self.user_agents)


class AntiDetectionManager:
    """Manage anti-detection techniques"""

    def __init__(self, proxies: List[str] = None, enable_delays: bool = True):
        self.proxy_rotator = ProxyRotator(proxies)
        self.user_agent_rotator = UserAgentRotator()
        self.enable_delays = enable_delays

    def get_session_config(self) -> Dict:
        """Get configuration for a scraping session"""
        config = {
            'headers': {
                'User-Agent': self.user_agent_rotator.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }

        # Add proxy if available
        proxy = self.proxy_rotator.get_next_proxy()
        if proxy:
            config['proxies'] = proxy

        return config

    def add_random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Add random delay between requests"""
        if self.enable_delays:
            delay = random.uniform(min_delay, max_delay)
            logger.debug(f"Adding {delay:.2f}s delay")
            time.sleep(delay)

    def get_playwright_config(self) -> Dict:
        """Get Playwright-specific configuration"""
        return {
            'user_agent': self.user_agent_rotator.get_random_user_agent(),
            'viewport': random.choice([
                {'width': 1920, 'height': 1080},
                {'width': 1366, 'height': 768},
                {'width': 1440, 'height': 900},
                {'width': 1536, 'height': 864},
            ]),
            'extra_http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            }
        }


# Example usage configurations
FREE_PROXY_LIST = [
    # Add free proxies here (not recommended for production)
    # 'http://proxy1:port',
    # 'http://proxy2:port',
]

PREMIUM_PROXY_SERVICES = {
    'brightdata': {
        'endpoint': 'http://brd-customer-{customer_id}-zone-{zone}:{password}@zproxy.lum-superproxy.io:22225',
        'description': 'Bright Data residential proxies'
    },
    'oxylabs': {
        'endpoint': 'http://customer-{username}:{password}@pr.oxylabs.io:7777',
        'description': 'Oxylabs residential proxies'
    },
    'smartproxy': {
        'endpoint': 'http://{username}:{password}@gate.smartproxy.com:7000',
        'description': 'Smartproxy residential proxies'
    }
}


def create_anti_detection_manager(proxy_config: Optional[Dict] = None) -> AntiDetectionManager:
    """
    Factory function to create an anti-detection manager

    Args:
        proxy_config: Configuration for proxy service
                     {'service': 'brightdata', 'username': 'user', 'password': 'pass', 'customer_id': 'id'}
    """
    proxies = []

    if proxy_config:
        service = proxy_config.get('service')
        if service in PREMIUM_PROXY_SERVICES:
            # Configure premium proxy service
            endpoint = PREMIUM_PROXY_SERVICES[service]['endpoint']

            # Format the endpoint with user credentials
            formatted_endpoint = endpoint.format(
                username=proxy_config.get('username', ''),
                password=proxy_config.get('password', ''),
                customer_id=proxy_config.get('customer_id', ''),
                zone=proxy_config.get('zone', 'residential')
            )
            proxies = [formatted_endpoint]

    return AntiDetectionManager(proxies=proxies)