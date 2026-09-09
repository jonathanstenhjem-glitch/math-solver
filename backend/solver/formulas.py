"""
Formula Database
Contains mathematical formulas organized by category and topic
Based on Jarle Johannessen: Tekniske Tabeller style
"""

import json
from typing import List, Dict, Optional


class FormulaDatabase:
    """Database of mathematical formulas with references"""
    
    def __init__(self):
        self.formulas = self._initialize_formulas()
    
    def _initialize_formulas(self) -> List[Dict]:
        """Initialize formula database"""
        return [
            # Calculus - Derivatives
            {
                "id": "CALC-D-001",
                "name": "Power Rule",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(x^n) = n*x^(n-1)",
                "description": "Derivative of power function",
                "reference": "Thomas' Calculus, Chapter 3.2",
                "conditions": "n is a constant",
                "examples": ["d/dx(x^3) = 3x^2", "d/dx(x) = 1"]
            },
            {
                "id": "CALC-D-002",
                "name": "Product Rule",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(u*v) = u'*v + u*v'",
                "description": "Derivative of product of two functions",
                "reference": "Thomas' Calculus, Chapter 3.3",
                "conditions": "u and v are differentiable functions",
                "examples": ["d/dx(x*sin(x)) = sin(x) + x*cos(x)"]
            },
            {
                "id": "CALC-D-003",
                "name": "Quotient Rule",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(u/v) = (u'*v - u*v') / v^2",
                "description": "Derivative of quotient of two functions",
                "reference": "Thomas' Calculus, Chapter 3.3",
                "conditions": "u and v are differentiable, v ≠ 0",
                "examples": ["d/dx(sin(x)/x) = (x*cos(x) - sin(x))/x^2"]
            },
            {
                "id": "CALC-D-004",
                "name": "Chain Rule",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(f(g(x))) = f'(g(x)) * g'(x)",
                "description": "Derivative of composite function",
                "reference": "Thomas' Calculus, Chapter 3.4",
                "conditions": "f and g are differentiable",
                "examples": ["d/dx(sin(x^2)) = 2x*cos(x^2)"]
            },
            {
                "id": "CALC-D-005",
                "name": "Exponential Derivative",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(e^x) = e^x",
                "description": "Derivative of natural exponential",
                "reference": "Thomas' Calculus, Chapter 3.8",
                "conditions": "Always valid for e^x",
                "examples": ["d/dx(e^(2x)) = 2*e^(2x)"]
            },
            {
                "id": "CALC-D-006",
                "name": "Logarithm Derivative",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(ln(x)) = 1/x",
                "description": "Derivative of natural logarithm",
                "reference": "Thomas' Calculus, Chapter 3.8",
                "conditions": "x > 0",
                "examples": ["d/dx(ln(2x)) = 1/x"]
            },
            {
                "id": "CALC-D-007",
                "name": "Sine Derivative",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(sin(x)) = cos(x)",
                "description": "Derivative of sine function",
                "reference": "Thomas' Calculus, Chapter 3.5",
                "conditions": "x in radians",
                "examples": ["d/dx(sin(3x)) = 3*cos(3x)"]
            },
            {
                "id": "CALC-D-008",
                "name": "Cosine Derivative",
                "category": "calculus",
                "topic": "derivatives",
                "formula": "d/dx(cos(x)) = -sin(x)",
                "description": "Derivative of cosine function",
                "reference": "Thomas' Calculus, Chapter 3.5",
                "conditions": "x in radians",
                "examples": ["d/dx(cos(x)) = -sin(x)"]
            },
            
            # Calculus - Integration
            {
                "id": "CALC-I-001",
                "name": "Power Rule Integration",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫x^n dx = x^(n+1)/(n+1) + C",
                "description": "Antiderivative of power function",
                "reference": "Thomas' Calculus, Chapter 5.3",
                "conditions": "n ≠ -1",
                "examples": ["∫x^2 dx = x^3/3 + C"]
            },
            {
                "id": "CALC-I-002",
                "name": "Exponential Integration",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫e^x dx = e^x + C",
                "description": "Antiderivative of natural exponential",
                "reference": "Thomas' Calculus, Chapter 5.3",
                "conditions": "Always valid",
                "examples": ["∫e^(2x) dx = e^(2x)/2 + C"]
            },
            {
                "id": "CALC-I-003",
                "name": "Logarithm Integration",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫(1/x) dx = ln|x| + C",
                "description": "Antiderivative of 1/x",
                "reference": "Thomas' Calculus, Chapter 5.3",
                "conditions": "x ≠ 0",
                "examples": ["∫(1/x) dx = ln|x| + C"]
            },
            {
                "id": "CALC-I-004",
                "name": "Sine Integration",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫sin(x) dx = -cos(x) + C",
                "description": "Antiderivative of sine",
                "reference": "Thomas' Calculus, Chapter 5.3",
                "conditions": "x in radians",
                "examples": ["∫sin(x) dx = -cos(x) + C"]
            },
            {
                "id": "CALC-I-005",
                "name": "Cosine Integration",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫cos(x) dx = sin(x) + C",
                "description": "Antiderivative of cosine",
                "reference": "Thomas' Calculus, Chapter 5.3",
                "conditions": "x in radians",
                "examples": ["∫cos(x) dx = sin(x) + C"]
            },
            {
                "id": "CALC-I-006",
                "name": "Integration by Substitution",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫f(g(x))*g'(x) dx = ∫f(u) du where u = g(x)",
                "description": "U-substitution technique",
                "reference": "Thomas' Calculus, Chapter 5.5",
                "conditions": "g must be differentiable, f must be integrable",
                "examples": ["∫2x*cos(x^2) dx = sin(x^2) + C"]
            },
            {
                "id": "CALC-I-007",
                "name": "Integration by Parts",
                "category": "calculus",
                "topic": "integration",
                "formula": "∫u dv = u*v - ∫v du",
                "description": "Product integration technique",
                "reference": "Thomas' Calculus, Chapter 8.1",
                "conditions": "u and v must be differentiable",
                "examples": ["∫x*sin(x) dx = -x*cos(x) + sin(x) + C"]
            },
            
            # Differential Equations
            {
                "id": "DIFFEQ-001",
                "name": "Separable Differential Equation",
                "category": "differential_equations",
                "topic": "first_order",
                "formula": "dy/dx = f(x)*g(y) => ∫(1/g(y)) dy = ∫f(x) dx",
                "description": "Separation of variables technique",
                "reference": "Edwards & Penney, Chapter 1.4",
                "conditions": "g(y) ≠ 0",
                "examples": ["dy/dx = xy => y = C*e^(x^2/2)"]
            },
            {
                "id": "DIFFEQ-002",
                "name": "First Order Linear ODE",
                "category": "differential_equations",
                "topic": "first_order",
                "formula": "dy/dx + P(x)*y = Q(x) => y = e^(-∫P dx) * (∫Q*e^(∫P dx) dx + C)",
                "description": "Solution by integrating factor",
                "reference": "Edwards & Penney, Chapter 2.1",
                "conditions": "P(x) and Q(x) continuous",
                "examples": ["dy/dx + y = e^x => y = (x + C)*e^(-x)"]
            },
            {
                "id": "DIFFEQ-003",
                "name": "Homogeneous Linear ODE (2nd order)",
                "category": "differential_equations",
                "topic": "second_order",
                "formula": "a*y'' + b*y' + c*y = 0, characteristic: ar^2 + br + c = 0",
                "description": "Characteristic equation method",
                "reference": "Edwards & Penney, Chapter 3.1",
                "conditions": "Constant coefficients a, b, c",
                "examples": ["y'' - 2y' + y = 0 => y = (C1 + C2*x)*e^x"]
            },
            {
                "id": "DIFFEQ-004",
                "name": "Particular Solution - Undetermined Coefficients",
                "category": "differential_equations",
                "topic": "second_order",
                "formula": "For a*y'' + b*y' + c*y = f(x), guess form based on f(x)",
                "description": "Method of undetermined coefficients",
                "reference": "Edwards & Penney, Chapter 3.5",
                "conditions": "f(x) is polynomial, exponential, trig, or product",
                "examples": ["y'' + y = x => yp = x"]
            },
            
            # Linear Algebra
            {
                "id": "LINALG-001",
                "name": "Matrix Multiplication",
                "category": "linear_algebra",
                "topic": "matrices",
                "formula": "(AB)_ij = Σ_k A_ik * B_kj",
                "description": "Product of two matrices",
                "reference": "Edwards & Penney, Chapter 5.1",
                "conditions": "A is m×n, B is n×p",
                "examples": ["A(2×3) * B(3×2) = C(2×2)"]
            },
            {
                "id": "LINALG-002",
                "name": "Determinant (2×2)",
                "category": "linear_algebra",
                "topic": "determinants",
                "formula": "det([[a, b], [c, d]]) = ad - bc",
                "description": "Determinant of 2×2 matrix",
                "reference": "Edwards & Penney, Chapter 5.2",
                "conditions": "Square 2×2 matrix",
                "examples": ["det([[1, 2], [3, 4]]) = -2"]
            },
            {
                "id": "LINALG-003",
                "name": "Determinant (3×3) - Sarrus Rule",
                "category": "linear_algebra",
                "topic": "determinants",
                "formula": "Repeat first 2 columns, sum products diagonally",
                "description": "Determinant of 3×3 matrix (Sarrus rule)",
                "reference": "Edwards & Penney, Chapter 5.2",
                "conditions": "Square 3×3 matrix",
                "examples": ["Useful for hand calculation"]
            },
            {
                "id": "LINALG-004",
                "name": "Inverse Matrix (2×2)",
                "category": "linear_algebra",
                "topic": "matrices",
                "formula": "A^(-1) = (1/det(A)) * [[d, -b], [-c, a]] for A = [[a, b], [c, d]]",
                "description": "Inverse of 2×2 matrix",
                "reference": "Edwards & Penney, Chapter 5.3",
                "conditions": "det(A) ≠ 0",
                "examples": ["[[1, 2], [3, 4]]^(-1) = -1/2 * [[4, -2], [-3, 1]]"]
            },
            {
                "id": "LINALG-005",
                "name": "Eigenvalue Problem",
                "category": "linear_algebra",
                "topic": "eigenvalues",
                "formula": "det(A - λI) = 0 to find eigenvalues, (A - λI)v = 0 for eigenvectors",
                "description": "Finding eigenvalues and eigenvectors",
                "reference": "Edwards & Penney, Chapter 6.1",
                "conditions": "A is square matrix",
                "examples": ["A = [[2, 1], [1, 2]] => λ = 3, 1"]
            },
            {
                "id": "LINALG-006",
                "name": "Solving Linear System Ax = b",
                "category": "linear_algebra",
                "topic": "systems",
                "formula": "x = A^(-1) * b if A is invertible",
                "description": "Matrix solution of linear system",
                "reference": "Edwards & Penney, Chapter 5.3",
                "conditions": "A is square and invertible",
                "examples": ["[[1, 2], [3, 4]] * x = [5, 6]"]
            },
            
            # Complex Numbers
            {
                "id": "COMPLEX-001",
                "name": "Complex Number Arithmetic",
                "category": "complex_numbers",
                "topic": "operations",
                "formula": "(a + bi) + (c + di) = (a+c) + (b+d)i",
                "description": "Addition of complex numbers",
                "reference": "Thomas' Calculus, Appendix",
                "conditions": "Always valid",
                "examples": ["(1 + 2i) + (3 - i) = 4 + i"]
            },
            {
                "id": "COMPLEX-002",
                "name": "Complex Multiplication",
                "category": "complex_numbers",
                "topic": "operations",
                "formula": "(a + bi)(c + di) = (ac - bd) + (ad + bc)i",
                "description": "Multiplication of complex numbers",
                "reference": "Thomas' Calculus, Appendix",
                "conditions": "Always valid",
                "examples": ["(1 + 2i)(3 - i) = 5 + 5i"]
            },
            {
                "id": "COMPLEX-003",
                "name": "Complex Conjugate",
                "category": "complex_numbers",
                "topic": "operations",
                "formula": "conj(a + bi) = a - bi",
                "description": "Complex conjugate",
                "reference": "Thomas' Calculus, Appendix",
                "conditions": "Always valid",
                "examples": ["conj(3 + 4i) = 3 - 4i"]
            },
            {
                "id": "COMPLEX-004",
                "name": "Complex Modulus",
                "category": "complex_numbers",
                "topic": "operations",
                "formula": "|a + bi| = sqrt(a^2 + b^2)",
                "description": "Magnitude of complex number",
                "reference": "Thomas' Calculus, Appendix",
                "conditions": "Always valid",
                "examples": ["|3 + 4i| = 5"]
            },
            {
                "id": "COMPLEX-005",
                "name": "Euler's Formula",
                "category": "complex_numbers",
                "topic": "exponential",
                "formula": "e^(ix) = cos(x) + i*sin(x)",
                "description": "Exponential form of complex numbers",
                "reference": "Thomas' Calculus, Chapter 11.9",
                "conditions": "x in radians",
                "examples": ["e^(iπ) = -1"]
            },
            {
                "id": "COMPLEX-006",
                "name": "Polar Form",
                "category": "complex_numbers",
                "topic": "representation",
                "formula": "z = r*e^(iθ) where r = |z|, θ = arg(z)",
                "description": "Polar representation of complex numbers",
                "reference": "Thomas' Calculus, Appendix",
                "conditions": "Always valid",
                "examples": ["1 + i = sqrt(2)*e^(i*π/4)"]
            },
        ]
    
    def get_formulas(self, category: Optional[str] = None, topic: Optional[str] = None) -> List[Dict]:
        """Get formulas filtered by category and/or topic"""
        result = self.formulas
        
        if category:
            result = [f for f in result if f.get("category") == category]
        
        if topic:
            result = [f for f in result if f.get("topic") == topic]
        
        return result
    
    def get_formula_by_id(self, formula_id: str) -> Optional[Dict]:
        """Get specific formula by ID"""
        for formula in self.formulas:
            if formula.get("id") == formula_id:
                return formula
        return None
    
    def get_categories(self) -> List[str]:
        """Get list of all categories"""
        return list(set(f.get("category") for f in self.formulas))
    
    def get_topics(self, category: Optional[str] = None) -> List[str]:
        """Get list of topics, optionally filtered by category"""
        if category:
            formulas = [f for f in self.formulas if f.get("category") == category]
        else:
            formulas = self.formulas
        return list(set(f.get("topic") for f in formulas))
