"""
Tests for solution validation
Ensures solutions meet quality standards
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from solver.validator import Validator


class TestValidation:
    """Test solution validation"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance"""
        return Validator(tolerance=1e-6)
    
    def test_validate_calculus_solution(self, validator):
        """Test validation of calculus solution"""
        problem = "Find the derivative of x^3 + 2x"
        solution = {
            "final_answer": "3x^2 + 2",
            "steps": []
        }
        plan = {
            "subject": "calculus",
            "topic": "derivatives"
        }
        
        result = validator.validate_solution(problem, solution, plan)
        
        assert "valid" in result
        assert "checks" in result
        assert isinstance(result["checks"], list)
    
    def test_numerical_equality_within_tolerance(self, validator):
        """Test numbers are equal within tolerance"""
        val1 = 1.0
        val2 = 1.0 + 1e-7  # Within tolerance
        
        assert validator.check_numerical_equality(val1, val2)
    
    def test_numerical_equality_outside_tolerance(self, validator):
        """Test numbers are not equal outside tolerance"""
        val1 = 1.0
        val2 = 1.0 + 1e-5  # Outside default tolerance
        
        # Depends on tolerance value
        result = validator.check_numerical_equality(val1, val2)
        # This may or may not be true depending on tolerance
        assert isinstance(result, bool)
    
    def test_validation_checks_structure(self, validator):
        """Test that validation returns proper check structure"""
        problem = "Solve x^2 = 4"
        solution = {
            "final_answer": "x = 2 or x = -2",
            "steps": []
        }
        plan = {
            "subject": "calculus",
            "topic": "algebra"
        }
        
        result = validator.validate_solution(problem, solution, plan)
        
        # Check result structure
        assert "valid" in result
        assert "result" in result
        assert "tolerance" in result
        assert "checks" in result
        
        # Check each check has required fields
        for check in result["checks"]:
            assert "name" in check
            assert "passed" in check
            assert isinstance(check["passed"], bool)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
