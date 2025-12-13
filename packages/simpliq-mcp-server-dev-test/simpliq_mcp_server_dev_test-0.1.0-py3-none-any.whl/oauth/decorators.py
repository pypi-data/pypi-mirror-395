"""
OAuth 2.0 Decorators for MCP Tools - Phase 3

Decoradores para proteger ferramentas MCP com validação de scopes.
Compatível com sistema de autenticação existente (JWT, API Keys, OAuth).

Author: Gerson Amorim
Date: 25 de Novembro de 2025
"""

from functools import wraps
from typing import List, Optional, Callable
from flask import g, jsonify
import logging

logger = logging.getLogger(__name__)


class ScopeRequired(Exception):
    """Exceção lançada quando scope requerido não está presente"""

    def __init__(self, required_scope: str, granted_scopes: List[str]):
        self.required_scope = required_scope
        self.granted_scopes = granted_scopes
        super().__init__(
            f"Scope '{required_scope}' required. "
            f"Granted scopes: {', '.join(granted_scopes) if granted_scopes else 'none'}"
        )


def require_scope(scope: str):
    """
    Decorador que requer um scope específico para acessar a ferramenta MCP.

    Este decorador é compatível com múltiplos métodos de autenticação:
    - OAuth 2.0 (valida scopes do token)
    - JWT tradicional (permite acesso - backward compatibility)
    - API Keys (permite acesso - backward compatibility)

    Uso:
        @require_scope("read:connections")
        def list_connections(arguments: dict, context: dict):
            # Código da ferramenta
            pass

    Args:
        scope: Nome do scope requerido (ex: "read:connections")

    Returns:
        Decorator function
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verificar se há contexto OAuth
            oauth_scopes = getattr(g, "oauth_scope", "")

            # Se não há OAuth context, permite acesso (backward compatibility)
            # Usuários autenticados via JWT ou API Key têm acesso total
            if not oauth_scopes:
                logger.debug(
                    f"Tool '{func.__name__}' accessed without OAuth "
                    f"(legacy auth - full access granted)"
                )
                return func(*args, **kwargs)

            # Parsear scopes (string separada por espaço)
            granted_scopes = [s.strip() for s in oauth_scopes.split() if s.strip()]

            # Admin tem acesso a tudo
            if "admin:org" in granted_scopes:
                logger.debug(
                    f"Tool '{func.__name__}' accessed with admin:org scope"
                )
                return func(*args, **kwargs)

            # Verificar se possui o scope requerido
            if scope in granted_scopes:
                logger.debug(
                    f"Tool '{func.__name__}' accessed with scope '{scope}'"
                )
                return func(*args, **kwargs)

            # Scope não encontrado - negado
            logger.warning(
                f"Tool '{func.__name__}' access denied. "
                f"Required: '{scope}', Granted: {granted_scopes}"
            )

            # Log de auditoria
            if hasattr(g, "oauth_user_id"):
                from user_manager.oauth.services.audit_logger import get_audit_logger
                audit_logger = get_audit_logger()
                audit_logger.log_scope_violation(
                    client_id=getattr(g, "oauth_client_id", "unknown"),
                    user_id=g.oauth_user_id,
                    resource=func.__name__,
                    required_scope=scope,
                    granted_scopes=granted_scopes,
                    ip_address=getattr(g, "client_ip", "unknown")
                )

            raise ScopeRequired(scope, granted_scopes)

        return wrapper

    return decorator


def require_any_scope(*scopes: str):
    """
    Decorador que requer QUALQUER UM dos scopes listados.

    Uso:
        @require_any_scope("read:connections", "admin:org")
        def list_connections(arguments: dict, context: dict):
            pass

    Args:
        *scopes: Lista de scopes aceitos (OR logic)

    Returns:
        Decorator function
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            oauth_scopes = getattr(g, "oauth_scope", "")

            # Backward compatibility
            if not oauth_scopes:
                return func(*args, **kwargs)

            granted_scopes = [s.strip() for s in oauth_scopes.split() if s.strip()]

            # Admin tem acesso a tudo
            if "admin:org" in granted_scopes:
                return func(*args, **kwargs)

            # Verificar se possui algum dos scopes requeridos
            for scope in scopes:
                if scope in granted_scopes:
                    logger.debug(
                        f"Tool '{func.__name__}' accessed with scope '{scope}'"
                    )
                    return func(*args, **kwargs)

            # Nenhum scope encontrado
            logger.warning(
                f"Tool '{func.__name__}' access denied. "
                f"Required any of: {scopes}, Granted: {granted_scopes}"
            )

            raise ScopeRequired(
                f"any of [{', '.join(scopes)}]",
                granted_scopes
            )

        return wrapper

    return decorator


