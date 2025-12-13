"""
Flow Builder for creating BullMQ-like job flows and dependencies.

This module provides utilities for creating complex job dependencies,
similar to BullMQ's FlowProducer functionality.
"""
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class JobNode:
    """
    Represents a job node in a flow.
    
    Similar to BullMQ's job flow nodes, this allows defining jobs
    with dependencies and creating complex job graphs.
    """
    queue_name: str
    job_name: str
    data: Dict[str, Any]
    opts: Dict[str, Any] = field(default_factory=dict)
    children: List['JobNode'] = field(default_factory=list)
    
    def add_child(self, child: 'JobNode') -> 'JobNode':
        """
        Add a child job to this node.
        
        Args:
            child: Child JobNode to add
            
        Returns:
            The child node for chaining
        """
        self.children.append(child)
        return child
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the job node to a dictionary representation.
        
        Returns:
            Dictionary with job definition and children
        """
        return {
            'queue_name': self.queue_name,
            'job_name': self.job_name,
            'data': self.data,
            'opts': self.opts,
            'children': [child.to_dict() for child in self.children]
        }


class FlowBuilder:
    """
    Builder for creating job flows with dependencies.
    
    This class mimics BullMQ's FlowProducer pattern, allowing you to
    create complex job graphs with parent-child relationships.
    
    Example:
        ```python
        flow = FlowBuilder()
        parent = flow.add_job('parent-queue', 'parent-job', {'data': 'parent'})
        child1 = flow.add_child(parent, 'child-queue', 'child-1', {'data': 'child1'})
        child2 = flow.add_child(parent, 'child-queue', 'child-2', {'data': 'child2'})
        
        # Execute the flow using QueueManager
        job_ids = await flow.execute(queue_manager)
        ```
    """
    
    def __init__(self):
        """Initialize the flow builder."""
        self.root_jobs: List[JobNode] = []
        self._all_nodes: List[JobNode] = []
    
    def add_job(
        self,
        queue_name: str,
        job_name: str,
        data: Dict[str, Any],
        opts: Optional[Dict[str, Any]] = None
    ) -> JobNode:
        """
        Add a root job to the flow.
        
        Args:
            queue_name: Queue to add job to
            job_name: Name/type of the job
            data: Job data/payload
            opts: Optional job options
            
        Returns:
            JobNode that can be used to add children
        """
        node = JobNode(
            queue_name=queue_name,
            job_name=job_name,
            data=data,
            opts=opts or {}
        )
        self.root_jobs.append(node)
        self._all_nodes.append(node)
        return node
    
    def add_child(
        self,
        parent: JobNode,
        queue_name: str,
        job_name: str,
        data: Dict[str, Any],
        opts: Optional[Dict[str, Any]] = None
    ) -> JobNode:
        """
        Add a child job to a parent job node.
        
        Args:
            parent: Parent JobNode
            queue_name: Queue to add child job to
            job_name: Name/type of the child job
            data: Job data/payload
            opts: Optional job options
            
        Returns:
            Child JobNode that can be used to add more children
        """
        child = JobNode(
            queue_name=queue_name,
            job_name=job_name,
            data=data,
            opts=opts or {}
        )
        parent.add_child(child)
        self._all_nodes.append(child)
        return child
    
    async def execute(self, queue_manager: Any) -> Dict[str, List[str]]:
        """
        Execute the flow by adding all jobs to their respective queues.
        
        Jobs are added bottom-up (children first, then parents) to ensure
        that parent jobs can reference their children.
        
        Args:
            queue_manager: QueueManager instance to use for adding jobs
            
        Returns:
            Dictionary mapping queue names to lists of job IDs
            
        Raises:
            Exception: If job creation fails
        """
        job_ids_by_queue: Dict[str, List[str]] = {}
        job_id_map: Dict[int, str] = {}  # Map node id to job ID
        
        # Execute bottom-up (leaf nodes first)
        for node in self._traverse_bottom_up():
            # Add child job IDs to opts if there are children
            if node.children:
                child_ids = [job_id_map[id(child)] for child in node.children]
                node.opts['children'] = child_ids
            
            # Add the job
            job_id = await queue_manager.safe_add_job(
                node.queue_name,
                node.job_name,
                node.data,
                node.opts
            )
            
            # Track the job ID
            job_id_map[id(node)] = job_id
            
            if node.queue_name not in job_ids_by_queue:
                job_ids_by_queue[node.queue_name] = []
            job_ids_by_queue[node.queue_name].append(job_id)
            
            logger.info(
                f"Added job {job_id} to queue '{node.queue_name}' "
                f"with {len(node.children)} children"
            )
        
        return job_ids_by_queue
    
    def _traverse_bottom_up(self) -> List[JobNode]:
        """
        Traverse the job graph bottom-up (children before parents).
        
        Returns:
            List of job nodes in bottom-up order
        """
        visited = set()
        result = []
        
        def visit(node: JobNode):
            if id(node) in visited:
                return
            
            # Visit children first
            for child in node.children:
                visit(child)
            
            # Then visit this node
            visited.add(id(node))
            result.append(node)
        
        # Visit all root nodes
        for root in self.root_jobs:
            visit(root)
        
        return result
    
    def get_all_nodes(self) -> List[JobNode]:
        """
        Get all job nodes in the flow.
        
        Returns:
            List of all JobNode instances
        """
        return self._all_nodes.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entire flow to a dictionary representation.
        
        Returns:
            Dictionary with flow structure
        """
        return {
            'root_jobs': [job.to_dict() for job in self.root_jobs],
            'total_jobs': len(self._all_nodes)
        }


