# AI Chat Integration & Data Export Reference

## 📋 **Project Overview**

This document outlines the complete integration between two key systems:

### **Backend System (Django)**
- **Location:** `/home/amit/projects/chat-backend`
- **Purpose:** Web scraping, data collection, business management
- **Technology:** Django + Beautiful Soup + Playwright + Firecrawl
- **Current Features:**
  - Multi-strategy web scraping (Firecrawl, Playwright, Beautiful Soup)
  - Business and CrawledPage models
  - Export functionality (JSON, CSV, TXT)
  - Anti-detection features (proxy rotation, user-agent rotation)
  - URL validation and update capabilities

### **Frontend System (Vue.js AI Chat)**
- **Location:** `/mnt/sdd2/projects/aichat-17092025`
- **Purpose:** AI business receptionist with intelligent chat interface
- **Technology:** Vue 3 + TypeScript + Pinia + Tailwind CSS
- **Current Features:**
  - AI-powered chat with business-specific knowledge
  - Dynamic content panel (PDFs, videos, forms, booking widgets)
  - Website scraping integration
  - Customizable branding per business
  - Voice support and lead capture

## 🔄 **Data Flow Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Django        │    │   AI Processing  │    │   Vue.js Chat   │
│   Backend       │───▶│   & Export       │───▶│   Frontend      │
│                 │    │                  │    │                 │
│ • Web Scraping  │    │ • Text Cleaning  │    │ • AI Chat       │
│ • Data Storage  │    │ • Text Chunking  │    │ • Knowledge Base│
│ • URL Management│    │ • Format Convert │    │ • Content Panel │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 **Current Export Capabilities**

### **Existing Django Exports:**
1. **JSON Format** - Structured business + pages data
2. **CSV Format** - Tabular data with content previews (truncated)
3. **TXT Format** - Plain text with full content

### **Current Vue.js Data Structure:**
```json
{
  "id": "business-id",
  "name": "Business Name",
  "description": "Business description for AI responses",
  "website": "https://business.com",
  "knowledgeBase": [
    {
      "id": "kb-1",
      "question": "What services do you offer?",
      "answer": "We provide...",
      "tags": ["services"],
      "contentIds": ["company-brochure"],
      "priority": 10
    }
  ],
  "content": [
    {
      "id": "company-brochure",
      "type": "website",
      "title": "Company Overview",
      "url": "https://company.com/about",
      "category": "company"
    }
  ]
}
```

## 🎯 **Implementation Plan**

### **Phase 1: AI-Ready Export Formats**

#### **1.1 JSONL Export (AI Training Standard)**
```python
# Format: One JSON object per line
{"text": "cleaned content", "metadata": {"url": "...", "title": "...", "source": "website"}}
{"text": "another page content", "metadata": {"url": "...", "title": "...", "source": "website"}}
```

#### **1.2 OpenAI Training Format**
```python
# Chat completion training format
{"messages": [
  {"role": "system", "content": "You are an expert on {business_name}"},
  {"role": "user", "content": "What does this page say about {topic}?"},
  {"role": "assistant", "content": "{processed_content}"}
]}
```

#### **1.3 Knowledge Base Format (Vue.js Compatible)**
```python
# Direct import format for Vue.js knowledgeBase array
{
  "knowledgeBase": [
    {
      "id": "kb-auto-1",
      "question": "What is mentioned about services on the website?",
      "answer": "Based on the website content...",
      "tags": ["services", "auto-generated"],
      "contentIds": ["scraped-services-page"],
      "priority": 5,
      "source": "auto-scraped"
    }
  ]
}
```

#### **1.4 RAG Chunks Format**
```python
# Optimized for vector databases and embeddings
{
  "chunk_id": "uuid-1234",
  "text": "chunk content (200-1000 tokens)",
  "chunk_index": 1,
  "total_chunks": 5,
  "metadata": {
    "url": "source-url",
    "title": "page-title",
    "business": "business-name",
    "section": "about|services|pricing|contact"
  }
}
```

### **Phase 2: Text Processing Pipeline**

#### **2.1 Content Cleaning Service**
```python
class ContentProcessor:
    def clean_text(self, html_content: str) -> str:
        # Remove HTML tags, normalize whitespace
        # Handle special characters and encoding
        # Remove navigation, footer, irrelevant content

    def extract_meaningful_content(self, content: str) -> str:
        # Identify main content sections
        # Remove boilerplate text
        # Extract key information
```

