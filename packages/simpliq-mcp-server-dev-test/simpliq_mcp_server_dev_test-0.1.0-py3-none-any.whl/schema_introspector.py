"""Schema Introspector Module - SimpliQ

This module provides detailed database schema introspection capabilities.

Classes:
    - SchemaIntrospector: Introspects database schema (tables, columns, relationships)
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


@dataclass
class ColumnInfo:
    """Information about a database column."""
    name: str
    type: str
    nullable: bool
    default: Optional[Any] = None
    autoincrement: bool = False
    primary_key: bool = False


@dataclass
class ForeignKeyInfo:
    """Information about a foreign key constraint."""
    name: Optional[str]
    constrained_columns: List[str]
    referred_table: str
    referred_columns: List[str]
    ondelete: Optional[str] = None
    onupdate: Optional[str] = None


@dataclass
class IndexInfo:
    """Information about a database index."""
    name: str
    unique: bool
    columns: List[str]


@dataclass
class TableDescription:
    """Complete description of a database table."""
    table_name: str
    schema: Optional[str]
    columns: List[ColumnInfo]
    primary_key: List[str]
    foreign_keys: List[ForeignKeyInfo]
    indexes: List[IndexInfo]
    unique_constraints: List[Dict[str, Any]] = field(default_factory=list)
    check_constraints: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TableRelationship:
    """Represents a relationship between two tables via foreign key."""
    from_table: str
    to_table: str
    from_columns: List[str]
    to_columns: List[str]
    constraint_name: Optional[str] = None
    ondelete: Optional[str] = None
    onupdate: Optional[str] = None


class SchemaIntrospector:
    """
    Provides detailed database schema introspection.

    This introspector uses SQLAlchemy's Inspector API to extract
    comprehensive metadata about database tables, columns, and relationships.
    """

    def __init__(self, engine: Engine):
        """
        Initialize the schema introspector.

        Args:
            engine: SQLAlchemy engine for database connection
        """
        self.engine = engine
        self.inspector = inspect(engine)

    def describe_table(
        self,
        table_name: str,
        schema: Optional[str] = None
    ) -> TableDescription:
        """
        Get complete description of a table.

        Args:
            table_name: Name of the table to describe
            schema: Optional schema name

        Returns:
            TableDescription with all table metadata

        Raises:
            ValueError: If table doesn't exist
            SQLAlchemyError: If database error occurs
        """
        try:
            # Verify table exists
            tables = self.inspector.get_table_names(schema=schema)
            if table_name not in tables:
                raise ValueError(f"Table '{table_name}' not found in database")

            logger.info(f"Describing table: {table_name} (schema: {schema})")

            # Get columns
            columns = self._get_columns(table_name, schema)

            # Get primary key
            primary_key = self._get_primary_key(table_name, schema)

            # Mark primary key columns
            pk_set = set(primary_key)
            for col in columns:
                if col.name in pk_set:
                    col.primary_key = True

            # Get foreign keys
            foreign_keys = self._get_foreign_keys(table_name, schema)

            # Get indexes
            indexes = self._get_indexes(table_name, schema)

            # Get unique constraints
            unique_constraints = self._get_unique_constraints(table_name, schema)

            # Get check constraints
            check_constraints = self._get_check_constraints(table_name, schema)

            return TableDescription(
                table_name=table_name,
                schema=schema,
                columns=columns,
                primary_key=primary_key,
                foreign_keys=foreign_keys,
                indexes=indexes,
                unique_constraints=unique_constraints,
                check_constraints=check_constraints
            )

        except ValueError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error describing table {table_name}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error describing table {table_name}: {str(e)}")
            raise

    def get_table_relationships(
        self,
        schema: Optional[str] = None
    ) -> List[TableRelationship]:
        """
        Get all foreign key relationships in the database.

        Args:
            schema: Optional schema name to filter tables

        Returns:
            List of TableRelationship objects representing FK relationships

        Raises:
            SQLAlchemyError: If database error occurs
        """
        try:
            logger.info(f"Getting table relationships (schema: {schema})")

            relationships = []

            # Get all tables
            tables = self.inspector.get_table_names(schema=schema)

            # For each table, get its foreign keys
            for table_name in tables:
                try:
                    fks = self.inspector.get_foreign_keys(table_name, schema=schema)

                    for fk in fks:
                        relationship = TableRelationship(
                            from_table=table_name,
                            to_table=fk['referred_table'],
                            from_columns=fk['constrained_columns'],
                            to_columns=fk['referred_columns'],
                            constraint_name=fk.get('name'),
                            ondelete=fk.get('options', {}).get('ondelete'),
                            onupdate=fk.get('options', {}).get('onupdate')
                        )
                        relationships.append(relationship)

                except Exception as e:
                    logger.warning(
                        f"Failed to get foreign keys for table {table_name}: {str(e)}"
                    )
                    continue

            logger.info(f"Found {len(relationships)} table relationships")
            return relationships

        except SQLAlchemyError as e:
            logger.error(f"Error getting table relationships: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting table relationships: {str(e)}")
            raise

    def _get_columns(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[ColumnInfo]:
        """Get column information for a table."""
        columns_data = self.inspector.get_columns(table_name, schema=schema)
        columns = []

        for col in columns_data:
            column_info = ColumnInfo(
                name=col['name'],
                type=str(col['type']),
                nullable=col.get('nullable', True),
                default=col.get('default'),
                autoincrement=col.get('autoincrement', False)
            )
            columns.append(column_info)

        return columns

    def _get_primary_key(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[str]:
        """Get primary key columns for a table."""
        pk_constraint = self.inspector.get_pk_constraint(table_name, schema=schema)
        return pk_constraint.get('constrained_columns', [])

    def _get_foreign_keys(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[ForeignKeyInfo]:
        """Get foreign key constraints for a table."""
        fks_data = self.inspector.get_foreign_keys(table_name, schema=schema)
        foreign_keys = []

        for fk in fks_data:
            fk_info = ForeignKeyInfo(
                name=fk.get('name'),
                constrained_columns=fk['constrained_columns'],
                referred_table=fk['referred_table'],
                referred_columns=fk['referred_columns'],
                ondelete=fk.get('options', {}).get('ondelete'),
                onupdate=fk.get('options', {}).get('onupdate')
            )
            foreign_keys.append(fk_info)

        return foreign_keys

    def _get_indexes(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[IndexInfo]:
        """Get indexes for a table."""
        indexes_data = self.inspector.get_indexes(table_name, schema=schema)
        indexes = []

        for idx in indexes_data:
            index_info = IndexInfo(
                name=idx['name'],
                unique=idx.get('unique', False),
                columns=idx['column_names']
            )
            indexes.append(index_info)

        return indexes

    def _get_unique_constraints(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Get unique constraints for a table."""
        try:
            return self.inspector.get_unique_constraints(table_name, schema=schema)
        except (NotImplementedError, AttributeError):
            # Some database drivers don't support this
            logger.warning(
                f"Unique constraints not supported for table {table_name}"
            )
            return []

    def _get_check_constraints(
        self,
        table_name: str,
        schema: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Get check constraints for a table."""
        try:
            return self.inspector.get_check_constraints(table_name, schema=schema)
        except (NotImplementedError, AttributeError):
            # Some database drivers don't support this
            logger.warning(
                f"Check constraints not supported for table {table_name}"
            )
            return []
