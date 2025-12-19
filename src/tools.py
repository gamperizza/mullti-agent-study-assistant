"""Definig tools"""

from typing import Dict, List
from langchain_core.tools import tool
from datetime import datetime, timedelta

@tool
def execute_python_code(code: str) -> str:
    """Executes Python code and returns result. Use for code testing."""
    try:
        # Safe execution environment
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'range': range,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round
            }
        }
        
        local_vars = {}
        exec(code, safe_globals, local_vars)
        
        # Format result
        result_vars = {}
        for key, value in local_vars.items():
            if not key.startswith('_'):
                result_vars[key] = str(value)[:100]  # Limit length
        
        if result_vars:
            return f" Code executed successfully. Variables: {result_vars}"
        else:
            return " Code executed successfully (no return variables)"
            
    except Exception as e:
        return f" Execution error: {str(e)}"

@tool
def search_knowledge_base(topic: str) -> str:
    """Searches for information on a topic in the knowledge base. Use for theoretical questions."""
    
    knowledge_base = {
        "python": [
            "Python - high-level interpreted programming language",
            "Basic data structures: list, dict, tuple, set",
            "Functions defined with def, classes with class",
            "Python supports paradigms: OOP, functional, imperative programming"
        ],
        "algorithm": [
            "Algorithm - finite sequence of steps to solve a problem",
            "Algorithm complexity measured in Big O notation (O(1), O(n), O(n²), O(log n))",
            "Basic sorting algorithms: bubble sort, quick sort, merge sort, heap sort",
            "Search algorithms: linear (O(n)), binary (O(log n)) for sorted arrays"
        ],
        "data structure": [
            "Array - contiguous memory area for storing elements of the same type",
            "Linked list - elements (nodes) contain data and pointer to next element",
            "Stack - LIFO (Last In, First Out), operations: push (add), pop (remove)",
            "Queue - FIFO (First In, First Out), operations: enqueue (to end), dequeue (from beginning)"
        ],
        "multi-agent system": [
            "Multi-Agent System (MAS) - system of multiple interacting agents",
            "Agent - autonomous entity perceiving environment and acting in it",
            "MAS patterns: Router, Planner-Executor, Supervisor",
            "LangGraph - library for building agent interaction graphs in LangChain"
        ],
        "langchain": [
            "LangChain - framework for developing applications using language models",
            "Main concepts: Prompts, Chains, Agents, Tools",
            "Memory - state preservation between calls",
            "LangGraph - extension for building cyclic graphs and multi-agent systems"
        ],
        "machine learning": [
            "Machine Learning - subset of AI focusing on algorithms learning from data",
            "ML types: supervised (with teacher), unsupervised (without teacher), reinforcement learning",
            "Neural networks consist of layers: input, hidden, output",
            "LLM (Large Language Models) - large language models trained on huge text corpora"
        ]
    }
    
    topic_lower = topic.lower()
    
    # Search by categories
    for category, facts in knowledge_base.items():
        if category in topic_lower:
            return "\n".join([f"• {fact}" for fact in facts[:3]])
    
    # Search by keywords in facts
    results = []
    for category, facts in knowledge_base.items():
        for fact in facts:
            words = topic_lower.split()
            if any(word in fact.lower() for word in words[:3]):
                results.append(f"• {fact}")
                if len(results) >= 3:
                    break
        if len(results) >= 3:
            break
    
    if results:
        return "\n".join(results)
    else:
        return "Information on this topic not found. Please clarify your query."

@tool
def create_study_plan(days: int, topic: str = "programming") -> str:
    """Creates a study plan for specified number of days. Use for learning planning."""
    
    start_date = datetime.now()
    
    plan = {
        "topic": topic,
        "duration_days": days,
        "start_date": start_date.strftime("%d.%m.%Y"),
        "end_date": (start_date + timedelta(days=days-1)).strftime("%d.%m.%Y"),
        "total_hours": days * 4,
        "daily_schedule": []
    }
    
    # Create schedule for each day
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        if "python" in topic.lower():
            tasks = [
                "Morning session: Python theory (1.5 hours)",
                "Day practice: writing code (2 hours)",
                "Evening review: problem analysis (0.5 hours)"
            ]
        elif "algorithm" in topic.lower():
            tasks = [
                "Learning new algorithm (1.5 hours)",
                "Implementation in Python (2 hours)",
                "Complexity analysis and optimization (0.5 hours)"
            ]
        elif "machine learning" in topic.lower() or "ml" in topic.lower():
            tasks = [
                "ML/neural networks theory (1.5 hours)",
                "Practice with libraries (scikit-learn, tensorflow) (2 hours)",
                "Solving Kaggle problems (0.5 hours)"
            ]
        else:
            tasks = [
                "Theoretical part (2 hours)",
                "Practical tasks (1.5 hours)",
                "Review and note-taking (0.5 hours)"
            ]
        
        plan["daily_schedule"].append({
            "day": day + 1,
            "date": current_date.strftime("%d.%m.%Y"),
            "day_of_week": current_date.strftime("%A"),
            "tasks": tasks
        })
    
    # Format response
    result = f" Study plan for '{topic}' for {days} days:\n"
    result += f" From {plan['start_date']} to {plan['end_date']}\n"
    result += f" Total hours: {plan['total_hours']} (~{plan['total_hours']/days:.1f} hours/day)\n\n"
    
    # Show first 3 days in detail
    result += "First 3 days:\n"
    for day_plan in plan["daily_schedule"][:3]:
        result += f"\nDay {day_plan['day']} ({day_plan['date']}, {day_plan['day_of_week']}):\n"
        for task in day_plan['tasks']:
            result += f" • {task}\n"
    
    if days > 3:
        result += f"\n... and {days-3} more days with similar schedule."
    
    return result

# Tools export
tools = [execute_python_code, search_knowledge_base, create_study_plan]