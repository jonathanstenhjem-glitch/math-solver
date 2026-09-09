"""
LLM Planner - Uses language model to plan and reason about math problems
Integrates with OpenAI API to identify problem type and create solution plan
"""

import openai
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LLMPlanner:
    """Plans solution approach using LLM before computation"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize LLM Planner
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo)
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
    
    def plan_solution(self, problem: str, context: str = "") -> Dict[str, Any]:
        """
        Analyze problem and create solution plan
        
        Returns:
        {
            "success": bool,
            "problem_type": "calculation|proof|reasoning",
            "subject": "calculus|linear_algebra|differential_equations|complex_numbers",
            "topic": "derivatives|integrals|eigenvalues|etc",
            "plan": "Step-by-step plan",
            "key_steps": ["Step 1", "Step 2", ...],
            "error": "..." (if success=false)
        }
        """
        try:
            system_prompt = """You are an expert mathematics teacher and problem analyzer.
Analyze the given math problem and:
1. Identify if it's a CALCULATION (solve equation, find derivative, etc), 
   PROOF (prove theorem, show identity), or REASONING (conceptual question)
2. Identify the subject area (calculus, linear_algebra, differential_equations, complex_numbers)
3. Identify the specific topic (derivatives, integrals, eigenvalues, etc)
4. Create a detailed step-by-step solution plan

Respond ONLY with valid JSON in this format:
{
    "problem_type": "calculation|proof|reasoning",
    "subject": "calculus|linear_algebra|differential_equations|complex_numbers",
    "topic": "specific topic",
    "plan": "Detailed explanation of how to solve",
    "key_steps": ["Step 1 description", "Step 2 description", ...],
    "notes": "Any important notes or constraints"
}"""
            
            user_message = f"""Problem: {problem}"""
            if context:
                user_message += f"\n\nContext: {context}"
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            try:
                plan_data = json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON if response has extra text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    plan_data = json.loads(json_match.group())
                else:
                    return {
                        "success": False,
                        "error": "Failed to parse LLM response"
                    }
            
            # Validate required fields
            required_fields = ["problem_type", "subject", "topic", "plan", "key_steps"]
            if not all(field in plan_data for field in required_fields):
                return {
                    "success": False,
                    "error": "LLM response missing required fields"
                }
            
            return {
                "success": True,
                **plan_data
            }
        
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                "success": False,
                "error": f"API error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error planning solution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def reason_solution(self, problem: str, context: str = "") -> Dict[str, Any]:
        """
        For proof/reasoning problems, provide detailed explanation
        
        Returns:
        {
            "steps": [...],
            "explanation": "...",
            "final_answer": "...",
            "note": "This is a reasoning-based answer and has not been verified numerically"
        }
        """
        try:
            system_prompt = """You are an expert mathematics teacher.
Provide a clear, step-by-step explanation for the given problem.
Use proper mathematical notation and reasoning.

Respond ONLY with valid JSON in this format:
{
    "steps": [
        {"step": 1, "description": "...", "explanation": "..."},
        {"step": 2, "description": "...", "explanation": "..."},
        ...
    ],
    "explanation": "Overall explanation",
    "final_answer": "The answer or conclusion"
}"""
            
            user_message = f"""Problem: {problem}"""
            if context:
                user_message += f"\n\nContext: {context}"
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            try:
                reasoning_data = json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    reasoning_data = json.loads(json_match.group())
                else:
                    reasoning_data = {
                        "steps": [{"step": 1, "description": content}],
                        "explanation": content,
                        "final_answer": "See explanation"
                    }
            
            return {
                "success": True,
                **reasoning_data,
                "note": "This is a reasoning-based answer and has not been verified numerically"
            }
        
        except Exception as e:
            logger.error(f"Error reasoning solution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_variables(self, problem: str) -> Dict[str, str]:
        """
        Extract mathematical variables and expressions from problem
        
        Returns:
        {
            "equation": "...",
            "variables": ["x", "y", ...],
            "parameters": {"a": "...", "b": "..."}
        }
        """
        try:
            system_prompt = """Extract mathematical elements from the problem.
Respond ONLY with valid JSON:
{
    "equation": "The main equation or expression",
    "variables": ["list of variables"],
    "parameters": {"param": "description"}
}"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": problem}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception as e:
            logger.error(f"Error extracting variables: {str(e)}")
            return {"equation": "", "variables": [], "parameters": {}}