class BullMQHelpers:
    """
    Helper methods that mimic common BullMQ patterns.
    
    This class provides utility methods for common job management tasks
    that mimic BullMQ's functionality.
    """
    
    @staticmethod
    async def add_job_with_retry(
        queue_manager: Any,
        queue_name: str,
        job_name: str,
        data: Dict[str, Any],
        max_attempts: int = 3,
        backoff_delay: int = 1000
    ) -> str:
        """
        Add a job with automatic retry configuration.
        
        This mimics BullMQ's retry options.
        
        Args:
            queue_manager: QueueManager instance
            queue_name: Queue to add job to
            job_name: Name/type of job
            data: Job data
            max_attempts: Maximum retry attempts
            backoff_delay: Delay between retries in milliseconds
            
        Returns:
            Job ID
        """
        opts = {
            'attempts': max_attempts,
            'backoff': {
                'type': 'exponential',
                'delay': backoff_delay
            }
        }
        
        return await queue_manager.safe_add_job(
            queue_name, job_name, data, opts
        )
    
    @staticmethod
    async def add_delayed_job(
        queue_manager: Any,
        queue_name: str,
        job_name: str,
        data: Dict[str, Any],
        delay_ms: int
    ) -> str:
        """
        Add a job with a delay before processing.
        
        This mimics BullMQ's delay option.
        
        Args:
            queue_manager: QueueManager instance
            queue_name: Queue to add job to
            job_name: Name/type of job
            data: Job data
            delay_ms: Delay in milliseconds
            
        Returns:
            Job ID
        """
        opts = {'delay': delay_ms}
        
        return await queue_manager.safe_add_job(
            queue_name, job_name, data, opts
        )
    
    @staticmethod
    async def add_job_with_priority(
        queue_manager: Any,
        queue_name: str,
        job_name: str,
        data: Dict[str, Any],
        priority: int = 0
    ) -> str:
        """
        Add a job with a specific priority.
        
        This mimics BullMQ's priority option.
        Higher priority jobs are processed first.
        
        Args:
            queue_manager: QueueManager instance
            queue_name: Queue to add job to
            job_name: Name/type of job
            data: Job data
            priority: Job priority (higher = more important)
            
        Returns:
            Job ID
        """
        opts = {'priority': priority}
        
        return await queue_manager.safe_add_job(
            queue_name, job_name, data, opts
        )
