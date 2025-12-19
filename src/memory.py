"""Session memory management system"""

from typing import Dict, Any, List
from datetime import datetime

class SessionMemorySystem:
    """Session memory management system"""
    
    def __init__(self):
        self.interactions = []
        self.user_profile = {
            "topics_discussed": [],
            "preferred_topics": [],
            "interaction_count": 0,
            "first_interaction": datetime.now().isoformat()
        }
    
    def add_interaction(self, query: str, response: str, agent: str, category: str, tools_used: List[str]):
        """Adds interaction to memory"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_preview": response[:200] + "..." if len(response) > 200 else response,
            "agent": agent,
            "category": category,
            "tools_used": tools_used
        }
        
        self.interactions.append(interaction)
        self.user_profile["interaction_count"] += 1
        
        # Add topic
        if query not in self.user_profile["topics_discussed"]:
            self.user_profile["topics_discussed"].append(query[:100])
        
        # Limit size
        if len(self.interactions) > 20:
            self.interactions = self.interactions[-20:]
    
    def get_context(self, n: int = 3) -> str:
        """Returns context from last n interactions"""
        if not self.interactions:
            return "Interaction history is empty."
        
        recent = self.interactions[-n:]
        context = " Recent interaction history:\n"
        for i, item in enumerate(recent, 1):
            context += f"{i}. [{item['category']}] {item['agent']}: {item['query'][:80]}...\n"
        
        return context
    
    def get_statistics(self) -> Dict[str, Any]:
        """Returns session statistics"""
        agents_used = list(set([i["agent"] for i in self.interactions]))
        categories_used = list(set([i["category"] for i in self.interactions]))
        all_tools = []
        for i in self.interactions:
            all_tools.extend(i["tools_used"])
        
        return {
            "total_interactions": len(self.interactions),
            "user_profile": self.user_profile,
            "agents_used": agents_used,
            "categories_used": categories_used,
            "unique_tools_used": list(set(all_tools))
        }