# Chat Backend - Clean Website Scraper

A clean, simple Django application for scraping websites using Firecrawl AI.

## Features

- **Simple Site Management**: Add websites to scrape
- **Modern Firecrawl Integration**: Uses the latest extract API for structured data
- **Clean Architecture**: ~150 lines total instead of 718 lines of legacy code
- **Live Status Updates**: Real-time scraping progress
- **Structured Data**: Extracts company name, description, and content

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Edit .env file
   FIRECRAWL_API_KEY=your-actual-api-key
   ```

3. **Setup Database**
   ```bash
   python manage.py migrate
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

5. **Visit Application**
   - Open http://localhost:8000
   - Add a website
   - Click "Start Scraping"

## Architecture

### Clean & Simple
- **Models**: Site + ScrapedContent (simple relationship)
- **Service**: Single ScrapingService class (~80 lines)
- **Views**: Clean view functions with proper separation
- **Templates**: Responsive, minimal UI

### Key Files
- `scraping/models.py` - Simple data models
- `scraping/services.py` - Clean Firecrawl integration
- `scraping/views.py` - Business logic separation
- `scraping/templates/` - Clean HTML templates

## How It Works

1. **Add Site**: Enter website name and URL
2. **Scrape**: Uses Firecrawl extract API with schema
3. **Extract**: AI extracts company name, description, content
4. **Store**: Saves structured data for later use

## Next Steps

This foundation supports your original plan:
- ✅ Website scraping (completed)
- 🔄 Content management (PDF, videos, forms)
- 🔄 AI Q&A generation
- 🔄 Export to business.json

## Benefits Over Previous Version

- **80% less code** (150 vs 718 lines)
- **Actually works** with current Firecrawl API
- **Easy to extend** for additional features
- **Clean separation** of concerns
- **Proper error handling**
- **Security best practices**

Built from scratch to be professional and maintainable.