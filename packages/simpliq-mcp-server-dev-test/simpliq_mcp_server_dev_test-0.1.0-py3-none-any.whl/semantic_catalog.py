"""Semantic Catalog - Storage and retrieval of semantic mappings.

This module provides the SemanticCatalog class for managing semantic mappings
between business concepts and database structures.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
from fuzzywuzzy import fuzz, process

from semantic_models import (
    SemanticMapping,
    SemanticCatalogData,
    MappingSearchResult,
    EntityMapping,
    RelationshipMapping
)

logger = logging.getLogger(__name__)


class SemanticCatalog:
    """Manages semantic mappings for organizations and connections."""

    def __init__(self, storage_dir: str = "semantic_mappings"):
        """Initialize the semantic catalog.

        Args:
            storage_dir: Directory to store semantic mapping files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"SemanticCatalog initialized with storage_dir: {self.storage_dir}")

    def _get_catalog_file(self, organization_id: str | None, connection_id: str) -> Path:
        """Get the file path for a catalog.

        Args:
            organization_id: Organization ID (defaults to "default" if None)
            connection_id: Connection ID

        Returns:
            Path to the catalog file
        """
        # Use "default" if organization_id is None
        org_id = organization_id or "default"
        
        # Create org directory if it doesn't exist
        org_dir = self.storage_dir / org_id
        org_dir.mkdir(parents=True, exist_ok=True)

        # Return path to connection catalog file
        return org_dir / f"{connection_id}.json"

    def _load_catalog(self, organization_id: str, connection_id: str) -> SemanticCatalogData:
        """Load catalog from disk.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID

        Returns:
            SemanticCatalogData object
        """
        catalog_file = self._get_catalog_file(organization_id, connection_id)

        if not catalog_file.exists():
            # Return empty catalog
            return SemanticCatalogData(
                organization_id=organization_id,
                connection_id=connection_id,
                mappings=[]
            )

        try:
            with open(catalog_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return SemanticCatalogData(**data)
        except Exception as e:
            logger.error(f"Error loading catalog from {catalog_file}: {e}")
            # Return empty catalog on error
            return SemanticCatalogData(
                organization_id=organization_id,
                connection_id=connection_id,
                mappings=[]
            )

    def _save_catalog(self, catalog: SemanticCatalogData) -> None:
        """Save catalog to disk.

        Args:
            catalog: Catalog data to save
        """
        catalog_file = self._get_catalog_file(catalog.organization_id, catalog.connection_id)

        try:
            with open(catalog_file, 'w', encoding='utf-8') as f:
                json.dump(catalog.model_dump(), f, indent=2, default=str)
            logger.info(f"Catalog saved to {catalog_file}")
        except Exception as e:
            logger.error(f"Error saving catalog to {catalog_file}: {e}")
            raise

    def add_mapping(
        self,
        organization_id: str,
        connection_id: str,
        mapping: SemanticMapping
    ) -> SemanticMapping:
        """Add a new semantic mapping.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            mapping: Mapping to add

        Returns:
            The added mapping with ID assigned

        Raises:
            ValueError: If a mapping with the same concept already exists
        """
        catalog = self._load_catalog(organization_id, connection_id)

        # Check if concept already exists
        existing = self._find_exact_match(catalog.mappings, mapping.concept)
        if existing:
            raise ValueError(
                f"Mapping for concept '{mapping.concept}' already exists. "
                f"Use update_mapping to modify it."
            )

        # Set organization and connection IDs
        mapping.organization_id = organization_id
        mapping.connection_id = connection_id
        mapping.created_at = datetime.utcnow()
        mapping.updated_at = datetime.utcnow()

        # Validate based on type
        if mapping.type == "entity":
            mapping.validate_entity_fields()
        else:
            mapping.validate_relationship_fields()

        # Add to catalog
        catalog.mappings.append(mapping)

        # Save
        self._save_catalog(catalog)

        logger.info(f"Added mapping for concept '{mapping.concept}' in {organization_id}/{connection_id}")
        return mapping

    def get_mapping(
        self,
        organization_id: str,
        connection_id: str,
        mapping_id: str
    ) -> Optional[SemanticMapping]:
        """Get a specific mapping by ID.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            mapping_id: Mapping ID

        Returns:
            The mapping if found, None otherwise
        """
        catalog = self._load_catalog(organization_id, connection_id)

        for mapping in catalog.mappings:
            if mapping.id == mapping_id:
                return mapping

        return None

    def get_mappings(
        self,
        organization_id: str,
        connection_id: str,
        mapping_type: Optional[str] = None
    ) -> List[SemanticMapping]:
        """Get all mappings for an organization/connection.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            mapping_type: Optional filter by type ('entity' or 'relationship')

        Returns:
            List of mappings
        """
        catalog = self._load_catalog(organization_id, connection_id)

        if mapping_type:
            return [m for m in catalog.mappings if m.type == mapping_type]

        return catalog.mappings

    def update_mapping(
        self,
        organization_id: str,
        connection_id: str,
        mapping_id: str,
        updates: Dict
    ) -> SemanticMapping:
        """Update an existing mapping.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            mapping_id: Mapping ID to update
            updates: Dictionary of fields to update

        Returns:
            The updated mapping

        Raises:
            ValueError: If mapping not found
        """
        catalog = self._load_catalog(organization_id, connection_id)

        # Find the mapping
        mapping_idx = None
        for idx, mapping in enumerate(catalog.mappings):
            if mapping.id == mapping_id:
                mapping_idx = idx
                break

        if mapping_idx is None:
            raise ValueError(f"Mapping with ID '{mapping_id}' not found")

        # Update fields
        mapping = catalog.mappings[mapping_idx]
        mapping_dict = mapping.model_dump()

        # Don't allow updating these fields
        protected_fields = {'id', 'organization_id', 'connection_id', 'created_at'}
        for key, value in updates.items():
            if key not in protected_fields:
                mapping_dict[key] = value

        # Update timestamp and version
        mapping_dict['updated_at'] = datetime.utcnow()
        mapping_dict['version'] += 1

        # Create new mapping object
        updated_mapping = SemanticMapping(**mapping_dict)

        # Validate
        if updated_mapping.type == "entity":
            updated_mapping.validate_entity_fields()
        else:
            updated_mapping.validate_relationship_fields()

        # Replace in catalog
        catalog.mappings[mapping_idx] = updated_mapping

        # Save
        self._save_catalog(catalog)

        logger.info(f"Updated mapping '{mapping_id}' in {organization_id}/{connection_id}")
        return updated_mapping

    def delete_mapping(
        self,
        organization_id: str,
        connection_id: str,
        mapping_id: str
    ) -> bool:
        """Delete a mapping.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            mapping_id: Mapping ID to delete

        Returns:
            True if deleted, False if not found
        """
        catalog = self._load_catalog(organization_id, connection_id)

        # Find and remove the mapping
        original_count = len(catalog.mappings)
        catalog.mappings = [m for m in catalog.mappings if m.id != mapping_id]

        if len(catalog.mappings) == original_count:
            return False  # Not found

        # Save
        self._save_catalog(catalog)

        logger.info(f"Deleted mapping '{mapping_id}' from {organization_id}/{connection_id}")
        return True

    def resolve_concept(
        self,
        organization_id: str,
        connection_id: str,
        concept: str,
        fuzzy_threshold: int = 80
    ) -> Optional[MappingSearchResult]:
        """Resolve a business concept to a mapping.

        This method searches for mappings using:
        1. Exact concept match
        2. Alias match
        3. Fuzzy match (if threshold met)

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            concept: Business concept to search for
            fuzzy_threshold: Minimum fuzzy match score (0-100)

        Returns:
            MappingSearchResult if found, None otherwise
        """
        catalog = self._load_catalog(organization_id, connection_id)
        concept_normalized = concept.strip().lower()

        # 1. Try exact match
        exact = self._find_exact_match(catalog.mappings, concept_normalized)
        if exact:
            return MappingSearchResult(
                mapping=exact,
                confidence=1.0,
                match_type="exact"
            )

        # 2. Try alias match
        alias_match = self._find_alias_match(catalog.mappings, concept_normalized)
        if alias_match:
            return MappingSearchResult(
                mapping=alias_match,
                confidence=0.95,
                match_type="alias"
            )

        # 3. Try fuzzy match
        fuzzy_result = self._find_fuzzy_match(
            catalog.mappings,
            concept_normalized,
            fuzzy_threshold
        )
        if fuzzy_result:
            mapping, score = fuzzy_result
            return MappingSearchResult(
                mapping=mapping,
                confidence=score / 100.0,
                match_type="fuzzy"
            )

        return None

    def _find_exact_match(
        self,
        mappings: List[SemanticMapping],
        concept: str
    ) -> Optional[SemanticMapping]:
        """Find exact concept match."""
        for mapping in mappings:
            if mapping.concept == concept:
                return mapping
        return None

    def _find_alias_match(
        self,
        mappings: List[SemanticMapping],
        concept: str
    ) -> Optional[SemanticMapping]:
        """Find match in aliases."""
        for mapping in mappings:
            if concept in mapping.aliases:
                return mapping
        return None

    def _find_fuzzy_match(
        self,
        mappings: List[SemanticMapping],
        concept: str,
        threshold: int
    ) -> Optional[Tuple[SemanticMapping, int]]:
        """Find fuzzy match using string similarity.

        Args:
            mappings: List of mappings to search
            concept: Concept to match
            threshold: Minimum similarity score (0-100)

        Returns:
            Tuple of (mapping, score) if found, None otherwise
        """
        if not mappings:
            return None

        # Build list of concepts to match against
        choices = []
        mapping_dict = {}

        for mapping in mappings:
            # Add main concept
            choices.append(mapping.concept)
            mapping_dict[mapping.concept] = mapping

            # Add aliases
            for alias in mapping.aliases:
                choices.append(alias)
                mapping_dict[alias] = mapping

        # Find best match
        if not choices:
            return None

        result = process.extractOne(concept, choices, scorer=fuzz.ratio)

        if result and result[1] >= threshold:
            matched_text, score = result[0], result[1]
            return (mapping_dict[matched_text], score)

        return None

    def get_context(
        self,
        organization_id: str,
        connection_id: str
    ) -> Dict:
        """Get semantic context for LLM prompts.

        Returns a dictionary with all mappings formatted for LLM consumption.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID

        Returns:
            Dictionary with semantic context
        """
        mappings = self.get_mappings(organization_id, connection_id)

        entities = []
        relationships = []

        for mapping in mappings:
            if mapping.type == "entity":
                entities.append({
                    "concept": mapping.concept,
                    "table": mapping.table,
                    "schema": mapping.schema,
                    "description": mapping.description,
                    "aliases": mapping.aliases,
                    "columns": mapping.column_mappings
                })
            else:
                relationships.append({
                    "concept": mapping.concept,
                    "from": f"{mapping.from_schema + '.' if mapping.from_schema else ''}{mapping.from_table}",
                    "to": f"{mapping.to_schema + '.' if mapping.to_schema else ''}{mapping.to_table}",
                    "condition": mapping.join_condition,
                    "description": mapping.description,
                    "aliases": mapping.aliases
                })

        return {
            "entities": entities,
            "relationships": relationships,
            "total_mappings": len(mappings)
        }