#### **2.2 Text Chunking Strategies**
```python
class TextChunker:
    def chunk_by_tokens(self, text: str, max_tokens: int = 500) -> List[str]:
        # Token-based chunking for AI models

    def chunk_by_semantics(self, text: str) -> List[str]:
        # Semantic chunking preserving meaning

    def chunk_by_sections(self, html: str) -> List[dict]:
        # Section-based chunking (headers, paragraphs)
```

#### **2.3 Quality Filtering**
```python
class QualityFilter:
    def score_content_quality(self, text: str) -> float:
        # Length, readability, information density

    def detect_duplicates(self, new_content: str, existing: List[str]) -> bool:
        # Semantic similarity detection

    def filter_low_quality(self, content_list: List[str]) -> List[str]:
        # Remove poor quality content
```

### **Phase 3: New Django Export APIs**

#### **3.1 AI Export Endpoints**
```python
# New URLs to add to scraping/urls.py
urlpatterns = [
    # ... existing URLs ...

    # AI Export endpoints
    path('<int:business_id>/export-ai/', views.export_ai_data, name='export_ai_data'),
    path('<int:business_id>/export-jsonl/', views.export_jsonl, name='export_jsonl'),
    path('<int:business_id>/export-openai/', views.export_openai_training, name='export_openai_training'),
    path('<int:business_id>/export-knowledge/', views.export_knowledge_base, name='export_knowledge_base'),
    path('<int:business_id>/export-vue-config/', views.export_vue_config, name='export_vue_config'),
]
```

#### **3.2 Export Views Implementation**
```python
def export_ai_data(request, business_id):
    """
    Main AI export endpoint with format selection
    ?format=jsonl|openai|knowledge|rag|vue-config
    """

def export_jsonl(request, business_id):
    """Export as JSONL for general AI training"""

def export_openai_training(request, business_id):
    """Export in OpenAI fine-tuning format"""

def export_knowledge_base(request, business_id):
    """Export as Vue.js compatible knowledge base"""

def export_vue_config(request, business_id):
    """Export complete Vue.js business.json configuration"""
```

### **Phase 4: Vue.js Integration Points**

#### **4.1 Business Configuration Sync**
```typescript
// Auto-generate Vue.js business.json from Django data
interface BusinessConfig {
  id: string
  name: string
  description: string
  website: string
  branding: {
    primaryColor: string
    secondaryColor: string
    logo: string
  }
  scrapingConfig: {
    enabled: boolean
    website: string
    contentPriority: string[]
  }
  knowledgeBase: KnowledgeBaseItem[]
  content: ContentItem[]
}
```

#### **4.2 Knowledge Base Import Service**
```typescript
// src/services/backendSync.ts
class BackendSyncService {
  async importBusinessConfig(businessId: string): Promise<BusinessConfig>
  async importKnowledgeBase(businessId: string): Promise<KnowledgeBaseItem[]>
  async importScrapedContent(businessId: string): Promise<ContentItem[]>
  async syncFromBackend(businessId: string): Promise<void>
}
```

#### **4.3 Auto-Generated Content Items**
```typescript
// Convert Django scraped pages to Vue.js content items
{
  "id": "scraped-about-page",
  "type": "website",
  "title": "About Us", // from scraped title
  "description": "Company overview and mission", // from scraped description
  "url": "https://company.com/about", // original URL
  "tags": ["about", "company", "auto-scraped"],
  "category": "company",
  "source": "django-scraper",
  "lastUpdated": "2025-01-21T10:00:00Z"
}
```

## 🛠️ **Implementation Code Examples**

