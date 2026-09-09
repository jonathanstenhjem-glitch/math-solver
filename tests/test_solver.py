"""
Unit tests for Math Solver
Tests core solving functionality
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'backend')))

from solver.llm_planner import LLMPlanner
from solver.sympy_engine import SympyEngine
from solver.validator import Validator
from solver.formulas import FormulaDatabase


class TestLLMPlanner:
    """Test LLM Planner"""
    
    @pytest.fixture
    def planner(self):
        """Create LLM planner instance"""
        # Note: Requires OPENAI_API_KEY env var
        return LLMPlanner(api_key='test-key', model='gpt-3.5-turbo')
    
    def test_planner_initialization(self, planner):
        """Test planner can be initialized"""
        assert planner is not None
        assert planner.model == 'gpt-3.5-turbo'
    
    def test_plan_solution_structure(self):
        """Test plan_solution returns correct structure"""
        # This would need mocking to avoid API calls
        pass


class TestSympyEngine:
    """Test SymPy Engine"""
    
    @pytest.fixture
    def engine(self):
        """Create SymPy engine instance"""
        return SympyEngine()
    
    def test_engine_initialization(self, engine):
        """Test engine can be initialized"""
        assert engine is not None
    
    def test_extract_expressions(self, engine):
        """Test expression extraction from problem text"""
        problem = "Find the derivative of x^2 + 2x"
        expressions = engine._extract_expressions(problem, {})
        # Would return extracted expressions
        assert isinstance(expressions, list)


class TestValidator:
    """Test Solution Validator"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance"""
        return Validator(tolerance=1e-6)
    
    def test_validator_initialization(self, validator):
        """Test validator can be initialized"""
        assert validator is not None
        assert validator.tolerance == 1e-6
    
    def test_numerical_equality(self, validator):
        """Test numerical equality check"""
        assert validator.check_numerical_equality(1.0, 1.0000001)
        assert not validator.check_numerical_equality(1.0, 1.1)


class TestFormulaDatabase:
    """Test Formula Database"""
    
    @pytest.fixture
    def db(self):
        """Create formula database instance"""
        return FormulaDatabase()
    
    def test_database_initialization(self, db):
        """Test database can be initialized"""
        assert db is not None
    
    def test_get_formulas(self, db):
        """Test retrieving formulas"""
        formulas = db.get_formulas()
        assert isinstance(formulas, list)
        # Should have some formulas loaded
        # assert len(formulas) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
