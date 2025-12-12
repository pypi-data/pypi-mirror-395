"""
Chat Engine Module
محرك المحادثة الذكي
"""

import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from almufti.core.language_processor import LanguageProcessor
from almufti.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class ChatEngine:
    """
    محرك المحادثة الذكي
    يدير المحادثات والحوارات مع المستخدم
    """

    def __init__(self, db_manager: DatabaseManager = None, language: str = "ar"):
        """
        تهيئة محرك المحادثة
        
        Args:
            db_manager: مدير قاعدة البيانات
            language: اللغة الافتراضية
        """
        self.db_manager = db_manager or DatabaseManager()
        self.language_processor = LanguageProcessor()
        self.default_language = language
        self.current_conversation_id = None
        self.context_window = []
        self.max_context_size = 10  # عدد الرسائل السابقة المحفوظة

    def start_conversation(self, title: str = None, language: str = None) -> int:
        """
        بدء محادثة جديدة
        
        Args:
            title: عنوان المحادثة
            language: لغة المحادثة
            
        Returns:
            معرف المحادثة
        """
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if not language:
            language = self.default_language
        
        self.current_conversation_id = self.db_manager.save_conversation(title, language)
        self.context_window = []
        logger.info(f"Started new conversation: {self.current_conversation_id}")
        
        return self.current_conversation_id

    def add_user_message(self, message: str) -> int:
        """
        إضافة رسالة من المستخدم
        
        Args:
            message: محتوى الرسالة
            
        Returns:
            معرف الرسالة
        """
        if not self.current_conversation_id:
            self.start_conversation()
        
        message_id = self.db_manager.add_message(
            self.current_conversation_id,
            "user",
            message
        )
        
        # إضافة إلى السياق
        self._update_context("user", message)
        
        logger.info(f"Added user message: {message_id}")
        return message_id

    def add_assistant_message(self, message: str) -> int:
        """
        إضافة رسالة من المساعد
        
        Args:
            message: محتوى الرسالة
            
        Returns:
            معرف الرسالة
        """
        if not self.current_conversation_id:
            self.start_conversation()
        
        message_id = self.db_manager.add_message(
            self.current_conversation_id,
            "assistant",
            message
        )
        
        # إضافة إلى السياق
        self._update_context("assistant", message)
        
        logger.info(f"Added assistant message: {message_id}")
        return message_id

    def _update_context(self, role: str, message: str):
        """
        تحديث نافذة السياق
        
        Args:
            role: دور المرسل
            message: محتوى الرسالة
        """
        self.context_window.append({
            "role": role,
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # الحفاظ على حجم السياق
        if len(self.context_window) > self.max_context_size * 2:
            self.context_window = self.context_window[-self.max_context_size * 2:]

    def get_context(self) -> List[Dict]:
        """
        الحصول على السياق الحالي
        
        Returns:
            قائمة الرسائل في السياق
        """
        return self.context_window.copy()

    def process_input(self, user_input: str) -> Dict:
        """
        معالجة إدخال المستخدم
        
        Args:
            user_input: إدخال المستخدم
            
        Returns:
            قاموس يحتوي على معلومات المعالجة
        """
        # كشف اللغة
        detected_language = self.language_processor.detect_language(user_input)
        
        # تنظيف النص
        cleaned_text = self.language_processor.clean_text(user_input)
        
        # استخراج الكلمات المفتاحية
        keywords = self.language_processor.extract_keywords(cleaned_text, detected_language)
        
        # استخراج الكيانات
        entities = self.language_processor.extract_entities(cleaned_text, detected_language)
        
        # حساب إحصائيات النص
        statistics = self.language_processor.get_text_statistics(cleaned_text, detected_language)
        
        return {
            "original_input": user_input,
            "cleaned_text": cleaned_text,
            "detected_language": detected_language,
            "keywords": keywords,
            "entities": entities,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        }

    def generate_response(self, user_input: str, use_web_search: bool = False) -> str:
        """
        توليد رد على إدخال المستخدم
        
        Args:
            user_input: إدخال المستخدم
            use_web_search: استخدام البحث على الويب
            
        Returns:
            الرد المولد
        """
        # معالجة الإدخال
        processed_input = self.process_input(user_input)
        
        # إضافة رسالة المستخدم
        self.add_user_message(user_input)
        
        # بناء الرد (نسخة مبسطة)
        response = self._build_response(processed_input)
        
        # إضافة رسالة المساعد
        self.add_assistant_message(response)
        
        return response

    def _build_response(self, processed_input: Dict) -> str:
        """
        بناء رد بناءً على الإدخال المعالج
        
        Args:
            processed_input: الإدخال المعالج
            
        Returns:
            الرد
        """
        language = processed_input['detected_language']
        keywords = processed_input['keywords']
        
        # البحث في قاعدة المعرفة
        if keywords:
            top_keyword = keywords[0][0]
            knowledge = self.db_manager.search_knowledge(top_keyword, limit=3)
            
            if knowledge:
                # بناء رد بناءً على المعرفة المخزنة
                response = f"بناءً على معرفتي حول '{top_keyword}':\n\n"
                for item in knowledge:
                    response += f"• {item['content']}\n"
                return response
        
        # رد افتراضي
        if language == 'ar':
            return "شكراً على سؤالك! أنا هنا لمساعدتك. يرجى توضيح سؤالك أكثر."
        else:
            return "Thank you for your question! I'm here to help. Please provide more details."

    def rate_last_response(self, rating: int, feedback: str = None):
        """
        تقييم آخر رد من المساعد
        
        Args:
            rating: التقييم (1-5)
            feedback: ملاحظات إضافية
        """
        if self.context_window:
            # البحث عن آخر رسالة من المساعد
            for i in range(len(self.context_window) - 1, -1, -1):
                if self.context_window[i]['role'] == 'assistant':
                    # الحصول على معرف الرسالة من قاعدة البيانات
                    # (في التطبيق الفعلي، يجب حفظ معرف الرسالة)
                    logger.info(f"Response rated: {rating}/5")
                    if feedback:
                        logger.info(f"Feedback: {feedback}")
                    break

    def get_conversation_summary(self) -> Optional[str]:
        """
        الحصول على ملخص المحادثة الحالية
        
        Returns:
            ملخص المحادثة
        """
        if not self.context_window:
            return None
        
        # استخراج الكلمات المفتاحية من كل الرسائل
        all_text = " ".join([msg['content'] for msg in self.context_window])
        keywords = self.language_processor.extract_keywords(all_text, top_n=5)
        
        language = self.language_processor.detect_language(all_text)
        
        if language == 'ar':
            summary = f"محادثة تتعلق بـ: {', '.join([kw[0] for kw in keywords])}"
        else:
            summary = f"Conversation about: {', '.join([kw[0] for kw in keywords])}"
        
        return summary

    def end_conversation(self, summary: str = None):
        """
        إنهاء المحادثة الحالية
        
        Args:
            summary: ملخص المحادثة
        """
        if not summary:
            summary = self.get_conversation_summary()
        
        logger.info(f"Ended conversation: {self.current_conversation_id}")
        self.current_conversation_id = None
        self.context_window = []
