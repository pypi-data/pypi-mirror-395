"""
Language Processor Module
معالج اللغة الطبيعية للعربية والإنجليزية
"""

import re
import logging
from typing import List, Dict, Tuple, Optional
from langdetect import detect, DetectorFactory
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# تحميل البيانات اللازمة
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

logger = logging.getLogger(__name__)
DetectorFactory.seed = 0


class LanguageProcessor:
    """
    معالج اللغة الطبيعية
    يقوم بمعالجة النصوص العربية والإنجليزية
    """

    def __init__(self):
        """تهيئة معالج اللغة"""
        self.arabic_stopwords = set(stopwords.words('arabic'))
        self.english_stopwords = set(stopwords.words('english'))
        self.supported_languages = ['ar', 'en']

    def detect_language(self, text: str) -> str:
        """
        كشف لغة النص
        
        Args:
            text: النص المراد كشف لغته
            
        Returns:
            رمز اللغة (ar/en)
        """
        try:
            lang = detect(text)
            return lang if lang in self.supported_languages else 'en'
        except Exception as e:
            logger.warning(f"Language detection error: {e}, defaulting to 'en'")
            return 'en'

    def tokenize_sentences(self, text: str, language: str = None) -> List[str]:
        """
        تقسيم النص إلى جمل
        
        Args:
            text: النص المراد تقسيمه
            language: اللغة (إذا لم تُحدد سيتم كشفها)
            
        Returns:
            قائمة الجمل
        """
        if not language:
            language = self.detect_language(text)
        
        try:
            if language == 'ar':
                # تقسيم بناءً على علامات الترقيم العربية
                sentences = re.split(r'[.!?؟!،؛]', text)
            else:
                sentences = sent_tokenize(text)
            
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            logger.error(f"Tokenization error: {e}")
            return [text]

    def tokenize_words(self, text: str, language: str = None, 
                      remove_stopwords: bool = False) -> List[str]:
        """
        تقسيم النص إلى كلمات
        
        Args:
            text: النص المراد تقسيمه
            language: اللغة
            remove_stopwords: إزالة الكلمات الشائعة
            
        Returns:
            قائمة الكلمات
        """
        if not language:
            language = self.detect_language(text)
        
        try:
            # تنظيف النص
            text = self.clean_text(text)
            
            if language == 'ar':
                # تقسيم بسيط للعربية
                words = text.split()
            else:
                words = word_tokenize(text.lower())
            
            # إزالة الكلمات الشائعة إذا لزم الأمر
            if remove_stopwords:
                stopwords_set = self.arabic_stopwords if language == 'ar' else self.english_stopwords
                words = [w for w in words if w not in stopwords_set]
            
            return words
        except Exception as e:
            logger.error(f"Word tokenization error: {e}")
            return text.split()

    def clean_text(self, text: str) -> str:
        """
        تنظيف النص من الأحرف الخاصة والمسافات الزائدة
        
        Args:
            text: النص المراد تنظيفه
            
        Returns:
            النص المنظف
        """
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text)
        
        # إزالة الأحرف الخاصة (مع الحفاظ على علامات الترقيم الأساسية)
        text = re.sub(r'[^\w\s.!?؟!،؛،-]', '', text, flags=re.UNICODE)
        
        return text.strip()

    def normalize_text(self, text: str, language: str = None) -> str:
        """
        تطبيع النص
        
        Args:
            text: النص المراد تطبيعه
            language: اللغة
            
        Returns:
            النص المطبع
        """
        if not language:
            language = self.detect_language(text)
        
        if language == 'ar':
            # تطبيع الأحرف العربية
            text = text.replace('أ', 'ا')
            text = text.replace('إ', 'ا')
            text = text.replace('آ', 'ا')
            text = text.replace('ة', 'ه')
        
        return text

    def extract_keywords(self, text: str, language: str = None, 
                        top_n: int = 10) -> List[Tuple[str, float]]:
        """
        استخراج الكلمات المفتاحية من النص
        
        Args:
            text: النص المراد استخراج الكلمات منه
            language: اللغة
            top_n: عدد الكلمات المفتاحية المطلوبة
            
        Returns:
            قائمة الكلمات المفتاحية مع درجاتها
        """
        if not language:
            language = self.detect_language(text)
        
        # استخراج الكلمات
        words = self.tokenize_words(text, language, remove_stopwords=True)
        
        # حساب التكرار
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # ترتيب حسب التكرار
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # تطبيع الدرجات
        max_freq = max([freq for _, freq in sorted_words]) if sorted_words else 1
        keywords = [(word, freq / max_freq) for word, freq in sorted_words[:top_n]]
        
        return keywords

    def extract_entities(self, text: str, language: str = None) -> Dict[str, List[str]]:
        """
        استخراج الكيانات المسماة (الأشخاص، الأماكن، إلخ)
        
        Args:
            text: النص المراد استخراج الكيانات منه
            language: اللغة
            
        Returns:
            قاموس الكيانات حسب النوع
        """
        if not language:
            language = self.detect_language(text)
        
        entities = {
            'persons': [],
            'locations': [],
            'organizations': [],
            'numbers': [],
            'dates': []
        }
        
        # استخراج الأرقام
        numbers = re.findall(r'\d+(?:[.,]\d+)?', text)
        entities['numbers'] = numbers
        
        # استخراج التواريخ
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # DD/MM/YYYY
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',    # YYYY/MM/DD
        ]
        for pattern in date_patterns:
            dates = re.findall(pattern, text)
            entities['dates'].extend(dates)
        
        return entities

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        حساب التشابه بين نصين
        
        Args:
            text1: النص الأول
            text2: النص الثاني
            
        Returns:
            درجة التشابه (0-1)
        """
        # استخراج الكلمات من كلا النصين
        words1 = set(self.tokenize_words(text1, remove_stopwords=True))
        words2 = set(self.tokenize_words(text2, remove_stopwords=True))
        
        if not words1 or not words2:
            return 0.0
        
        # حساب التقاطع والاتحاد
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        # معامل جاكارد
        similarity = intersection / union if union > 0 else 0.0
        
        return similarity

    def get_text_statistics(self, text: str, language: str = None) -> Dict:
        """
        الحصول على إحصائيات النص
        
        Args:
            text: النص المراد تحليله
            language: اللغة
            
        Returns:
            قاموس الإحصائيات
        """
        if not language:
            language = self.detect_language(text)
        
        sentences = self.tokenize_sentences(text, language)
        words = self.tokenize_words(text, language)
        
        return {
            'language': language,
            'character_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(words)),
            'vocabulary_richness': len(set(words)) / len(words) if words else 0
        }
