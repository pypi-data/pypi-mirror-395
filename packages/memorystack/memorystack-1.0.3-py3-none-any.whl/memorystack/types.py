"""Type definitions for Memory OS SDK"""

from typing import List, Dict, Any, Optional, Union, Literal
from dataclasses import dataclass


MessageRole = Literal["user", "assistant", "system"]


@dataclass
class TextPart:
    """Text content part"""
    type: Literal["text"] = "text"
    text: str = ""


@dataclass
class ImagePart:
    """Image content part"""
    type: Literal["image"] = "image"
    data: str = ""  # base64 encoded
    mime_type: str = ""


@dataclass
class DocumentPart:
    """Document content part"""
    type: Literal["document"] = "document"
    data: str = ""  # base64 encoded
    mime_type: Optional[str] = None


@dataclass
class AudioPart:
    """Audio content part"""
    type: Literal["audio"] = "audio"
    data: str = ""  # base64 encoded
    mime_type: Optional[str] = None


MessagePart = Union[TextPart, ImagePart, DocumentPart, AudioPart]
MessageContent = Union[str, MessagePart, List[MessagePart]]


@dataclass
class Message:
    """Message in a conversation"""
    role: MessageRole
    content: MessageContent


@dataclass
class CreateMemoryRequest:
    """Request to create new memories"""
    messages: List[Message]
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CreateMemoryResponse:
    """Response from creating memories"""
    success: bool
    memories_created: int
    memory_ids: List[str]
    owner_id: str
    user_id: Optional[str]
    message: Optional[str] = None
    agent_id: Optional[str] = None
    project_id: Optional[str] = None


@dataclass
class Memory:
    """Memory object with dict-like access support"""
    id: str
    owner_clerk_id: str
    end_user_id: Optional[str]
    content: str
    memory_type: str
    confidence: float
    metadata: Dict[str, Any]
    source_type: str
    created_at: str
    updated_at: str
    embedding: Optional[List[float]] = None
    
    def __getitem__(self, key: str) -> Any:
        """Support dict-like access for backwards compatibility"""
        return getattr(self, key)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Support dict.get() for backwards compatibility"""
        return getattr(self, key, default)


@dataclass
class ListMemoriesRequest:
    """Request to list memories"""
    user_id: Optional[str] = None
    limit: int = 20
    cursor: Optional[str] = None
    order: Literal["asc", "desc"] = "desc"
    memory_type: Optional[str] = None
    min_confidence: Optional[float] = None
    include_embedding: bool = False


@dataclass
class ListMemoriesResponse:
    """Response from listing memories"""
    success: bool
    count: int
    next_cursor: Optional[str]
    results: List[Memory]


@dataclass
class UsageStats:
    """Usage statistics"""
    success: bool
    owner_id: str
    plan_tier: Optional[str]
    totals: Dict[str, int]
    usage: Dict[str, int]
    storage: Dict[str, int]


@dataclass
class GraphNode:
    """Graph node"""
    id: str
    label: str
    type: Literal["owner", "enduser", "memory"]
    group: int
    content: Optional[str] = None


@dataclass
class GraphLink:
    """Graph link/edge"""
    source: str
    target: str
    label: str


@dataclass
class GraphData:
    """Knowledge graph data"""
    nodes: List[GraphNode]
    links: List[GraphLink]
    error: Optional[str] = None


# Search modes:
# - hybrid (default): RRF-based fusion of vector + text search - best for general queries
# - vector: Pure semantic similarity search - best for conceptual queries
# - text: Pure keyword/text search - best for exact term matching
# - graph: Full graph-enhanced search with entity extraction - best for complex multi-hop queries
SearchMode = Literal["hybrid", "vector", "text", "graph"]


@dataclass
class SearchMemoriesResponse:
    """Response from searching memories"""
    success: bool
    count: int
    mode: SearchMode
    results: List[Memory]
    graph_search_used: Optional[bool] = None
    entity_boosted_results: Optional[int] = None
    relationship_boosted_results: Optional[int] = None


@dataclass
class Contradiction:
    """Contradiction detection result"""
    memory_id: str
    content: str
    confidence: float
    created_at: str
    similarity: float
    contradiction_type: str
    explanation: str


@dataclass
class DetectContradictionsResponse:
    """Response from contradiction detection"""
    success: bool
    has_contradictions: bool
    contradictions: List[Contradiction]
    suggested_resolution: str
    reasoning: str


@dataclass
class UpdateBeliefResponse:
    """Response from belief update"""
    success: bool
    action_taken: str
    original_memory_id: str
    new_memory_id: Optional[str] = None
    updated_memory: Dict[str, Any] = None
    reasoning: str = ""
    metadata: Dict[str, Any] = None


@dataclass
class ProvenanceEvent:
    """Provenance event in memory lineage"""
    event_type: str
    memory_id: str
    related_memory_ids: Optional[List[str]] = None
    actor: str = "system"
    action_details: Dict[str, Any] = None
    timestamp: str = ""


@dataclass
class AncestorMemory:
    """Ancestor memory in lineage"""
    memory_id: str
    content: str
    relationship: str
    timestamp: str


@dataclass
class DescendantMemory:
    """Descendant memory in lineage"""
    memory_id: str
    content: str
    relationship: str
    timestamp: str


@dataclass
class MemoryLineageResponse:
    """Response from memory lineage query"""
    success: bool
    memory_id: str
    current_content: str
    current_confidence: float
    created_at: str
    lineage: List[Dict[str, Any]]
    ancestors: List[Dict[str, Any]]
    descendants: List[Dict[str, Any]]


@dataclass
class BatchJob:
    """Batch job information"""
    id: str
    job_type: str
    status: Literal["pending", "running", "completed", "failed", "cancelled"]
    total_items: int
    processed_items: int
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    estimated_completion: Optional[str] = None


@dataclass
class BatchJobResponse:
    """Response from batch job status"""
    success: bool
    job: Dict[str, Any]  # BatchJob as dict for easier deserialization


@dataclass
class CreateMemoriesBatchResponse:
    """Response from batch memory creation"""
    success: bool
    created: int
    failed: int
    total: int
    memory_ids: List[str]
    embedding_generation: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingStatistics:
    """Embedding statistics"""
    total_memories: int
    with_embeddings: int
    missing_embeddings: int
    coverage_percent: float


@dataclass
class EmbeddingStatisticsResponse:
    """Response from embedding statistics"""
    success: bool
    statistics: EmbeddingStatistics
    recommendation: str


@dataclass
class ReflectionResponse:
    """Response from reflection operation"""
    success: bool
    insights_generated: Optional[int] = None
    patterns_detected: Optional[int] = None
    batch_job_id: Optional[str] = None
    mode: Optional[Literal["sync", "async"]] = None
    estimated_completion: Optional[str] = None
    message: Optional[str] = None


@dataclass
class ConsolidationResponse:
    """Response from consolidation operation"""
    success: bool
    memories_merged: Optional[int] = None
    duplicates_found: Optional[int] = None
    batch_job_id: Optional[str] = None
    mode: Optional[Literal["sync", "async"]] = None
    estimated_completion: Optional[str] = None
    message: Optional[str] = None


@dataclass
class DeleteMemoryResponse:
    """Response from deleting a memory"""
    success: bool
    deleted_count: int
    hard_delete: bool


@dataclass
class ListAgentMemoriesResponse:
    """Response from listing agent memories"""
    success: bool
    count: int
    data: List[Memory]
    next_cursor: Optional[str] = None

