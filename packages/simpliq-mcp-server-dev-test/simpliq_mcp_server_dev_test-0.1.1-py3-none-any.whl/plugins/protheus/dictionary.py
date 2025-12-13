# -*- coding: utf-8 -*-
"""
Protheus Data Dictionary Reader

Reads metadata from Protheus TOTVS data dictionary tables:
- SX2: Tables metadata
- SX3: Columns/fields metadata
- SIX: Indexes metadata

Author: SimpliQ Development Team
Date: 2025-11-18
"""

from typing import Dict, List, Optional, Any
from sqlalchemy import text
import logging
from .cache import ProtheusDictionaryCache

logger = logging.getLogger(__name__)


class ProtheusDataDictionary:
    """Reads Protheus data dictionary tables."""

    def __init__(self, connection, use_persistent_cache: bool = True, cache_ttl_hours: int = 24):
        """
        Initialize the data dictionary reader.

        Args:
            connection: SQLAlchemy engine/connection
            use_persistent_cache: Enable persistent disk cache (default: True)
            cache_ttl_hours: Cache time-to-live in hours (default: 24)
        """
        self.connection = connection

        # In-memory cache (fast, session-scoped)
        self.cache = {
            'tables': {},
            'columns': {},
            'indexes': {}
        }

        # Persistent cache (disk-based, survives restarts)
        self.use_persistent_cache = use_persistent_cache
        if use_persistent_cache:
            self.persistent_cache = ProtheusDictionaryCache(ttl_hours=cache_ttl_hours)
        else:
            self.persistent_cache = None

    def get_tables(self,
                   module_prefix: Optional[str] = None,
                   company: str = "010") -> List[Dict[str, Any]]:
        """
        Get tables from SX2 (Cadastro de Arquivos).

        Args:
            module_prefix: Filter by module prefix (e.g., "SE" for SIGAFIN)
            company: Company code (default: "010")

        Returns:
            List of table metadata dictionaries

        Example:
            >>> tables = dd.get_tables(module_prefix="SE", company="010")
            >>> print(tables[0])
            {
                'alias': 'SE1',
                'physical_table': 'SE1010',
                'description': 'Títulos a Receber',
                'primary_key': 'E1_FILIAL+E1_PREFIXO+E1_NUM',
                'share_mode': 'C'
            }
        """
        cache_key = f"{module_prefix}_{company}"

        # Check in-memory cache first
        if cache_key in self.cache['tables']:
            logger.debug(f"Returning in-memory cached tables for {cache_key}")
            return self.cache['tables'][cache_key]

        # Check persistent cache
        if self.persistent_cache:
            cached_data = self.persistent_cache.get("tables", module_prefix=module_prefix, company=company)
            if cached_data is not None:
                self.cache['tables'][cache_key] = cached_data
                logger.debug(f"Returning persistent cached tables for {cache_key}")
                return cached_data

        try:
            # Query SX2 table
            query = f"""
                SELECT
                    X2_CHAVE AS alias,
                    X2_ARQUIVO AS physical_table,
                    X2_NOME AS description,
                    X2_UNICO AS primary_key,
                    X2_MODO AS share_mode,
                    X2_MODOUN AS unit_mode,
                    X2_MODOEMP AS company_mode
                FROM SX2{company}
                WHERE D_E_L_E_T_ = ''
            """

            if module_prefix:
                query += f" AND X2_CHAVE LIKE '{module_prefix}%'"

            query += " ORDER BY X2_CHAVE"

            with self.connection.connect() as conn:
                result = conn.execute(text(query))
                tables = []

                for row in result:
                    table = {
                        'alias': row.alias.strip() if row.alias else '',
                        'physical_table': row.physical_table.strip() if row.physical_table else '',
                        'description': row.description.strip() if row.description else '',
                        'primary_key': row.primary_key.strip() if row.primary_key else '',
                        'share_mode': row.share_mode.strip() if row.share_mode else '',
                        'unit_mode': row.unit_mode.strip() if row.unit_mode else '',
                        'company_mode': row.company_mode.strip() if row.company_mode else ''
                    }
                    tables.append(table)

                logger.info(f"Retrieved {len(tables)} tables from SX2{company}")

                # Store in both caches
                self.cache['tables'][cache_key] = tables
                if self.persistent_cache:
                    self.persistent_cache.set(tables, "tables", module_prefix=module_prefix, company=company)

                return tables

        except Exception as e:
            logger.error(f"Error reading SX2 table: {e}")
            raise

    def get_columns(self, table_alias: str, company: str = "010") -> List[Dict[str, Any]]:
        """
        Get columns from SX3 (Cadastro de Campos).

        Args:
            table_alias: Table alias from SX2 (e.g., "SE1")
            company: Company code (default: "010")

        Returns:
            List of column metadata dictionaries

        Example:
            >>> columns = dd.get_columns("SE1", "010")
            >>> print(columns[0])
            {
                'column_name': 'E1_FILIAL',
                'data_type': 'C',
                'size': 2,
                'decimals': 0,
                'title': 'Filial',
                'description': 'Filial do Sistema',
                'picture': '@!',
                'required': True
            }
        """
        cache_key = f"{table_alias}_{company}"

        # Check in-memory cache first
        if cache_key in self.cache['columns']:
            logger.debug(f"Returning in-memory cached columns for {cache_key}")
            return self.cache['columns'][cache_key]

        # Check persistent cache
        if self.persistent_cache:
            cached_data = self.persistent_cache.get("columns", table_alias=table_alias, company=company)
            if cached_data is not None:
                self.cache['columns'][cache_key] = cached_data
                logger.debug(f"Returning persistent cached columns for {cache_key}")
                return cached_data

        try:
            query = f"""
                SELECT
                    X3_CAMPO AS column_name,
                    X3_TIPO AS data_type,
                    X3_TAMANHO AS size,
                    X3_DECIMAL AS decimals,
                    X3_TITULO AS title,
                    X3_DESCRIC AS description,
                    X3_PICTURE AS picture,
                    X3_VALID AS validation,
                    X3_F3 AS lookup,
                    X3_OBRIGAT AS required,
                    X3_BROWSE AS browse,
                    X3_VISUAL AS visual,
                    X3_CONTEXT AS context,
                    X3_ORDEM AS order_num
                FROM SX3{company}
                WHERE X3_ARQUIVO = :table_alias
                  AND D_E_L_E_T_ = ''
                ORDER BY X3_ORDEM
            """

            with self.connection.connect() as conn:
                result = conn.execute(text(query), {"table_alias": table_alias})
                columns = []

                for row in result:
                    column = {
                        'column_name': row.column_name.strip() if row.column_name else '',
                        'data_type': row.data_type.strip() if row.data_type else '',
                        'size': int(row.size) if row.size else 0,
                        'decimals': int(row.decimals) if row.decimals else 0,
                        'title': row.title.strip() if row.title else '',
                        'description': row.description.strip() if row.description else '',
                        'picture': row.picture.strip() if row.picture else '',
                        'validation': row.validation.strip() if row.validation else '',
                        'lookup': row.lookup.strip() if row.lookup else '',
                        'required': row.required.strip() == 'S' if row.required else False,
                        'browse': row.browse.strip() == 'S' if row.browse else False,
                        'visual': row.visual.strip() if row.visual else '',
                        'context': row.context.strip() if row.context else '',
                        'order_num': row.order_num.strip() if row.order_num else ''
                    }
                    columns.append(column)

                logger.info(f"Retrieved {len(columns)} columns for table {table_alias}")

                # Store in both caches
                self.cache['columns'][cache_key] = columns
                if self.persistent_cache:
                    self.persistent_cache.set(columns, "columns", table_alias=table_alias, company=company)

                return columns

        except Exception as e:
            logger.error(f"Error reading SX3 for table {table_alias}: {e}")
            raise

    def get_indexes(self, table_alias: str, company: str = "010") -> List[Dict[str, Any]]:
        """
        Get indexes from SIX (Cadastro de Índices).

        Args:
            table_alias: Table alias from SX2 (e.g., "SE1")
            company: Company code (default: "010")

        Returns:
            List of index metadata dictionaries

        Example:
            >>> indexes = dd.get_indexes("SE1", "010")
            >>> print(indexes[0])
            {
                'order': '1',
                'key': 'E1_FILIAL+E1_PREFIXO+E1_NUM+E1_PARCELA+E1_TIPO',
                'description': 'Filial+Prefixo+Número+Parcela+Tipo',
                'nickname': 'SE1001',
                'unique': False
            }
        """
        cache_key = f"{table_alias}_{company}"
        if cache_key in self.cache['indexes']:
            logger.debug(f"Returning cached indexes for {cache_key}")
            return self.cache['indexes'][cache_key]

        try:
            query = f"""
                SELECT
                    INDICE AS order_num,
                    CHAVE AS key_expression,
                    DESCRICAO AS description,
                    APELIDO AS nickname,
                    PROPRI AS proprietary,
                    SHOWPESQ AS show_search
                FROM SIX{company}
                WHERE INDICE LIKE :table_pattern
                  AND D_E_L_E_T_ = ''
                ORDER BY CAST(INDICE AS INTEGER)
            """

            with self.connection.connect() as conn:
                # SIX stores indexes with pattern like "SE1" in the INDICE field
                result = conn.execute(text(query), {"table_pattern": f"{table_alias}%"})
                indexes = []

                for row in result:
                    index = {
                        'order': row.order_num.strip() if row.order_num else '',
                        'key': row.key_expression.strip() if row.key_expression else '',
                        'description': row.description.strip() if row.description else '',
                        'nickname': row.nickname.strip() if row.nickname else '',
                        'proprietary': row.proprietary.strip() if row.proprietary else '',
                        'show_search': row.show_search.strip() == 'S' if row.show_search else False
                    }
                    indexes.append(index)

                logger.info(f"Retrieved {len(indexes)} indexes for table {table_alias}")
                self.cache['indexes'][cache_key] = indexes
                return indexes

        except Exception as e:
            logger.error(f"Error reading SIX for table {table_alias}: {e}")
            # Indexes are optional, return empty list on error
            return []

    def clear_cache(self, clear_persistent: bool = False):
        """
        Clear all cached data.

        Args:
            clear_persistent: If True, also clear persistent cache on disk
        """
        # Clear in-memory cache
        self.cache = {
            'tables': {},
            'columns': {},
            'indexes': {}
        }

        # Clear persistent cache if requested
        if clear_persistent and self.persistent_cache:
            self.persistent_cache.invalidate()

        logger.info(f"Dictionary cache cleared (persistent: {clear_persistent})")

    def get_module_tables(self, module: str, company: str = "010") -> List[Dict[str, Any]]:
        """
        Get all tables for a specific Protheus module.

        Args:
            module: Module name (e.g., "SIGAFIN", "SIGAEST")
            company: Company code (default: "010")

        Returns:
            List of tables for the module
        """
        prefixes = self._module_to_prefixes(module)
        all_tables = []

        for prefix in prefixes:
            tables = self.get_tables(module_prefix=prefix, company=company)
            all_tables.extend(tables)

        return all_tables

    def _module_to_prefixes(self, module: str) -> List[str]:
        """
        Convert module name to table prefixes.

        Args:
            module: Module name (e.g., "SIGAFIN")

        Returns:
            List of table prefixes for the module
        """
        module_map = {
            "SIGAFIN": ["SE", "SA6"],  # Financeiro
            "SIGAEST": ["SB", "SD3"],  # Estoque
            "SIGACOM": ["SC", "SD1", "SA2"],  # Compras
            "SIGAFAT": ["SC5", "SC6", "SF2", "SA1"],  # Faturamento
            "SIGAGCT": ["CN"],  # Gestão de Contratos
            "SIGACTB": ["CT"],  # Contabilidade
            "SIGAATF": ["SN"],  # Ativo Fixo
            "SIGAPCP": ["SC2", "SH"],  # Planejamento e Controle de Produção
        }

        return module_map.get(module.upper(), [module[:2].upper()])

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "in_memory": {
                "tables": len(self.cache['tables']),
                "columns": len(self.cache['columns']),
                "indexes": len(self.cache['indexes']),
                "total": len(self.cache['tables']) + len(self.cache['columns']) + len(self.cache['indexes'])
            },
            "persistent_enabled": self.use_persistent_cache
        }

        if self.persistent_cache:
            stats["persistent"] = self.persistent_cache.get_stats()

        return stats

    def cleanup_expired_cache(self) -> int:
        """
        Clean up expired persistent cache entries.

        Returns:
            Number of entries removed
        """
        if self.persistent_cache:
            return self.persistent_cache.cleanup_expired()
        return 0