### **Django AI Export Service**
```python
# scraping/ai_export_service.py
import json
import uuid
from typing import List, Dict
from .models import Business, CrawledPage

class AIExportService:
    def __init__(self, business_id: int):
        self.business = Business.objects.get(id=business_id)
        self.pages = self.business.pages.filter(success=True)

    def export_jsonl(self) -> str:
        """Export as JSONL for AI training"""
        lines = []
        for page in self.pages:
            data = {
                "text": self._clean_content(page.content),
                "metadata": {
                    "url": page.url,
                    "title": page.title,
                    "description": page.description,
                    "business": self.business.name,
                    "industry": self.business.industry,
                    "scraped_at": page.crawled_at.isoformat()
                }
            }
            lines.append(json.dumps(data))
        return '\n'.join(lines)

    def export_openai_training(self) -> str:
        """Export for OpenAI fine-tuning"""
        lines = []
        for page in self.pages:
            data = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an AI assistant for {self.business.name}, a {self.business.industry} company."
                    },
                    {
                        "role": "user",
                        "content": f"What can you tell me about {page.title}?"
                    },
                    {
                        "role": "assistant",
                        "content": self._clean_content(page.content)[:2000]  # Limit length
                    }
                ]
            }
            lines.append(json.dumps(data))
        return '\n'.join(lines)

    def export_vue_knowledge_base(self) -> Dict:
        """Export for Vue.js knowledge base"""
        knowledge_items = []
        for i, page in enumerate(self.pages):
            knowledge_items.append({
                "id": f"kb-auto-{i+1}",
                "question": f"What information is available about {page.title}?",
                "answer": f"Based on our website: {self._clean_content(page.content)[:500]}...",
                "tags": self._extract_tags(page),
                "contentIds": [f"scraped-{page.id}"],
                "priority": 5,
                "source": "auto-generated"
            })

        return {"knowledgeBase": knowledge_items}

    def export_vue_business_config(self) -> Dict:
        """Export complete Vue.js business configuration"""
        return {
            "id": f"business-{self.business.id}",
            "name": self.business.name,
            "description": self.business.description,
            "industry": self.business.industry,
            "website": self.business.website_url,
            "branding": {
                "primaryColor": self.business.primary_color,
                "secondaryColor": self.business.secondary_color,
                "logo": self.business.logo_url or "/logos/default.svg",
                "font": "Inter"
            },
            "scrapingConfig": {
                "enabled": True,
                "website": self.business.website_url,
                "contentPriority": ["about", "services", "pricing", "contact"],
                "updateSchedule": "weekly"
            },
            "content": self._generate_content_items(),
            "knowledgeBase": self.export_vue_knowledge_base()["knowledgeBase"],
            "settings": {
                "welcomeMessage": f"Hello! I'm your AI assistant at {self.business.name}. How can I help you today?",
                "aiPersonality": "professional and helpful",
                "enableVoice": True,
                "enableLeadCapture": True
            }
        }

    def _clean_content(self, content: str) -> str:
        """Clean and normalize content for AI consumption"""
        # Remove HTML tags, normalize whitespace, etc.
        import re
        cleaned = re.sub(r'<[^>]+>', '', content)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()

    def _extract_tags(self, page: CrawledPage) -> List[str]:
        """Extract relevant tags from page content"""
        tags = []
        if 'about' in page.url.lower() or 'about' in page.title.lower():
            tags.append('about')
        if 'service' in page.url.lower() or 'service' in page.title.lower():
            tags.append('services')
        if 'pricing' in page.url.lower() or 'price' in page.title.lower():
            tags.append('pricing')
        if 'contact' in page.url.lower() or 'contact' in page.title.lower():
            tags.append('contact')
        tags.append('auto-generated')
        return tags

    def _generate_content_items(self) -> List[Dict]:
        """Generate Vue.js content items from scraped pages"""
        content_items = []
        for page in self.pages:
            content_items.append({
                "id": f"scraped-{page.id}",
                "type": "website",
                "title": page.title or "Website Page",
                "description": page.description or "Information from our website",
                "url": page.url,
                "tags": self._extract_tags(page),
                "category": self._categorize_page(page),
                "source": "django-scraper",
                "lastUpdated": page.crawled_at.isoformat()
            })
        return content_items

    def _categorize_page(self, page: CrawledPage) -> str:
        """Categorize page content"""
        url_lower = page.url.lower()
        title_lower = page.title.lower() if page.title else ""

        if 'about' in url_lower or 'about' in title_lower:
            return 'company'
        elif 'service' in url_lower or 'service' in title_lower:
            return 'services'
        elif 'pricing' in url_lower or 'price' in title_lower:
            return 'pricing'
        elif 'contact' in url_lower or 'contact' in title_lower:
            return 'contact'
        else:
            return 'general'
```

