"""
Database Manager Module
إدارة قاعدة البيانات SQLite للمحادثات والمعلومات
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    مدير قاعدة البيانات SQLite
    يدير تخزين المحادثات والمعلومات والإحصائيات
    """

    def __init__(self, db_path: str = "data/almufti.db"):
        """
        تهيئة مدير قاعدة البيانات
        
        Args:
            db_path: مسار قاعدة البيانات
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.init_database()

    def init_database(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()

            # جدول المحادثات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    language TEXT DEFAULT 'ar',
                    summary TEXT
                )
            """)

            # جدول الرسائل
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    rating INTEGER,
                    feedback TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)

            # جدول قاعدة المعرفة
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confidence REAL DEFAULT 0.8,
                    language TEXT DEFAULT 'ar'
                )
            """)

            # جدول الإحصائيات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT
                )
            """)

            # جدول التعلم المستمر
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_type TEXT NOT NULL,
                    data JSON NOT NULL,
                    improvement_score REAL DEFAULT 0.0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # جدول الكلمات المفتاحية
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    category TEXT,
                    language TEXT DEFAULT 'ar'
                )
            """)

            self.connection.commit()
            logger.info("Database initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def save_conversation(self, title: str, language: str = "ar") -> int:
        """
        حفظ محادثة جديدة
        
        Args:
            title: عنوان المحادثة
            language: لغة المحادثة
            
        Returns:
            معرف المحادثة
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO conversations (title, language)
                VALUES (?, ?)
            """, (title, language))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error saving conversation: {e}")
            raise

    def add_message(self, conversation_id: int, role: str, content: str) -> int:
        """
        إضافة رسالة إلى محادثة
        
        Args:
            conversation_id: معرف المحادثة
            role: دور المرسل (user/assistant)
            content: محتوى الرسالة
            
        Returns:
            معرف الرسالة
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
            """, (conversation_id, role, content))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding message: {e}")
            raise

    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """
        استرجاع محادثة كاملة
        
        Args:
            conversation_id: معرف المحادثة
            
        Returns:
            بيانات المحادثة والرسائل
        """
        try:
            cursor = self.connection.cursor()
            
            # استرجاع بيانات المحادثة
            cursor.execute("""
                SELECT * FROM conversations WHERE id = ?
            """, (conversation_id,))
            conv = cursor.fetchone()
            
            if not conv:
                return None
            
            # استرجاع الرسائل
            cursor.execute("""
                SELECT * FROM messages WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """, (conversation_id,))
            messages = cursor.fetchall()
            
            return {
                "conversation": dict(conv),
                "messages": [dict(msg) for msg in messages]
            }
        except sqlite3.Error as e:
            logger.error(f"Error retrieving conversation: {e}")
            raise

    def add_knowledge(self, topic: str, content: str, source: str = None, 
                     confidence: float = 0.8, language: str = "ar") -> int:
        """
        إضافة معرفة جديدة إلى قاعدة المعرفة
        
        Args:
            topic: موضوع المعرفة
            content: محتوى المعرفة
            source: مصدر المعرفة
            confidence: درجة الثقة
            language: اللغة
            
        Returns:
            معرف المعرفة
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source, confidence, language)
                VALUES (?, ?, ?, ?, ?)
            """, (topic, content, source, confidence, language))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding knowledge: {e}")
            raise

    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """
        البحث في قاعدة المعرفة
        
        Args:
            query: استعلام البحث
            limit: عدد النتائج
            
        Returns:
            قائمة النتائج
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM knowledge_base 
                WHERE topic LIKE ? OR content LIKE ?
                ORDER BY confidence DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error searching knowledge: {e}")
            raise

    def rate_message(self, message_id: int, rating: int, feedback: str = None):
        """
        تقييم رسالة
        
        Args:
            message_id: معرف الرسالة
            rating: التقييم (1-5)
            feedback: ملاحظات إضافية
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE messages SET rating = ?, feedback = ?
                WHERE id = ?
            """, (rating, feedback, message_id))
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error rating message: {e}")
            raise

    def log_learning(self, interaction_type: str, data: Dict, improvement_score: float = 0.0):
        """
        تسجيل تفاعل للتعلم المستمر
        
        Args:
            interaction_type: نوع التفاعل
            data: بيانات التفاعل
            improvement_score: درجة التحسن
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO learning_log (interaction_type, data, improvement_score)
                VALUES (?, ?, ?)
            """, (interaction_type, json.dumps(data, ensure_ascii=False), improvement_score))
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error logging learning: {e}")
            raise

    def get_statistics(self, category: str = None, limit: int = 100) -> List[Dict]:
        """
        استرجاع الإحصائيات
        
        Args:
            category: فئة الإحصائيات
            limit: عدد النتائج
            
        Returns:
            قائمة الإحصائيات
        """
        try:
            cursor = self.connection.cursor()
            
            if category:
                cursor.execute("""
                    SELECT * FROM statistics 
                    WHERE category = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (category, limit))
            else:
                cursor.execute("""
                    SELECT * FROM statistics 
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error retrieving statistics: {e}")
            raise

    def close(self):
        """إغلاق اتصال قاعدة البيانات"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
