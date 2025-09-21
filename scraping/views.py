from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
import json
import csv

from .models import Business, CrawledPage
from .services import CrawlService

logger = logging.getLogger(__name__)


def business_list(request):
    """List all businesses"""
    businesses = Business.objects.all()
    return render(request, 'scraping/business_list.html', {'businesses': businesses})


def create_business(request):
    """Create a new business"""
    if request.method == 'POST':
        name = request.POST.get('name')
        website_url = request.POST.get('website_url')
        description = request.POST.get('description', '')
        industry = request.POST.get('industry', '')

        # Create user for demo (in real app, use request.user)
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='demo_user')

        business = Business.objects.create(
            name=name,
            website_url=website_url,
            description=description,
            industry=industry,
            created_by=user
        )

        messages.success(request, f'Business "{name}" created successfully!')
        return redirect('business_detail', business_id=business.id)

    return render(request, 'scraping/create_business.html')


def business_detail(request, business_id):
    """Show business details and page management"""
    business = get_object_or_404(Business, id=business_id)
    pages = business.pages.all()

    return render(request, 'scraping/business_detail.html', {
        'business': business,
        'pages': pages
    })


@csrf_exempt
@require_http_methods(["POST"])
def crawl_website(request, business_id):
    """Crawl the business website and discover all pages"""
    business = get_object_or_404(Business, id=business_id)

    try:
        # Update business status
        business.status = 'crawling'
        business.save()

        # Crawl the website
        crawler = CrawlService()
        result = crawler.crawl_website(business.website_url)

        if result['success']:
            # Clear existing pages
            business.pages.all().delete()

            # Save all discovered pages
            successful_pages = 0
            for page_data in result['pages']:
                CrawledPage.objects.create(
                    business=business,
                    url=page_data['url'],
                    title=page_data['title'],
                    description=page_data['description'],
                    content=page_data['content'],
                    success=True
                )
                successful_pages += 1

            # Update business status
            business.status = 'completed'
            business.save()

            return JsonResponse({
                'success': True,
                'message': f'Successfully crawled {successful_pages} pages from {business.name}',
                'total_pages': successful_pages
            })

        else:
            # Handle failure
            business.status = 'failed'
            business.save()

            return JsonResponse({
                'success': False,
                'error': result['error']
            })

    except Exception as e:
        business.status = 'failed'
        business.save()

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def page_content(request, page_id):
    """View content for a specific crawled page"""
    page = get_object_or_404(CrawledPage, id=page_id)

    return render(request, 'scraping/page_content.html', {
        'page': page
    })


