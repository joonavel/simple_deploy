from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from node import GraphState, target_number_creation, answer_checking, diff_calculation, human_interaction, router

def make_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("target_number_creation", target_number_creation)
    workflow.add_node("answer_checking", answer_checking)
    workflow.add_node("diff_calculation", diff_calculation)
    workflow.add_node("human_interaction", human_interaction)

    workflow.add_edge("target_number_creation", "answer_checking")
    
    workflow.add_conditional_edges(
        "answer_checking",
        router,
        {"HUMAN": "diff_calculation", "KEEP": END},
    )
    
    workflow.add_edge("diff_calculation", "human_interaction")
    workflow.add_edge("human_interaction", "answer_checking")
    
    # Set the entry point
    workflow.set_entry_point("target_number_creation")
    # Set up memory storage for recording
    memory = MemorySaver()

    # Compile the graph
    app = workflow.compile(checkpointer=memory)

    return app
    