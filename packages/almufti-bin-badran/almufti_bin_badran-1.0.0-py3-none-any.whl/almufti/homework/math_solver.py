"""
Math Solver Module
حل المسائل الرياضية
"""

import re
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class MathSolver:
    """
    حل المسائل الرياضية
    يقوم بحل معادلات وعمليات حسابية مختلفة
    """

    def __init__(self):
        """تهيئة حل المسائل الرياضية"""
        self.operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else None,
            '**': lambda a, b: a ** b,
            '%': lambda a, b: a % b if b != 0 else None,
        }

    def solve_linear_equation(self, equation: str) -> Optional[Dict]:
        """
        حل معادلة خطية من الشكل ax + b = c
        
        Args:
            equation: المعادلة (مثال: "2x + 5 = 15")
            
        Returns:
            قاموس يحتوي على الحل والخطوات
        """
        try:
            # تنظيف المعادلة
            equation = equation.replace(' ', '')
            
            # فصل الطرفين
            if '=' not in equation:
                return {'error': 'المعادلة يجب أن تحتوي على علامة ='}
            
            left, right = equation.split('=')
            
            # استخراج المعاملات
            # معادلة من الشكل ax + b = c
            left_pattern = r'([+-]?\d*)\*?x([+-]\d+)?'
            right_pattern = r'([+-]?\d+)'
            
            left_match = re.match(left_pattern, left)
            right_match = re.match(right_pattern, right)
            
            if not left_match or not right_match:
                return {'error': 'صيغة المعادلة غير صحيحة'}
            
            # استخراج المعاملات
            a_str = left_match.group(1)
            a = float(a_str) if a_str and a_str not in ['+', '-'] else (1 if a_str != '-' else -1)
            
            b_str = left_match.group(2)
            b = float(b_str) if b_str else 0
            
            c = float(right_match.group(1))
            
            # حل المعادلة: ax + b = c => x = (c - b) / a
            if a == 0:
                return {'error': 'المعادلة ليس لها حل فريد'}
            
            x = (c - b) / a
            
            return {
                'equation': equation,
                'solution': x,
                'steps': [
                    f"المعادلة الأصلية: {equation}",
                    f"نقل {b} إلى الطرف الأيمن: {a}x = {c - b}",
                    f"قسمة على {a}: x = {(c - b) / a}",
                    f"الحل: x = {x}"
                ],
                'verification': f"{a} * {x} + {b} = {a * x + b} = {c}"
            }
            
        except Exception as e:
            logger.error(f"Error solving linear equation: {e}")
            return {'error': str(e)}

    def solve_quadratic_equation(self, a: float, b: float, c: float) -> Optional[Dict]:
        """
        حل معادلة تربيعية من الشكل ax² + bx + c = 0
        
        Args:
            a: معامل x²
            b: معامل x
            c: الحد الثابت
            
        Returns:
            قاموس يحتوي على الحلول والخطوات
        """
        try:
            if a == 0:
                return {'error': 'ليست معادلة تربيعية (a ≠ 0)'}
            
            # حساب المميز
            discriminant = b ** 2 - 4 * a * c
            
            steps = [
                f"المعادلة: {a}x² + {b}x + {c} = 0",
                f"المميز (Δ) = b² - 4ac = {b}² - 4({a})({c}) = {discriminant}"
            ]
            
            if discriminant > 0:
                # حلان حقيقيان مختلفان
                sqrt_discriminant = discriminant ** 0.5
                x1 = (-b + sqrt_discriminant) / (2 * a)
                x2 = (-b - sqrt_discriminant) / (2 * a)
                
                steps.append(f"√Δ = √{discriminant} = {sqrt_discriminant}")
                steps.append(f"x₁ = (-{b} + {sqrt_discriminant}) / (2 * {a}) = {x1}")
                steps.append(f"x₂ = (-{b} - {sqrt_discriminant}) / (2 * {a}) = {x2}")
                
                return {
                    'equation': f"{a}x² + {b}x + {c} = 0",
                    'solutions': [x1, x2],
                    'discriminant': discriminant,
                    'type': 'two_real_solutions',
                    'steps': steps
                }
            
            elif discriminant == 0:
                # حل واحد مكرر
                x = -b / (2 * a)
                steps.append(f"x = -b / (2a) = -{b} / (2 * {a}) = {x}")
                
                return {
                    'equation': f"{a}x² + {b}x + {c} = 0",
                    'solution': x,
                    'discriminant': discriminant,
                    'type': 'one_repeated_solution',
                    'steps': steps
                }
            
            else:
                # حلان عقديان
                real_part = -b / (2 * a)
                imaginary_part = (-discriminant) ** 0.5 / (2 * a)
                
                steps.append(f"الحلول عقدية (معقدة)")
                steps.append(f"x₁ = {real_part} + {imaginary_part}i")
                steps.append(f"x₂ = {real_part} - {imaginary_part}i")
                
                return {
                    'equation': f"{a}x² + {b}x + {c} = 0",
                    'solutions': [
                        f"{real_part} + {imaginary_part}i",
                        f"{real_part} - {imaginary_part}i"
                    ],
                    'discriminant': discriminant,
                    'type': 'complex_solutions',
                    'steps': steps
                }
            
        except Exception as e:
            logger.error(f"Error solving quadratic equation: {e}")
            return {'error': str(e)}

    def calculate_expression(self, expression: str) -> Optional[Dict]:
        """
        حساب تعبير حسابي
        
        Args:
            expression: التعبير الحسابي
            
        Returns:
            قاموس يحتوي على النتيجة والخطوات
        """
        try:
            # التحقق من الأمان
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return {'error': 'التعبير يحتوي على أحرف غير مسموحة'}
            
            # حساب النتيجة
            result = eval(expression)
            
            return {
                'expression': expression,
                'result': result,
                'steps': [
                    f"التعبير: {expression}",
                    f"النتيجة: {result}"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error calculating expression: {e}")
            return {'error': f'خطأ في التعبير: {str(e)}'}

    def solve_system_of_equations(self, equations: List[str]) -> Optional[Dict]:
        """
        حل نظام معادلات خطية
        
        Args:
            equations: قائمة المعادلات
            
        Returns:
            قاموس يحتوي على الحل
        """
        try:
            # محاولة حل نظام بسيط من معادلتين
            if len(equations) != 2:
                return {'error': 'يدعم فقط نظام من معادلتين'}
            
            # هذا مثال مبسط
            # في التطبيق الفعلي، يجب استخدام مكتبة numpy أو sympy
            
            return {
                'equations': equations,
                'note': 'يتطلب تطوير إضافي لحل الأنظمة المعقدة',
                'suggestion': 'يرجى استخدام أدوات متخصصة مثل Wolfram Alpha'
            }
            
        except Exception as e:
            logger.error(f"Error solving system of equations: {e}")
            return {'error': str(e)}

    def calculate_percentage(self, part: float, whole: float) -> Dict:
        """
        حساب النسبة المئوية
        
        Args:
            part: الجزء
            whole: الكل
            
        Returns:
            قاموس يحتوي على النسبة المئوية والخطوات
        """
        try:
            if whole == 0:
                return {'error': 'الكل لا يمكن أن يكون صفر'}
            
            percentage = (part / whole) * 100
            
            return {
                'part': part,
                'whole': whole,
                'percentage': percentage,
                'steps': [
                    f"النسبة المئوية = (الجزء / الكل) × 100",
                    f"النسبة المئوية = ({part} / {whole}) × 100",
                    f"النسبة المئوية = {percentage}%"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error calculating percentage: {e}")
            return {'error': str(e)}

    def solve_geometry_problem(self, problem_type: str, **params) -> Optional[Dict]:
        """
        حل مسائل هندسية
        
        Args:
            problem_type: نوع المسألة (rectangle, circle, triangle)
            **params: معاملات المسألة
            
        Returns:
            قاموس يحتوي على الحل
        """
        try:
            if problem_type == 'rectangle':
                length = params.get('length')
                width = params.get('width')
                
                if not length or not width:
                    return {'error': 'يتطلب الطول والعرض'}
                
                area = length * width
                perimeter = 2 * (length + width)
                
                return {
                    'shape': 'مستطيل',
                    'length': length,
                    'width': width,
                    'area': area,
                    'perimeter': perimeter,
                    'steps': [
                        f"المساحة = الطول × العرض = {length} × {width} = {area}",
                        f"المحيط = 2 × (الطول + العرض) = 2 × ({length} + {width}) = {perimeter}"
                    ]
                }
            
            elif problem_type == 'circle':
                radius = params.get('radius')
                
                if not radius:
                    return {'error': 'يتطلب نصف القطر'}
                
                import math
                area = math.pi * radius ** 2
                circumference = 2 * math.pi * radius
                
                return {
                    'shape': 'دائرة',
                    'radius': radius,
                    'area': area,
                    'circumference': circumference,
                    'steps': [
                        f"المساحة = π × r² = π × {radius}² = {area:.2f}",
                        f"المحيط = 2π × r = 2π × {radius} = {circumference:.2f}"
                    ]
                }
            
            else:
                return {'error': f'نوع المسألة غير مدعوم: {problem_type}'}
            
        except Exception as e:
            logger.error(f"Error solving geometry problem: {e}")
            return {'error': str(e)}
