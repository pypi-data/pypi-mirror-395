"""
Continuous Learning Module
نظام التعلم المستمر وتحسين الأداء
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from almufti.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class ContinuousLearning:
    """
    نظام التعلم المستمر
    يقوم بتحسين الأداء بناءً على التفاعلات والملاحظات
    """

    def __init__(self, db_manager: DatabaseManager = None):
        """
        تهيئة نظام التعلم المستمر
        
        Args:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager or DatabaseManager()
        self.learning_history = []
        self.performance_metrics = {}

    def record_interaction(self, interaction_type: str, data: Dict, 
                          success: bool = True, rating: float = 0.0) -> int:
        """
        تسجيل تفاعل للتعلم منه
        
        Args:
            interaction_type: نوع التفاعل (chat, search, homework)
            data: بيانات التفاعل
            success: هل كان التفاعل ناجحاً
            rating: تقييم التفاعل (0-1)
            
        Returns:
            معرف التفاعل المسجل
        """
        try:
            improvement_score = rating if success else -rating
            
            self.db_manager.log_learning(
                interaction_type=interaction_type,
                data=data,
                improvement_score=improvement_score
            )
            
            logger.info(f"Recorded interaction: {interaction_type}")
            return 1  # معرف مؤقت
            
        except Exception as e:
            logger.error(f"Error recording interaction: {e}")
            raise

    def analyze_feedback(self, feedback: str, rating: int) -> Dict:
        """
        تحليل ملاحظات المستخدم
        
        Args:
            feedback: ملاحظات المستخدم
            rating: التقييم (1-5)
            
        Returns:
            قاموس يحتوي على تحليل الملاحظات
        """
        try:
            analysis = {
                'feedback': feedback,
                'rating': rating,
                'sentiment': self._analyze_sentiment(feedback),
                'improvement_areas': self._identify_improvement_areas(feedback),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Feedback analyzed: rating={rating}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing feedback: {e}")
            return {'error': str(e)}

    def _analyze_sentiment(self, text: str) -> str:
        """
        تحليل المشاعر في النص
        
        Args:
            text: النص المراد تحليله
            
        Returns:
            المشاعر (positive, negative, neutral)
        """
        # كلمات إيجابية وسلبية بسيطة
        positive_words = ['ممتاز', 'رائع', 'جيد', 'ممتاز', 'مفيد', 'excellent', 'great', 'good']
        negative_words = ['سيء', 'سوء', 'خطأ', 'مشكلة', 'bad', 'poor', 'wrong', 'error']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def _identify_improvement_areas(self, feedback: str) -> List[str]:
        """
        تحديد مجالات التحسن من الملاحظات
        
        Args:
            feedback: الملاحظات
            
        Returns:
            قائمة مجالات التحسن
        """
        improvement_areas = []
        
        keywords = {
            'accuracy': ['دقة', 'صحة', 'accuracy', 'correct'],
            'speed': ['سرعة', 'أسرع', 'speed', 'faster'],
            'clarity': ['وضوح', 'فهم', 'clarity', 'understand'],
            'relevance': ['صلة', 'ذات صلة', 'relevance', 'relevant'],
            'completeness': ['اكتمال', 'شامل', 'complete', 'comprehensive']
        }
        
        feedback_lower = feedback.lower()
        
        for area, keywords_list in keywords.items():
            if any(keyword in feedback_lower for keyword in keywords_list):
                improvement_areas.append(area)
        
        return improvement_areas

    def get_performance_report(self) -> Dict:
        """
        الحصول على تقرير الأداء
        
        Returns:
            قاموس يحتوي على معلومات الأداء
        """
        try:
            stats = self.db_manager.get_statistics()
            
            report = {
                'total_interactions': len(stats),
                'average_rating': self._calculate_average_rating(stats),
                'improvement_trend': self._calculate_improvement_trend(stats),
                'strengths': self._identify_strengths(stats),
                'weaknesses': self._identify_weaknesses(stats),
                'recommendations': self._generate_recommendations(stats),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info("Performance report generated")
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {'error': str(e)}

    def _calculate_average_rating(self, stats: List[Dict]) -> float:
        """حساب متوسط التقييم"""
        if not stats:
            return 0.0
        
        ratings = [s.get('metric_value', 0) for s in stats if 'rating' in s.get('metric_name', '')]
        return sum(ratings) / len(ratings) if ratings else 0.0

    def _calculate_improvement_trend(self, stats: List[Dict]) -> str:
        """حساب اتجاه التحسن"""
        if len(stats) < 2:
            return 'insufficient_data'
        
        # مقارنة الأداء الأخير بالأداء السابق
        recent = stats[-5:] if len(stats) >= 5 else stats
        older = stats[-10:-5] if len(stats) >= 10 else stats[:len(stats)//2]
        
        recent_avg = sum(s.get('metric_value', 0) for s in recent) / len(recent) if recent else 0
        older_avg = sum(s.get('metric_value', 0) for s in older) / len(older) if older else 0
        
        if recent_avg > older_avg:
            return 'improving'
        elif recent_avg < older_avg:
            return 'declining'
        else:
            return 'stable'

    def _identify_strengths(self, stats: List[Dict]) -> List[str]:
        """تحديد نقاط القوة"""
        strengths = []
        
        # تحليل الإحصائيات لتحديد المجالات القوية
        high_performing_areas = [s.get('category', 'unknown') 
                                for s in stats 
                                if s.get('metric_value', 0) > 0.8]
        
        if 'chat' in high_performing_areas:
            strengths.append('قدرات محادثة قوية')
        if 'search' in high_performing_areas:
            strengths.append('بحث فعال')
        if 'homework' in high_performing_areas:
            strengths.append('حل مسائل جيد')
        
        return strengths if strengths else ['أداء عام جيد']

    def _identify_weaknesses(self, stats: List[Dict]) -> List[str]:
        """تحديد نقاط الضعف"""
        weaknesses = []
        
        # تحليل الإحصائيات لتحديد المجالات الضعيفة
        low_performing_areas = [s.get('category', 'unknown') 
                               for s in stats 
                               if s.get('metric_value', 0) < 0.5]
        
        if 'chat' in low_performing_areas:
            weaknesses.append('تحسين قدرات المحادثة')
        if 'search' in low_performing_areas:
            weaknesses.append('تحسين البحث')
        if 'homework' in low_performing_areas:
            weaknesses.append('تحسين حل المسائل')
        
        return weaknesses if weaknesses else []

    def _generate_recommendations(self, stats: List[Dict]) -> List[str]:
        """توليد توصيات التحسن"""
        recommendations = []
        
        # توصيات بناءً على الأداء
        avg_rating = self._calculate_average_rating(stats)
        
        if avg_rating < 0.6:
            recommendations.append('يتطلب تحسين شامل في جميع المجالات')
        elif avg_rating < 0.8:
            recommendations.append('التركيز على تحسين المجالات الضعيفة')
        else:
            recommendations.append('الأداء جيد، استمر في التحسن')
        
        recommendations.append('تتبع الملاحظات والتقييمات بانتظام')
        recommendations.append('استخدام البيانات لتحديد أولويات التحسن')
        
        return recommendations

    def suggest_improvements(self) -> Dict:
        """
        اقتراح تحسينات بناءً على الأداء
        
        Returns:
            قاموس يحتوي على الاقتراحات
        """
        try:
            report = self.get_performance_report()
            
            suggestions = {
                'current_performance': report.get('average_rating', 0),
                'improvement_areas': report.get('weaknesses', []),
                'recommended_actions': [
                    'زيادة عدد التفاعلات في المجالات الضعيفة',
                    'تحليل الأخطاء الشائعة',
                    'تحديث قاعدة المعرفة بمعلومات جديدة',
                    'تحسين خوارزميات المعالجة'
                ],
                'expected_improvement': 'تحسن بنسبة 10-20% في الأداء العام',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info("Improvement suggestions generated")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return {'error': str(e)}

    def export_learning_data(self) -> Dict:
        """
        تصدير بيانات التعلم
        
        Returns:
            بيانات التعلم المصدرة
        """
        try:
            stats = self.db_manager.get_statistics()
            
            return {
                'total_records': len(stats),
                'data': stats,
                'export_date': datetime.now().isoformat(),
                'format': 'json'
            }
            
        except Exception as e:
            logger.error(f"Error exporting learning data: {e}")
            return {'error': str(e)}
