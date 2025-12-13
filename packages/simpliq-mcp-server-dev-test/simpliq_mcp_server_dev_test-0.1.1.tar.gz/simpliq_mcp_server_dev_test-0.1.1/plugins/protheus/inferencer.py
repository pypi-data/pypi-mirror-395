# -*- coding: utf-8 -*-
"""
Protheus Relationship Inference

Infers relationships between Protheus tables based on naming conventions
and data dictionary metadata.

Author: SimpliQ Development Team
Date: 2025-11-18
"""

from typing import Dict, List, Optional, Any, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class ProtheusRelationshipInferencer:
    """Infers relationships between Protheus tables."""

    def __init__(self, dictionary):
        """
        Initialize the relationship inferencer.

        Args:
            dictionary: ProtheusDataDictionary instance
        """
        self.dictionary = dictionary

        # Known Protheus table patterns for relationships
        self.known_patterns = self._initialize_known_patterns()

    def _initialize_known_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize known relationship patterns in Protheus.

        Returns:
            Dictionary of known patterns
        """
        return {
            # Cliente patterns
            "CLIENTE": {
                "suffixes": ["CLIENTE", "CLIEN", "CLI"],
                "loja_suffix": "LOJA",
                "target_table": "SA1",
                "target_key": ["A1_COD", "A1_LOJA"],
                "description": "Cliente"
            },
            # Fornecedor patterns
            "FORNECE": {
                "suffixes": ["FORNECE", "FORNEC", "FORN"],
                "loja_suffix": "LOJA",
                "target_table": "SA2",
                "target_key": ["A2_COD", "A2_LOJA"],
                "description": "Fornecedor"
            },
            # Produto patterns
            "PRODUTO": {
                "suffixes": ["PRODUTO", "PROD", "COD"],
                "loja_suffix": None,
                "target_table": "SB1",
                "target_key": ["B1_COD"],
                "description": "Produto"
            },
            # Filial patterns
            "FILIAL": {
                "suffixes": ["FILIAL", "FIL"],
                "loja_suffix": None,
                "target_table": "SM0",
                "target_key": ["M0_CODFIL"],
                "description": "Filial"
            },
            # Tipo de Contrato
            "TPCTO": {
                "suffixes": ["TPCTO"],
                "loja_suffix": None,
                "target_table": "CN1",
                "target_key": ["CN1_CODIGO"],
                "description": "Tipo de Contrato"
            }
        }

    def infer_relationships(
        self,
        entities: List[Dict[str, Any]],
        company: str = "010"
    ) -> List[Dict[str, Any]]:
        """
        Infer relationships between entities based on Protheus conventions.

        Args:
            entities: List of entity mappings
            company: Company code

        Returns:
            List of relationship mappings
        """
        relationships = []

        logger.info(f"Inferring relationships for {len(entities)} entities")

        # Build entity lookup for quick access
        entity_lookup = {e['alias']: e for e in entities}

        for entity in entities:
            try:
                entity_relationships = self._infer_entity_relationships(
                    entity,
                    entity_lookup,
                    company
                )
                relationships.extend(entity_relationships)
            except Exception as e:
                logger.error(f"Error inferring relationships for {entity.get('alias')}: {e}")

        logger.info(f"Inferred {len(relationships)} relationships")
        return relationships

    def _infer_entity_relationships(
        self,
        entity: Dict[str, Any],
        entity_lookup: Dict[str, Dict],
        company: str
    ) -> List[Dict[str, Any]]:
        """
        Infer relationships for a single entity.

        Args:
            entity: Entity mapping
            entity_lookup: Lookup dict of all entities by alias
            company: Company code

        Returns:
            List of relationship mappings for this entity
        """
        relationships = []
        table_alias = entity['alias']

        # Get columns for this entity
        columns = self.dictionary.get_columns(table_alias, company)

        # Analyze each column for relationship hints
        for column in columns:
            column_name = column['column_name']

            # Check for known patterns
            for pattern_name, pattern_config in self.known_patterns.items():
                relationship = self._check_pattern_match(
                    entity,
                    column,
                    pattern_config,
                    entity_lookup,
                    company
                )
                if relationship:
                    relationships.append(relationship)

        return relationships

    def _check_pattern_match(
        self,
        from_entity: Dict[str, Any],
        column: Dict[str, Any],
        pattern_config: Dict[str, Any],
        entity_lookup: Dict[str, Dict],
        company: str
    ) -> Optional[Dict[str, Any]]:
        """
        Check if a column matches a known relationship pattern.

        Args:
            from_entity: Source entity
            column: Column metadata
            pattern_config: Pattern configuration
            entity_lookup: Entity lookup dict
            company: Company code

        Returns:
            Relationship mapping if match found, None otherwise
        """
        column_name = column['column_name']
        # In Protheus, table SC7 has columns C7_xxx, SA1 has A1_xxx, etc.
        # Column prefix is the last 2-3 chars of table alias (e.g., "C7" from "SC7", "A1" from "SA1")
        table_prefix = from_entity['alias'][1:]  # e.g., "C7" from "SC7", "A1" from "SA1"

        # Extract column suffix (part after prefix + underscore)
        # E.g., "C7_FORNECE" -> "FORNECE"
        match = re.match(rf'{table_prefix}_(.+)', column_name)
        if not match:
            return None

        column_suffix = match.group(1)

        # Check if column suffix matches any of the pattern suffixes
        for pattern_suffix in pattern_config['suffixes']:
            if column_suffix.startswith(pattern_suffix):
                # Found a match!
                target_table_alias = pattern_config['target_table']

                # Build full target table name with company
                target_table_full = f"{target_table_alias}{company}"

                # Check if target table exists in our entities
                if target_table_alias not in entity_lookup:
                    logger.debug(f"Target table {target_table_alias} not in entity list, skipping")
                    return None

                target_entity = entity_lookup[target_table_alias]

                # Build join condition
                loja_suffix = pattern_config.get('loja_suffix')
                if loja_suffix:
                    # Multi-column key (e.g., FORNECE + LOJA)
                    # Check if loja column exists
                    entity_columns = self.dictionary.get_columns(from_entity['alias'], company)
                    has_loja = any(c['column_name'] == f"{table_prefix}_{loja_suffix}" for c in entity_columns)

                    if has_loja and len(pattern_config['target_key']) >= 2:
                        join_condition = (
                            f"{from_entity['alias']}.{column_name} = "
                            f"{target_table_alias}.{pattern_config['target_key'][0]} AND "
                            f"{from_entity['alias']}.{table_prefix}_{loja_suffix} = "
                            f"{target_table_alias}.{pattern_config['target_key'][1]}"
                        )
                    else:
                        # Single key
                        join_condition = (
                            f"{from_entity['alias']}.{column_name} = "
                            f"{target_table_alias}.{pattern_config['target_key'][0]}"
                        )
                else:
                    # Single column key
                    join_condition = (
                        f"{from_entity['alias']}.{column_name} = "
                        f"{target_table_alias}.{pattern_config['target_key'][0]}"
                    )

                # Create relationship mapping
                concept = f"{from_entity['concept']}_{pattern_config['description'].lower().replace(' ', '_')}"

                relationship = {
                    "concept": concept,
                    "type": "relationship",
                    "from_table": from_entity['table'],
                    "from_alias": from_entity['alias'],
                    "to_table": target_entity['table'],
                    "to_alias": target_table_alias,
                    "join_condition": join_condition,
                    "relationship_type": "many-to-one",
                    "description": f"{from_entity['description']} → {pattern_config['description']}",
                    "metadata": {
                        "source": "protheus_inference",
                        "pattern": pattern_suffix,
                        "confidence": "high",
                        "inferred_from": column_name
                    }
                }

                logger.debug(f"Inferred relationship: {concept}")
                return relationship

        return None

    def infer_from_foreign_key_patterns(
        self,
        from_entity: Dict[str, Any],
        entity_lookup: Dict[str, Dict],
        company: str
    ) -> List[Dict[str, Any]]:
        """
        Infer relationships based on generic FK patterns.

        Looks for columns that match patterns like:
        - {PREFIX}_COD + {PREFIX}_LOJA pointing to S{PREFIX}
        - Fields with F3 lookup references

        Args:
            from_entity: Source entity
            entity_lookup: Entity lookup dict
            company: Company code

        Returns:
            List of inferred relationships
        """
        relationships = []
        columns = self.dictionary.get_columns(from_entity['alias'], company)

        # Group columns by potential FK sets (e.g., COD + LOJA)
        fk_candidates = {}

        for column in columns:
            # Check for F3 lookup (foreign key hint in Protheus)
            if column.get('lookup'):
                lookup_table = self._extract_lookup_table(column['lookup'])
                if lookup_table and lookup_table in entity_lookup:
                    relationship = self._create_lookup_relationship(
                        from_entity,
                        column,
                        lookup_table,
                        entity_lookup[lookup_table]
                    )
                    if relationship:
                        relationships.append(relationship)

        return relationships

    def _extract_lookup_table(self, f3_code: str) -> Optional[str]:
        """
        Extract target table from F3 lookup code.

        Args:
            f3_code: F3 code from SX3 (e.g., "SA1", "SA2")

        Returns:
            Table alias if valid, None otherwise
        """
        # F3 codes often directly reference tables
        # Examples: "SA1", "SA2", "SB1"
        if f3_code and len(f3_code) >= 3:
            # Check if it looks like a table alias
            if re.match(r'S[A-Z]\d?', f3_code):
                return f3_code[:3]  # Return first 3 chars (e.g., "SA1")
        return None

    def _create_lookup_relationship(
        self,
        from_entity: Dict[str, Any],
        column: Dict[str, Any],
        target_alias: str,
        target_entity: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create relationship from F3 lookup.

        Args:
            from_entity: Source entity
            column: Column with F3 lookup
            target_alias: Target table alias
            target_entity: Target entity mapping

        Returns:
            Relationship mapping
        """
        column_name = column['column_name']

        # Simple join condition (may need refinement)
        join_condition = (
            f"{from_entity['alias']}.{column_name} = "
            f"{target_alias}.{target_alias[1:]}_COD"  # e.g., SA1 -> A1_COD
        )

        concept = f"{from_entity['concept']}_{target_entity['concept']}"

        return {
            "concept": concept,
            "type": "relationship",
            "from_table": from_entity['table'],
            "from_alias": from_entity['alias'],
            "to_table": target_entity['table'],
            "to_alias": target_alias,
            "join_condition": join_condition,
            "relationship_type": "many-to-one",
            "description": f"{from_entity['description']} → {target_entity['description']}",
            "metadata": {
                "source": "protheus_inference",
                "pattern": "f3_lookup",
                "confidence": "medium",
                "inferred_from": column_name,
                "f3_code": column.get('lookup')
            }
        }

    def validate_relationships(
        self,
        relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate inferred relationships and remove duplicates.

        Args:
            relationships: List of relationship mappings

        Returns:
            Validated and deduplicated relationships
        """
        # Remove duplicates based on from_table + to_table + join_condition
        seen = set()
        validated = []

        for rel in relationships:
            key = (
                rel['from_table'],
                rel['to_table'],
                rel['join_condition']
            )

            if key not in seen:
                seen.add(key)
                validated.append(rel)
            else:
                logger.debug(f"Skipping duplicate relationship: {rel['concept']}")

        logger.info(f"Validated {len(validated)} unique relationships from {len(relationships)} inferred")
        return validated

    def get_relationship_statistics(
        self,
        relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get statistics about inferred relationships.

        Args:
            relationships: List of relationship mappings

        Returns:
            Statistics dictionary
        """
        stats = {
            "total": len(relationships),
            "by_pattern": {},
            "by_confidence": {},
            "by_type": {}
        }

        for rel in relationships:
            # Count by pattern
            pattern = rel.get('metadata', {}).get('pattern', 'unknown')
            stats['by_pattern'][pattern] = stats['by_pattern'].get(pattern, 0) + 1

            # Count by confidence
            confidence = rel.get('metadata', {}).get('confidence', 'unknown')
            stats['by_confidence'][confidence] = stats['by_confidence'].get(confidence, 0) + 1

            # Count by relationship type
            rel_type = rel.get('relationship_type', 'unknown')
            stats['by_type'][rel_type] = stats['by_type'].get(rel_type, 0) + 1

        return stats
