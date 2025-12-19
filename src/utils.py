"""Auxiliary functions"""

from agents import MultiAgentSystem

def interactive_demo(system: MultiAgentSystem):
    """Interactive demonstration mode"""
    print("\n INTERACTIVE DEMONSTRATION MODE")
    print("="*60)
    print("Type your queries or commands:")
    print("• 'stats' - show system statistics")
    print("• 'history' - show interaction history")
    print("• 'info' - show system information")
    print("• 'exit' or 'quit' - exit demonstration")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n Your query: ").strip()
            
            if not user_input:
                continue
                
            # Check commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n Goodbye! Thank you for using StudyCoder Assistant!")
                break
                
            elif user_input.lower() in ['stats', 'statistics']:
                stats = system.memory.get_statistics()
                print(f"\n SYSTEM STATISTICS:")
                print(f"• Total interactions: {stats['total_interactions']}")
                print(f"• Categories used: {stats['categories_used']}")
                print(f"• Agents used: {stats['agents_used']}")
                print(f"• Tools used: {stats['unique_tools_used']}")
                continue
                
            elif user_input.lower() in ['history', 'hist']:
                print(f"\n INTERACTION HISTORY:")
                for i, interaction in enumerate(system.memory.interactions[-5:], 1):
                    print(f"{i}. [{interaction['agent']}] {interaction['query'][:50]}...")
                continue
                
            elif user_input.lower() in ['info', 'system']:
                info = system.get_system_info()
                print(f"\n SYSTEM INFORMATION:")
                print(f"• Version: {info['version']}")
                print(f"• LLM: {info['llm_config']['model']}")
                print(f"• Temperature: {info['llm_config']['temperature']}")
                print(f"• Agents: {', '.join(info['agents'])}")
                continue
            
            # Process regular query
            result = system.process(user_input)
            print(result["formatted"])
            
        except KeyboardInterrupt:
            print("\n\n Demonstration interrupted.")
            break
        except Exception as e:
            print(f"\n Error: {e}")