@csrf_exempt
@require_http_methods(["POST"])
def crawl_with_method(request, business_id):
    """Crawl website with specific method (basic, playwright, firecrawl)"""
    business = get_object_or_404(Business, id=business_id)
    method = request.POST.get('method', 'auto')  # auto, basic, playwright
    max_pages = int(request.POST.get('max_pages', 10))

    try:
        business.status = 'crawling'
        business.save()

        crawler = CrawlService()

        # Choose scraping method
        if method == 'basic':
            result = crawler.crawl_basic(business.website_url, max_pages)
        elif method == 'playwright':
            result = crawler.crawl_with_playwright(business.website_url, max_pages)
        else:  # auto or firecrawl
            result = crawler.crawl_website(business.website_url)

        if result['success']:
            # Clear existing pages
            business.pages.all().delete()

            # Save discovered pages
            successful_pages = 0
            for page_data in result['pages']:
                CrawledPage.objects.create(
                    business=business,
                    url=page_data['url'],
                    title=page_data['title'],
                    description=page_data['description'],
                    content=page_data['content'],
                    success=True
                )
                successful_pages += 1

            business.status = 'completed'
            business.save()

            return JsonResponse({
                'success': True,
                'message': f'Successfully crawled {successful_pages} pages using {method} method',
                'total_pages': successful_pages,
                'method_used': method
            })
        else:
            business.status = 'failed'
            business.save()
            return JsonResponse({
                'success': False,
                'error': result['error']
            })

    except Exception as e:
        business.status = 'failed'
        business.save()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def export_data(request, business_id):
    """Export scraped data in various formats"""
    business = get_object_or_404(Business, id=business_id)
    format_type = request.GET.get('format', 'json')  # json, csv, txt

    pages = business.pages.filter(success=True)

    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{business.name}_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['URL', 'Title', 'Description', 'Content Preview', 'Crawled At'])

        for page in pages:
            content_preview = page.content[:200] + '...' if len(page.content) > 200 else page.content
            writer.writerow([
                page.url,
                page.title,
                page.description,
                content_preview,
                page.crawled_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return response

    elif format_type == 'txt':
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{business.name}_data.txt"'

        content = f"Scraped Data for {business.name}\n"
        content += f"Website: {business.website_url}\n"
        content += f"Total Pages: {pages.count()}\n"
        content += "=" * 50 + "\n\n"

        for page in pages:
            content += f"URL: {page.url}\n"
            content += f"Title: {page.title}\n"
            content += f"Description: {page.description}\n"
            content += f"Content:\n{page.content}\n"
            content += "-" * 30 + "\n\n"

        response.write(content)
        return response

    else:  # JSON format
        data = {
            'business': {
                'name': business.name,
                'website_url': business.website_url,
                'industry': business.industry,
                'total_pages': pages.count(),
                'crawled_at': business.updated_at.isoformat()
            },
            'pages': []
        }

        for page in pages:
            data['pages'].append({
                'url': page.url,
                'title': page.title,
                'description': page.description,
                'content': page.content,
                'crawled_at': page.crawled_at.isoformat()
            })

        response = HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="{business.name}_data.json"'
        return response


def edit_business(request, business_id):
    """Edit business information"""
    business = get_object_or_404(Business, id=business_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        website_url = request.POST.get('website_url')
        description = request.POST.get('description', '')
        industry = request.POST.get('industry', '')

        # Update basic fields
        if name:
            business.name = name
        if description is not None:
            business.description = description
        if industry is not None:
            business.industry = industry

        # Handle URL update separately
        url_update_result = None
        if website_url and website_url != business.website_url:
            url_update_result = business.update_website_url(website_url)

            if url_update_result['success']:
                messages.success(request, url_update_result['message'])

                # Ask if user wants to re-crawl
                if request.POST.get('recrawl_after_update') == 'on':
                    return redirect('recrawl_business', business_id=business.id)
            else:
                messages.error(request, f"URL update failed: {url_update_result['error']}")

        # Save other changes
        try:
            business.save()
            if not url_update_result:  # Only show this if URL wasn't updated
                messages.success(request, f'Business "{business.name}" updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating business: {str(e)}')

        return redirect('business_detail', business_id=business.id)

    return render(request, 'scraping/edit_business.html', {
        'business': business
    })


@csrf_exempt
@require_http_methods(["POST"])
def update_business_url(request, business_id):
    """API endpoint to update business URL"""
    business = get_object_or_404(Business, id=business_id)
    new_url = request.POST.get('website_url')

    if not new_url:
        return JsonResponse({
            'success': False,
            'error': 'Website URL is required'
        })

    result = business.update_website_url(new_url)

    if result['success']:
        return JsonResponse({
            'success': True,
            'message': result['message'],
            'old_url': result['old_url'],
            'new_url': result['new_url'],
            'business_id': business.id
        })
    else:
        return JsonResponse({
            'success': False,
            'error': result['error']
        })


@csrf_exempt
@require_http_methods(["POST"])
def recrawl_business(request, business_id):
    """Re-crawl business after URL update"""
    business = get_object_or_404(Business, id=business_id)

    try:
        # Clear existing pages
        old_page_count = business.pages.count()
        business.pages.all().delete()

        # Update status
        business.status = 'crawling'
        business.save()

        # Start crawling
        crawler = CrawlService()
        result = crawler.crawl_website(business.website_url)

        if result['success']:
            # Save new pages
            successful_pages = 0
            for page_data in result['pages']:
                CrawledPage.objects.create(
                    business=business,
                    url=page_data['url'],
                    title=page_data['title'],
                    description=page_data['description'],
                    content=page_data['content'],
                    success=True
                )
                successful_pages += 1

            business.status = 'completed'
            business.save()

            return JsonResponse({
                'success': True,
                'message': f'Re-crawled successfully! Found {successful_pages} pages (previously {old_page_count})',
                'total_pages': successful_pages,
                'old_page_count': old_page_count
            })
        else:
            business.status = 'failed'
            business.save()
            return JsonResponse({
                'success': False,
                'error': result['error']
            })

    except Exception as e:
        business.status = 'failed'
        business.save()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })