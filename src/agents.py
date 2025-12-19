"""Defining agents and graph"""

from typing import Dict, List, Any, Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
from datetime import datetime
from config import LLMConfig
from tools import tools, search_knowledge_base, execute_python_code, create_study_plan
from memory import SessionMemorySystem

class AgentState(TypedDict):
    """State of the multi-agent system"""
    messages: Annotated[List[Dict], add_messages]  # Message history
    current_agent: str  # Current active agent
    agent_history: List[str]  # History of activated agents
    tools_used: List[str]  # History of used tools
    query: str  # Original user query
    category: str  # Query category
    final_answer: str  # Final answer
    memory: Dict[str, Any]  # Session memory
    execution_time: float  # Execution time

class MultiAgentSystem:
    """Multi-agent system with 5 agents"""
    
    def __init__(self):
        print("\n Initializing multi-agent system...")
        
        # Initialize LLM with your configuration
        self.llm = LLMConfig.get_llm()
        self.memory = SessionMemorySystem()
        
        # Create agents
        print("  Creating agents...")
        self.router_agent = self._create_router_agent()
        self.theory_agent = self._create_theory_agent()
        self.code_agent = self._create_code_agent()
        self.planner_agent = self._create_planner_agent()
        self.general_agent = self._create_general_agent()
        
        # Create graph
        print("  Building LangGraph...")
        self.graph = self._build_graph()
        
        print("Multi-agent system initialized\n")
    
    def _create_router_agent(self):
        """Creates router agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent router of the StudyCoder Assistant multi-agent system.
            Your task is to classify user queries into one of categories.
            
            Categories:
            1. theory - theoretical questions (what is, explain, definition, concept)
            2. code - programming questions (write code, function, fix error, how to do)
            3. planning - planning questions (create plan, schedule, organize, plan)
            4. general - general questions (hello, help, information, system capabilities)
            
            Return ONLY one word: theory, code, planning or general.
            Do not add any explanations.
            
            Examples:
            - "What is Python?" → theory
            - "Write factorial function" → code
            - "Create learning plan for a week" → planning
            - "Hello, tell about yourself" → general
            """),
            ("human", "{query}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def _create_theory_agent(self):
        """Creates theory agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in programming theory, algorithms and computer science.
            
            Your tasks:
            1. Explain concepts clearly and in detail
            2. Use examples and analogies
            3. Structure response (introduction, main part, conclusion)
            4. Highlight key terms
            5. Give practical recommendations
            
            Previous discussion context: {context}
            
            Use search_knowledge_base tool to find accurate information.
            If information is insufficient, supplement with your knowledge.
            """),
            ("human", "{query}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def _create_code_agent(self):
        """Creates code agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experienced programmer assistant, Python expert.
            
            Response requirements:
            1. Provide complete, working code
            2. Add comments for explanation
            3. Explain logic and key points
            4. Consider best practices (PEP 8)
            5. Warn about possible errors
            6. Suggest alternative solutions
            
            Previous discussion context: {context}
            
            Use execute_python_code tool to test code.
            Show code execution results to user.
            """),
            ("human", "{query}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def _create_planner_agent(self):
        """Creates planner agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in planning and time management.
            
            Your tasks:
            1. Create realistic and achievable plans
            2. Break big goals into small steps
            3. Consider time constraints
            4. Add time for rest and review
            5. Suggest productivity methods (Pomodoro, Eisenhower Matrix)
            
            Previous discussion context: {context}
            
            Use create_study_plan tool to create structured plans.
            Adapt plan to specific user needs.
            """),
            ("human", "{query}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def _create_general_agent(self):
        """Creates general agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly and helpful assistant of StudyCoder Assistant multi-agent system.
            
            System information:
            - Name: StudyCoder Assistant
            - 5 specialized agents: Router, Theory, Code, Planner, General
            - 3 tools: code execution, knowledge search, plan creation
            - Memory: saves interaction history
            - Uses model: qwen3-32b via LiteLLM server
            
            Previous discussion context: {context}
            
            Be polite, helpful and informative.
            If question is not in your specialization, suggest contacting appropriate agent.
            """),
            ("human", "{query}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def _build_graph(self):
        """Builds LangGraph"""
        
        # Handler functions for each node
        def router_node(state: AgentState) -> Dict:
            """Router node"""
            import time
            start_time = time.time()
            
            print(f"\n [Router] Analyzing query: '{state['query'][:50]}...'")
            
            # Get category from router
            category = self.router_agent.invoke({"query": state["query"]})
            category = category.strip().lower()
            
            # Category validation
            valid_categories = ["theory", "code", "planning", "general"]
            if category not in valid_categories:
                category = "general"
            
            execution_time = time.time() - start_time
            print(f"  Category determined: {category} ({execution_time:.2f} sec)")
            
            return {
                "category": category,
                "current_agent": "router",
                "agent_history": ["router"],
                "tools_used": [],
                "execution_time": execution_time
            }
        
        def theory_node(state: AgentState) -> Dict:
            """Theory agent node"""
            import time
            start_time = time.time()
            
            print(f" [Theory Agent] Processing theoretical question")
            
            # Get context from memory
            context = self.memory.get_context(2)
            
            # Process query
            response = self.theory_agent.invoke({
                "query": state["query"],
                "context": context
            })
            
            # Use knowledge search tool if needed
            tools_used = []
            if any(keyword in state["query"].lower() for keyword in ["what is", "explain", "definition"]):
                knowledge = search_knowledge_base.invoke({"topic": state["query"]})
                response += f"\n\n Additional information:\n{knowledge}"
                tools_used.append("search_knowledge_base")
            
            execution_time = time.time() - start_time
            print(f" Completed ({execution_time:.2f} sec). Tools: {tools_used}")
            
            return {
                "current_agent": "theory",
                "agent_history": state["agent_history"] + ["theory"],
                "tools_used": state["tools_used"] + tools_used,
                "final_answer": response,
                "execution_time": execution_time
            }
        
        def code_node(state: AgentState) -> Dict:
            """Code agent node"""
            import time
            start_time = time.time()
            
            print(f" [Code Agent] Processing programming query")
            
            # Get context from memory
            context = self.memory.get_context(2)
            
            # Process query
            response = self.code_agent.invoke({
                "query": state["query"],
                "context": context
            })
            
            # Try to execute code if present
            tools_used = []
            if "```python" in response or "def " in response:
                # Extract code
                code_to_execute = ""
                if "```python" in response:
                    start = response.find("```python") + 9
                    end = response.find("```", start)
                    if start > 8 and end > start:
                        code_to_execute = response[start:end].strip()
                
                # Execute code
                if code_to_execute:
                    try:
                        execution_result = execute_python_code.invoke({"code": code_to_execute})
                        response += f"\n\n🔧 Code execution result:\n{execution_result}"
                        tools_used.append("execute_python_code")
                    except Exception as e:
                        response += f"\n\n Failed to execute code: {str(e)}"
            
            execution_time = time.time() - start_time
            print(f" Completed ({execution_time:.2f} sec). Tools: {tools_used}")
            
            return {
                "current_agent": "code",
                "agent_history": state["agent_history"] + ["code"],
                "tools_used": state["tools_used"] + tools_used,
                "final_answer": response,
                "execution_time": execution_time
            }
        
        def planner_node(state: AgentState) -> Dict:
            """Planner agent node"""
            import time
            start_time = time.time()
            
            print(f" [Planner Agent] Processing planning query")
            
            # Get context from memory
            context = self.memory.get_context(2)
            
            # Process query
            response = self.planner_agent.invoke({
                "query": state["query"],
                "context": context
            })
            
            # Use plan creation tool
            tools_used = []
            if any(keyword in state["query"].lower() for keyword in ["plan", "schedule", "days", "weeks"]):
                # Extract number of days
                days = 7
                for word in state["query"].split():
                    if word.isdigit():
                        days = min(int(word), 30)
                        break
                
                try:
                    plan = create_study_plan.invoke({"days": days, "topic": state["query"]})
                    response += f"\n\n📋 Structured plan:\n{plan}"
                    tools_used.append("create_study_plan")
                except Exception as e:
                    response += f"\n\n Failed to create detailed plan: {str(e)}"
            
            execution_time = time.time() - start_time
            print(f" Completed ({execution_time:.2f} sec). Tools: {tools_used}")
            
            return {
                "current_agent": "planner",
                "agent_history": state["agent_history"] + ["planner"],
                "tools_used": state["tools_used"] + tools_used,
                "final_answer": response,
                "execution_time": execution_time
            }
        
        def general_node(state: AgentState) -> Dict:
            """General agent node"""
            import time
            start_time = time.time()
            
            print(f" [General Agent] Processing general query")
            
            # Get context from memory
            context = self.memory.get_context(2)
            
            # Process query
            response = self.general_agent.invoke({
                "query": state["query"],
                "context": context
            })
            
            execution_time = time.time() - start_time
            print(f" Completed ({execution_time:.2f} sec)")
            
            return {
                "current_agent": "general",
                "agent_history": state["agent_history"] + ["general"],
                "tools_used": state["tools_used"],
                "final_answer": response,
                "execution_time": execution_time
            }
        
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", router_node)
        workflow.add_node("theory", theory_node)
        workflow.add_node("code", code_node)
        workflow.add_node("planner", planner_node)
        workflow.add_node("general", general_node)
        
        # Set entry point
        workflow.set_entry_point("router")

        def start_node(state: AgentState) -> Dict:
            """Начальный узел - инициализирует состояние"""
            # Убедимся, что category есть
            if not state.get("category"):
                state["category"] = "general"
            return state
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "router",
            lambda state: state["category"],
            {
                "theory": "theory",
                "code": "code",
                "planning": "planner",
                "general": "general"
            }
        )
        
        # Add end points
        workflow.add_edge("theory", END)
        workflow.add_edge("code", END)
        workflow.add_edge("planner", END)
        workflow.add_edge("general", END)
        
        return workflow.compile()
    
    def process(self, query: str) -> Dict[str, Any]:
        """Processes query through multi-agent system"""
        import time
        total_start_time = time.time()
        
        print(f"\n Starting query processing: '{query}'")
        
        # Initialize state
        initial_state: AgentState = {
            "messages": [{"role": "user", "content": query}],
            "current_agent": "",
            "agent_history": [],
            "tools_used": [],
            "query": query,
            "category": "",
            "final_answer": "",
            "memory": {},
            "execution_time": 0.0
        }
            
        # Execute graph
        result = self.graph.invoke(initial_state)
        
        # Save to memory
        self.memory.add_interaction(
            query=query,
            response=result["final_answer"],
            agent=result["current_agent"],
            category=result["category"],
            tools_used=result["tools_used"]
        )
        
        total_execution_time = time.time() - total_start_time
        
        # Format response
        formatted_response = self._format_response(query, result, total_execution_time)
        
        return {
            "query": query,
            "category": result["category"],
            "agent": result["current_agent"],
            "agents_used": result["agent_history"],
            "tools_used": result["tools_used"],
            "response": result["final_answer"],
            "agent_execution_time": result.get("execution_time", 0),
            "total_execution_time": total_execution_time,
            "formatted": formatted_response,
            "memory_stats": self.memory.get_statistics()
        }
    
    def _format_response(self, query: str, result: Dict, total_time: float) -> str:
        """Formats final response"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        return f"""
{'='*60}
STUDYCODER ASSISTANT | {current_time}
{'='*60}

QUERY: {query}

CATEGORY: {result['category']}
AGENTS USED: {' → '.join(result['agent_history'])}
TOOLS: {', '.join(result['tools_used']) if result['tools_used'] else 'not used'}

PROCESSING TIME:
   • Agent: {result.get('execution_time', 0):.2f} sec
   • Total: {total_time:.2f} sec

{'='*60}

ANSWER:

{result['final_answer']}

{'='*60}

SESSION STATISTICS:
• Total interactions: {self.memory.user_profile['interaction_count']}
• Topics discussed: {len(self.memory.user_profile['topics_discussed'])}
• Unique agents: {', '.join(self.memory.get_statistics()['agents_used'])}
{'='*60}
"""
    
    def get_system_info(self) -> Dict[str, Any]:
        """Returns system information"""
        return {
            "version": "1.0",
            "llm_config": {
                "model": "qwen3-32b",
                "base_url": "http://a6k2.dgx:34000/v1",
                "temperature": 0.3
            },
            "agents": ["router", "theory", "code", "planner", "general"],
            "tools": ["execute_python_code", "search_knowledge_base", "create_study_plan"],
            "memory_system": "SessionMemorySystem",
            "graph_engine": "LangGraph",
            "statistics": self.memory.get_statistics()
        }