### **Vue.js Backend Integration Service**
```typescript
// src/services/backendSync.ts
import axios from 'axios'

interface ScrapedData {
  business: BusinessConfig
  knowledgeBase: KnowledgeBaseItem[]
  content: ContentItem[]
}

class BackendSyncService {
  private baseURL = 'http://localhost:8000/scraping'

  async syncBusinessData(businessId: string): Promise<ScrapedData> {
    try {
      // Fetch complete Vue.js configuration from Django
      const response = await axios.get(`${this.baseURL}/${businessId}/export-vue-config/`)

      return {
        business: response.data,
        knowledgeBase: response.data.knowledgeBase || [],
        content: response.data.content || []
      }
    } catch (error) {
      console.error('Failed to sync business data:', error)
      throw error
    }
  }

  async downloadAITrainingData(businessId: string, format: 'jsonl' | 'openai' | 'rag'): Promise<Blob> {
    const response = await axios.get(`${this.baseURL}/${businessId}/export-ai/?format=${format}`, {
      responseType: 'blob'
    })
    return response.data
  }

  async importKnowledgeBase(businessId: string): Promise<KnowledgeBaseItem[]> {
    const response = await axios.get(`${this.baseURL}/${businessId}/export-knowledge/`)
    return response.data.knowledgeBase
  }
}

export default new BackendSyncService()
```

## 📁 **File Organization**

### **Django Backend Structure**
```
chat-backend/
├── scraping/
│   ├── ai_export_service.py        # AI data processing
│   ├── text_processor.py           # Content cleaning & chunking
│   ├── vue_js_exporter.py          # Vue.js format converter
│   ├── views.py                    # Updated with AI export views
│   ├── urls.py                     # New AI export URLs
│   └── templates/scraping/
│       └── ai_export.html          # Export interface
├── requirements.txt                # Add: tiktoken, nltk
└── AI_CHAT_INTEGRATION.md          # This file
```

### **Vue.js Frontend Integration**
```
aichat-17092025/
├── src/
│   ├── services/
│   │   ├── backendSync.ts          # Django integration
│   │   └── dataImporter.ts         # Import scraped data
│   ├── data/
│   │   ├── business.json           # Auto-generated from Django
│   │   └── imported-knowledge.json # Scraped knowledge base
│   └── stores/
│       └── knowledge.ts            # Enhanced with import capability
└── BACKEND_INTEGRATION.md          # Django integration guide
```

## 🚀 **Deployment Workflow**

### **Step 1: Setup Django AI Exports**
```bash
# Add new dependencies
echo "tiktoken==0.5.1" >> requirements.txt
echo "nltk==3.8.1" >> requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run migrations (if any model changes)
python manage.py makemigrations
python manage.py migrate
```

### **Step 2: Configure Vue.js Integration**
```bash
# Add axios for API calls (if not already present)
npm install axios

# Update environment variables
echo "VITE_DJANGO_API_URL=http://localhost:8000" >> .env.local
```

### **Step 3: Test Data Flow**
```bash
# 1. Scrape a business website in Django
# 2. Export AI-ready data
curl "http://localhost:8000/scraping/1/export-vue-config/"

# 3. Import into Vue.js
# 4. Test chat functionality with scraped knowledge
```

## 📋 **API Reference**

### **Django Export Endpoints**

#### **GET `/scraping/{business_id}/export-ai/`**
**Parameters:**
- `format`: `jsonl|openai|knowledge|rag|vue-config`

**Response:** File download with appropriate format

#### **GET `/scraping/{business_id}/export-vue-config/`**
**Response:**
```json
{
  "id": "business-1",
  "name": "Company Name",
  "knowledgeBase": [...],
  "content": [...],
  "settings": {...}
}
```

#### **GET `/scraping/{business_id}/export-jsonl/`**
**Response:** JSONL file
```
{"text": "content", "metadata": {...}}
{"text": "content", "metadata": {...}}
```

#### **GET `/scraping/{business_id}/export-openai/`**
**Response:** OpenAI training format JSONL
```
{"messages": [{"role": "system", "content": "..."}, ...]}
{"messages": [{"role": "system", "content": "..."}, ...]}
```

### **Vue.js Integration Methods**

#### **Manual Import**
```typescript
// Import scraped data manually
import backendSync from '@/services/backendSync'

const businessData = await backendSync.syncBusinessData('business-1')
// Update stores with imported data
```

#### **Automated Sync**
```typescript
// Scheduled import every hour
setInterval(async () => {
  await backendSync.syncBusinessData(currentBusinessId)
}, 3600000)
```

## 🔍 **Testing & Validation**

