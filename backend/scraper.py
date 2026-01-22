"""
Web scraper module for monitoring news websites
Scrapes multiple telecom industry websites and detects new articles
"""
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import List, Dict, Set
import hashlib

class NewsScraperConfig:
    """Configuration for news websites to monitor"""

    # List of websites to monitor: [name, url, category]
    WEBSITES = [
        ["Ericsson Customer Cases", "https://www.ericsson.com/en/cases", "case_study"],
        ["Ericsson News", "https://www.ericsson.com/en/news", "news"],
        ["Ericsson Blog", "https://www.ericsson.com/en/blog", "blog"],
        ["Nokia Case Studies", "https://www.nokia.com/case-studies/", "case_study"],
        ["Nokia Newsroom", "https://www.nokia.com/about-us/newsroom/", "news"],
        ["Nokia Blog", "https://www.nokia.com/blog/", "blog"],
        ["Huawei Case Studies", "https://e.huawei.com/en/case-studies", "case_study"],
        ["Huawei News", "https://e.huawei.com/en/news", "news"],
        ["Huawei Blogs", "https://e.huawei.com/en/blogs", "blog"],
        ["Cisco Case Studies", "https://www.cisco.com/site/us/en/about/case-studies-customer-stories/index.html", "case_study"],
        ["Cisco Newsroom", "https://newsroom.cisco.com/", "news"],
        ["Cisco Blogs", "https://blogs.cisco.com/", "blog"],
        ["Samsung Insights", "https://www.samsung.com/in/business/insights/", "case_study"],
        ["Samsung News", "https://www.samsung.com/global/business/networks/insights/?press-release", "news"],
        ["Samsung Blog", "https://www.samsung.com/global/business/networks/insights/?blog", "blog"],
        ["ZTE News", "https://www.zte.com.cn/global/about/news.html", "news"],
        ["Motorola Newsroom", "https://www.motorolasolutions.com/newsroom.html", "news"],
        ["Motorola Blog", "https://blog.motorolasolutions.com/", "blog"],
        ["Ciena Case Studies", "https://www.ciena.com/insights/list?type=case-studies", "case_study"],
        ["Ciena Newsroom", "https://www.ciena.com/about/newsroom", "news"],
        ["Ciena Articles", "https://www.ciena.com/insights/list?type=articles", "blog"],
        ["CommScope Case Studies", "https://www.commscope.com/resources/case-studies/", "case_study"],
        ["CommScope News", "https://www.commscope.com/news-center/", "news"],
        ["CommScope News Center", "https://www.commscope.com/news-center/", "blog"],
        ["Juniper Customers", "https://www.juniper.net/us/en/customers.html", "case_study"],
        ["HPE Newsroom", "https://www.hpe.com/us/en/newsroom.html", "news"],
        ["ADTRAN Press Releases", "https://www.adtran.com/en/newsroom/press-releases", "news"],
        ["ADTRAN Blog", "https://www.blog.adtran.com/en", "blog"],
        ["Lumentum Media", "https://www.lumentum.com/en/newsroom/media-resources", "news"],
        ["Lumentum Newsroom", "https://www.lumentum.com/en/newsroom", "news"],
        ["Lumentum Blog", "https://www.lumentum.com/en/blog", "blog"],
        ["Extreme Networks Newsroom", "https://www.extremenetworks.com/about-extreme-networks/company/newsroom", "news"],
        ["Extreme Networks Blogs", "https://www.extremenetworks.com/resources/blogs", "blog"],
        ["Viavi News Releases", "https://www.viavisolutions.com/en-us/corporate/news-and-events/news-releases", "news"],
        ["Viavi Blog", "https://blog.viavisolutions.com/", "blog"],
        ["NETGEAR Case Studies", "https://www.netgear.com/hub/business/case-studies/", "case_study"],
        ["NETGEAR Pressroom", "https://www.netgear.com/hub/pressroom/", "news"],
        ["NETGEAR Hub", "https://www.netgear.com/hub/", "blog"],
        ["Ubiquiti Case Studies", "https://casestudies.ui.com/?s=in", "case_study"],
        ["Ubiquiti Blog", "https://blog.ui.com/?s=in", "blog"],
        ["Tejas Networks Press", "https://www.tejasnetworks.com/press-release/", "news"],
        ["Fujitsu Insights", "https://global.fujitsu/en-global/insight", "news"],
        ["Fujitsu Insights Blog", "https://global.fujitsu/en-global/insight", "blog"],
        ["Radisys White Papers", "https://hub.radisys.com/white-papers", "case_study"],
        ["Radisys In The News", "https://hub.radisys.com/inthenews", "news"],
        ["Radisys Blog", "https://hub.radisys.com/blog", "blog"],
        ["ALE Customers", "https://www.al-enterprise.com/en/company/customers", "case_study"],
        ["ALE News", "https://www.al-enterprise.com/en/company/news", "news"],
        ["ALE Blog", "https://www.al-enterprise.com/en/blog", "blog"],
        ["HFCL Insights", "https://www.hfcl.com/insights", "case_study"],
        ["HFCL News", "https://www.hfcl.com/news", "news"],
        ["HFCL Blog", "https://www.hfcl.com/blog/", "blog"],
        ["STL Case Study", "https://stl.tech/case-study/", "case_study"],
        ["STL Newsroom", "https://stl.tech/newsroom/", "news"],
        ["STL Blog", "https://stl.tech/blog/", "blog"],
        ["Aksh Optifibre News", "https://akshoptifibre.com/Newspaper-add.php", "news"],
        ["Matrix Case Studies", "https://www.matrixcomsec.com/resources/case-studies/", "case_study"],
        ["Matrix Blogs", "https://www.matrixcomsec.com/blogs/", "blog"],
        ["Paramount Cables News", "https://paramountcables.com/news-media/#news-sec", "news"],
        ["Paramount Cables Blog", "https://paramountcables.com/blog-posts/", "blog"],
        ["Comba Case Study", "https://www.comba-telecom.com/en/case-study", "case_study"],
        ["Comba News", "https://www.comba-telecom.com/en/news", "news"],
        ["Comba Blogs", "https://www.comba-telecom.com/en/blogs#1", "blog"],
        ["Unistar Home", "https://unistar.co.in/index.aspx#", "news"],
        ["Unistar Blog", "https://unistar.co.in/blog.aspx", "blog"],
        ["Vanu News", "https://www.vanu.com/category/news/", "news"],
        ["Vanu Insights", "https://www.vanu.com/category/insights/", "blog"],
        ["Polycab News & Media", "https://polycab.com/news-and-media#media", "news"],
        ["Lava Press & Media", "https://www.lavamobiles.com/press-and-media", "news"],
        ["ITI Press Releases", "https://itiltd.in/press_release.php?lan=en", "news"],
    ]

