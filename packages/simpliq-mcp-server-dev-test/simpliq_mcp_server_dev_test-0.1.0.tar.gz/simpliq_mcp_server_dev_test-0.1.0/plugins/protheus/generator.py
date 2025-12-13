# -*- coding: utf-8 -*-
"""
Protheus Semantic Mapping Generator

Generates semantic mappings from Protheus data dictionary.

Author: SimpliQ Development Team
Date: 2025-11-18
"""

from typing import Dict, List, Optional, Any, Callable
import re
import logging
from .dictionary import ProtheusDataDictionary
from .inferencer import ProtheusRelationshipInferencer

logger = logging.getLogger(__name__)


class ProtheusSemanticGenerator:
    """Generates semantic mappings from Protheus dictionary."""

    def __init__(self, connection, semantic_catalog):
        """
        Initialize the semantic generator.

        Args:
            connection: SQLAlchemy engine/connection
            semantic_catalog: SemanticCatalog instance
        """
        self.dictionary = ProtheusDataDictionary(connection)
        self.catalog = semantic_catalog
        self.connection = connection
        self.inferencer = ProtheusRelationshipInferencer(self.dictionary)

    def generate_mappings(
        self,
        organization_id: str,
        connection_id: str,
        modules: Optional[List[str]] = None,
        companies: Optional[List[str]] = None,
        dry_run: bool = False,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Generate semantic mappings from Protheus dictionary.

        Args:
            organization_id: Organization ID
            connection_id: Connection ID
            modules: List of modules to map (e.g., ["SIGAFIN", "SIGAEST"])
                    If None, maps all available modules
            companies: List of company codes (e.g., ["010", "030"])
                      If None, uses default company "010"
            dry_run: If True, return preview without creating mappings
            progress_callback: Optional callback for progress reporting
                             Called with (message, current, total)

        Returns:
            Dictionary with generation results:
            {
                "entities": [...],
                "relationships": [...],
                "errors": [...],
                "summary": {...}
            }
        """
        results = {
            "entities": [],
            "relationships": [],
            "errors": [],
            "summary": {}
        }

        companies_list = companies or ["010"]
        modules_list = modules or self._get_default_modules()

        logger.info(f"Generating mappings for modules: {modules_list}, companies: {companies_list}")

        # Calculate total work for progress reporting
        total_tables = 0
        for module in modules_list:
            for company in companies_list:
                try:
                    module_tables = self.dictionary.get_module_tables(module, company)
                    total_tables += len(module_tables)
                except:
                    pass

        current_table = 0

        # Generate entity mappings
        for module in modules_list:
            for company in companies_list:
                try:
                    if progress_callback:
                        progress_callback(f"📋 Lendo tabelas do módulo {module}/{company}...", current_table, total_tables)

                    module_tables = self.dictionary.get_module_tables(module, company)
                    logger.info(f"Processing {len(module_tables)} tables for {module}/{company}")

                    for table in module_tables:
                        current_table += 1

                        if progress_callback:
                            progress_callback(
                                f"🔄 Mapeando {table['alias']} ({table['description'][:40]}...)",
                                current_table,
                                total_tables
                            )

                        try:
                            entity_mapping = self._generate_entity_mapping(table, company)

                            if not dry_run:
                                # Create mapping in catalog
                                self.catalog.add_mapping(
                                    organization_id,
                                    connection_id,
                                    entity_mapping
                                )
                                logger.debug(f"Created mapping for {table['alias']}")

                            results["entities"].append(entity_mapping)

                        except Exception as e:
                            error_msg = f"Error generating mapping for {table.get('alias', 'unknown')}: {e}"
                            logger.error(error_msg)
                            results["errors"].append(error_msg)

                except Exception as e:
                    error_msg = f"Error processing module {module}/{company}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)

        # Infer relationships between entities
        if results["entities"]:
            try:
                if progress_callback:
                    progress_callback("🔗 Inferindo relacionamentos...", current_table, total_tables)

                logger.info("Inferring relationships...")
                relationships = self.inferencer.infer_relationships(
                    results["entities"],
                    company=companies_list[0] if companies_list else "010"
                )

                # Validate and deduplicate
                if progress_callback:
                    progress_callback(f"✓ Validando {len(relationships)} relacionamentos...", current_table, total_tables)

                relationships = self.inferencer.validate_relationships(relationships)

                # Create relationships in catalog
                for relationship in relationships:
                    try:
                        if not dry_run:
                            self.catalog.add_mapping(
                                organization_id,
                                connection_id,
                                relationship
                            )
                            logger.debug(f"Created relationship: {relationship['concept']}")

                        results["relationships"].append(relationship)

                    except Exception as e:
                        error_msg = f"Error creating relationship {relationship.get('concept')}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)

                # Log relationship statistics
                stats = self.inferencer.get_relationship_statistics(relationships)
                logger.info(f"Relationship inference stats: {stats}")

                if progress_callback:
                    progress_callback(f"✅ Concluído! {len(results['entities'])} entidades + {len(relationships)} relacionamentos", total_tables, total_tables)

            except Exception as e:
                error_msg = f"Error during relationship inference: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        else:
            if progress_callback:
                progress_callback(f"✅ Concluído! {len(results['entities'])} entidades", total_tables, total_tables)

        # Generate summary
        results["summary"] = {
            "total_entities": len(results["entities"]),
            "total_relationships": len(results["relationships"]),
            "total_errors": len(results["errors"]),
            "modules_mapped": modules_list,
            "companies": companies_list,
            "dry_run": dry_run
        }

        logger.info(f"Mapping generation complete: {results['summary']}")
        return results

    def _generate_entity_mapping(self, table: Dict[str, Any], company: str) -> Dict[str, Any]:
        """
        Generate entity mapping from table metadata.

        Args:
            table: Table metadata from SX2
            company: Company code

        Returns:
            Entity mapping dictionary
        """
        table_alias = table['alias']

        # Get columns for this table
        columns = self.dictionary.get_columns(table_alias, company)

        # Create column mappings (semantic name -> physical name)
        column_mappings = {}
        for col in columns:
            # Use X3_TITULO (title) as semantic name
            # Normalize: lowercase, remove special chars
            semantic_name = self._normalize_semantic_name(col['title'])
            if semantic_name:
                column_mappings[semantic_name] = {
                    "column": col['column_name'],
                    "description": col['description'],
                    "data_type": self._map_protheus_type(col['data_type']),
                    "is_primary_key": col['column_name'] in table.get('primary_key', ''),
                    "required": col['required']
                }

        # Create entity mapping
        concept = self._normalize_concept_name(table['description'])

        mapping = {
            "concept": concept,
            "type": "entity",
            "table": table['physical_table'],
            "alias": table_alias,
            "description": f"{table['description']} (Protheus {table_alias})",
            "columns": column_mappings,
            "metadata": {
                "source": "protheus_dictionary",
                "company": company,
                "protheus_alias": table_alias,
                "share_mode": table.get('share_mode', ''),
                "primary_key": table.get('primary_key', '')
            }
        }

        return mapping

    def _normalize_semantic_name(self, name: str) -> str:
        """
        Normalize a field name for use as semantic name.

        Args:
            name: Original name from dictionary

        Returns:
            Normalized semantic name

        Example:
            "Número do Título" -> "numero_titulo"
            "Data de Emissão" -> "data_emissao"
        """
        if not name:
            return ""

        # Remove acentos
        name = self._remove_accents(name)

        # Convert to lowercase
        name = name.lower()

        # Remove special characters, keep only alphanumeric and spaces
        name = re.sub(r'[^a-z0-9\s]', '', name)

        # Replace spaces with underscores
        name = re.sub(r'\s+', '_', name.strip())

        return name

    def _normalize_concept_name(self, description: str) -> str:
        """
        Normalize table description for use as concept name.

        Args:
            description: Table description from SX2

        Returns:
            Normalized concept name

        Example:
            "Títulos a Receber" -> "titulos_receber"
        """
        return self._normalize_semantic_name(description)

    def _remove_accents(self, text: str) -> str:
        """
        Remove accents from text.

        Args:
            text: Text with accents

        Returns:
            Text without accents
        """
        import unicodedata

        # Normalize to NFD (decomposed form)
        nfd = unicodedata.normalize('NFD', text)

        # Filter out combining characters (accents)
        without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

        return without_accents

    def _map_protheus_type(self, protheus_type: str) -> str:
        """
        Map Protheus data type to SQL type.

        Args:
            protheus_type: Protheus type (C, N, D, L, M)

        Returns:
            SQL type (string, number, date, boolean, text)
        """
        type_map = {
            'C': 'string',    # Character
            'N': 'number',    # Numeric
            'D': 'date',      # Date
            'L': 'boolean',   # Logical
            'M': 'text'       # Memo
        }
        return type_map.get(protheus_type.upper(), 'string')

    def _get_default_modules(self) -> List[str]:
        """
        Get default list of modules to map.

        Returns:
            List of default module names
        """
        return [
            "SIGAFIN",  # Financeiro
            "SIGAEST",  # Estoque
            "SIGACOM",  # Compras
            "SIGAGCT"   # Gestão de Contratos
        ]

    def preview_table_mapping(self, table_alias: str, company: str = "010") -> Dict[str, Any]:
        """
        Preview mapping for a specific table without creating it.

        Args:
            table_alias: Protheus table alias (e.g., "SE1")
            company: Company code

        Returns:
            Preview of the mapping
        """
        try:
            # Get table info
            tables = self.dictionary.get_tables(company=company)
            table = next((t for t in tables if t['alias'] == table_alias), None)

            if not table:
                raise ValueError(f"Table {table_alias} not found in company {company}")

            # Generate preview
            mapping = self._generate_entity_mapping(table, company)

            # Add additional preview info
            preview = {
                "mapping": mapping,
                "table_info": table,
                "column_count": len(mapping['columns']),
                "estimated_size": "medium"  # Could calculate based on column count
            }

            return preview

        except Exception as e:
            logger.error(f"Error previewing table {table_alias}: {e}")
            raise
