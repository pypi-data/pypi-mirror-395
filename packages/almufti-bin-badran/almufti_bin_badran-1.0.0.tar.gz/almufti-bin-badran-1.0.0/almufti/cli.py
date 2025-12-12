"""
Command Line Interface for Almufti Bin Badran
واجهة سطر الأوامر للتطبيق
"""

import sys
import argparse
import logging
from pathlib import Path
from almufti.core.chat_engine import ChatEngine
from almufti.search.web_search import WebSearch
from almufti.homework.math_solver import MathSolver
from almufti.database.db_manager import DatabaseManager
from almufti.learning.continuous_learning import ContinuousLearning

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AlmuftiCLI:
    """واجهة سطر الأوامر للمفتي بن بدران"""

    def __init__(self):
        """تهيئة واجهة سطر الأوامر"""
        self.db = DatabaseManager()
        self.chat = ChatEngine(self.db)
        self.search = WebSearch()
        self.math_solver = MathSolver()
        self.learning = ContinuousLearning(self.db)

    def run_chat_mode(self):
        """تشغيل وضع المحادثة التفاعلي"""
        print("\n" + "="*50)
        print("المفتي بن بدران - وضع المحادثة")
        print("Almufti Bin Badran - Chat Mode")
        print("="*50)
        print("اكتب 'exit' للخروج | Type 'exit' to quit\n")

        self.chat.start_conversation("Interactive Chat")

        while True:
            try:
                user_input = input("أنت: ").strip()

                if user_input.lower() in ['exit', 'quit', 'خروج']:
                    print("شكراً لاستخدامك المفتي بن بدران!")
                    break

                if not user_input:
                    continue

                # توليد الرد
                response = self.chat.generate_response(user_input)
                print(f"\nالمفتي: {response}\n")

            except KeyboardInterrupt:
                print("\n\nتم الخروج من البرنامج")
                break
            except Exception as e:
                logger.error(f"Error in chat mode: {e}")
                print(f"حدث خطأ: {e}")

    def run_search_mode(self, query: str):
        """تشغيل وضع البحث"""
        print("\n" + "="*50)
        print(f"البحث عن: {query}")
        print("="*50 + "\n")

        result = self.search.search_and_summarize(query)

        if result.get('results'):
            print(result['summary'])
            print("\nالنتائج الكاملة:")
            for i, result_item in enumerate(result['results'][:5], 1):
                print(f"\n{i}. {result_item['title']}")
                print(f"   {result_item['snippet'][:200]}...")
                print(f"   المصدر: {result_item['url']}")
        else:
            print(result.get('summary', 'لم يتم العثور على نتائج'))

    def run_math_mode(self, problem: str):
        """تشغيل وضع حل المسائل الرياضية"""
        print("\n" + "="*50)
        print(f"حل المسألة: {problem}")
        print("="*50 + "\n")

        # محاولة حل المعادلة الخطية
        result = self.math_solver.solve_linear_equation(problem)

        if 'error' not in result:
            print(f"الحل: x = {result['solution']}")
            print("\nالخطوات:")
            for step in result['steps']:
                print(f"  • {step}")
            print(f"\nالتحقق: {result['verification']}")
        else:
            print(f"خطأ: {result['error']}")

    def run_performance_report(self):
        """عرض تقرير الأداء"""
        print("\n" + "="*50)
        print("تقرير الأداء")
        print("="*50 + "\n")

        report = self.learning.get_performance_report()

        print(f"متوسط التقييم: {report.get('average_rating', 0):.2f}/1.0")
        print(f"اتجاه التحسن: {report.get('improvement_trend', 'غير معروف')}")

        if report.get('strengths'):
            print("\nنقاط القوة:")
            for strength in report['strengths']:
                print(f"  ✓ {strength}")

        if report.get('weaknesses'):
            print("\nنقاط الضعف:")
            for weakness in report['weaknesses']:
                print(f"  ✗ {weakness}")

        if report.get('recommendations'):
            print("\nالتوصيات:")
            for rec in report['recommendations']:
                print(f"  → {rec}")

    def run_interactive_menu(self):
        """تشغيل القائمة التفاعلية"""
        while True:
            print("\n" + "="*50)
            print("المفتي بن بدران - القائمة الرئيسية")
            print("="*50)
            print("1. وضع المحادثة")
            print("2. البحث على الإنترنت")
            print("3. حل مسألة رياضية")
            print("4. عرض تقرير الأداء")
            print("5. الخروج")
            print("-"*50)

            choice = input("اختر خياراً (1-5): ").strip()

            if choice == '1':
                self.run_chat_mode()
            elif choice == '2':
                query = input("أدخل استعلام البحث: ").strip()
                if query:
                    self.run_search_mode(query)
            elif choice == '3':
                problem = input("أدخل المسألة الرياضية (مثال: 2x + 5 = 15): ").strip()
                if problem:
                    self.run_math_mode(problem)
            elif choice == '4':
                self.run_performance_report()
            elif choice == '5':
                print("\nشكراً لاستخدامك المفتي بن بدران!")
                break
            else:
                print("اختيار غير صحيح. يرجى المحاولة مرة أخرى.")


def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="المفتي بن بدران - AI Assistant with Arabic Support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  almufti chat                    # Start interactive chat
  almufti search "الذكاء الاصطناعي"  # Search for a topic
  almufti math "2x + 5 = 15"     # Solve a math problem
  almufti report                  # Show performance report
        """
    )

    parser.add_argument(
        'command',
        nargs='?',
        choices=['chat', 'search', 'math', 'report', 'menu'],
        default='menu',
        help='Command to run'
    )

    parser.add_argument(
        'query',
        nargs='?',
        help='Query or problem to solve'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Almufti Bin Badran v1.0.0'
    )

    args = parser.parse_args()

    cli = AlmuftiCLI()

    try:
        if args.command == 'chat':
            cli.run_chat_mode()
        elif args.command == 'search':
            if not args.query:
                print("Error: search command requires a query")
                sys.exit(1)
            cli.run_search_mode(args.query)
        elif args.command == 'math':
            if not args.query:
                print("Error: math command requires a problem")
                sys.exit(1)
            cli.run_math_mode(args.query)
        elif args.command == 'report':
            cli.run_performance_report()
        else:  # menu
            cli.run_interactive_menu()

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"خطأ: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