class NewsScraper:
    """Main scraper class for monitoring news websites"""

    def __init__(self, cache_file: str = 'data/scraper_cache.json'):
        """Initialize scraper with cache file path"""
        self.cache_file = cache_file
        self.websites = NewsScraperConfig.WEBSITES
        self.cache = self.load_cache()

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)

        # User agent to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def load_cache(self) -> Dict:
        """Load previously scraped articles from cache"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {str(e)}")
                return {}
        return {}

    def save_cache(self):
        """Save current cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {str(e)}")

    def generate_article_id(self, title: str, url: str) -> str:
        """Generate unique ID for article based on title and URL"""
        content = f"{title}{url}".encode('utf-8')
        return hashlib.md5(content).hexdigest()

    def scrape_website(self, name: str, url: str, category: str) -> List[Dict]:
        """
        Scrape a single website for articles
        Returns list of articles with title, link, and metadata
        """
        articles = []

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Generic scraping logic - looks for common article patterns
            # Try multiple selectors to catch different site structures

            # Find all links that might be articles
            potential_articles = []

            # Strategy 1: Find article tags
            potential_articles.extend(soup.find_all('article'))

            # Strategy 2: Find divs/sections with article-like classes
            for selector in ['.article', '.post', '.news-item', '.case-study', '.blog-post',
                           '[class*="article"]', '[class*="post"]', '[class*="news"]',
                           '[class*="case"]', '[class*="blog"]']:
                potential_articles.extend(soup.select(selector))

            # Strategy 3: Find all links with meaningful text
            all_links = soup.find_all('a', href=True)

            seen_urls = set()

            for element in potential_articles[:10]:  # Limit to first 10 to avoid noise
                # Try to find title and link within the element
                link_tag = element.find('a', href=True) if element.name != 'a' else element

                if link_tag and link_tag.get('href'):
                    title_text = None

                    # Try to get title from various elements
                    for tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
                        title_elem = element.find(tag)
                        if title_elem:
                            title_text = title_elem.get_text(strip=True)
                            break

                    # Fallback to link text
                    if not title_text:
                        title_text = link_tag.get_text(strip=True)

                    # Get full URL
                    article_url = link_tag['href']
                    if not article_url.startswith('http'):
                        from urllib.parse import urljoin
                        article_url = urljoin(url, article_url)

                    # Avoid duplicates and empty titles
                    if title_text and len(title_text) > 10 and article_url not in seen_urls:
                        articles.append({
                            'title': title_text[:200],  # Limit title length
                            'url': article_url,
                            'source': name,
                            'category': category,
                            'scraped_at': datetime.now().isoformat()
                        })
                        seen_urls.add(article_url)

            # Fallback: If no articles found, try getting recent links
            if len(articles) == 0:
                for link in all_links[:20]:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')

                    # Filter out navigation, footer, and other non-article links
                    skip_keywords = ['login', 'signup', 'contact', 'about', 'privacy', 
                                   'terms', 'cookie', 'careers', 'home', 'menu']

                    if (title and len(title) > 15 and href and 
                        not any(kw in href.lower() for kw in skip_keywords)):

                        if not href.startswith('http'):
                            from urllib.parse import urljoin
                            href = urljoin(url, href)

                        if href not in seen_urls:
                            articles.append({
                                'title': title[:200],
                                'url': href,
                                'source': name,
                                'category': category,
                                'scraped_at': datetime.now().isoformat()
                            })
                            seen_urls.add(href)

                        if len(articles) >= 5:
                            break

        except requests.RequestException as e:
            print(f"Error scraping {name}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error scraping {name}: {str(e)}")

        return articles

    def scrape_all(self) -> List[Dict]:
        """
        Scrape all configured websites
        Returns list of NEW articles found
        """
        all_new_articles = []

        print(f"\n🔍 Starting scrape of {len(self.websites)} websites...")

        for name, url, category in self.websites:
            print(f"  Scraping: {name}...")
            articles = self.scrape_website(name, url, category)

            # Check for new articles
            for article in articles:
                article_id = self.generate_article_id(article['title'], article['url'])

                # If article ID not in cache, it's new
                if article_id not in self.cache:
                    article['id'] = article_id
                    all_new_articles.append(article)
                    self.cache[article_id] = article

        # Save updated cache
        if all_new_articles:
            self.save_cache()
            print(f"\n✅ Found {len(all_new_articles)} new articles!")
        else:
            print(f"\nℹ️  No new articles found.")

        return all_new_articles

    def get_cache_stats(self) -> Dict:
        """Get statistics about cached articles"""
        return {
            'total_articles': len(self.cache),
            'last_updated': datetime.now().isoformat()
        }
