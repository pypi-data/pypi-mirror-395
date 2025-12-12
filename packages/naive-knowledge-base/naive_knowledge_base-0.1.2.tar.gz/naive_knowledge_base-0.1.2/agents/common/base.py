from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from smolagents import Tool, CodeAgent, ToolCallingAgent

from .logging import get_logger

logger = get_logger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the refactor system.
    
    This class defines the common interface that all agents must implement.
    """
    
    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Run the agent with the provided input data.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Agent output
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the agent name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the agent description."""
        pass

class AnalysisAgent(BaseAgent):
    """
    Base class for agents that analyze code.
    
    These agents are responsible for analyzing code and providing information about it.
    """
    
    @abstractmethod
    def analyze(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Analyze the code in the given file.
        
        Args:
            file_path: Path to the file to analyze
            **kwargs: Additional arguments for the analysis
            
        Returns:
            Analysis results
        """
        pass

class RefactoringAgent(BaseAgent):
    """
    Base class for agents that refactor code.
    
    These agents are responsible for refactoring code based on analysis results.
    """
    
    @abstractmethod
    def generate_plan(self, file_path: str, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a refactoring plan for the given file based on analysis results.
        
        Args:
            file_path: Path to the file to refactor
            analysis_results: Results from analysis agents
            
        Returns:
            Refactoring plan
        """
        pass
        
    @abstractmethod
    def execute_plan(self, file_path: str, plan: str) -> bool:
        """
        Execute a refactoring plan on the given file.
        
        Args:
            file_path: Path to the file to refactor
            plan: Refactoring plan
            
        Returns:
            True if successful, False otherwise
        """
        pass

class SmolagentsAdapter(BaseAgent):
    """
    Adapter class for smolagents agents.
    
    This class adapts smolagents agents to our BaseAgent interface.
    """
    
    def __init__(self, agent: Union[CodeAgent, ToolCallingAgent]):
        """
        Initialize the adapter.
        
        Args:
            agent: The smolagents agent to adapt
        """
        self._agent = agent
    
    def run(self, input_data: Any) -> Any:
        """
        Run the smolagents agent.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Agent output
        """
        return self._agent.run(input_data)
    
    @property
    def name(self) -> str:
        """Get the agent name."""
        return self._agent.name
    
    @property
    def description(self) -> str:
        """Get the agent description."""
        return self._agent.description
    
    @property
    def agent(self) -> Union[CodeAgent, ToolCallingAgent]:
        """Get the underlying smolagents agent."""
        return self._agent

class AgentFactory:
    """
    Factory class for creating agents.
    
    This class provides methods for creating different types of agents.
    """
    
    @staticmethod
    def create_analysis_agent(agent_type: str, **kwargs) -> AnalysisAgent:
        """
        Create an analysis agent of the specified type.
        
        Args:
            agent_type: Type of analysis agent to create
            **kwargs: Additional arguments for the agent
            
        Returns:
            An instance of the requested analysis agent
            
        Raises:
            ValueError: If the agent type is not supported
        """
        # Import here to avoid circular imports
        from agents.sonar import create_sonar_agent
        from agents.dependency_graph import create_dependency_graph_agent
        
        if agent_type == "sonar":
            return create_sonar_agent(**kwargs)
        elif agent_type == "dependency_graph":
            return create_dependency_graph_agent(**kwargs)
        else:
            raise ValueError(f"Unsupported analysis agent type: {agent_type}")
    
    @staticmethod
    def create_refactoring_agent(**kwargs) -> RefactoringAgent:
        """
        Create a refactoring agent.
        
        Args:
            **kwargs: Additional arguments for the agent
            
        Returns:
            An instance of the refactoring agent
        """
        # Import here to avoid circular imports
        from agents.coder import create_coder_agent
        
        return create_coder_agent(**kwargs)