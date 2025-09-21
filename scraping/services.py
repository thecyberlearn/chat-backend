from firecrawl import Firecrawl
from django.conf import settings
from typing import Dict
import logging
from .scrapers import AdvancedCrawlService

logger = logging.getLogger(__name__)


class CrawlService:
    """Enhanced website crawling service with multiple scraping methods"""

    def __init__(self):
        self.api_key = getattr(settings, 'FIRECRAWL_API_KEY', 'your-firecrawl-api-key-here')
        if self.api_key == 'your-firecrawl-api-key-here':
            logger.warning("Firecrawl API key not configured. Using advanced scraping methods.")
            self.firecrawl = None
        else:
            self.firecrawl = Firecrawl(api_key=self.api_key)

        # Initialize advanced scraper as backup
        self.advanced_scraper = AdvancedCrawlService()

    def crawl_website(self, url: str) -> Dict:
        """
        Crawl an entire website and discover all pages

        Returns:
            {
                'success': bool,
                'pages': [
                    {
                        'url': str,
                        'title': str,
                        'description': str,
                        'content': str
                    }
                ],
                'total_pages': int,
                'error': str (if failed)
            }
        """

        if not self.firecrawl:
            # Use advanced scraper instead of demo
            logger.info(f"Using advanced scraper for {url}")
            return self.advanced_scraper.crawl_website(url, max_pages=10)

        try:
            # Use simple scraping of main URL and common pages
            # This uses fewer API credits than map + scrape

            pages = []

            # Common URLs to try for most websites
            urls_to_try = [
                url,  # Main page
                f"{url.rstrip('/')}/about",
                f"{url.rstrip('/')}/services",
                f"{url.rstrip('/')}/contact",
                f"{url.rstrip('/')}/products"
            ]

            for page_url in urls_to_try:
                try:
                    scrape_result = self.firecrawl.scrape(
                        url=page_url,
                        formats=['markdown']
                    )

                    if scrape_result and scrape_result.data:
                        pages.append({
                            'url': page_url,
                            'title': scrape_result.data.get('metadata', {}).get('title', ''),
                            'description': scrape_result.data.get('metadata', {}).get('description', ''),
                            'content': scrape_result.data.get('markdown', '')
                        })
                except Exception as e:
                    logger.warning(f"Failed to scrape {page_url}: {str(e)}")
                    # Don't break on individual failures
                    continue

            if not pages:
                return {
                    'success': False,
                    'error': 'Failed to scrape any pages from website'
                }

            return {
                'success': True,
                'pages': pages,
                'total_pages': len(pages)
            }

        except Exception as e:
            logger.error(f"Firecrawl error for {url}: {str(e)}")
            # Fallback to advanced scraper
            logger.info(f"Falling back to advanced scraper for {url}")
            return self.advanced_scraper.crawl_website(url, max_pages=10)

    def crawl_with_playwright(self, url: str, max_pages: int = 10) -> Dict:
        """Crawl website using Playwright for JavaScript-heavy sites"""
        logger.info(f"Using Playwright scraper for {url}")
        return self.advanced_scraper.crawl_website(url, max_pages=max_pages, use_playwright=True)

    def crawl_basic(self, url: str, max_pages: int = 10) -> Dict:
        """Crawl website using basic Beautiful Soup scraper"""
        logger.info(f"Using basic scraper for {url}")
        return self.advanced_scraper.crawl_website(url, max_pages=max_pages, use_playwright=False)

    def _extract_name_from_url(self, url: str) -> str:
        """Extract a company name from URL as fallback"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace('www.', '')
        return domain.split('.')[0].replace('-', ' ').title()

    def _demo_crawl_response(self, url: str) -> Dict:
        """Return demo crawl data when API key is not configured"""
        company_name = self._extract_name_from_url(url)
        pages = [
            {
                'url': url,
                'title': f'{company_name} - Innovative Solutions for the Future',
                'description': f'{company_name} is a forward-thinking company providing innovative solutions across multiple industries with cutting-edge technology.',
                'content': f'''# {company_name}

## Welcome to {company_name}

We are a leading technology company dedicated to transforming businesses through innovative solutions. Our comprehensive suite of services helps organizations navigate the digital landscape and achieve sustainable growth.

### What We Do

At {company_name}, we specialize in:

- **Digital Transformation**: Modernizing legacy systems and processes
- **Cloud Solutions**: Scalable infrastructure and platform services
- **AI & Machine Learning**: Intelligent automation and analytics
- **Custom Software Development**: Tailored applications for unique business needs
- **Cybersecurity**: Comprehensive protection for digital assets

### Our Approach

We believe in a collaborative approach that puts our clients at the center of everything we do. Our methodology combines:

1. **Discovery**: Understanding your unique challenges and goals
2. **Strategy**: Developing comprehensive roadmaps for success
3. **Implementation**: Executing solutions with precision and care
4. **Optimization**: Continuous improvement and support

### Industry Leadership

With over 15 years of experience, we have successfully delivered projects for Fortune 500 companies, startups, and everything in between. Our team of expert engineers, designers, and strategists work together to deliver exceptional results.

### Contact Us

Ready to transform your business? Get in touch with our team today to discuss how we can help you achieve your goals.

**Phone**: (555) 123-4567
**Email**: hello@{company_name.lower().replace(' ', '')}.com
**Address**: 123 Innovation Drive, Tech City, TC 12345'''
            },
            {
                'url': f'{url.rstrip("/")}/about',
                'title': f'About {company_name} - Our Story & Mission',
                'description': f'Learn about {company_name}\'s journey, our core values, and the passionate team driving innovation in technology solutions.',
                'content': f'''# About {company_name}

## Our Story

Founded in 2008 by a team of passionate technologists, {company_name} began as a small consulting firm with a big vision: to democratize access to cutting-edge technology solutions. What started as a three-person team working out of a garage has grown into a thriving company with over 200 employees and offices in major cities worldwide.

## Our Mission

To empower businesses of all sizes to harness the full potential of technology, driving innovation and creating lasting value for their customers and communities.

## Our Values

### Innovation First
We continuously push the boundaries of what's possible, investing in research and development to stay ahead of emerging trends.

### Client Success
Your success is our success. We measure our achievements by the positive impact we create for our clients.

### Integrity & Transparency
We build trust through honest communication, ethical practices, and delivering on our promises.

### Collaborative Excellence
We believe the best solutions emerge from diverse perspectives and collaborative teamwork.

## Leadership Team

### Sarah Johnson, CEO & Founder
With 20 years of experience in enterprise technology, Sarah leads our strategic vision and ensures we stay true to our core mission.

### Michael Chen, CTO
A former Google engineer, Michael oversees our technical architecture and drives innovation across all our service lines.

### Elena Rodriguez, VP of Operations
Elena ensures our projects are delivered on time and exceed client expectations through operational excellence.

### David Thompson, VP of Sales
David builds lasting relationships with our clients and helps them identify opportunities for growth through technology.

## Awards & Recognition

- **2023**: Best Technology Consulting Firm - Tech Excellence Awards
- **2022**: Top Workplace Culture - Local Business Journal
- **2021**: Innovation Leader - Industry Innovation Summit
- **2020**: Fastest Growing Tech Company - Regional Business Awards

## Community Impact

We believe in giving back to the communities that support us. Through our {company_name} Foundation, we provide technology education and resources to underserved communities, sponsor local coding bootcamps, and offer pro-bono services to non-profit organizations.'''
            },
            {
                'url': f'{url.rstrip("/")}/services',
                'title': f'{company_name} Services - Comprehensive Technology Solutions',
                'description': f'Explore {company_name}\'s full range of technology services including cloud migration, AI/ML, custom development, and cybersecurity solutions.',
                'content': f'''# Our Services

## Digital Transformation

Transform your business for the digital age with our comprehensive digital transformation services.

### What We Offer:
- **Legacy System Modernization**: Upgrade outdated systems while preserving critical business data
- **Process Automation**: Streamline workflows with intelligent automation solutions
- **Digital Strategy Consulting**: Develop roadmaps for digital success
- **Change Management**: Guide your team through technological transitions

**Starting at $25,000** | **Timeline: 3-6 months**

---

## Cloud Solutions

Migrate to the cloud with confidence using our proven methodologies and expertise.

### Services Include:
- **Cloud Migration**: Seamless transition from on-premises to cloud infrastructure
- **Multi-Cloud Strategy**: Optimize costs and performance across cloud providers
- **DevOps Implementation**: Automate deployment pipelines and improve development velocity
- **Cloud Security**: Implement robust security frameworks for cloud environments

**Popular Packages:**
- Basic Migration: $15,000
- Enterprise Cloud Strategy: $50,000
- Full DevOps Implementation: $75,000

---

## AI & Machine Learning

Harness the power of artificial intelligence to unlock new insights and capabilities.

### Capabilities:
- **Predictive Analytics**: Forecast trends and make data-driven decisions
- **Natural Language Processing**: Build intelligent chatbots and content analysis systems
- **Computer Vision**: Implement image recognition and processing solutions
- **Recommendation Engines**: Personalize user experiences and increase engagement

**Project Examples:**
- Customer Service Chatbot: $30,000
- Predictive Maintenance System: $100,000
- Fraud Detection Platform: $150,000

---

## Custom Software Development

Build tailored applications that perfectly fit your unique business requirements.

### Technologies We Use:
- **Frontend**: React, Vue.js, Angular, Next.js
- **Backend**: Node.js, Python, Java, .NET
- **Mobile**: React Native, Flutter, Native iOS/Android
- **Databases**: PostgreSQL, MongoDB, Redis, Elasticsearch

### Development Process:
1. **Requirements Gathering** (1-2 weeks)
2. **Design & Architecture** (2-3 weeks)
3. **Development Sprints** (8-16 weeks)
4. **Testing & QA** (2-4 weeks)
5. **Deployment & Training** (1-2 weeks)

---

## Cybersecurity

Protect your digital assets with enterprise-grade security solutions.

### Security Services:
- **Security Audits**: Comprehensive assessment of your current security posture
- **Penetration Testing**: Identify vulnerabilities before attackers do
- **Compliance Solutions**: Meet regulatory requirements (SOC 2, HIPAA, GDPR)
- **Incident Response**: 24/7 monitoring and rapid response to security threats

### Security Packages:
- **Startup Security Package**: $10,000/year
- **Enterprise Security Suite**: $50,000/year
- **Custom Security Solutions**: Contact for pricing

---

## Support & Maintenance

Keep your systems running smoothly with our comprehensive support services.

### What's Included:
- **24/7 Monitoring**: Proactive system monitoring and alerting
- **Regular Updates**: Security patches and feature updates
- **Performance Optimization**: Continuous improvement of system performance
- **Technical Support**: Direct access to our expert technical team

**Support Plans:**
- Basic Support: $2,000/month
- Premium Support: $5,000/month
- Enterprise Support: $10,000/month

---

## Ready to Get Started?

Contact our team today to discuss your specific needs and receive a customized proposal.

**Schedule a free consultation**: [Contact Us](#{url.rstrip('/')}/contact)'''
            },
            {
                'url': f'{url.rstrip("/")}/contact',
                'title': f'Contact {company_name} - Get In Touch Today',
                'description': f'Reach out to {company_name} for project inquiries, support, or partnership opportunities. Multiple ways to connect with our expert team.',
                'content': f'''# Contact {company_name}

## Get In Touch

Ready to start your next project or have questions about our services? We'd love to hear from you.

### Office Locations

#### Headquarters - San Francisco
**{company_name} HQ**
123 Innovation Drive
San Francisco, CA 94105
Phone: (415) 555-0123
Email: sf@{company_name.lower().replace(' ', '')}.com

#### East Coast Office - New York
**{company_name} NYC**
456 Tech Avenue, 15th Floor
New York, NY 10001
Phone: (212) 555-0456
Email: nyc@{company_name.lower().replace(' ', '')}.com

#### European Office - London
**{company_name} Europe**
789 Digital Street
London, EC1A 1BB, UK
Phone: +44 20 7555 0789
Email: london@{company_name.lower().replace(' ', '')}.com

### Business Hours

**Monday - Friday**: 9:00 AM - 6:00 PM (Local Time)
**Saturday**: 10:00 AM - 2:00 PM (Emergency Support Only)
**Sunday**: Closed

### Contact Methods

#### For New Projects
**Email**: projects@{company_name.lower().replace(' ', '')}.com
**Phone**: (555) 123-PROJECT
**Response Time**: Within 4 business hours

#### For Existing Clients
**Support Portal**: support.{company_name.lower().replace(' ', '')}.com
**Emergency Hotline**: (555) 911-TECH
**Response Time**: Within 1 hour for critical issues

#### For Partnerships
**Email**: partnerships@{company_name.lower().replace(' ', '')}.com
**Phone**: (555) 123-PARTNER

#### For Media Inquiries
**Email**: media@{company_name.lower().replace(' ', '')}.com
**Contact**: Sarah Johnson, CEO

### Quick Contact Form

**Project Type**:
- [ ] Digital Transformation
- [ ] Cloud Migration
- [ ] AI/ML Development
- [ ] Custom Software
- [ ] Cybersecurity
- [ ] Other

**Timeline**:
- [ ] ASAP (Within 1 month)
- [ ] 1-3 months
- [ ] 3-6 months
- [ ] 6+ months

**Budget Range**:
- [ ] Under $25K
- [ ] $25K - $100K
- [ ] $100K - $500K
- [ ] $500K+

### Follow Us

Stay connected with {company_name} for the latest updates, insights, and industry news.

**LinkedIn**: linkedin.com/company/{company_name.lower().replace(' ', '-')}
**Twitter**: @{company_name.replace(' ', '')}Tech
**GitHub**: github.com/{company_name.lower().replace(' ', '')}
**Blog**: blog.{company_name.lower().replace(' ', '')}.com

### Careers

Interested in joining our team? We're always looking for talented individuals who share our passion for technology and innovation.

**Careers Page**: careers.{company_name.lower().replace(' ', '')}.com
**HR Contact**: hr@{company_name.lower().replace(' ', '')}.com

### Legal & Compliance

**Privacy Policy**: {url.rstrip('/')}/privacy
**Terms of Service**: {url.rstrip('/')}/terms
**Security**: {url.rstrip('/')}/security
'''
            }
        ]

        return {
            'success': True,
            'pages': pages,
            'total_pages': len(pages)
        }