def require_all_scopes(*scopes: str):
    """
    Decorador que requer TODOS os scopes listados.

    Uso:
        @require_all_scopes("read:connections", "execute:queries")
        def execute_connection_query(arguments: dict, context: dict):
            pass

    Args:
        *scopes: Lista de scopes necessários (AND logic)

    Returns:
        Decorator function
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            oauth_scopes = getattr(g, "oauth_scope", "")

            # Backward compatibility
            if not oauth_scopes:
                return func(*args, **kwargs)

            granted_scopes = [s.strip() for s in oauth_scopes.split() if s.strip()]

            # Admin tem acesso a tudo
            if "admin:org" in granted_scopes:
                return func(*args, **kwargs)

            # Verificar se possui todos os scopes requeridos
            missing_scopes = [s for s in scopes if s not in granted_scopes]

            if not missing_scopes:
                logger.debug(
                    f"Tool '{func.__name__}' accessed with all required scopes"
                )
                return func(*args, **kwargs)

            # Faltam scopes
            logger.warning(
                f"Tool '{func.__name__}' access denied. "
                f"Missing scopes: {missing_scopes}, Granted: {granted_scopes}"
            )

            raise ScopeRequired(
                f"all of [{', '.join(scopes)}]",
                granted_scopes
            )

        return wrapper

    return decorator


def optional_scope(scope: str):
    """
    Decorador que marca um scope como opcional.
    Se presente, valida; se ausente, permite acesso com funcionalidade limitada.

    Útil para ferramentas que têm comportamento diferente baseado em scopes.

    Uso:
        @optional_scope("admin:org")
        def list_users(arguments: dict, context: dict):
            # Se tem admin:org, mostra todos os usuários
            # Se não tem, mostra apenas usuários da própria org
            if has_oauth_scope("admin:org"):
                return all_users()
            else:
                return own_org_users()

    Args:
        scope: Nome do scope opcional

    Returns:
        Decorator function
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            oauth_scopes = getattr(g, "oauth_scope", "")

            if oauth_scopes:
                granted_scopes = [s.strip() for s in oauth_scopes.split() if s.strip()]

                # Adicionar flag indicando se possui o scope opcional
                if scope in granted_scopes or "admin:org" in granted_scopes:
                    g.has_optional_scope = True
                    logger.debug(
                        f"Tool '{func.__name__}' accessed with optional scope '{scope}'"
                    )
                else:
                    g.has_optional_scope = False
                    logger.debug(
                        f"Tool '{func.__name__}' accessed without optional scope '{scope}'"
                    )
            else:
                # Backward compatibility - assume que tem acesso total
                g.has_optional_scope = True

            return func(*args, **kwargs)

        return wrapper

    return decorator


def has_oauth_scope(scope: str) -> bool:
    """
    Função utilitária para verificar se o contexto atual possui um scope.

    Uso dentro de uma ferramenta MCP:
        if has_oauth_scope("admin:org"):
            # Código admin
        else:
            # Código usuário normal

    Args:
        scope: Nome do scope a verificar

    Returns:
        bool: True se possui o scope
    """
    oauth_scopes = getattr(g, "oauth_scope", "")

    if not oauth_scopes:
        # Sem OAuth = acesso total (backward compatibility)
        return True

    granted_scopes = [s.strip() for s in oauth_scopes.split() if s.strip()]

    return scope in granted_scopes or "admin:org" in granted_scopes


def get_oauth_scopes() -> List[str]:
    """
    Retorna lista de scopes OAuth do contexto atual.

    Returns:
        List[str]: Lista de scopes concedidos
    """
    oauth_scopes = getattr(g, "oauth_scope", "")

    if not oauth_scopes:
        return []

    return [s.strip() for s in oauth_scopes.split() if s.strip()]


def get_oauth_context() -> dict:
    """
    Retorna todo o contexto OAuth disponível.

    Returns:
        dict: Contexto OAuth completo
    """
    return {
        "user_id": getattr(g, "oauth_user_id", None),
        "client_id": getattr(g, "oauth_client_id", None),
        "org_id": getattr(g, "oauth_org_id", None),
        "scopes": get_oauth_scopes(),
        "user_info": getattr(g, "oauth_user_info", None)
    }
