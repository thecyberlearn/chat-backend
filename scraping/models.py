from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import requests
from urllib.parse import urlparse


class Business(models.Model):
    """Business/Company for comprehensive scraping and content management"""

    STATUS_CHOICES = [
        ('setup', 'Setup'),
        ('crawling', 'Crawling'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    # Basic Info
    name = models.CharField(max_length=200)
    website_url = models.URLField(help_text="Main website URL to crawl")
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='setup')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Branding
    primary_color = models.CharField(max_length=7, default='#3b82f6')
    secondary_color = models.CharField(max_length=7, default='#1e40af')
    logo_url = models.URLField(blank=True)

    # AI Settings
    ai_personality = models.CharField(max_length=200, default='professional and helpful')
    welcome_message = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Businesses"

    @property
    def total_pages(self):
        return self.pages.count()

    @property
    def scraped_pages(self):
        return self.pages.filter(success=True).count()

    def clean(self):
        """Validate the website URL"""
        if self.website_url:
            # Parse URL
            parsed = urlparse(self.website_url)

            # Check if URL has scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                raise ValidationError({'website_url': 'Please enter a valid URL with http:// or https://'})

            # Check if scheme is http or https
            if parsed.scheme not in ['http', 'https']:
                raise ValidationError({'website_url': 'URL must start with http:// or https://'})

    def update_website_url(self, new_url):
        """
        Update website URL and optionally clear existing pages

        Args:
            new_url (str): The new website URL

        Returns:
            dict: Result of the update operation
        """
        old_url = self.website_url

        # Validate new URL
        self.website_url = new_url
        try:
            self.clean()
        except ValidationError as e:
            # Restore old URL if validation fails
            self.website_url = old_url
            return {
                'success': False,
                'error': str(e.message_dict.get('website_url', ['Invalid URL'])[0])
            }

        # Test if URL is accessible
        try:
            response = requests.head(new_url, timeout=10, allow_redirects=True)
            if response.status_code >= 400:
                self.website_url = old_url
                return {
                    'success': False,
                    'error': f'URL returned status code {response.status_code}. Please check if the website is accessible.'
                }
        except requests.RequestException as e:
            self.website_url = old_url
            return {
                'success': False,
                'error': f'Cannot access URL: {str(e)}'
            }

        # Save the new URL
        self.save()

        return {
            'success': True,
            'message': f'Website URL updated from {old_url} to {new_url}',
            'old_url': old_url,
            'new_url': new_url
        }


class CrawledPage(models.Model):
    """Store crawled pages discovered and scraped by Firecrawl"""

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='pages')

    # Page info discovered by Firecrawl crawl
    url = models.URLField()
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    content = models.TextField()  # Full markdown content

    # Metadata
    crawled_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.business.name} - {self.title or self.url}"

    class Meta:
        ordering = ['-crawled_at']
        unique_together = ['business', 'url']
