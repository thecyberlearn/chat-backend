from django.db import models
from django.contrib.auth.models import User


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
