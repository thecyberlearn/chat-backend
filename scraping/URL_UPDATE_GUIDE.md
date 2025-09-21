# URL Update & Management Guide

## 🔄 **URL Update Functionality**

Your Django application now has comprehensive URL update and management features for handling wrong URLs or URL changes.

## ✅ **Features Implemented**

### **1. URL Validation**
- ✅ **Format validation** - Ensures URL has proper http/https scheme
- ✅ **Accessibility testing** - Checks if URL is actually reachable
- ✅ **Real-time validation** - Tests URL before saving to database

### **2. Multiple Update Methods**
- ✅ **Full business edit** - Update URL along with other business details
- ✅ **Quick URL update** - Update only the URL via modal/API
- ✅ **Validation feedback** - Clear error messages for invalid URLs

### **3. Smart Re-crawling**
- ✅ **Optional re-crawl** - Choose whether to re-scrape after URL change
- ✅ **Page comparison** - Shows old vs new page counts
- ✅ **Status tracking** - Real-time crawling status updates

## 🛠️ **How to Update URLs**

### **Method 1: Full Business Edit**
1. Go to business detail page
2. Click **"Edit Business"** button
3. Change the website URL
4. Optionally check **"Re-crawl website if URL changes"**
5. Click **"Update Business"**

### **Method 2: Quick URL Update**
1. On edit page, click **"Update URL Only"**
2. Enter new URL in modal
3. Click **"Update URL"**
4. System validates and updates immediately

### **Method 3: API Update**
```javascript
fetch('/scraping/{business_id}/update-url/', {
    method: 'POST',
    body: new FormData([['website_url', 'https://newdomain.com']]),
    headers: {'X-CSRFToken': csrfToken}
})
```

## 🔍 **Validation Process**

When you update a URL, the system:

1. **Format Check** - Validates URL format (must have http/https)
2. **Accessibility Test** - Sends HTTP HEAD request to verify URL is reachable
3. **Status Code Check** - Ensures server responds with 200-399 status
4. **Database Update** - Only saves if all validations pass
5. **Rollback Protection** - Reverts to old URL if any step fails

## 📱 **User Interface Features**

### **Business Detail Page**
- ✅ **Edit Business** button in header
- ✅ **Re-crawl** button (if pages exist)
- ✅ **Export Data** button for current data

### **Edit Business Page**
- ✅ **Current info sidebar** - Shows existing values
- ✅ **URL validation** - Real-time feedback
- ✅ **Re-crawl checkbox** - Automatic re-crawl option
- ✅ **Quick actions** - Test URL, Update URL only, Re-crawl now

### **URL Update Modal**
- ✅ **Focused URL editing** - Quick URL-only changes
- ✅ **Validation feedback** - Shows success/error messages
- ✅ **Auto-refresh** - Updates main form after successful change

## 🚨 **Error Handling**

### **Common Error Scenarios**

1. **Invalid URL Format**
   ```
   Error: Please enter a valid URL with http:// or https://
   ```

2. **Unreachable URL**
   ```
   Error: Cannot access URL: Connection timeout
   ```

3. **Server Error**
   ```
   Error: URL returned status code 404. Please check if the website is accessible.
   ```

4. **Network Issues**
   ```
   Error: Network error: DNS resolution failed
   ```

### **Error Recovery**
- Original URL is preserved if update fails
- Clear error messages guide user to fix issues
- Option to test URL accessibility before updating

## 🔄 **Re-crawling After URL Update**

### **Automatic Re-crawl**
When updating URL with re-crawl option:
1. URL is validated and updated
2. Old scraped pages are deleted
3. New crawling begins automatically
4. Page count comparison is shown

### **Manual Re-crawl**
Click **"Re-crawl Now"** to:
1. Delete all existing pages
2. Scrape the current URL
3. Show before/after page counts
4. Update business status

### **Re-crawl Results**
```json
{
    "success": true,
    "message": "Re-crawled successfully! Found 15 pages (previously 8)",
    "total_pages": 15,
    "old_page_count": 8
}
```

## 🎯 **API Endpoints**

### **Update Business URL**
```
POST /scraping/{business_id}/update-url/
Content-Type: application/x-www-form-urlencoded

website_url=https://newdomain.com
```

**Response:**
```json
{
    "success": true,
    "message": "Website URL updated from https://old.com to https://new.com",
    "old_url": "https://old.com",
    "new_url": "https://new.com",
    "business_id": 123
}
```

### **Re-crawl Business**
```
POST /scraping/{business_id}/recrawl/
X-CSRFToken: {token}
```

**Response:**
```json
{
    "success": true,
    "message": "Re-crawled successfully! Found 12 pages (previously 5)",
    "total_pages": 12,
    "old_page_count": 5
}
```

### **Edit Business (Full)**
```
GET/POST /scraping/{business_id}/edit/
```

## 🛡️ **Security & Validation**

### **Built-in Protections**
- ✅ **CSRF Protection** - All forms include CSRF tokens
- ✅ **URL Validation** - Prevents malicious URL injection
- ✅ **Access Control** - Only authorized users can edit
- ✅ **Data Rollback** - Failed updates don't corrupt data

### **Validation Rules**
```python
# URL must have proper scheme
if not parsed.scheme or not parsed.netloc:
    raise ValidationError('Invalid URL format')

# Only allow HTTP/HTTPS
if parsed.scheme not in ['http', 'https']:
    raise ValidationError('URL must start with http:// or https://')

# Test accessibility
response = requests.head(url, timeout=10)
if response.status_code >= 400:
    raise ValidationError('URL not accessible')
```

## 📊 **Usage Examples**

### **Scenario 1: Company Changed Domain**
```
Old: https://oldcompany.com
New: https://newcompany.com

1. Go to Edit Business
2. Update URL to https://newcompany.com
3. Check "Re-crawl website if URL changes"
4. Click Update Business
→ Result: URL updated, 15 new pages scraped
```

### **Scenario 2: Wrong URL Entered Initially**
```
Wrong: https://exampl.com (typo)
Correct: https://example.com

1. Click "Update URL Only" in sidebar
2. Enter https://example.com
3. Click Update URL
→ Result: URL corrected, ready to re-crawl
```

### **Scenario 3: Website Structure Changed**
```
Same URL, but site was redesigned

1. Click "Re-crawl Now" button
2. Confirm deletion of old pages
3. Wait for re-crawling to complete
→ Result: Fresh content from redesigned site
```

## 🚀 **Best Practices**

1. **Always test URLs** before updating in production
2. **Backup data** before major URL changes
3. **Use re-crawl option** when URL structure changes significantly
4. **Monitor crawling status** to ensure completion
5. **Export data** before making changes as backup

---

Your URL update system is now **production-ready** with comprehensive validation, error handling, and user-friendly interfaces! 🎉