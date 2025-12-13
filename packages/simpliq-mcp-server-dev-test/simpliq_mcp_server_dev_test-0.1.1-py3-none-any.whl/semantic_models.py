"""Semantic Mapping Models.

This module defines the data models for the semantic mapping system,
which allows mapping business concepts to database structures.
"""

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime
import uuid


class ColumnMapping(BaseModel):
    """Mapping from business term to actual column name."""

    business_term: str = Field(..., description="Business-friendly name for the column")
    column_name: str = Field(..., description="Actual database column name")
    description: Optional[str] = Field(None, description="Description of what this column represents")


class EntityMapping(BaseModel):
    """Mapping for a database entity (table/view)."""

    concept: str = Field(..., description="Business concept name (e.g., 'cliente', 'pedido')")
    type: Literal["entity", "relationship"] = Field("entity", description="Type of mapping")
    table: str = Field(..., description="Database table or view name")
    schema: Optional[str] = Field(None, description="Database schema name")
    description: Optional[str] = Field(None, description="Description of the business concept")
    aliases: List[str] = Field(default_factory=list, description="Alternative names for this concept")
    column_mappings: Dict[str, str] = Field(
        default_factory=dict,
        description="Map business terms to column names"
    )

    @validator('concept')
    def concept_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Concept must not be empty')
        return v.strip().lower()

    @validator('table')
    def table_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Table name must not be empty')
        return v.strip()

    @validator('aliases', pre=True)
    def normalize_aliases(cls, v):
        if v is None:
            return []
        return [alias.strip().lower() for alias in v if alias and alias.strip()]


class RelationshipMapping(BaseModel):
    """Mapping for relationships between entities."""

    concept: str = Field(..., description="Relationship concept (e.g., 'comprou', 'pertence_a')")
    type: Literal["relationship"] = Field("relationship", description="Type of mapping")
    from_table: str = Field(..., description="Source table")
    to_table: str = Field(..., description="Target table")
    from_schema: Optional[str] = Field(None, description="Source schema")
    to_schema: Optional[str] = Field(None, description="Target schema")
    join_condition: str = Field(..., description="Join condition (e.g., 'customers.id = orders.customer_id')")
    description: Optional[str] = Field(None, description="Description of the relationship")
    aliases: List[str] = Field(default_factory=list, description="Alternative names for this relationship")

    @validator('concept')
    def concept_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Concept must not be empty')
        return v.strip().lower()


class SemanticMapping(BaseModel):
    """Complete semantic mapping entry."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique mapping ID")
    organization_id: str | None = Field(default="default", description="Organization that owns this mapping")
    connection_id: str = Field(..., description="Database connection this mapping applies to")
    concept: str = Field(..., description="Business concept name")
    type: Literal["entity", "relationship"] = Field(..., description="Type of mapping")

    # Entity-specific fields
    table: Optional[str] = Field(None, description="Table name (for entity mappings)")
    schema: Optional[str] = Field(None, description="Schema name (for entity mappings)")
    column_mappings: Dict[str, str] = Field(default_factory=dict, description="Column mappings")

    # Relationship-specific fields
    from_table: Optional[str] = Field(None, description="Source table (for relationships)")
    to_table: Optional[str] = Field(None, description="Target table (for relationships)")
    from_schema: Optional[str] = Field(None, description="Source schema (for relationships)")
    to_schema: Optional[str] = Field(None, description="Target schema (for relationships)")
    join_condition: Optional[str] = Field(None, description="Join condition (for relationships)")

    # Common fields
    description: Optional[str] = Field(None, description="Description of the concept")
    aliases: List[str] = Field(default_factory=list, description="Alternative names")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    version: int = Field(1, description="Version number for optimistic locking")

    @validator('concept')
    def concept_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Concept must not be empty')
        return v.strip().lower()

    @validator('aliases', pre=True)
    def normalize_aliases(cls, v):
        if v is None:
            return []
        return [alias.strip().lower() for alias in v if alias and alias.strip()]

    def validate_entity_fields(self):
        """Validate that entity mappings have required fields."""
        if self.type == "entity" and not self.table:
            raise ValueError("Entity mappings must have a table name")

    def validate_relationship_fields(self):
        """Validate that relationship mappings have required fields."""
        if self.type == "relationship":
            if not self.from_table or not self.to_table:
                raise ValueError("Relationship mappings must have from_table and to_table")
            if not self.join_condition:
                raise ValueError("Relationship mappings must have a join_condition")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SemanticCatalogData(BaseModel):
    """Complete catalog data structure for storage."""

    organization_id: str | None = Field(default="default", description="Organization ID")
    connection_id: str = Field(..., description="Connection ID")
    mappings: List[SemanticMapping] = Field(default_factory=list, description="All semantic mappings")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")
    version: str = Field("1.0", description="Catalog schema version")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MappingSearchResult(BaseModel):
    """Result of a concept search/resolution."""

    mapping: SemanticMapping = Field(..., description="The matched mapping")
    confidence: float = Field(..., description="Confidence score (0.0 to 1.0)")
    match_type: Literal["exact", "alias", "fuzzy"] = Field(..., description="Type of match found")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
