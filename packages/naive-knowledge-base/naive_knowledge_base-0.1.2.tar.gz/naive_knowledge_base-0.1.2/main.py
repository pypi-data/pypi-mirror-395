from requests import RequestException
from smolagents import CodeAgent, ToolCallingAgent
from api_models import FlowApiModel
from tools import save_content_to_file, read_file_content, delete_folder_or_file, generate_folder_tree
import dotenv
import sys
from agents.dependency_graph import generate_dependency_graph
dotenv.load_dotenv()

model = FlowApiModel(
    model_id="gpt-4.1",
    temperature=0.5,
)

dependency_graph_agent = ToolCallingAgent(
    tools=[
        generate_dependency_graph,
    ],
    planning_interval=1,
    final_answer_checks=[],
    model=FlowApiModel(
        model_id="gpt-4.1",
        temperature=0.4,
    ),
    max_steps=7,
    name="dependency_graph_agent",
    description="Generates a dependency graph for the given source directory.",
)

manager_agent = CodeAgent(
    managed_agents=[dependency_graph_agent],
    model=FlowApiModel(
        model_id="gpt-4.1",
    ),
    tools=[read_file_content, save_content_to_file, delete_folder_or_file, generate_folder_tree],
    additional_authorized_imports=[
        "os",
        "json",
        "pandas",
        "numpy",
        "pathlib",
        "ast",
        "re",
        "networkx",
        "collections",
    ],
    planning_interval=3,
    max_steps=30,
    name="tech_lead_agent",
    description="This agent is responsible for building and analyzing dependency graphs from source code. It analyzes code files, extracts dependencies, and creates comprehensive dependency graphs with metrics and relationships.",
)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_directory>", file=sys.stderr)
        sys.exit(1)
    
    source_directory = sys.argv[1]
    file_extensions = sys.argv[2] if len(sys.argv) > 2 else "java"
    ignore_dirs = sys.argv[3] if len(sys.argv) > 3 else "target,.git,test,node_modules,Pods"
    print("Running main agent...")
    try:
        result = manager_agent.run(f"""
Tasks:
1. Generate the tree and dependency graph of the {file_extensions} files in the source: {source_directory}. Make sure to ignore the {ignore_dirs} directories.
        """.strip())
    except Exception as e:
        print(f"Error running main agent: {e}", file=sys.stderr)