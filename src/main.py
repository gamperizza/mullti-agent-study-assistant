"""Main module for running the project"""

from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents import MultiAgentSystem, AgentState
from config import LLMConfig

def test_system_connection():
    """Tests connection to LLM server"""
    print("\n Testing LLM connection...")
    
    try:
        llm = LLMConfig.get_llm()
        
        # Simple test query
        test_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a test assistant. Reply 'Test completed successfully'."),
            ("human", "Hello! This is connection test.")
        ])
        
        chain = test_prompt | llm | StrOutputParser()
        response = chain.invoke({})
        
        print(f" Connection successful: {response}")
        return True
        
    except Exception as e:
        print(f" Connection error: {e}")
        return False

def run_laboratory_work():
    """Runs complete project"""
    
    print("Design and implementation of multi-agent system")
    print("Used: LangChain 1.x + LangGraph")
    print(f"Model: qwen3-32b via LiteLLM")
    print("="*60)
    
    # Test connection
    if not test_system_connection():
        print(" Failed to connect to LLM. Cannot continue.")
        return None, None
    
    # Create system
    print("\n Creating multi-agent system...")
    system = MultiAgentSystem()
    
    # Test queries 
    test_cases = [
        {
            "query": "What are multi-agent systems in LangChain context?",
            "expected": "theory",
            "description": "Conceptual question about MAS"
        },
        {
            "query": "Write Python function to check if string is palindrome",
            "expected": "code",
            "description": "Code writing request"
        },
        {
            "query": "Help create Python and algorithms study plan for 2 weeks",
            "expected": "planning",
            "description": "Planning request"
        },
        {
            "query": "Hello! Tell me about agents in your system and how they work?",
            "expected": "general",
            "description": "General system inquiry"
        },
        {
            "query": "Explain difference between array and linked list",
            "expected": "theory",
            "description": "Theoretical question about data structures"
        },
        {
            "query": "Write code to read CSV file and calculate column average",
            "expected": "code",
            "description": "Practical programming request"
        }
    ]
    
    print(f"\n STARTING TESTING: {len(test_cases)} queries")
    print("-"*60)
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n TEST {i}: {test['description']}")
        print(f" Query: {test['query']}")
        
        result = system.process(test["query"])
        results.append(result)
        
        # Brief results
        is_correct = result["category"] == test["expected"]
        print(f"  Result:")
        print(f" • Category: {result['category']} ({'✓' if is_correct else '✗'})")
        print(f" • Agent: {result['agent']}")
        print(f" • Tools: {', '.join(result['tools_used']) if result['tools_used'] else 'none'}")
        print(f" • Time: {result['total_execution_time']:.2f} sec")
    
    # Statistics
    print("\n" + "="*60)
    print(" TESTING STATISTICS")
    print("="*60)
    
    categories_count = {}
    agents_count = {}
    all_tools = set()
    
    for result in results:
        cat = result['category']
        agent = result['agent']
        
        categories_count[cat] = categories_count.get(cat, 0) + 1
        agents_count[agent] = agents_count.get(agent, 0) + 1
        all_tools.update(result['tools_used'])
    
    print(f"\n TESTING RESULTS:")
    print(f"• Total queries: {len(results)}")
    print(f"• Category distribution: {categories_count}")
    print(f"• Agents used: {agents_count}")
    print(f"• Unique tools: {len(all_tools)} ({', '.join(all_tools) if all_tools else 'none'})")
    
    # Classification accuracy
    correct_classifications = sum(1 for i, r in enumerate(results)
                                  if r['category'] == test_cases[i]['expected'])
    accuracy = (correct_classifications / len(results)) * 100
    
    print(f"• Classification accuracy: {accuracy:.1f}% ({correct_classifications}/{len(results)})")
    
    # System information
    system_info = system.get_system_info()
    print(f"\n SYSTEM INFORMATION:")
    print(f"• Agents: {', '.join(system_info['agents'])}")
    print(f"• Tools: {', '.join(system_info['tools'])}")
    print(f"• Memory: {system_info['memory_system']}")
    print(f"• Graph: {system_info['graph_engine']}")
    print(f"• Total interactions: {system_info['statistics']['total_interactions']}")
    
    print("\n" + "="*60)
    
    return system, results

if __name__ == "__main__":
    print("\n STARTING PROJECT EXECUTION")
    
    try:
        # Run project
        system, results = run_laboratory_work()
        
        if system and results:
            # Start interactive demonstration
            from utils import interactive_demo
            interactive_demo(system)
        
    except Exception as e:
        print(f"\n Execution error: {e}")