### **Data Quality Checks**
```python
def validate_export_quality(business_id: int):
    """Validate exported data quality"""
    service = AIExportService(business_id)

    # Check content completeness
    assert len(service.pages) > 0, "No pages to export"

    # Check knowledge base generation
    kb = service.export_vue_knowledge_base()
    assert len(kb['knowledgeBase']) > 0, "No knowledge base items generated"

    # Check content cleaning
    for page in service.pages:
        cleaned = service._clean_content(page.content)
        assert len(cleaned) > 50, f"Content too short after cleaning: {page.url}"
```

### **Integration Tests**
```typescript
// Test Vue.js import functionality
describe('Backend Integration', () => {
  test('imports business configuration', async () => {
    const config = await backendSync.syncBusinessData('test-business')
    expect(config.business.name).toBeTruthy()
    expect(config.knowledgeBase.length).toBeGreaterThan(0)
  })

  test('downloads AI training data', async () => {
    const blob = await backendSync.downloadAITrainingData('test-business', 'jsonl')
    expect(blob.size).toBeGreaterThan(0)
  })
})
```

## 🎯 **Success Metrics**

### **Technical Metrics**
- ✅ **Export Coverage**: 95%+ of scraped content successfully exported
- ✅ **Data Quality**: 90%+ content relevance after processing
- ✅ **Format Compliance**: 100% valid JSONL/JSON output
- ✅ **Integration Success**: Vue.js imports work without errors

### **Business Metrics**
- ✅ **Knowledge Accuracy**: AI responses match website content
- ✅ **Response Quality**: Users get relevant, helpful answers
- ✅ **Automation Level**: Minimal manual configuration required
- ✅ **Update Frequency**: Fresh data synced weekly/daily

## 🚨 **Troubleshooting Guide**

### **Common Issues**

#### **Django Export Fails**
```python
# Check business exists and has scraped pages
business = Business.objects.get(id=business_id)
pages = business.pages.filter(success=True)
print(f"Found {pages.count()} pages to export")
```

#### **Vue.js Import Fails**
```typescript
// Check API connectivity
try {
  const response = await axios.get('/scraping/1/export-vue-config/')
  console.log('API Response:', response.status)
} catch (error) {
  console.error('API Error:', error.response?.data)
}
```

#### **Content Quality Issues**
```python
# Debug content cleaning
original = page.content
cleaned = service._clean_content(original)
print(f"Original: {len(original)} chars")
print(f"Cleaned: {len(cleaned)} chars")
print(f"Cleaned preview: {cleaned[:200]}")
```

### **Performance Optimization**

#### **Large Dataset Handling**
```python
# Process exports in chunks for large businesses
def export_large_dataset(business_id: int, chunk_size: int = 100):
    pages = Business.objects.get(id=business_id).pages.filter(success=True)

    for i in range(0, pages.count(), chunk_size):
        chunk = pages[i:i+chunk_size]
        yield process_chunk(chunk)
```

#### **Caching Strategy**
```python
# Cache processed exports for faster repeated access
from django.core.cache import cache

def get_cached_export(business_id: int, format_type: str):
    cache_key = f"export_{business_id}_{format_type}"
    cached = cache.get(cache_key)

    if not cached:
        service = AIExportService(business_id)
        cached = service.export_by_format(format_type)
        cache.set(cache_key, cached, timeout=3600)  # 1 hour

    return cached
```

## 📚 **Additional Resources**

### **External Documentation**
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [JSONL Format Specification](https://jsonlines.org/)
- [Vue.js + TypeScript Best Practices](https://vuejs.org/guide/typescript/overview.html)
- [Django REST Framework](https://www.django-rest-framework.org/)

### **Related Files**
- `SCRAPING_GUIDE.md` - Web scraping implementation details
- `URL_UPDATE_GUIDE.md` - URL management and validation
- `README.md` - General project overview

### **Future Enhancements**
- [ ] Real-time WebSocket sync between Django and Vue.js
- [ ] AI-powered content quality scoring
- [ ] Multi-language support for scraped content
- [ ] Advanced chunking strategies for better embeddings
- [ ] Integration with vector databases (Pinecone, Weaviate)

---

**Last Updated:** January 2025
**Version:** 1.0
**Maintained By:** Development Team

This document serves as the complete reference for integrating Django web scraping backend with Vue.js AI chat frontend applications.