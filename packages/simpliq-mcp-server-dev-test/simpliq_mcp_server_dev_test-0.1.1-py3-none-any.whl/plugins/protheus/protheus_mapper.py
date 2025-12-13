# -*- coding: utf-8 -*-
"""
Protheus Mapper Plugin

MCP Plugin for Protheus TOTVS semantic mapping automation.

Author: SimpliQ Development Team
Date: 2025-11-18
"""

from typing import Dict, List, Optional, Any
import logging
import json
from .dictionary import ProtheusDataDictionary
from .generator import ProtheusSemanticGenerator

logger = logging.getLogger(__name__)


class ProtheusMapperPlugin:
    """MCP Plugin for Protheus semantic mapping."""

    def __init__(self):
        """Initialize the plugin."""
        self.generator = None
        self.dictionary = None
        self.connection = None
        self.catalog = None

    def initialize(self, connection, semantic_catalog):
        """
        Initialize plugin with connection and catalog.

        Args:
            connection: SQLAlchemy engine/connection
            semantic_catalog: SemanticCatalog instance
        """
        self.connection = connection
        self.catalog = semantic_catalog
        self.generator = ProtheusSemanticGenerator(connection, semantic_catalog)
        self.dictionary = ProtheusDataDictionary(connection)
        logger.info("Protheus Mapper Plugin initialized successfully")

    def get_tools(self) -> Dict[str, Dict]:
        """
        Return MCP tools provided by this plugin.

        Returns:
            Dictionary of tool definitions
        """
        return {
            "auto_map_protheus": {
                "description": "Automatically generate semantic mappings from Protheus data dictionary (SX2, SX3, SIX)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID"
                        },
                        "connection_id": {
                            "type": "string",
                            "description": "Connection ID"
                        },
                        "modules": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Modules to map (e.g., ['SIGAFIN', 'SIGAEST']). If not provided, maps default modules."
                        },
                        "companies": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Company codes (e.g., ['010', '030']). Default: ['010']"
                        },
                        "dry_run": {
                            "type": "boolean",
                            "description": "If true, preview without creating mappings. Default: false"
                        }
                    },
                    "required": ["organization_id", "connection_id"]
                }
            },
            "list_protheus_modules": {
                "description": "List available Protheus modules that can be mapped",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "company": {
                            "type": "string",
                            "description": "Company code. Default: '010'"
                        }
                    }
                }
            },
            "preview_protheus_table": {
                "description": "Preview mapping for a specific Protheus table without creating it",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_alias": {
                            "type": "string",
                            "description": "Protheus table alias (e.g., 'SE1', 'SA2')"
                        },
                        "company": {
                            "type": "string",
                            "description": "Company code. Default: '010'"
                        }
                    },
                    "required": ["table_alias"]
                }
            },
            "list_protheus_tables": {
                "description": "List tables available in Protheus data dictionary",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "module": {
                            "type": "string",
                            "description": "Filter by module (e.g., 'SIGAFIN'). Optional."
                        },
                        "company": {
                            "type": "string",
                            "description": "Company code. Default: '010'"
                        }
                    }
                }
            },
            "manage_protheus_cache": {
                "description": "Manage Protheus data dictionary cache (view stats, clear cache, cleanup expired entries)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["stats", "clear", "cleanup"],
                            "description": "Action: 'stats' (view statistics), 'clear' (clear all cache), 'cleanup' (remove expired entries)"
                        },
                        "clear_persistent": {
                            "type": "boolean",
                            "description": "For 'clear' action: if true, also clear persistent cache. Default: false"
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def handle_tool_call(self, tool_name: str, args: Dict) -> Optional[Dict]:
        """
        Handle tool execution.

        Args:
            tool_name: Name of the tool being called
            args: Dictionary of arguments

        Returns:
            Tool result in MCP format, or None if tool not handled
        """
        try:
            if tool_name == "auto_map_protheus":
                return self._auto_map_protheus(args)
            elif tool_name == "list_protheus_modules":
                return self._list_modules(args)
            elif tool_name == "preview_protheus_table":
                return self._preview_table(args)
            elif tool_name == "list_protheus_tables":
                return self._list_tables(args)
            elif tool_name == "manage_protheus_cache":
                return self._manage_cache(args)
            else:
                return None

        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {e}")
            raise

    def _auto_map_protheus(self, args: Dict) -> Dict:
        """
        Execute automatic mapping generation.

        Args:
            args: Tool arguments

        Returns:
            MCP-formatted result
        """
        organization_id = args.get("organization_id")
        connection_id = args.get("connection_id")
        modules = args.get("modules")
        companies = args.get("companies")
        dry_run = args.get("dry_run", False)

        if not organization_id or not connection_id:
            raise ValueError("organization_id and connection_id are required")

        logger.info(f"auto_map_protheus: org={organization_id}, conn={connection_id}, "
                   f"modules={modules}, companies={companies}, dry_run={dry_run}")

        # Generate mappings
        results = self.generator.generate_mappings(
            organization_id=organization_id,
            connection_id=connection_id,
            modules=modules,
            companies=companies,
            dry_run=dry_run
        )

        # Format response
        response_text = self._format_mapping_results(results, dry_run)

        return {
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        }

    def _list_modules(self, args: Dict) -> Dict:
        """
        List available Protheus modules.

        Args:
            args: Tool arguments

        Returns:
            MCP-formatted result
        """
        company = args.get("company", "010")

        modules = [
            {
                "name": "SIGAFIN",
                "description": "Financeiro",
                "prefixes": ["SE", "SA6"],
                "tables_sample": ["SE1", "SE2", "SE5", "SA6"]
            },
            {
                "name": "SIGAEST",
                "description": "Estoque e Custos",
                "prefixes": ["SB", "SD3"],
                "tables_sample": ["SB1", "SB2", "SD3"]
            },
            {
                "name": "SIGACOM",
                "description": "Compras",
                "prefixes": ["SC", "SD1", "SA2"],
                "tables_sample": ["SC7", "SD1", "SA2"]
            },
            {
                "name": "SIGAFAT",
                "description": "Faturamento",
                "prefixes": ["SC5", "SC6", "SF2", "SA1"],
                "tables_sample": ["SC5", "SC6", "SF2", "SA1"]
            },
            {
                "name": "SIGAGCT",
                "description": "Gestão de Contratos",
                "prefixes": ["CN"],
                "tables_sample": ["CN9", "CN1", "CNA", "CNN"]
            },
            {
                "name": "SIGACTB",
                "description": "Contabilidade",
                "prefixes": ["CT"],
                "tables_sample": ["CT1", "CT2", "CT7"]
            },
            {
                "name": "SIGAATF",
                "description": "Ativo Fixo",
                "prefixes": ["SN"],
                "tables_sample": ["SN1", "SN3"]
            },
            {
                "name": "SIGAPCP",
                "description": "Planejamento e Controle de Produção",
                "prefixes": ["SC2", "SH"],
                "tables_sample": ["SC2", "SH1"]
            }
        ]

        result_text = "# Módulos Protheus Disponíveis\n\n"
        for module in modules:
            result_text += f"## {module['name']}\n"
            result_text += f"**Descrição:** {module['description']}\n"
            result_text += f"**Prefixos de Tabelas:** {', '.join(module['prefixes'])}\n"
            result_text += f"**Tabelas de Exemplo:** {', '.join(module['tables_sample'])}\n\n"

        result_text += f"\n**Total:** {len(modules)} módulos disponíveis\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }

    def _preview_table(self, args: Dict) -> Dict:
        """
        Preview mapping for a specific table.

        Args:
            args: Tool arguments

        Returns:
            MCP-formatted result
        """
        table_alias = args.get("table_alias")
        company = args.get("company", "010")

        if not table_alias:
            raise ValueError("table_alias is required")

        logger.info(f"preview_protheus_table: table={table_alias}, company={company}")

        # Generate preview
        preview = self.generator.preview_table_mapping(table_alias, company)

        # Format response
        mapping = preview['mapping']
        table_info = preview['table_info']

        result_text = f"# Preview: {table_alias}\n\n"
        result_text += f"**Conceito:** {mapping['concept']}\n"
        result_text += f"**Tabela Física:** {mapping['table']}\n"
        result_text += f"**Descrição:** {mapping['description']}\n"
        result_text += f"**Total de Colunas:** {preview['column_count']}\n\n"

        result_text += "## Mapeamento de Colunas\n\n"
        for semantic_name, col_info in list(mapping['columns'].items())[:10]:  # Show first 10
            result_text += f"- **{semantic_name}** → `{col_info['column']}`\n"
            if col_info.get('description'):
                result_text += f"  - {col_info['description']}\n"

        if len(mapping['columns']) > 10:
            result_text += f"\n... e mais {len(mapping['columns']) - 10} colunas\n"

        result_text += f"\n## Metadados\n"
        result_text += f"- **Empresa:** {company}\n"
        result_text += f"- **Modo de Compartilhamento:** {table_info.get('share_mode', 'N/A')}\n"
        result_text += f"- **Chave Primária:** {table_info.get('primary_key', 'N/A')}\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }

    def _list_tables(self, args: Dict) -> Dict:
        """
        List tables from Protheus data dictionary.

        Args:
            args: Tool arguments

        Returns:
            MCP-formatted result
        """
        module = args.get("module")
        company = args.get("company", "010")

        logger.info(f"list_protheus_tables: module={module}, company={company}")

        if module:
            tables = self.dictionary.get_module_tables(module, company)
        else:
            tables = self.dictionary.get_tables(company=company)

        result_text = f"# Tabelas Protheus"
        if module:
            result_text += f" - Módulo {module}"
        result_text += f" (Empresa {company})\n\n"

        for table in tables[:50]:  # Limit to first 50
            result_text += f"- **{table['alias']}** - {table['description']}\n"
            result_text += f"  Tabela física: `{table['physical_table']}`\n"

        if len(tables) > 50:
            result_text += f"\n... e mais {len(tables) - 50} tabelas\n"

        result_text += f"\n**Total:** {len(tables)} tabelas encontradas\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }

    def _format_mapping_results(self, results: Dict, dry_run: bool) -> str:
        """
        Format mapping generation results as text.

        Args:
            results: Generation results
            dry_run: Whether this was a dry run

        Returns:
            Formatted text
        """
        summary = results['summary']

        if dry_run:
            text = "# Preview de Mapeamento Automático Protheus (DRY RUN)\n\n"
        else:
            text = "# Mapeamento Automático Protheus - Resultado\n\n"

        text += f"## Resumo\n\n"
        text += f"- **Entidades Mapeadas:** {summary['total_entities']}\n"
        text += f"- **Relacionamentos Inferidos:** {summary['total_relationships']}\n"
        text += f"- **Erros:** {summary['total_errors']}\n"
        text += f"- **Módulos:** {', '.join(summary['modules_mapped'])}\n"
        text += f"- **Empresas:** {', '.join(summary['companies'])}\n\n"

        if summary['total_entities'] > 0:
            text += "## Entidades Criadas\n\n"
            for entity in results['entities'][:10]:  # Show first 10
                text += f"- **{entity['concept']}**\n"
                text += f"  - Tabela: `{entity['table']}`\n"
                text += f"  - Colunas: {len(entity.get('columns', {}))}\n"

            if len(results['entities']) > 10:
                text += f"\n... e mais {len(results['entities']) - 10} entidades\n"

        if summary['total_errors'] > 0:
            text += "\n## Erros\n\n"
            for error in results['errors'][:5]:  # Show first 5 errors
                text += f"- {error}\n"

        if dry_run:
            text += "\n---\n"
            text += "**Nota:** Este foi um DRY RUN. Nenhum mapeamento foi criado.\n"
            text += "Execute novamente com `dry_run: false` para criar os mapeamentos.\n"
        else:
            text += "\n---\n"
            text += f"✅ **{summary['total_entities']} mapeamentos criados com sucesso!**\n"

        return text

    def _manage_cache(self, args: Dict) -> Dict:
        """
        Manage Protheus data dictionary cache.

        Args:
            args: Arguments with action and options

        Returns:
            Cache management result
        """
        action = args.get("action")
        clear_persistent = args.get("clear_persistent", False)

        if action == "stats":
            # Get cache statistics
            stats = self.dictionary.get_cache_stats()

            result_text = "# Cache do Dicionário Protheus\n\n"
            result_text += "## Cache em Memória\n\n"
            result_text += f"- **Tabelas:** {stats['in_memory']['tables']} entradas\n"
            result_text += f"- **Colunas:** {stats['in_memory']['columns']} entradas\n"
            result_text += f"- **Índices:** {stats['in_memory']['indexes']} entradas\n"
            result_text += f"- **Total:** {stats['in_memory']['total']} entradas\n\n"

            if stats.get('persistent_enabled'):
                result_text += "## Cache Persistente\n\n"
                if 'persistent' in stats:
                    pstats = stats['persistent']
                    if 'error' not in pstats:
                        result_text += f"- **Total de Arquivos:** {pstats['total_entries']}\n"
                        result_text += f"- **Entradas Válidas:** {pstats['valid_entries']}\n"
                        result_text += f"- **Entradas Expiradas:** {pstats['expired_entries']}\n"
                        result_text += f"- **Tamanho Total:** {pstats['total_size_mb']} MB\n"
                        result_text += f"- **Diretório:** `{pstats['cache_dir']}`\n"
                        result_text += f"- **TTL:** {pstats['ttl_hours']} horas\n"
                    else:
                        result_text += f"❌ **Erro:** {pstats['error']}\n"
            else:
                result_text += "## Cache Persistente\n\n"
                result_text += "⚠️ Cache persistente desabilitado\n"

        elif action == "clear":
            # Clear cache
            self.dictionary.clear_cache(clear_persistent=clear_persistent)

            result_text = "# Cache Limpo\n\n"
            result_text += "✅ Cache em memória foi limpo\n"
            if clear_persistent:
                result_text += "✅ Cache persistente foi limpo\n"
            else:
                result_text += "ℹ️ Cache persistente não foi limpo (use `clear_persistent: true` para limpar)\n"

        elif action == "cleanup":
            # Cleanup expired entries
            removed = self.dictionary.cleanup_expired_cache()

            result_text = "# Limpeza de Cache\n\n"
            if removed > 0:
                result_text += f"✅ {removed} entradas expiradas foram removidas\n"
            else:
                result_text += "ℹ️ Nenhuma entrada expirada encontrada\n"

        else:
            result_text = f"❌ Ação inválida: {action}\n\nAções disponíveis: stats, clear, cleanup"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }
