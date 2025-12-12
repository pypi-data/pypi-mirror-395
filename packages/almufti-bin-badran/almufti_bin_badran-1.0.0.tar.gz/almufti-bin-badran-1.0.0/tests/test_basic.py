"""
Basic Tests for Almufti Bin Badran
اختبارات أساسية للتطبيق
"""

import unittest
import sys
from pathlib import Path

# إضافة المسار إلى sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from almufti.core.language_processor import LanguageProcessor
from almufti.core.chat_engine import ChatEngine
from almufti.homework.math_solver import MathSolver
from almufti.database.db_manager import DatabaseManager


class TestLanguageProcessor(unittest.TestCase):
    """اختبارات معالج اللغة"""

    def setUp(self):
        self.processor = LanguageProcessor()

    def test_language_detection_arabic(self):
        """اختبار كشف اللغة العربية"""
        text = "السلام عليكم ورحمة الله وبركاته"
        lang = self.processor.detect_language(text)
        self.assertEqual(lang, 'ar')

    def test_language_detection_english(self):
        """اختبار كشف اللغة الإنجليزية"""
        text = "Hello, how are you today?"
        lang = self.processor.detect_language(text)
        self.assertEqual(lang, 'en')

    def test_tokenize_sentences_arabic(self):
        """اختبار تقسيم الجمل العربية"""
        text = "هذه جملة أولى. هذه جملة ثانية."
        sentences = self.processor.tokenize_sentences(text, 'ar')
        self.assertGreater(len(sentences), 0)

    def test_clean_text(self):
        """اختبار تنظيف النص"""
        text = "  هذا   نص   به   مسافات   زائدة  "
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "هذا نص به مسافات زائدة")

    def test_extract_keywords(self):
        """اختبار استخراج الكلمات المفتاحية"""
        text = "الذكاء الاصطناعي والتعلم الآلي والشبكات العصبية"
        keywords = self.processor.extract_keywords(text, 'ar', top_n=3)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 3)

    def test_text_statistics(self):
        """اختبار إحصائيات النص"""
        text = "هذا نص تجريبي لاختبار الإحصائيات"
        stats = self.processor.get_text_statistics(text, 'ar')
        self.assertIn('word_count', stats)
        self.assertIn('character_count', stats)
        self.assertIn('sentence_count', stats)


class TestMathSolver(unittest.TestCase):
    """اختبارات حل المسائل الرياضية"""

    def setUp(self):
        self.solver = MathSolver()

    def test_calculate_expression(self):
        """اختبار حساب تعبير حسابي"""
        result = self.solver.calculate_expression("2 + 3 * 4")
        self.assertEqual(result['result'], 14)

    def test_calculate_percentage(self):
        """اختبار حساب النسبة المئوية"""
        result = self.solver.calculate_percentage(25, 100)
        self.assertEqual(result['percentage'], 25)

    def test_solve_quadratic_equation_two_solutions(self):
        """اختبار حل معادلة تربيعية بحلين"""
        result = self.solver.solve_quadratic_equation(1, -5, 6)
        self.assertEqual(result['type'], 'two_real_solutions')
        self.assertEqual(len(result['solutions']), 2)

    def test_solve_geometry_rectangle(self):
        """اختبار حل مسألة هندسية (مستطيل)"""
        result = self.solver.solve_geometry_problem('rectangle', length=5, width=3)
        self.assertEqual(result['area'], 15)
        self.assertEqual(result['perimeter'], 16)

    def test_solve_geometry_circle(self):
        """اختبار حل مسألة هندسية (دائرة)"""
        result = self.solver.solve_geometry_problem('circle', radius=2)
        self.assertIn('area', result)
        self.assertIn('circumference', result)


class TestDatabaseManager(unittest.TestCase):
    """اختبارات مدير قاعدة البيانات"""

    def setUp(self):
        # استخدام قاعدة بيانات مؤقتة للاختبار
        self.db = DatabaseManager("data/test.db")

    def tearDown(self):
        self.db.close()

    def test_save_conversation(self):
        """اختبار حفظ محادثة"""
        conv_id = self.db.save_conversation("اختبار", "ar")
        self.assertIsNotNone(conv_id)
        self.assertGreater(conv_id, 0)

    def test_add_message(self):
        """اختبار إضافة رسالة"""
        conv_id = self.db.save_conversation("اختبار", "ar")
        msg_id = self.db.add_message(conv_id, "user", "مرحبا")
        self.assertIsNotNone(msg_id)

    def test_add_knowledge(self):
        """اختبار إضافة معرفة"""
        knowledge_id = self.db.add_knowledge(
            "الذكاء الاصطناعي",
            "الذكاء الاصطناعي هو محاكاة الذكاء البشري",
            "wikipedia",
            0.9,
            "ar"
        )
        self.assertIsNotNone(knowledge_id)

    def test_search_knowledge(self):
        """اختبار البحث في قاعدة المعرفة"""
        self.db.add_knowledge(
            "الرياضيات",
            "الرياضيات هي دراسة الأرقام والأشكال",
            "wikipedia",
            0.9,
            "ar"
        )
        results = self.db.search_knowledge("الرياضيات")
        self.assertGreater(len(results), 0)


class TestChatEngine(unittest.TestCase):
    """اختبارات محرك المحادثة"""

    def setUp(self):
        self.db = DatabaseManager("data/test_chat.db")
        self.chat = ChatEngine(self.db, "ar")

    def tearDown(self):
        self.db.close()

    def test_start_conversation(self):
        """اختبار بدء محادثة"""
        conv_id = self.chat.start_conversation("اختبار المحادثة")
        self.assertIsNotNone(conv_id)

    def test_add_user_message(self):
        """اختبار إضافة رسالة مستخدم"""
        self.chat.start_conversation()
        msg_id = self.chat.add_user_message("السلام عليكم")
        self.assertIsNotNone(msg_id)

    def test_add_assistant_message(self):
        """اختبار إضافة رسالة مساعد"""
        self.chat.start_conversation()
        msg_id = self.chat.add_assistant_message("وعليكم السلام ورحمة الله")
        self.assertIsNotNone(msg_id)

    def test_process_input(self):
        """اختبار معالجة إدخال المستخدم"""
        result = self.chat.process_input("السلام عليكم ورحمة الله")
        self.assertIn('detected_language', result)
        self.assertIn('keywords', result)
        self.assertEqual(result['detected_language'], 'ar')


if __name__ == '__main__':
    unittest.main()
