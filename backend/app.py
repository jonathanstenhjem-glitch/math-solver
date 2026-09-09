"""
Math Solver Backend - Flask Application
Handles solver routes, LLM integration, and validation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

from solver.llm_planner import LLMPlanner
from solver.sympy_engine import SympyEngine
from solver.validator import Validator
from solver.formulas import FormulaDatabase

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize solvers and validators
llm_planner = LLMPlanner(api_key=os.getenv("OPENAI_API_KEY"))
sympy_engine = SympyEngine()
validator = Validator()
formula_db = FormulaDatabase()


@app.route("/", methods=["GET"])
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "Math Solver API",
        "version": "0.1.0"
    })


@app.route("/solve", methods=["POST"])
def solve():
    """
    Main solver endpoint.
    
    Request:
    {
        "problem": "Solve the differential equation dy/dx = 2x",
        "context": "Optional context or hints"
    }
    
    Response:
    {
        "success": bool,
        "problem_type": "calculation|proof|reasoning",
        "solution": {
            "steps": [...],
            "final_answer": "...",
            "formulas_used": [...]
        },
        "validation": {
            "valid": bool,
            "result": "...",
            "tolerance": "..."
        },
        "error": "..." (if success=false)
    }
    """
    try:
        data = request.get_json()
        problem = data.get("problem")
        context = data.get("context", "")
        
        if not problem:
            return jsonify({
                "success": False,
                "error": "Problem statement is required"
            }), 400
        
        logger.info(f"Solving problem: {problem[:100]}...")
        
        # Step 1: LLM identifies problem type and creates plan
        plan = llm_planner.plan_solution(problem, context)
        
        if not plan["success"]:
            return jsonify({
                "success": False,
                "error": plan.get("error", "Failed to plan solution")
            }), 400
        
        problem_type = plan.get("problem_type")
        
        # Step 2: Handle based on problem type
        if problem_type == "calculation":
            solution = sympy_engine.solve_calculation(problem, plan)
            
            if not solution["success"]:
                return jsonify({
                    "success": False,
                    "error": solution.get("error", "Failed to solve")
                }), 400
            
            # Step 3: Validate solution
            validation = validator.validate_solution(problem, solution, plan)
            
            return jsonify({
                "success": True,
                "problem_type": problem_type,
                "solution": solution,
                "validation": validation
            })
        
        elif problem_type in ["proof", "reasoning"]:
            # LLM handles reasoning with disclaimer
            reasoning = llm_planner.reason_solution(problem, context)
            
            return jsonify({
                "success": True,
                "problem_type": problem_type,
                "solution": reasoning,
                "validation": {
                    "valid": False,
                    "note": "Reasoning-based answers are not numerically verified"
                }
            })
        
        else:
            return jsonify({
                "success": False,
                "error": f"Unknown problem type: {problem_type}"
            }), 400
    
    except Exception as e:
        logger.error(f"Error solving problem: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/formulas", methods=["GET"])
def get_formulas():
    """
    Get available formulas from database.
    
    Query params:
    - category: filter by category (calculus, linear_algebra, etc.)
    - topic: filter by topic
    """
    try:
        category = request.args.get("category")
        topic = request.args.get("topic")
        
        formulas = formula_db.get_formulas(category=category, topic=topic)
        
        return jsonify({
            "success": True,
            "count": len(formulas),
            "formulas": formulas
        })
    
    except Exception as e:
        logger.error(f"Error fetching formulas: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/formulas/<formula_id>", methods=["GET"])
def get_formula(formula_id):
    """Get specific formula by ID"""
    try:
        formula = formula_db.get_formula_by_id(formula_id)
        
        if not formula:
            return jsonify({
                "success": False,
                "error": f"Formula not found: {formula_id}"
            }), 404
        
        return jsonify({
            "success": True,
            "formula": formula
        })
    
    except Exception as e:
        logger.error(f"Error fetching formula: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check for deployment"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
