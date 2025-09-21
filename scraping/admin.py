from django.contrib import admin
from .models import Business, CrawledPage


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_url', 'industry', 'status', 'total_pages', 'scraped_pages', 'created_by', 'created_at']
    list_filter = ['status', 'industry', 'created_at']
    search_fields = ['name', 'description', 'industry', 'website_url']
    readonly_fields = ['total_pages', 'scraped_pages']


@admin.register(CrawledPage)
class CrawledPageAdmin(admin.ModelAdmin):
    list_display = ['business', 'title', 'url', 'success', 'crawled_at']
    list_filter = ['success', 'crawled_at']
    search_fields = ['business__name', 'title', 'url', 'description']
    readonly_fields = ['crawled_at']
