"""
Web Search Module
نظام البحث الذكي على الإنترنت
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


class WebSearch:
    """
    محرك البحث الذكي
    يقوم بالبحث على الإنترنت واستخراج المعلومات ذات الصلة
    """

    def __init__(self, timeout: int = 10, max_results: int = 10):
        """
        تهيئة محرك البحث
        
        Args:
            timeout: مهلة الانتظار بالثواني
            max_results: عدد النتائج الأقصى
        """
        self.timeout = timeout
        self.max_results = max_results
        self.ddgs = DDGS()

    def search(self, query: str, language: str = "ar", 
               max_results: int = None) -> List[Dict]:
        """
        البحث على الإنترنت
        
        Args:
            query: استعلام البحث
            language: لغة البحث
            max_results: عدد النتائج
            
        Returns:
            قائمة النتائج
        """
        if not max_results:
            max_results = self.max_results
        
        try:
            results = []
            
            # البحث باستخدام DuckDuckGo
            search_results = self.ddgs.text(
                query,
                max_results=max_results,
                timelimit=None
            )
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': 'duckduckgo',
                    'timestamp': datetime.now().isoformat()
                })
            
            logger.info(f"Search completed: {query} - Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def search_academic(self, query: str, max_results: int = None) -> List[Dict]:
        """
        البحث عن المراجع الأكاديمية
        
        Args:
            query: استعلام البحث
            max_results: عدد النتائج
            
        Returns:
            قائمة النتائج الأكاديمية
        """
        if not max_results:
            max_results = self.max_results
        
        try:
            # إضافة كلمات مفتاحية أكاديمية
            academic_query = f"{query} site:scholar.google.com OR site:arxiv.org OR site:researchgate.net"
            
            results = self.search(academic_query, max_results=max_results)
            
            logger.info(f"Academic search completed: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Academic search error: {e}")
            return []

    def extract_content(self, url: str) -> Optional[str]:
        """
        استخراج محتوى صفحة ويب
        
        Args:
            url: عنوان الصفحة
            
        Returns:
            محتوى الصفحة
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # إزالة السكريبتات والأنماط
            for script in soup(['script', 'style']):
                script.decompose()
            
            # استخراج النص
            text = soup.get_text()
            
            # تنظيف النص
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            logger.info(f"Content extracted from: {url}")
            return text[:5000]  # الحد الأقصى 5000 حرف
            
        except Exception as e:
            logger.error(f"Content extraction error: {e}")
            return None

    def search_and_summarize(self, query: str, language: str = "ar") -> Dict:
        """
        البحث وتلخيص النتائج
        
        Args:
            query: استعلام البحث
            language: اللغة
            
        Returns:
            قاموس يحتوي على النتائج والملخص
        """
        try:
            # البحث
            results = self.search(query, language)
            
            if not results:
                return {
                    'query': query,
                    'results': [],
                    'summary': 'لم يتم العثور على نتائج' if language == 'ar' else 'No results found',
                    'timestamp': datetime.now().isoformat()
                }
            
            # استخراج المحتوى من أفضل النتائج
            top_content = []
            for result in results[:3]:
                content = self.extract_content(result['url'])
                if content:
                    top_content.append({
                        'title': result['title'],
                        'content': content[:1000],
                        'url': result['url']
                    })
            
            # بناء ملخص
            summary = self._build_summary(query, top_content, language)
            
            return {
                'query': query,
                'results': results,
                'top_content': top_content,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Search and summarize error: {e}")
            return {
                'query': query,
                'results': [],
                'summary': 'حدث خطأ في البحث' if language == 'ar' else 'Search error occurred',
                'error': str(e)
            }

    def _build_summary(self, query: str, content_list: List[Dict], 
                      language: str = "ar") -> str:
        """
        بناء ملخص من المحتوى
        
        Args:
            query: الاستعلام الأصلي
            content_list: قائمة المحتوى
            language: اللغة
            
        Returns:
            الملخص
        """
        if not content_list:
            return 'لم يتم العثور على معلومات' if language == 'ar' else 'No information found'
        
        if language == 'ar':
            summary = f"نتائج البحث عن '{query}':\n\n"
        else:
            summary = f"Search results for '{query}':\n\n"
        
        for i, item in enumerate(content_list, 1):
            summary += f"{i}. {item['title']}\n"
            summary += f"   {item['content'][:200]}...\n"
            summary += f"   المصدر: {item['url']}\n\n"
        
        return summary

    def search_images(self, query: str, max_results: int = None) -> List[Dict]:
        """
        البحث عن الصور
        
        Args:
            query: استعلام البحث
            max_results: عدد النتائج
            
        Returns:
            قائمة نتائج الصور
        """
        if not max_results:
            max_results = self.max_results
        
        try:
            results = []
            
            # البحث عن الصور باستخدام DuckDuckGo
            image_results = self.ddgs.images(
                query,
                max_results=max_results
            )
            
            for result in image_results:
                results.append({
                    'title': result.get('title', ''),
                    'image_url': result.get('image', ''),
                    'source_url': result.get('url', ''),
                    'source': 'duckduckgo',
                    'timestamp': datetime.now().isoformat()
                })
            
            logger.info(f"Image search completed: {query} - Found {len(results)} images")
            return results
            
        except Exception as e:
            logger.error(f"Image search error: {e}")
            return []

    def search_news(self, query: str, max_results: int = None) -> List[Dict]:
        """
        البحث عن الأخبار
        
        Args:
            query: استعلام البحث
            max_results: عدد النتائج
            
        Returns:
            قائمة نتائج الأخبار
        """
        if not max_results:
            max_results = self.max_results
        
        try:
            results = []
            
            # البحث عن الأخبار
            news_results = self.ddgs.news(
                query,
                max_results=max_results
            )
            
            for result in news_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'source': result.get('source', ''),
                    'date': result.get('date', ''),
                    'body': result.get('body', ''),
                    'timestamp': datetime.now().isoformat()
                })
            
            logger.info(f"News search completed: {query} - Found {len(results)} news")
            return results
            
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []
