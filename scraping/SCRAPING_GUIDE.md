# Enhanced Web Scraping System

## 🚀 What's Been Implemented

Your Django project now has a **comprehensive web scraping system** with multiple scraping strategies:

### **Scraping Methods Available:**

1. **Firecrawl API** (Premium) - Your existing implementation
2. **Beautiful Soup + Requests** (Free) - For static websites
3. **Playwright** (Free) - For JavaScript-heavy dynamic websites
4. **Anti-Detection Features** - Proxy rotation, user-agent rotation, random delays

### **Key Features Added:**

✅ **Multiple Scraping Strategies** - Automatic fallback from Firecrawl → Advanced scrapers
✅ **URL Discovery** - Automatically finds common pages (/about, /contact, etc.)
✅ **Anti-Detection** - User-agent rotation, random delays, proxy support
✅ **Data Export** - Export scraped data as JSON, CSV, or TXT
✅ **Enhanced Error Handling** - Robust fallback mechanisms

## 📁 New Files Added

```
scraping/
├── scrapers.py          # Advanced scraping implementations
├── proxy_manager.py     # Anti-detection and proxy rotation
└── SCRAPING_GUIDE.md   # This documentation
```

## 🛠️ Usage Examples

### **Basic Scraping (Auto-selection)**
```python
# In your Django views or shell
from scraping.services import CrawlService

crawler = CrawlService()
result = crawler.crawl_website('https://example.com')
```

### **Force Specific Scraping Method**
```python
# Use Beautiful Soup for static sites
result = crawler.crawl_basic('https://example.com', max_pages=5)

# Use Playwright for dynamic sites
result = crawler.crawl_with_playwright('https://example.com', max_pages=10)
```

### **With Anti-Detection**
```python
from scraping.proxy_manager import create_anti_detection_manager
from scraping.scrapers import BasicScraper

# Create anti-detection manager
anti_detect = create_anti_detection_manager()
scraper = BasicScraper(anti_detection=anti_detect)
```

## 🌐 New API Endpoints

### **Enhanced Crawling**
```
POST /scraping/{business_id}/crawl-method/
```
**Parameters:**
- `method`: `basic`, `playwright`, or `auto`
- `max_pages`: Number of pages to scrape (default: 10)

### **Data Export**
```
GET /scraping/{business_id}/export/?format=json
GET /scraping/{business_id}/export/?format=csv
GET /scraping/{business_id}/export/?format=txt
```

## ⚙️ Configuration

### **Environment Variables**
```bash
# .env file
FIRECRAWL_API_KEY=your-api-key-here  # Optional - falls back to free scrapers
```

### **Proxy Configuration (Optional)**
```python
# For premium proxy services
proxy_config = {
    'service': 'brightdata',  # or 'oxylabs', 'smartproxy'
    'username': 'your-username',
    'password': 'your-password',
    'customer_id': 'your-customer-id'
}

anti_detect = create_anti_detection_manager(proxy_config)
```

## 📊 Performance Comparison

| Method | Speed | Dynamic Content | Setup Complexity | Cost |
|--------|-------|----------------|------------------|------|
| **Beautiful Soup** | ⚡⚡⚡ Fast | ❌ No | ⭐ Easy | 🆓 Free |
| **Playwright** | ⚡⚡ Medium | ✅ Yes | ⭐⭐ Medium | 🆓 Free |
| **Firecrawl** | ⚡ Depends | ✅ Yes | ⭐ Easy | 💰 Paid |

## 🔧 Installation & Setup

Dependencies are already added to `requirements.txt`. Install with:

```bash
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium  # For Playwright support
```

## 📝 Usage in Frontend

### **JavaScript Example**
```javascript
// Enhanced crawling with method selection
fetch(`/scraping/${businessId}/crawl-method/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `method=playwright&max_pages=15`
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log(`Scraped ${data.total_pages} pages using ${data.method_used}`);
    }
});

// Export data
window.open(`/scraping/${businessId}/export/?format=csv`);
```

## 🛡️ Best Practices

### **Rate Limiting**
- Built-in random delays (1-3 seconds between requests)
- Respects robots.txt automatically
- User-agent rotation to appear more human

### **Error Handling**
- Automatic fallback: Firecrawl → Playwright → Beautiful Soup
- Individual page failures don't stop the entire crawl
- Detailed error logging for debugging

### **Legal Compliance**
- Always check website's robots.txt
- Respect rate limits and be polite
- Don't scrape personal data without consent
- Consider reaching out to website owners for permission

## 🚨 Troubleshooting

### **Playwright Issues**
```bash
# Reinstall Playwright browsers
playwright install chromium
```

### **Proxy Issues**
```python
# Test without proxies first
anti_detect = AntiDetectionManager(proxies=None)
```

### **Memory Issues**
- Reduce `max_pages` parameter
- Use `crawl_basic()` instead of `crawl_with_playwright()`

## 📈 Next Steps

**Possible Enhancements:**
- [ ] CAPTCHA solving integration
- [ ] Database caching of scraped data
- [ ] Scheduled scraping jobs
- [ ] Real-time scraping status updates
- [ ] Custom scraping rules per website

---

Your web scraping system is now **production-ready** with multiple fallback strategies and enterprise-grade features! 🎉