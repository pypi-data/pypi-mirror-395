# src/kl_exec_gateway/pipeline_registry.py

"""
Pipeline registry for managing and selecting pipelines.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .pipeline_types import Pipeline


class PipelineRegistry:
    """
    Registry for pipeline definitions.
    
    Manages a collection of pipelines by ID and provides lookup.
    """
    
    def __init__(self, pipelines: Optional[List[Pipeline]] = None) -> None:
        """
        Initialize registry with optional list of pipelines.
        
        Args:
            pipelines: List of Pipeline objects to register
        """
        self._by_id: Dict[str, Pipeline] = {}
        
        if pipelines:
            for pipeline in pipelines:
                self.register(pipeline)
    
    def register(self, pipeline: Pipeline) -> None:
        """
        Register a pipeline.
        
        Args:
            pipeline: Pipeline to register
            
        Raises:
            ValueError: If pipeline_id already exists
        """
        if pipeline.pipeline_id in self._by_id:
            raise ValueError(
                f"Pipeline with ID '{pipeline.pipeline_id}' already registered"
            )
        
        self._by_id[pipeline.pipeline_id] = pipeline
    
    def get(self, pipeline_id: str) -> Pipeline:
        """
        Get a pipeline by ID.
        
        Args:
            pipeline_id: ID of the pipeline
            
        Returns:
            Pipeline object
            
        Raises:
            KeyError: If pipeline_id not found
        """
        if pipeline_id not in self._by_id:
            available = ", ".join(self._by_id.keys())
            raise KeyError(
                f"Pipeline '{pipeline_id}' not found. "
                f"Available: {available}"
            )
        
        return self._by_id[pipeline_id]
    
    def list_ids(self) -> List[str]:
        """
        List all registered pipeline IDs.
        
        Returns:
            List of pipeline IDs
        """
        return list(self._by_id.keys())
    
    def has(self, pipeline_id: str) -> bool:
        """
        Check if a pipeline is registered.
        
        Args:
            pipeline_id: ID to check
            
        Returns:
            True if registered, False otherwise
        """
        return pipeline_id in self._by_id


def create_default_registry() -> PipelineRegistry:
    """
    Create a registry with built-in pipelines.
    
    Returns:
        PipelineRegistry with all BUILTIN_PIPELINES registered
    """
    from .pipelines import BUILTIN_PIPELINES
    
    return PipelineRegistry(pipelines=BUILTIN_PIPELINES)

