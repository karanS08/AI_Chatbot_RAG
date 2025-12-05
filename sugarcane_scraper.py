#!/usr/bin/env python3
"""
Sugarcane Farming Knowledge Scraper
====================================
Scrapes comprehensive sugarcane farming information from multiple agricultural sources.

Features:
- Scrapes government agriculture websites
- Extracts farming practices, pest control, disease management
- Saves data in organized format (PDF, TXT, JSON)
- Handles rate limiting and retries
- Validates and cleans scraped content

Sources:
- Government agriculture departments (India, USA, Brazil)
- Agricultural research institutions
- Farming advisory websites
- Academic publications (when available)
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SugarcaneScraper:
    """Comprehensive sugarcane farming knowledge scraper"""
    
    def __init__(self, output_dir='knowledge_base/sugarcane'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict] = []
        
        # Rate limiting
        self.request_delay = 2  # seconds between requests
        
    def scrape_all(self):
        """Main method to scrape all sources"""
        logger.info("🌾 Starting comprehensive sugarcane farming knowledge scraping...")
        
        sources = [
            self.scrape_government_sites,
            self.scrape_research_institutions,
            self.scrape_farming_advisory_sites,
            self.scrape_agricultural_universities,
        ]
        
        for scrape_func in sources:
            try:
                logger.info(f"Running: {scrape_func.__name__}")
                scrape_func()
                time.sleep(self.request_delay)
            except Exception as e:
                logger.error(f"Error in {scrape_func.__name__}: {e}")
        
        self.save_all_data()
        logger.info(f"✅ Scraping complete! Total articles: {len(self.scraped_data)}")
    
    def scrape_government_sites(self):
        """Scrape government agriculture department websites"""
        logger.info("📋 Scraping government agriculture sites...")
        
        # Indian Agricultural Research Institute
        urls = [
            "https://icar.org.in/content/sugarcane",
            "https://sugarcane.dac.gov.in/",
        ]
        
        for url in urls:
            try:
                self.scrape_page(url, category="government")
            except Exception as e:
                logger.warning(f"Failed to scrape {url}: {e}")
    
    def scrape_research_institutions(self):
        """Scrape agricultural research institution websites"""
        logger.info("🔬 Scraping research institutions...")
        
        urls = [
            "https://www.icar.org.in/node/3468",  # ICAR Sugarcane
            "https://iisr.icar.gov.in/",  # Indian Institute of Sugarcane Research
        ]
        
        for url in urls:
            try:
                self.scrape_page(url, category="research")
            except Exception as e:
                logger.warning(f"Failed to scrape {url}: {e}")
    
    def scrape_farming_advisory_sites(self):
        """Scrape farming advisory and extension websites"""
        logger.info("👨‍🌾 Scraping farming advisory sites...")
        
        # These are example URLs - many require specific state/region
        urls = [
            "https://farmer.gov.in/",
            "https://agritech.tnau.ac.in/",  # Tamil Nadu Agricultural University
        ]
        
        for url in urls:
            try:
                self.scrape_page(url, category="advisory")
            except Exception as e:
                logger.warning(f"Failed to scrape {url}: {e}")
    
    def scrape_agricultural_universities(self):
        """Scrape agricultural university extension pages"""
        logger.info("🎓 Scraping agricultural universities...")
        
        urls = [
            "https://pau.edu/",  # Punjab Agricultural University
            "https://www.angrau.ac.in/",  # Acharya N.G. Ranga Agricultural University
        ]
        
        for url in urls:
            try:
                self.scrape_page(url, category="university")
            except Exception as e:
                logger.warning(f"Failed to scrape {url}: {e}")
    
    def scrape_page(self, url: str, category: str = "general", max_depth: int = 2):
        """
        Scrape a single page and optionally follow links
        
        Args:
            url: URL to scrape
            category: Category of the content (government, research, etc.)
            max_depth: How many levels deep to follow links
        """
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        logger.info(f"Scraping: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            content = self.extract_content(soup, url)
            
            if content and len(content.strip()) > 200:  # Minimum content length
                data = {
                    'url': url,
                    'title': self.extract_title(soup),
                    'content': content,
                    'category': category,
                    'scraped_at': datetime.now().isoformat(),
                    'word_count': len(content.split())
                }
                self.scraped_data.append(data)
                logger.info(f"✓ Extracted {data['word_count']} words from: {data['title']}")
            
            # Follow relevant links (if depth allows)
            if max_depth > 0:
                relevant_links = self.find_relevant_links(soup, url)
                for link in relevant_links[:5]:  # Limit to 5 links per page
                    time.sleep(self.request_delay)
                    self.scrape_page(link, category, max_depth - 1)
                    
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {url}: {e}")
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try multiple methods
        if soup.title:
            return soup.title.string.strip()
        
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return "Unknown Title"
    
    def extract_content(self, soup: BeautifulSoup, url: str) -> str:
        """
        Extract main content from page, filtering out navigation, ads, etc.
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            element.decompose()
        
        # Try to find main content area
        main_content = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find('div', class_=re.compile('content|main|article', re.I)) or
            soup.find('div', id=re.compile('content|main|article', re.I)) or
            soup.body
        )
        
        if not main_content:
            return ""
        
        # Extract text
        text = main_content.get_text(separator='\n', strip=True)
        
        # Clean up text
        text = self.clean_text(text)
        
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.,;:!?()\-\'\"°%/]', ' ', text)
        
        return text.strip()
    
    def find_relevant_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Find links relevant to sugarcane farming
        """
        relevant_keywords = [
            'sugarcane', 'cane', 'farming', 'cultivation', 'crop', 'pest', 
            'disease', 'fertilizer', 'irrigation', 'variety', 'harvest',
            'management', 'advisory', 'practices', 'guide'
        ]
        
        relevant_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Skip if already visited
            if full_url in self.visited_urls:
                continue
            
            # Check if URL or link text contains relevant keywords
            link_text = link.get_text().lower()
            url_lower = full_url.lower()
            
            if any(keyword in url_lower or keyword in link_text for keyword in relevant_keywords):
                # Only follow links from same domain
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    relevant_links.append(full_url)
        
        return relevant_links
    
    def save_all_data(self):
        """Save scraped data in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_file = self.output_dir / f'scraped_data_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Saved JSON: {json_file}")
        
        # Save as individual text files by category
        for data in self.scraped_data:
            category_dir = self.output_dir / data['category']
            category_dir.mkdir(exist_ok=True)
            
            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', data['title'])[:50]
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            
            txt_file = category_dir / f"{safe_title}_{timestamp}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {data['title']}\n")
                f.write(f"URL: {data['url']}\n")
                f.write(f"Category: {data['category']}\n")
                f.write(f"Scraped: {data['scraped_at']}\n")
                f.write(f"Word Count: {data['word_count']}\n")
                f.write("\n" + "="*80 + "\n\n")
                f.write(data['content'])
        
        # Save summary report
        summary_file = self.output_dir / f'scraping_summary_{timestamp}.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("SUGARCANE FARMING KNOWLEDGE SCRAPING SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total articles scraped: {len(self.scraped_data)}\n")
            f.write(f"Total words collected: {sum(d['word_count'] for d in self.scraped_data)}\n")
            f.write(f"Scraping completed: {datetime.now()}\n\n")
            
            # Category breakdown
            categories = {}
            for data in self.scraped_data:
                cat = data['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            f.write("Articles by category:\n")
            for cat, count in sorted(categories.items()):
                f.write(f"  {cat}: {count}\n")
            
            f.write("\n" + "=" * 80 + "\n\n")
            f.write("Scraped URLs:\n")
            for data in self.scraped_data:
                f.write(f"  - {data['title']} ({data['url']})\n")
        
        logger.info(f"📊 Saved summary: {summary_file}")


def main():
    """Main entry point"""
    print("=" * 80)
    print("🌾 SUGARCANE FARMING KNOWLEDGE SCRAPER")
    print("=" * 80)
    print("\nThis scraper will collect comprehensive information about:")
    print("  • Sugarcane cultivation practices")
    print("  • Pest and disease management")
    print("  • Fertilizer and irrigation schedules")
    print("  • Variety information")
    print("  • Harvesting and post-harvest practices")
    print("  • Government schemes and advisories")
    print("\n⚠️  Note: Please respect robots.txt and terms of service")
    print("=" * 80 + "\n")
    
    # Confirm to proceed
    response = input("Proceed with scraping? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Scraping cancelled.")
        return
    
    scraper = SugarcaneScraper()
    scraper.scrape_all()
    
    print("\n" + "=" * 80)
    print("✅ SCRAPING COMPLETED!")
    print("=" * 80)
    print(f"\nData saved to: {scraper.output_dir}")
    print(f"Total articles: {len(scraper.scraped_data)}")
    print(f"Total words: {sum(d['word_count'] for d in scraper.scraped_data)}")
    print("\nNext steps:")
    print("  1. Review the scraped content in knowledge_base/sugarcane/")
    print("  2. Upload the files to the chatbot using /upload endpoint")
    print("  3. Test the chatbot with sugarcane-related questions")


if __name__ == "__main__":
    main()
